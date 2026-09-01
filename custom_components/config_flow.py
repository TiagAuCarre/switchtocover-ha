"""Config flow for SwitchToCover."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.helpers import selector

from . import DOMAIN

CONF_COVER_TYPE = "cover_type"
CONF_SWITCH_ENTITY = "switch_entity"
CONF_CONTACT_ENTITY = "contact_entity"


def _entity_selector(domain: str) -> selector.EntitySelector:
    return selector.EntitySelector(
        selector.EntitySelectorConfig(domain=domain, multiple=False)
    )


class SwitchToCoverConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle adding one switch-controlled cover at a time."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the setup form shown in the Home Assistant UI."""
        errors = {}
        if user_input is not None:
            switch = self.hass.states.get(user_input[CONF_SWITCH_ENTITY])
            contact = self.hass.states.get(user_input[CONF_CONTACT_ENTITY])

            if switch is None or switch.domain != "switch":
                errors[CONF_SWITCH_ENTITY] = "invalid_switch"
            elif contact is None or contact.domain != "binary_sensor":
                errors[CONF_CONTACT_ENTITY] = "invalid_contact"
            else:
                unique_id = (
                    f"{user_input[CONF_SWITCH_ENTITY]}|"
                    f"{user_input[CONF_CONTACT_ENTITY]}"
                )
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default="Garage"): str,
                vol.Required(CONF_COVER_TYPE, default="garage"): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            selector.SelectOptionDict(value="garage", label="Garage"),
                            selector.SelectOptionDict(value="gate", label="Portail"),
                            selector.SelectOptionDict(value="other", label="Autre"),
                        ],
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
                vol.Required(
                    CONF_SWITCH_ENTITY, default="switch.exterieur_garage"
                ): _entity_selector("switch"),
                vol.Required(
                    CONF_CONTACT_ENTITY, default="binary_sensor.garage_contact"
                ): _entity_selector("binary_sensor"),
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
