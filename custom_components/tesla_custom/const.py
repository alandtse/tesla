"""Const file for Tesla cars."""
VERSION = "3.9.1"
CONF_EXPIRATION = "expiration"
CONF_INCLUDE_VEHICLES = "include_vehicles"
CONF_INCLUDE_ENERGYSITES = "include_energysites"
CONF_POLLING_POLICY = "polling_policy"
CONF_WAKE_ON_START = "enable_wake_on_start"
DOMAIN = "tesla_custom"
ATTRIBUTION = "Data provided by Tesla"
DATA_LISTENER = "listener"
DEFAULT_SCAN_INTERVAL = 660
DEFAULT_WAKE_ON_START = False
ERROR_URL_NOT_DETECTED = "url_not_detected"
MIN_SCAN_INTERVAL = 10

PLATFORMS = [
    "sensor",
    "lock",
    "climate",
    "cover",
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
DISTANCE_UNITS_KM_HR = "km/hr"
SERVICE_API = "api"
SERVICE_SCAN_INTERVAL = "polling_interval"
