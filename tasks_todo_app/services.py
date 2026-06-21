"""Services for Tasks Todo App integration."""
import voluptuous as vol
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.service import verify_domain_control

from .const import (
    DOMAIN,
    SERVICE_CREATE_ITEM,
    SERVICE_COMPLETE_ITEM,
    SERVICE_UNDO_ITEM,
    SERVICE_CREATE_LIST,
    DATA_CLIENT,
)

# Service schemas
CREATE_ITEM_SCHEMA = vol.Schema({
    vol.Required("list_id"): str,
    vol.Required("title"): str,
    vol.Optional("description", default=""): str,
    vol.Optional("tags", default=[]): [str],
})

COMPLETE_ITEM_SCHEMA = vol.Schema({
    vol.Required("list_id"): str,
    vol.Required("item_id"): str,
})

CREATE_LIST_SCHEMA = vol.Schema({
    vol.Required("name"): str,
    vol.Optional("description", default=""): str,
})


async def setup_services(hass: HomeAssistant):
    """Set up services for Tasks Todo App."""

    async def handle_create_item(call: ServiceCall):
        """Handle create_item service."""
        list_id = call.data["list_id"]
        title = call.data["title"]
        description = call.data.get("description", "")
        tags = call.data.get("tags", [])

        # Get first configured client
        for entry_id in hass.data[DOMAIN]:
            client = hass.data[DOMAIN][entry_id].get(DATA_CLIENT)
            if client:
                result = await client.create_item(
                    list_id, title, description, tags=tags
                )
                return result

    async def handle_complete_item(call: ServiceCall):
        """Handle complete_item service."""
        list_id = call.data["list_id"]
        item_id = call.data["item_id"]

        for entry_id in hass.data[DOMAIN]:
            client = hass.data[DOMAIN][entry_id].get(DATA_CLIENT)
            if client:
                result = await client.complete_item(list_id, item_id)
                return result

    async def handle_undo_item(call: ServiceCall):
        """Handle undo_item service."""
        list_id = call.data["list_id"]
        item_id = call.data["item_id"]

        for entry_id in hass.data[DOMAIN]:
            client = hass.data[DOMAIN][entry_id].get(DATA_CLIENT)
            if client:
                result = await client.undo_item(list_id, item_id)
                return result

    async def handle_create_list(call: ServiceCall):
        """Handle create_list service."""
        name = call.data["name"]
        description = call.data.get("description", "")

        for entry_id in hass.data[DOMAIN]:
            client = hass.data[DOMAIN][entry_id].get(DATA_CLIENT)
            if client:
                result = await client.create_list(name, description)
                return result

    # Register services
    hass.services.async_register(
        DOMAIN,
        SERVICE_CREATE_ITEM,
        handle_create_item,
        schema=CREATE_ITEM_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_COMPLETE_ITEM,
        handle_complete_item,
        schema=COMPLETE_ITEM_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_UNDO_ITEM,
        handle_undo_item,
        schema=COMPLETE_ITEM_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_CREATE_LIST,
        handle_create_list,
        schema=CREATE_LIST_SCHEMA,
    )
