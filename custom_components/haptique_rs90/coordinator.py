"""Coordinator for Haptique RS90 Remote integration."""
from __future__ import annotations

import asyncio
import json
import logging
import os
from datetime import timedelta
from typing import Any

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import file as file_util

from .const import (
    DOMAIN,
    CONF_REMOTE_ID,
    TOPIC_BASE,
    TOPIC_STATUS,
    TOPIC_DEVICE_LIST,
    TOPIC_MACRO_LIST,
    TOPIC_BATTERY_STATUS,
    TOPIC_BATTERY_LEVEL,
    TOPIC_KEYS,
    TOPIC_TEST_STATUS,
    STATE_ONLINE,
    STATE_OFFLINE,
    SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


class HaptiqueRS90Coordinator(DataUpdateCoordinator):
    """Class to manage fetching Haptique RS90 data from MQTT."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )
        
        self.entry = entry
        self.remote_id = entry.data[CONF_REMOTE_ID]
        self._subscriptions: list[callable] = []
        
        # Path to store persistent macro states
        self._state_file = hass.config.path(f".storage/haptique_rs90_{self.remote_id}_states.json")
        
        # Track subscribed devices and macros to handle add/remove
        self._subscribed_devices: set[str] = set()
        self._subscribed_macros: set[str] = set()
        
        # Data storage
        self.data: dict[str, Any] = {
            "status": STATE_OFFLINE,
            "battery_level": None,
            "last_key": None,
            "running_macro": None,
            "devices": [],
            "macros": [],
            "device_commands": {},
            "test_status": None,
            "macro_states": {},  # Store macro states (on/off)
        }

    async def _load_macro_states(self) -> None:
        """Load saved macro states from file (async)."""
        def _load_sync():
            """Synchronous load operation."""
            try:
                if os.path.exists(self._state_file):
                    with open(self._state_file, 'r') as f:
                        return json.load(f)
            except Exception as err:
                _LOGGER.error("Failed to load macro states: %s", err)
            return None
        
        try:
            saved_states = await self.hass.async_add_executor_job(_load_sync)
            if saved_states:
                self.data["macro_states"] = saved_states.get("macro_states", {})
                _LOGGER.info("Loaded saved macro states: %s", self.data["macro_states"])
            else:
                _LOGGER.debug("No saved macro states file found")
        except Exception as err:
            _LOGGER.error("Failed to load macro states: %s", err)

    async def _save_macro_states(self) -> None:
        """Save macro states to file (async)."""
        def _save_sync():
            """Synchronous save operation."""
            try:
                # Ensure directory exists
                os.makedirs(os.path.dirname(self._state_file), exist_ok=True)
                
                with open(self._state_file, 'w') as f:
                    json.dump({"macro_states": self.data["macro_states"]}, f)
                _LOGGER.debug("Saved macro states to file")
            except Exception as err:
                _LOGGER.error("Failed to save macro states: %s", err)
        
        await self.hass.async_add_executor_job(_save_sync)

    @property
    def base_topic(self) -> str:
        """Return base MQTT topic for this remote."""
        return f"{TOPIC_BASE}/{self.remote_id}"

    async def async_config_entry_first_refresh(self) -> None:
        """Perform first refresh and subscribe to MQTT topics."""
        # Load saved macro states before subscribing
        await self._load_macro_states()
        await self._subscribe_topics()
        await super().async_config_entry_first_refresh()

    async def _subscribe_topics(self) -> None:
        """Subscribe to MQTT topics."""
        _LOGGER.debug("Subscribing to MQTT topics for remote %s", self.remote_id)
        
        # Subscribe to status topic
        await self._subscribe(
            f"{self.base_topic}/{TOPIC_STATUS}",
            self._handle_status
        )
        
        # Subscribe to device list
        await self._subscribe(
            f"{self.base_topic}/{TOPIC_DEVICE_LIST}",
            self._handle_device_list
        )
        
        # Subscribe to macro list
        await self._subscribe(
            f"{self.base_topic}/{TOPIC_MACRO_LIST}",
            self._handle_macro_list
        )
        
        # Subscribe to battery level (receives value after publishing to battery/status)
        await self._subscribe(
            f"{self.base_topic}/{TOPIC_BATTERY_LEVEL}",
            self._handle_battery
        )
        _LOGGER.info("Subscribed to battery_level topic")
        
        # Subscribe to key events
        await self._subscribe(
            f"{self.base_topic}/{TOPIC_KEYS}",
            self._handle_keys
        )
        
        # Subscribe to test status (for running macro detection)
        await self._subscribe(
            f"{self.base_topic}/{TOPIC_TEST_STATUS}",
            self._handle_test_status
        )
        
        # Request initial battery level by publishing to battery/status
        # This triggers the remote to publish the value on battery_level
        battery_trigger_topic = f"{self.base_topic}/{TOPIC_BATTERY_STATUS}"
        _LOGGER.info("Publishing to %s to trigger battery level update", battery_trigger_topic)
        try:
            await mqtt.async_publish(
                self.hass,
                battery_trigger_topic,
                "",  # Empty payload to trigger update
                qos=1,
                retain=False
            )
            _LOGGER.info("✓ Battery level trigger published successfully")
        except Exception as err:
            _LOGGER.error("✗ Failed to publish battery trigger: %s", err)

    async def _subscribe(self, topic: str, callback_func: callable) -> None:
        """Subscribe to an MQTT topic."""
        @callback
        def message_received(msg):
            """Handle new MQTT message."""
            callback_func(msg.payload)
        
        _LOGGER.info("Attempting to subscribe to MQTT topic: %s", topic)
        try:
            unsubscribe = await mqtt.async_subscribe(
                self.hass, topic, message_received, qos=1
            )
            self._subscriptions.append(unsubscribe)
            _LOGGER.info("✓ Successfully subscribed to topic: %s", topic)
        except Exception as err:
            _LOGGER.error("✗ Failed to subscribe to topic %s: %s", topic, err)

    @callback
    def _handle_status(self, payload: str) -> None:
        """Handle status message."""
        status = payload.strip()
        _LOGGER.debug("Status update: %s", status)
        self.data["status"] = status
        self.async_set_updated_data(self.data)

    @callback
    def _handle_device_list(self, payload: str) -> None:
        """Handle device list message and manage subscriptions."""
        try:
            devices = json.loads(payload)
            _LOGGER.debug("Received device list: %s", devices)
            
            # Normalize ID field (handle both "id" and "Id")
            normalized_devices = []
            current_device_names = set()
            
            for device in devices:
                normalized_device = {
                    "id": device.get("id") or device.get("Id"),
                    "name": device.get("name")
                }
                normalized_devices.append(normalized_device)
                device_name = normalized_device.get("name")
                if device_name:
                    current_device_names.add(device_name)
            
            self.data["devices"] = normalized_devices
            _LOGGER.debug("Normalized devices: %s", normalized_devices)
            
            # Detect new devices (not yet subscribed)
            new_devices = current_device_names - self._subscribed_devices
            
            # Detect removed devices (subscribed but not in current list)
            removed_devices = self._subscribed_devices - current_device_names
            
            # Subscribe to new devices
            for device_name in new_devices:
                _LOGGER.info("🆕 New device detected: %s - subscribing to details", device_name)
                asyncio.create_task(
                    self._subscribe_device_details(device_name)
                )
                self._subscribed_devices.add(device_name)
            
            # Clean up removed devices
            for device_name in removed_devices:
                _LOGGER.info("🗑️ Device removed: %s - cleaning up", device_name)
                self._subscribed_devices.discard(device_name)
                # Remove commands from storage
                if device_name in self.data["device_commands"]:
                    del self.data["device_commands"][device_name]
                    _LOGGER.debug("Removed commands for deleted device: %s", device_name)
            
            self.async_set_updated_data(self.data)
        except json.JSONDecodeError:
            _LOGGER.error("Failed to parse device list: %s", payload)

    @callback
    def _handle_macro_list(self, payload: str) -> None:
        """Handle macro list message and manage subscriptions."""
        try:
            macros = json.loads(payload)
            _LOGGER.debug("Received macro list: %s", macros)
            
            # Normalize ID field (handle both "id" and "Id")
            normalized_macros = []
            current_macro_names = set()
            
            for macro in macros:
                normalized_macro = {
                    "id": macro.get("id") or macro.get("Id"),
                    "name": macro.get("name")
                }
                normalized_macros.append(normalized_macro)
                macro_name = normalized_macro.get("name")
                if macro_name:
                    current_macro_names.add(macro_name)
            
            self.data["macros"] = normalized_macros
            _LOGGER.debug("Normalized macros: %s", normalized_macros)
            
            # Detect new macros (not yet subscribed)
            new_macros = current_macro_names - self._subscribed_macros
            
            # Detect removed macros (subscribed but not in current list)
            removed_macros = self._subscribed_macros - current_macro_names
            
            # Subscribe to new macros
            for macro_name in new_macros:
                _LOGGER.info("🆕 New macro detected: %s - subscribing to trigger", macro_name)
                asyncio.create_task(
                    self._subscribe_macro_trigger(macro_name)
                )
                self._subscribed_macros.add(macro_name)
            
            # Clean up removed macros
            for macro_name in removed_macros:
                _LOGGER.info("🗑️ Macro removed: %s - cleaning up", macro_name)
                self._subscribed_macros.discard(macro_name)
                # Remove state from storage
                if macro_name in self.data["macro_states"]:
                    del self.data["macro_states"][macro_name]
                    _LOGGER.debug("Removed state for deleted macro: %s", macro_name)
                    # Save updated states (non-blocking)
                    self.hass.async_create_task(self._save_macro_states())
            
            self.async_set_updated_data(self.data)
        except json.JSONDecodeError:
            _LOGGER.error("Failed to parse macro list: %s", payload)

    @callback
    def _handle_battery(self, payload: str) -> None:
        """Handle battery level message from battery_level topic."""
        try:
            payload = payload.strip()
            _LOGGER.debug("Raw battery_level payload: '%s'", payload)
            
            battery_level = None
            
            # Topic battery_level should contain direct value (0-100)
            # Format 1: Just the number "85"
            if payload.isdigit():
                battery_level = int(payload)
            # Format 2: With percent "85%"
            elif "%" in payload:
                battery_str = payload.replace("%", "").strip()
                if battery_str.isdigit():
                    battery_level = int(battery_str)
            # Format 3: Any text with a number (fallback)
            else:
                import re
                numbers = re.findall(r'\d+', payload)
                if numbers:
                    battery_level = int(numbers[0])
            
            if battery_level is not None:
                # Clamp to 0-100
                battery_level = max(0, min(100, battery_level))
                _LOGGER.info("Battery level updated: %d%%", battery_level)
                self.data["battery_level"] = battery_level
                self.async_set_updated_data(self.data)
            else:
                _LOGGER.warning("Could not parse battery level from: %s", payload)
        except (ValueError, TypeError) as err:
            _LOGGER.error("Failed to parse battery level: %s - %s", payload, err)

    @callback
    def _handle_keys(self, payload: str) -> None:
        """Handle key press events."""
        try:
            # Payload format: "button:#"
            if "button:" in payload:
                button_num = payload.split("button:")[1].strip()
                _LOGGER.debug("Key pressed: button %s", button_num)
                self.data["last_key"] = button_num
                self.async_set_updated_data(self.data)
            else:
                _LOGGER.warning("Unexpected key payload format: %s", payload)
        except (IndexError, AttributeError) as err:
            _LOGGER.error("Failed to parse key event: %s - %s", payload, err)

    @callback
    def _handle_test_status(self, payload: str) -> None:
        """Handle test status message (running macro info)."""
        _LOGGER.debug("Test status: %s", payload)
        self.data["test_status"] = payload
        
        # Try to extract running macro/device info
        # Format: "Pioneer - VSX/SC Series - Off 200"
        if payload and payload != "":
            self.data["running_macro"] = payload
        else:
            self.data["running_macro"] = None
            
        self.async_set_updated_data(self.data)

    async def _subscribe_device_details(self, device_name: str) -> None:
        """Subscribe to device detail/commands topics and request details."""
        topic_commands = f"{self.base_topic}/device/{device_name}/commands"
        topic_detail = f"{self.base_topic}/device/{device_name}/detail"
        
        @callback
        def handle_device_detail(payload: str) -> None:
            """Handle device detail message."""
            # Ignore empty payloads (our own publish request)
            if not payload or payload.strip() == "":
                _LOGGER.debug("Received empty payload for device '%s' - ignoring (our request trigger)", device_name)
                return
            
            try:
                commands = json.loads(payload)
                _LOGGER.info("✓ Received %d commands for device '%s'", len(commands), device_name)
                
                # Normalize ID field (handle both "id" and "Id")
                normalized_commands = []
                for command in commands:
                    normalized_command = {
                        "id": command.get("id") or command.get("Id"),
                        "name": command.get("name")
                    }
                    normalized_commands.append(normalized_command)
                
                self.data["device_commands"][device_name] = normalized_commands
                _LOGGER.info("✓ Stored %d normalized commands for '%s'", len(normalized_commands), device_name)
                self.async_set_updated_data(self.data)
            except json.JSONDecodeError as err:
                _LOGGER.error("Failed to parse device commands for %s: %s - Error: %s", device_name, payload, err)
        
        # Subscribe to BOTH topics for compatibility
        await self._subscribe(topic_commands, handle_device_detail)
        _LOGGER.info("✓ Subscribed to: %s", topic_commands)
        
        await self._subscribe(topic_detail, handle_device_detail)
        _LOGGER.info("✓ Subscribed to (legacy): %s", topic_detail)
        
        # Publish to BOTH topics to request device details (with retained=True)
        for topic in [topic_commands, topic_detail]:
            _LOGGER.debug("Publishing to %s to request device details", topic)
            try:
                await mqtt.async_publish(
                    self.hass,
                    topic,
                    "",  # Empty payload to trigger details request
                    qos=1,
                    retain=True
                )
            except Exception as err:
                _LOGGER.error("✗ Failed to publish device details request for %s: %s", device_name, err)

    async def _subscribe_macro_trigger(self, macro_name: str) -> None:
        """Subscribe to macro trigger topic for state tracking."""
        topic = f"{self.base_topic}/macro/{macro_name}/trigger"
        
        @callback
        def handle_macro_trigger(payload: str) -> None:
            """Handle macro trigger state."""
            state = payload.strip().lower()
            _LOGGER.debug("Macro %s trigger state: %s", macro_name, state)
            
            # Store the macro state
            if state in ["on", "off"]:
                self.data["macro_states"][macro_name] = state
                # Save states to file for persistence (non-blocking)
                self.hass.async_create_task(self._save_macro_states())
                self.async_set_updated_data(self.data)
        
        await self._subscribe(topic, handle_macro_trigger)

    async def async_trigger_macro(self, macro_name: str, action: str = "on") -> None:
        """Trigger a macro with ON or OFF action."""
        topic = f"{self.base_topic}/macro/{macro_name}/trigger"
        _LOGGER.debug("Triggering macro: %s with action: %s", macro_name, action)
        
        # Publish with retained=True so state persists across HA restarts
        await mqtt.async_publish(self.hass, topic, action, qos=1, retain=True)
        
        # Also update local state immediately
        self.data["macro_states"][macro_name] = action
        await self._save_macro_states()
        self.async_set_updated_data(self.data)

    async def async_trigger_device_command(self, device_name: str, command_name: str) -> None:
        """Trigger a device command."""
        topic = f"{self.base_topic}/device/{device_name}/trigger"
        _LOGGER.debug("Triggering command %s for device %s", command_name, device_name)
        await mqtt.async_publish(self.hass, topic, command_name, qos=1, retain=False)

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from MQTT - Request fresh battery level and device details."""
        try:
            _LOGGER.debug("Periodic update triggered - refreshing data")
            
            # Trigger battery level update by publishing to battery/status
            battery_trigger_topic = f"{self.base_topic}/{TOPIC_BATTERY_STATUS}"
            try:
                await mqtt.async_publish(
                    self.hass,
                    battery_trigger_topic,
                    "",  # Empty payload to trigger update
                    qos=1,
                    retain=False
                )
                _LOGGER.debug("Battery level trigger published to %s", battery_trigger_topic)
            except Exception as pub_err:
                _LOGGER.error("Failed to publish battery trigger: %s", pub_err)
            
            # Refresh device details for all subscribed devices
            for device_name in self._subscribed_devices:
                # Publish to both topics for compatibility
                for suffix in ["commands", "detail"]:
                    detail_topic = f"{self.base_topic}/device/{device_name}/{suffix}"
                    try:
                        await mqtt.async_publish(
                            self.hass,
                            detail_topic,
                            "",  # Empty payload to trigger refresh
                            qos=1,
                            retain=True
                        )
                        _LOGGER.debug("Device details refresh published to: %s", detail_topic)
                    except Exception as pub_err:
                        _LOGGER.error("Failed to publish device details refresh for %s: %s", device_name, pub_err)
            
            # Return current data (updates come via MQTT callbacks)
            return self.data
        except Exception as err:
            _LOGGER.error("Error updating data: %s", err)
            raise UpdateFailed(f"Error updating data: {err}") from err

    async def async_shutdown(self) -> None:
        """Unsubscribe from all MQTT topics."""
        _LOGGER.debug("Shutting down coordinator for remote %s", self.remote_id)
        for unsubscribe in self._subscriptions:
            unsubscribe()
        self._subscriptions.clear()

    def get_diagnostics(self) -> dict:
        """Get diagnostic information."""
        return {
            "remote_id": self.remote_id,
            "status": self.data.get("status"),
            "devices_count": len(self.data.get("devices", [])),
            "devices": self.data.get("devices", []),
            "macros_count": len(self.data.get("macros", [])),
            "macros": self.data.get("macros", []),
            "device_commands": {
                device: len(commands) 
                for device, commands in self.data.get("device_commands", {}).items()
            },
            "subscriptions_count": len(self._subscriptions),
        }
