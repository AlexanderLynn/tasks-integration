"""Sensor platform for Tasks Todo App integration."""
from __future__ import annotations

from typing import Any
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DOMAIN, DATA_COORDINATOR, DATA_CLIENT
from .entity import TasksAppEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_COORDINATOR]
    client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]

    entities = []

    # Get lists from coordinator data
    if coordinator.data and "lists" in coordinator.data:
        for list_data in coordinator.data.get("lists", []):
            list_id = list_data.get("id")
            list_name = list_data.get("name", "Unknown")
            
            if not list_id:
                continue

            # Active items sensor
            entities.append(
                ActiveItemsSensor(
                    coordinator,
                    list_id,
                    list_name,
                )
            )

            # Completion percentage sensor
            entities.append(
                CompletionPercentSensor(
                    coordinator,
                    list_id,
                    list_name,
                )
            )

    # Overall status sensors
    entities.append(OverdueItemsSensor(coordinator))
    entities.append(SyncStatusSensor(coordinator, client))

    async_add_entities(entities)


class ActiveItemsSensor(TasksAppEntity, SensorEntity):
    """Sensor for active items count."""

    _attr_icon: str = "mdi:format-list-checks"
    _attr_native_unit_of_measurement: str = "items"

    def __init__(
        self, coordinator: Any, list_id: str, list_name: str
    ) -> None:
        """Initialize sensor."""
        super().__init__(coordinator, list_id)
        self._list_name = list_name
        self._attr_unique_id = f"tasks_{list_id}_active_items"
        self._attr_name = f"Tasks {list_name} Active Items"

    @property
    def native_value(self) -> int:
        """Return the state."""
        if not self.coordinator.data or "lists" not in self.coordinator.data:
            return 0

        for list_data in self.coordinator.data.get("lists", []):
            if list_data.get("id") == self.list_id:
                items = list_data.get("items", [])
                active = sum(1 for item in items if not item.get("completed"))
                return active
        return 0


class CompletionPercentSensor(TasksAppEntity, SensorEntity):
    """Sensor for completion percentage."""

    _attr_icon: str = "mdi:progress-clock"
    _attr_native_unit_of_measurement: str = PERCENTAGE

    def __init__(
        self, coordinator: Any, list_id: str, list_name: str
    ) -> None:
        """Initialize sensor."""
        super().__init__(coordinator, list_id)
        self._list_name = list_name
        self._attr_unique_id = f"tasks_{list_id}_completion_percent"
        self._attr_name = f"Tasks {list_name} Completion %"

    @property
    def native_value(self) -> int:
        """Return the state."""
        if not self.coordinator.data or "lists" not in self.coordinator.data:
            return 0

        for list_data in self.coordinator.data.get("lists", []):
            if list_data.get("id") == self.list_id:
                items = list_data.get("items", [])
                if not items:
                    return 0
                completed = sum(1 for item in items if item.get("completed"))
                return round((completed / len(items)) * 100)
class OverdueItemsSensor(TasksAppEntity, SensorEntity):
    """Sensor for overdue items."""

    _attr_icon: str = "mdi:clock-alert"
    _attr_native_unit_of_measurement: str = "items"

    def __init__(self, coordinator: Any) -> None:
        """Initialize sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = "tasks_overdue_items_total"
        self._attr_name = "Tasks Overdue Items"

    @property
    def native_value(self) -> int:
        """Return the state."""
        if not self.coordinator.data:
            return 0

        from datetime import datetime

        overdue_count = 0
        now = datetime.now()

        for list_data in self.coordinator.data.get("lists", []):
            for item in list_data.get("items", []):
                if not item.get("completed"):
                    due_date = item.get("dueDate")
                    if due_date:
                        due_datetime = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
                        if due_datetime < now:
                            overdue_count += 1

        return overdue_count


class SyncStatusSensor(TasksAppEntity, SensorEntity):
    """Sensor for sync status."""

    _attr_icon: str = "mdi:cloud-sync"

    def __init__(self, coordinator: Any, client: Any) -> None:
        """Initialize sensor."""
        super().__init__(coordinator)
        self._client = client
        self._attr_unique_id = "tasks_sync_status"
        self._attr_name = "Tasks Sync Status"

    @property
    def native_value(self) -> str:
        """Return the state."""
        if not self.coordinator.last_update_success:
            return "offline"
        return "synced"
