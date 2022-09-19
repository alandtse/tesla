"""Const file for Tesla cars."""
VERSION = "2.1.1"
CONF_WAKE_ON_START = "enable_wake_on_start"
CONF_EXPIRATION = "expiration"
CONF_POLLING_POLICY = "polling_policy"
DOMAIN = "tesla_custom"
ATTRIBUTION = "Data provided by Tesla"
DATA_LISTENER = "listener"
DEFAULT_SCAN_INTERVAL = 660
DEFAULT_WAKE_ON_START = True
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
    "update",
    "number",
]

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
