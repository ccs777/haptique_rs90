"""Switch platform for Haptique RS90 Remote integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
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
    """Set up Haptique RS90 switch platform."""
    coordinator: HaptiqueRS90Coordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities: list[SwitchEntity] = []
    
    # Create switches for macros
    for macro in coordinator.data.get("macros", []):
        macro_id = macro.get("id")
        macro_name = macro.get("name")
        if macro_id and macro_name:
            entities.append(HaptiqueRS90MacroSwitch(coordinator, entry, macro_id, macro_name))
    
    async_add_entities(entities)
    
    # Setup dynamic entity addition for future discoveries
    @coordinator.async_add_listener
    def _async_update_entities() -> None:
        """Add new entities when discovered."""
        new_entities: list[SwitchEntity] = []
        
        # Check for new macros
        existing_macro_ids = {
            entity.unique_id.split("_macro_")[1]
            for entity in entities
            if isinstance(entity, HaptiqueRS90MacroSwitch)
        }
        
        for macro in coordinator.data.get("macros", []):
            macro_id = macro.get("id")
            macro_name = macro.get("name")
            if macro_id and macro_name and macro_id not in existing_macro_ids:
                new_entity = HaptiqueRS90MacroSwitch(coordinator, entry, macro_id, macro_name)
                new_entities.append(new_entity)
                entities.append(new_entity)
        
        if new_entities:
            async_add_entities(new_entities)


class HaptiqueRS90SwitchBase(CoordinatorEntity, SwitchEntity):
    """Base class for Haptique RS90 switches."""

    def __init__(
        self,
        coordinator: HaptiqueRS90Coordinator,
        entry: ConfigEntry,
        switch_type: str,
        switch_id: str,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self.coordinator = coordinator
        self._switch_type = switch_type
        self._switch_id = switch_id
        
        # Unique ID for the entity
        self._attr_unique_id = (
            f"{entry.data[CONF_REMOTE_ID]}_{switch_type}_{switch_id}"
        )
        
        # Device info
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data[CONF_REMOTE_ID])},
        }

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.data.get("status") == "online"


class HaptiqueRS90MacroSwitch(HaptiqueRS90SwitchBase):
    """Switch to control a macro on/off."""

    def __init__(
        self,
        coordinator: HaptiqueRS90Coordinator,
        entry: ConfigEntry,
        macro_id: str,
        macro_name: str,
    ) -> None:
        """Initialize the macro switch."""
        super().__init__(coordinator, entry, "macro", macro_id)
        self._macro_name = macro_name
        self._attr_name = f"Macro: {macro_name}"
        self._attr_icon = "mdi:play-circle"

    @property
    def is_on(self) -> bool:
        """Return True if the macro is currently running."""
        macro_states = self.coordinator.data.get("macro_states", {})
        current_state = macro_states.get(self._macro_name, "off")
        return current_state == "on"

    @property
    def icon(self) -> str:
        """Return dynamic icon based on state."""
        return "mdi:stop-circle" if self.is_on else "mdi:play-circle"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        macro_states = self.coordinator.data.get("macro_states", {})
        current_state = macro_states.get(self._macro_name, "off")
        return {
            "macro_name": self._macro_name,
            "macro_id": self._switch_id,
            "current_state": current_state,
        }

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the macro on."""
        _LOGGER.debug("Turning on macro: %s", self._macro_name)
        await self.coordinator.async_trigger_macro(self._macro_name, "on")

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the macro off."""
        _LOGGER.debug("Turning off macro: %s", self._macro_name)
        await self.coordinator.async_trigger_macro(self._macro_name, "off")
