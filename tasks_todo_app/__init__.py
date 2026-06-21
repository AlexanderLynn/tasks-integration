"""Main integration file for Tasks Todo App."""
from __future__ import annotations

import asyncio
from datetime import timedelta
from typing import Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import TasksAppAPIClient
from .const import CONF_HOST, CONF_PORT, DATA_CLIENT, DATA_COORDINATOR, DOMAIN
from .services import setup_services

PLATFORMS: list[Platform] = [Platform.SENSOR]
SCAN_INTERVAL = timedelta(seconds=30)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Tasks Todo App from a config entry."""

    # Ensure domain data exists
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    # Get configuration
    host = entry.data.get(CONF_HOST, "localhost")
    port = entry.data.get(CONF_PORT, 8080)
    api_key = entry.data.get(CONF_API_KEY)

    # Create session and client
    session = async_get_clientsession(hass)
    client = TasksAppAPIClient(host, port, api_key, session)

    # Create coordinator
    coordinator = DataUpdateCoordinator(
        hass,
        name="Tasks Todo App",
        update_interval=SCAN_INTERVAL,
        update_method=lambda: _fetch_data(client),
    )

    # Perform initial update
    await coordinator.async_config_entry_first_refresh()

    # Store client and coordinator
    hass.data[DOMAIN][entry.entry_id] = {
        DATA_CLIENT: client,
        DATA_COORDINATOR: coordinator,
    }

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Set up services
    await setup_services(hass)

    # Listen for unload
    entry.async_on_unload(entry.add_update_listener(update_listener))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
        await client.close()
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def _fetch_data(client: TasksAppAPIClient) -> dict:
    """Fetch data from the API."""
    try:
        lists = await client.get_lists()
        
        # Enrich list data with items
        for list_data in lists:
            items = await client.get_items(list_data["id"])
            list_data["items"] = items

        return {"lists": lists}

    except Exception as err:
        raise UpdateFailed(f"Error fetching data from Tasks API: {err}")
