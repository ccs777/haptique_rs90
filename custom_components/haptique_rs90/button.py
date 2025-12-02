"""Button platform for Haptique RS90 Remote integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
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
    """Set up Haptique RS90 button platform."""
    coordinator: HaptiqueRS90Coordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities: list[ButtonEntity] = []
    
    # Create toggle buttons for macros (single button that toggles on/off)
    for macro in coordinator.data.get("macros", []):
        macro_id = macro.get("id")
        macro_name = macro.get("name")
        if macro_id and macro_name:
            entities.append(HaptiqueRS90MacroButton(coordinator, entry, macro_id, macro_name))
    
    async_add_entities(entities)
    
    # Setup dynamic entity addition for future discoveries
    @coordinator.async_add_listener
    def _async_update_entities() -> None:
        """Add new entities when discovered."""
        new_entities: list[ButtonEntity] = []
        
        # Check for new macros
        existing_macro_ids = {
            entity.unique_id.split("_macro_")[1]
            for entity in entities
            if isinstance(entity, HaptiqueRS90MacroButton)
        }
        
        for macro in coordinator.data.get("macros", []):
            macro_id = macro.get("id")
            macro_name = macro.get("name")
            if macro_id and macro_name and macro_id not in existing_macro_ids:
                new_entity = HaptiqueRS90MacroButton(coordinator, entry, macro_id, macro_name)
                new_entities.append(new_entity)
                entities.append(new_entity)
        
        if new_entities:
            async_add_entities(new_entities)


class HaptiqueRS90ButtonBase(CoordinatorEntity, ButtonEntity):
    """Base class for Haptique RS90 buttons."""

    def __init__(
        self,
        coordinator: HaptiqueRS90Coordinator,
        entry: ConfigEntry,
        button_type: str,
        button_id: str,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self._entry = entry
        self._remote_id = entry.data[CONF_REMOTE_ID]
        self._button_type = button_type
        self._button_id = button_id
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
        """Return unique ID for the button."""
        return f"{self._remote_id}_{self._button_type}_{self._button_id}"

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.data.get("status") == "online"


class HaptiqueRS90MacroButton(HaptiqueRS90ButtonBase):
    """Button to toggle a macro on/off."""

    def __init__(
        self,
        coordinator: HaptiqueRS90Coordinator,
        entry: ConfigEntry,
        macro_id: str,
        macro_name: str,
    ) -> None:
        """Initialize the macro button."""
        super().__init__(coordinator, entry, "macro", macro_id)
        self._macro_name = macro_name
        self._attr_name = f"Macro: {macro_name}"
        self._attr_icon = "mdi:play-circle"

    @property
    def icon(self) -> str:
        """Return dynamic icon based on macro state."""
        macro_states = self.coordinator.data.get("macro_states", {})
        current_state = macro_states.get(self._macro_name, "off")
        return "mdi:stop-circle" if current_state == "on" else "mdi:play-circle"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        macro_states = self.coordinator.data.get("macro_states", {})
        current_state = macro_states.get(self._macro_name, "off")
        return {
            "macro_name": self._macro_name,
            "macro_id": self._button_id,
            "current_state": current_state,
        }

    async def async_press(self) -> None:
        """Handle the button press - toggle between on and off."""
        macro_states = self.coordinator.data.get("macro_states", {})
        current_state = macro_states.get(self._macro_name, "off")
        
        # Toggle: if currently "on", send "off", otherwise send "on"
        new_action = "off" if current_state == "on" else "on"
        
        _LOGGER.debug(
            "Toggling macro: %s from %s to %s",
            self._macro_name,
            current_state,
            new_action
        )
        await self.coordinator.async_trigger_macro(self._macro_name, new_action)

