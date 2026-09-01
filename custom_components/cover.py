"""Cover entities controlled by existing Home Assistant switches."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.cover import CoverEntity, CoverEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_OFF, STATE_ON
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from . import DOMAIN


@dataclass(frozen=True)
class SwitchToCoverConfig:
    name: str
    switch_entity_id: str
    contact_entity_id: str


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up one cover from one UI-created config entry."""
    data = entry.data
    config = SwitchToCoverConfig(
        name=data["name"],
        switch_entity_id=data["switch_entity"],
        contact_entity_id=data["contact_entity"],
    )
    async_add_entities([SwitchToCover(hass, config, entry.entry_id)])


class SwitchToCover(CoverEntity):
    """Represent a cover backed by a switch and a contact sensor."""

    _attr_has_entity_name = False
    _attr_supported_features = CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE

    def __init__(self, hass: HomeAssistant, config: SwitchToCoverConfig, entry_id: str):
        self.hass = hass
        self._config = config
        self._attr_name = config.name
        self._attr_unique_id = entry_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry_id)},
            name=config.name,
            manufacturer="SwitchToCover",
            model="Switch and contact sensor",
        )

    async def async_added_to_hass(self) -> None:
        """Refresh the cover as soon as a linked entity changes."""
        self.async_on_remove(
            async_track_state_change_event(
                self.hass,
                [self._config.switch_entity_id, self._config.contact_entity_id],
                self._async_linked_entity_changed,
            )
        )

    @callback
    def _async_linked_entity_changed(self, event) -> None:
        self.async_write_ha_state()

    @property
    def is_closed(self) -> bool | None:
        """Return closed when the contact sensor is off."""
        state = self.hass.states.get(self._config.contact_entity_id)
        return None if state is None else state.state == STATE_OFF

    @property
    def is_opening(self) -> bool | None:
        """Infer opening from the switch command and contact state."""
        return self._switch_state == STATE_ON and self.is_closed is False

    @property
    def is_closing(self) -> bool | None:
        """Infer closing from the switch command and contact state."""
        return self._switch_state == STATE_OFF and self.is_closed is True

    @property
    def _switch_state(self) -> str | None:
        state = self.hass.states.get(self._config.switch_entity_id)
        return None if state is None else state.state

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Expose source entities for troubleshooting and automations."""
        return {
            "switch_entity": self._config.switch_entity_id,
            "contact_entity": self._config.contact_entity_id,
        }

    async def async_open_cover(self, **kwargs) -> None:
        """Open the cover by turning on the linked switch."""
        await self.hass.services.async_call(
            "switch", "turn_on", {"entity_id": self._config.switch_entity_id}, blocking=True
        )

    async def async_close_cover(self, **kwargs) -> None:
        """Close the cover by turning off the linked switch."""
        await self.hass.services.async_call(
            "switch", "turn_off", {"entity_id": self._config.switch_entity_id}, blocking=True
        )
