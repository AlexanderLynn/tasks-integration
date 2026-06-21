"""Base entity for Tasks Todo App integration."""
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_registry import async_get


class TasksAppEntity(Entity):
    """Base entity for Tasks Todo App."""

    def __init__(self, coordinator, list_id=None, item_id=None):
        """Initialize the entity."""
        self.coordinator = coordinator
        self.list_id = list_id
        self.item_id = item_id

    @property
    def device_info(self):
        """Return device info."""
        return {
            "identifiers": {("tasks_todo_app", "main")},
            "name": "Tasks Todo App",
            "manufacturer": "Tasks Team",
            "model": "1.0",
        }

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
