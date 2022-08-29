"""Const file for Tesla cars."""
VERSION = "2.4.2"
CONF_WAKE_ON_START = "enable_wake_on_start"
CONF_EXPIRATION = "expiration"
CONF_POLLING_POLICY = "polling_policy"
DOMAIN = "tesla_custom"
DATA_LISTENER = "listener"
DEFAULT_SCAN_INTERVAL = 660
DEFAULT_WAKE_ON_START = False
ERROR_URL_NOT_DETECTED = "url_not_detected"
MIN_SCAN_INTERVAL = 10

PLATFORMS = [
    "sensor",
    "lock",
    "climate",
    "binary_sensor",
    "device_tracker",
    "switch",
    "button",
    "select",
]

ICONS = {
    "battery sensor": "mdi:battery",
    "range sensor": "mdi:gauge",
    "mileage sensor": "mdi:counter",
    "parking brake sensor": "mdi:car-brake-parking",
    "charger sensor": "mdi:ev-station",
    "charger switch": "mdi:battery-charging",
    "update switch": "mdi:car-connected",
    "maxrange switch": "mdi:gauge-full",
    "temperature sensor": "mdi:thermometer",
    "location tracker": "mdi:crosshairs-gps",
    "charging rate sensor": "mdi:speedometer",
    "sentry mode switch": "mdi:shield-car",
    "horn": "mdi:bullhorn",
    "flash lights": "mdi:car-light-high",
    "trigger homelink": "mdi:garage",
    "solar panel": "mdi:solar-panel",
    "heated steering wheel": "mdi:steering",
}
AUTH_CALLBACK_PATH = "/auth/tesla/callback"
AUTH_CALLBACK_NAME = "auth:tesla:callback"
AUTH_PROXY_PATH = "/auth/tesla/proxy"
AUTH_PROXY_NAME = "auth:tesla:proxy"

ATTR_PARAMETERS = "parameters"
ATTR_PATH_VARS = "path_vars"
ATTR_POLLING_POLICY_NORMAL = "normal"
ATTR_POLLING_POLICY_CONNECTED = "connected"
ATTR_POLLING_POLICY_ALWAYS = "always"
ATTR_VIN = "vin"
DEFAULT_POLLING_POLICY = ATTR_POLLING_POLICY_NORMAL
SERVICE_API = "api"
SERVICE_SCAN_INTERVAL = "polling_interval"
