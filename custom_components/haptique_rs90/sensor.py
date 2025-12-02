"""Sensor platform for Haptique RS90 Remote integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, CONF_REMOTE_ID
from .coordinator import HaptiqueRS90Coordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Haptique RS90 sensor platform."""
    coordinator: HaptiqueRS90Coordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        HaptiqueRS90BatterySensor(coordinator, entry),
        HaptiqueRS90LastKeySensor(coordinator, entry),
        HaptiqueRS90RunningMacroSensor(coordinator, entry),
        HaptiqueRS90DeviceListSensor(coordinator, entry),
    ]
    
    async_add_entities(entities)


class HaptiqueRS90SensorBase(CoordinatorEntity, SensorEntity):
    """Base class for Haptique RS90 sensors."""

    def __init__(
        self,
        coordinator: HaptiqueRS90Coordinator,
        entry: ConfigEntry,
        sensor_type: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry = entry
        self._remote_id = entry.data[CONF_REMOTE_ID]
        self._sensor_type = sensor_type
        self._attr_has_entity_name = True
        self._attr_device_info = {
            "identifiers": {(DOMAIN, self._remote_id)},
            "name": entry.data.get("name", f"Haptique RS90 {self._remote_id[:8]}"),
            "manufacturer": "Haptique",
            "model": "RS90",
            "sw_version": "1.0",
        }

    @property
    def unique_id(self) -> str:
        """Return unique ID for the sensor."""
        return f"{self._remote_id}_{self._sensor_type}"


class HaptiqueRS90BatterySensor(HaptiqueRS90SensorBase):
    """Battery level sensor for Haptique RS90."""

    def __init__(
        self,
        coordinator: HaptiqueRS90Coordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the battery sensor."""
        super().__init__(coordinator, entry, "battery")
        self._attr_name = "Battery"
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:battery"

    @property
    def native_value(self) -> int | None:
        """Return the battery level."""
        return self.coordinator.data.get("battery_level")

    @property
    def icon(self) -> str:
        """Return the icon based on battery level."""
        battery_level = self.native_value
        if battery_level is None:
            return "mdi:battery-unknown"
        if battery_level <= 10:
            return "mdi:battery-10"
        if battery_level <= 20:
            return "mdi:battery-20"
        if battery_level <= 30:
            return "mdi:battery-30"
        if battery_level <= 40:
            return "mdi:battery-40"
        if battery_level <= 50:
            return "mdi:battery-50"
        if battery_level <= 60:
            return "mdi:battery-60"
        if battery_level <= 70:
            return "mdi:battery-70"
        if battery_level <= 80:
            return "mdi:battery-80"
        if battery_level <= 90:
            return "mdi:battery-90"
        return "mdi:battery"


class HaptiqueRS90LastKeySensor(HaptiqueRS90SensorBase):
    """Last key pressed sensor for Haptique RS90."""

    def __init__(
        self,
        coordinator: HaptiqueRS90Coordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the last key sensor."""
        super().__init__(coordinator, entry, "last_key")
        self._attr_name = "Last Key Pressed"
        self._attr_icon = "mdi:gesture-tap-button"

    @property
    def native_value(self) -> str | None:
        """Return the last key pressed."""
        last_key = self.coordinator.data.get("last_key")
        if last_key:
            return f"Button {last_key}"
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        last_key = self.coordinator.data.get("last_key")
        if last_key:
            return {"button_number": last_key}
        return {}


class HaptiqueRS90RunningMacroSensor(HaptiqueRS90SensorBase):
    """Running macro sensor for Haptique RS90."""

    def __init__(
        self,
        coordinator: HaptiqueRS90Coordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the running macro sensor."""
        super().__init__(coordinator, entry, "running_macro")
        self._attr_name = "Running Macro"
        self._attr_icon = "mdi:play-circle"

    @property
    def native_value(self) -> str | None:
        """Return the running macro name or Idle."""
        # Get the macro that has status "on"
        macro_states = self.coordinator.data.get("macro_states", {})
        for macro_name, state in macro_states.items():
            if state == "on":
                return macro_name
        return "Idle"

    @property
    def icon(self) -> str:
        """Return icon based on state."""
        if self.native_value and self.native_value != "Idle":
            return "mdi:play-circle"
        return "mdi:stop-circle"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        macro_states = self.coordinator.data.get("macro_states", {})
        return {
            "macro_states": macro_states,
            "active_macros": [name for name, state in macro_states.items() if state == "on"],
        }


class HaptiqueRS90DeviceListSensor(HaptiqueRS90SensorBase):
    """Device list sensor for Haptique RS90."""

    def __init__(
        self,
        coordinator: HaptiqueRS90Coordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the device list sensor."""
        super().__init__(coordinator, entry, "device_list")
        self._attr_name = "Device List"
        self._attr_icon = "mdi:devices"

    @property
    def native_value(self) -> int:
        """Return the number of devices."""
        devices = self.coordinator.data.get("devices", [])
        return len(devices)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return device names as attributes."""
        devices = self.coordinator.data.get("devices", [])
        device_names = [device.get("name") for device in devices if device.get("name")]
        
        attributes = {
            "device_count": len(devices),
            "devices": device_names,
        }
        
        # Add each device as a separate attribute for easy access
        for idx, name in enumerate(device_names, 1):
            attributes[f"device_{idx}"] = name
        
        return attributes
