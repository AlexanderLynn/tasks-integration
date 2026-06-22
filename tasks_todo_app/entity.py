"""Base entity for Tasks Todo App integration."""
from __future__ import annotations

from typing import Any, Optional
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator


class TasksAppEntity(Entity):
    """Base entity for Tasks Todo App."""

    coordinator: DataUpdateCoordinator
    list_id: Optional[str]
    item_id: Optional[str]

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        list_id: Optional[str] = None,
        item_id: Optional[str] = None,
    ) -> None:
        """Initialize the entity."""
        self.coordinator = coordinator
        self.list_id = list_id
        self.item_id = item_id

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device info."""
        return {
            "identifiers": {("tasks_todo_app", "main")},
            "name": "Tasks Todo App",
            "manufacturer": "Tasks Team",
            "model": "1.0",
        }

    @property
    def should_poll(self) -> bool:
        """No polling needed."""
        return False

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
