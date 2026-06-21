# Tasks Todo App - Home Assistant Integration

Custom Home Assistant integration for Tasks Todo App with real-time task management and scheduling.

## Features

- **4 Sensors**: Active items, completion percentage, overdue items, sync status
- **Service Calls**: Create items, complete items, undo items, create lists
- **Real-time Sync**: Automatic polling every 30 seconds (configurable)
- **DataUpdateCoordinator**: Efficient async data handling
- **Home Assistant 2026.6.0+**: Built for latest HA with proper async patterns

## Installation

### Via HACS (Recommended)
1. Open HACS in Home Assistant
2. Go to **Integrations** → **⋮** → **Custom repositories**
3. Add: `https://github.com/AlexanderLynn/tasks-integration`
4. Select category: **Integration**
5. Click **Explore & Download**
6. Search for "Tasks Todo App"
7. Click **Install**
8. Restart Home Assistant
9. Go to Settings → Devices & Services → Create Integration
10. Search for "Tasks Todo App" and configure

### Manual Installation
1. Clone this repository
2. Copy `tasks_todo_app` folder to `~/.homeassistant/custom_components/`
3. Restart Home Assistant

## Configuration

After installation:
1. Go to Settings → Devices & Services
2. Click **Create Integration**
3. Search for "Tasks Todo App"
4. Enter API URL (e.g., `http://192.168.1.100:8080`)
5. Enter API Key (from addon configuration)
6. Complete the flow

## Available Sensors

- `sensor.tasks_todo_app_active_items` - Number of active tasks
- `sensor.tasks_todo_app_completion_percent` - Overall completion percentage
- `sensor.tasks_todo_app_overdue_items` - Number of overdue tasks
- `sensor.tasks_todo_app_sync_status` - Sync status with backend

## Available Services

- `tasks_todo_app.create_item` - Add new task
- `tasks_todo_app.complete_item` - Mark task complete
- `tasks_todo_app.undo_item` - Undo task completion
- `tasks_todo_app.create_list` - Create new list

## Requirements

- Home Assistant 2026.6.0 or later
- Tasks Todo App addon (for backend API) or standalone backend running

## Links

- **Main Repository**: https://github.com/AlexanderLynn/tasks
- **Addon Repository**: https://github.com/AlexanderLynn/tasks-addon
- **Issues**: https://github.com/AlexanderLynn/tasks/issues

## License

MIT License - See LICENSE file
