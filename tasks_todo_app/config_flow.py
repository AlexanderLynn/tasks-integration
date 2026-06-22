"""Config flow for Tasks Todo App integration."""
from __future__ import annotations

from typing import Any, Optional

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_HOST, CONF_PORT, DEFAULT_HOST, DEFAULT_PORT, DOMAIN
from .api import TasksAppAPIClient


class TasksAppConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Tasks Todo App."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        """Handle a flow initiated by the user."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Validate the connection
            try:
                session = async_get_clientsession(self.hass)
                client = TasksAppAPIClient(
                    user_input[CONF_HOST],
                    user_input[CONF_PORT],
                    user_input[CONF_API_KEY],
                    session
                )
                
                # Test the connection
                await client.get_current_user()
                
            except Exception as e:
                errors["base"] = "cannot_connect"
                return self.async_show_form(
                    step_id="user",
                    data_schema=self._get_schema(user_input),
                    errors=errors,
                )

            # Create config entry
            return self.async_create_entry(
                title="Tasks Todo App",
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=self._get_schema(),
        )

    async def async_step_import(
        self, import_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Handle import from configuration.yaml."""
        return await self.async_step_user(import_data)

    @staticmethod
    def _get_schema(
        data: Optional[dict[str, Any]] = None,
    ) -> vol.Schema:
        """Get the configuration schema."""
        if data is None:
            data = {}

        return vol.Schema({
            vol.Required(
                CONF_HOST,
                default=data.get(CONF_HOST, DEFAULT_HOST)
            ): str,
            vol.Required(
                CONF_PORT,
                default=data.get(CONF_PORT, DEFAULT_PORT)
            ): int,
            vol.Required(
                CONF_API_KEY,
                default=data.get(CONF_API_KEY, "")
            ): str,
        })

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> TasksAppOptionsFlow:
        """Get the options flow."""
        return TasksAppOptionsFlow(config_entry)


class TasksAppOptionsFlow(config_entries.OptionsFlow):
    """Options flow for Tasks Todo App."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    "poll_interval",
                    default=self.config_entry.options.get("poll_interval", 30),
                ): int,
                vol.Optional(
                    "enable_sync",
                    default=self.config_entry.options.get("enable_sync", True),
                ): bool,
            })
        )
