# Tasks Todo App - Home Assistant Integration

The Python-based Home Assistant integration that communicates with the **Tasks Todo App addon**.

## Installation

### Option 1: Manual Installation (Recommended)

1. **Copy integration to custom_components**:
   ```bash
   mkdir -p ~/.homeassistant/custom_components/tasks_todo_app
   cp -r ./home-assistant-integration/* ~/.homeassistant/custom_components/tasks_todo_app/
   ```

2. **Restart Home Assistant**:
   - Go to **Settings → System → Restart**
   - Or via command: `systemctl restart homeassistant@homeassistant`

3. **Add integration**:
   - Go to **Settings → Devices & Services**
   - Click **Create Integration**
   - Search for **Tasks Todo App**
   - Fill in:
     - **Host**: `localhost` (or addon container hostname)
     - **Port**: `8080`
     - **API Key**: The key set in addon configuration
   - Click **Create**

### Option 2: YAML Configuration

Add to your `configuration.yaml`:

```yaml
tasks_todo_app:
  host: localhost
  port: 8080
  api_key: your-secret-key-here
```

Then restart Home Assistant.

## Features

### Sensors

The integration creates the following sensors:

- **Active Items** per list
- **Completion Percentage** per list
- **Total Overdue Items** across all lists
- **Sync Status** (synced/offline)

### Services

Call these services from automations and scripts:

#### `tasks_todo_app.create_item`
Create a new item in a list:
```yaml
service: tasks_todo_app.create_item
data:
  list_id: "list-123"
  title: "Buy groceries"
  description: "Milk, eggs, bread"
  tags: ["shopping"]
```

#### `tasks_todo_app.complete_item`
Mark an item as complete:
```yaml
service: tasks_todo_app.complete_item
data:
  list_id: "list-123"
  item_id: "item-456"
```

#### `tasks_todo_app.undo_item`
Undo completion of an item:
```yaml
service: tasks_todo_app.undo_item
data:
  list_id: "list-123"
  item_id: "item-456"
```

#### `tasks_todo_app.create_list`
Create a new list:
```yaml
service: tasks_todo_app.create_list
data:
  name: "Groceries"
  description: "Weekly shopping list"
```

## Configuration

### Options

In Home Assistant UI:
- **Host**: The hostname/IP of the addon (default: localhost)
- **Port**: The port the addon is running on (default: 8080)
- **API Key**: The API key from addon configuration
- **Poll Interval** (options): How often to update sensors (default: 30s)
- **Enable Sync** (options): Background sync when changes detected (default: on)

### Automations Example

Complete an item via button press:
```yaml
automation:
  - alias: "Mark item done"
    trigger:
      platform: state
      entity_id: input_button.mark_item_done
      to: "on"
    action:
      service: tasks_todo_app.complete_item
      data:
        list_id: "{{ state_attr('sensor.tasks_shopping_active_items', 'list_id') }}"
        item_id: "{{ trigger.entity_id }}"
```

## Troubleshooting

### Integration not showing up
- Make sure files are in `~/.homeassistant/custom_components/tasks_todo_app/`
- Restart Home Assistant (not just reload)
- Check Home Assistant logs: **Settings → System → Logs**

### Cannot connect error
- Verify addon is running: **Settings → Add-ons → Tasks Todo App → Check status**
- Check host/port/API key in integration configuration
- Try connecting directly: `curl http://localhost:8080/api/lists -H "Authorization: Bearer YOUR_KEY"`

### Sensors not updating
- Check **Poll Interval** in integration options (should be 30 seconds)
- Verify API key is correct (compare with addon settings)
- Check integration status: **Settings → Devices & Services → Integrations**

### API Key errors
- Regenerate key in addon configuration
- Update integration configuration with new key
- Restart integration or Home Assistant

## File Structure

```
home-assistant-integration/
├── __init__.py          # Main integration setup
├── api.py              # API client
├── config_flow.py      # Configuration UI flow
├── const.py            # Constants
├── entity.py           # Base entity class
├── sensor.py           # Sensor platform
├── services.py         # Service definitions
├── strings.json        # UI strings
├── manifest.json       # Integration metadata
└── README.md          # This file
```

## Requirements

- Home Assistant 2025.1.0 or later
- Tasks Todo App addon (Phase 6)
- Network connectivity between Home Assistant and addon
