# Home Assistant Constants for Tasks Todo App Integration

DOMAIN = "tasks_todo_app"
VERSION = "1.0.0"

# Configuration
CONF_HOST = "host"
CONF_PORT = "port"
CONF_API_KEY = "api_key"

# Defaults
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8080
DEFAULT_NAME = "Tasks Todo App"

# Data keys
DATA_CLIENT = "client"
DATA_COORDINATOR = "coordinator"

# Platforms
PLATFORMS = ["sensor", "switch"]

# Service names
SERVICE_CREATE_ITEM = "create_item"
SERVICE_COMPLETE_ITEM = "complete_item"
SERVICE_UNDO_ITEM = "undo_item"
SERVICE_CREATE_LIST = "create_list"

# Entity prefixes
SENSOR_PREFIX = "sensor.tasks_"
SWITCH_PREFIX = "switch.tasks_"
