"""Sensor platform for Tasks Todo App integration."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import PERCENTAGE
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from typing import Any

from .const import DOMAIN, DATA_COORDINATOR, DATA_CLIENT
from .entity import TasksAppEntity


async def async_setup_entry(hass, entry, async_add_entities: AddEntitiesCallback):
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

    def __init__(self, coordinator, list_id, list_name):
        """Initialize sensor."""
        super().__init__(coordinator, list_id)
        self._list_name = list_name
        self._attr_unique_id = f"tasks_{list_id}_active_items"
        self._attr_name = f"Tasks {list_name} Active Items"
        self._attr_icon = "mdi:format-list-checks"
        self._attr_native_unit_of_measurement = "items"

    @property
    def native_value(self) -> StateType:
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

    def __init__(self, coordinator, list_id, list_name):
        """Initialize sensor."""
        super().__init__(coordinator, list_id)
        self._list_name = list_name
        self._attr_unique_id = f"tasks_{list_id}_completion_percent"
        self._attr_name = f"Tasks {list_name} Completion %"
        self._attr_icon = "mdi:progress-clock"
        self._attr_native_unit_of_measurement = PERCENTAGE

    @property or "lists" not in self.coordinator.data:
            return 0

        for list_data in self.coordinator.data.get("lists", []):
            if list_data.get("id") == self.list_id:
                items = list_data.get("items", [])
                if not items:
                    return 0
                completed = sum(1 for item in items if item.get("completed"))
                return round((completed / len(items)) * 100)
        return 0

        completed = sum(1 for item in items if item.get("completed"))
        return round((completed / len(items)) * 100)


class OverdueItemsSensor(TasksAppEntity, SensorEntity):
    """Sensor for overdue items."""

    def __init__(self, coordinator):
        """Initialize sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = "tasks_overdue_items_total"
        self._attr_name = "Tasks Overdue Items"
        self._attr_icon = "mdi:clock-alert"
        self._attr_native_unit_of_measurement = "items"

    @property
    def native_value(self) -> StateType:
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

    def __init__(self, coordinator, client):
        """Initialize sensor."""
        super().__init__(coordinator)
        self._client = client
        self._attr_unique_id = "tasks_sync_status"
        self._attr_name = "Tasks Sync Status"
        self._attr_icon = "mdi:cloud-sync"

    @property
    def native_value(self) -> StateType:
        """Return the state."""
        if not self.coordinator.last_update_success:
            return "offline"
        return "synced"
