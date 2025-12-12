"""Tesla Config Flow."""

from http import HTTPStatus
import logging
import os

from homeassistant import config_entries, core, exceptions
from homeassistant.const import (
    CONF_ACCESS_TOKEN,
    CONF_CLIENT_ID,
    CONF_DOMAIN,
    CONF_SCAN_INTERVAL,
    CONF_TOKEN,
    CONF_USERNAME,
)
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.httpx_client import SERVER_SOFTWARE, USER_AGENT
import httpx
from teslajsonpy import Controller as TeslaAPI, TeslaException
from teslajsonpy.const import AUTH_DOMAIN
from teslajsonpy.exceptions import IncompleteCredentials
import voluptuous as vol

from .const import (
    ATTR_POLLING_POLICY_ALWAYS,
    ATTR_POLLING_POLICY_CONNECTED,
    ATTR_POLLING_POLICY_NORMAL,
    CONF_API_PROXY_CERT,
    CONF_API_PROXY_ENABLE,
    CONF_API_PROXY_URL,
    CONF_ENABLE_TESLAMATE,
    CONF_EXPIRATION,
    CONF_INCLUDE_ENERGYSITES,
    CONF_INCLUDE_VEHICLES,
    CONF_POLLING_POLICY,
    CONF_WAKE_ON_START,
    DEFAULT_ENABLE_TESLAMATE,
    DEFAULT_POLLING_POLICY,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_WAKE_ON_START,
    DOMAIN,
    MIN_SCAN_INTERVAL,
)
from .util import SSL_CONTEXT

_LOGGER = logging.getLogger(__name__)


class TeslaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Tesla."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the tesla flow."""
        self.username = None
        self.reauth = False
        self.use_proxy = False

    async def async_step_import(self, import_config):
        """Import a config entry from configuration.yaml."""
        return await self.async_step_user(import_config)

    async def async_step_user(self, user_input=None):
        """Handle the start of the config flow."""
        data_schema = vol.Schema(
            {
                vol.Required(CONF_API_PROXY_ENABLE, default=False): bool,
            }
        )

        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=data_schema,
            )

        # in case we import a config entry from configuration.yaml
        if CONF_API_PROXY_CERT in user_input:
            return await self.async_step_credentials(user_input)

        self.use_proxy = user_input.get(CONF_API_PROXY_ENABLE, False)
        return await self.async_step_credentials()

    async def async_step_credentials(self, user_input=None):
        """Handle the second step of the config flow."""
        errors = {}

        if user_input is not None:
            existing_entry = self._async_entry_for_username(user_input[CONF_USERNAME])
            if existing_entry and not self.reauth:
                return self.async_abort(reason="already_configured")

            try:
                info = await validate_input(self.hass, user_input)
                # Used for only forcing cars awake on initial setup in async_setup_entry
                info.update({"initial_setup": True})
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"

            if not errors:
                if existing_entry:
                    self.hass.config_entries.async_update_entry(
                        existing_entry, data=info
                    )
                    await self.hass.config_entries.async_reload(existing_entry.entry_id)
                    return self.async_abort(reason="reauth_successful")

                return self.async_create_entry(
                    title=user_input[CONF_USERNAME], data=info
                )

        return self.async_show_form(
            step_id="credentials",
            data_schema=self._async_schema(api_proxy_enable=self.use_proxy),
            errors=errors,
            description_placeholders={},
        )

    async def async_step_reauth(self, data):
        """Handle configuration by re-auth."""
        self.username = data[CONF_USERNAME]
        self.reauth = True
        return await self.async_step_user()

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler()

    @callback
    def _async_schema(self, api_proxy_enable: bool):
        """Fetch schema with defaults."""

        schema = vol.Schema(
            {
                vol.Required(CONF_USERNAME, default=self.username): str,
                vol.Required(CONF_TOKEN): str,
                vol.Required(CONF_DOMAIN, default=AUTH_DOMAIN): str,
                vol.Required(CONF_INCLUDE_VEHICLES, default=True): bool,
                vol.Required(CONF_INCLUDE_ENERGYSITES, default=True): bool,
            }
        )

        api_proxy_cert = api_proxy_url = client_id = None
        if api_proxy_enable:
            # autofill fields if HTTP Proxy is running as addon
            if "SUPERVISOR_TOKEN" in os.environ:
                _LOGGER.debug("Running in supervised environment")
                # find out if addon is running from normal repo or local
                req = httpx.get(
                    "http://supervisor/addons",
                    headers={
                        "Authorization": f"Bearer {os.environ['SUPERVISOR_TOKEN']}"
                    },
                )
                for addon in req.json()["data"]["addons"]:
                    if addon["name"] == "Tesla HTTP Proxy":
                        addon_slug = addon["slug"]
                        break

                try:
                    # read Client ID from addon
                    req = httpx.get(
                        f"http://supervisor/addons/{addon_slug}/info",
                        headers={
                            "Authorization": f"Bearer {os.environ['SUPERVISOR_TOKEN']}"
                        },
                    )
                    client_id = req.json()["data"]["options"]["client_id"]
                    api_proxy_url = "https://" + req.json()["data"]["hostname"]
                    api_proxy_cert = "/share/tesla/selfsigned.pem"
                    _LOGGER.debug("Found addon: %s", addon_slug)
                except NameError:
                    _LOGGER.warning("Unable to communicate with Tesla HTTP Proxy addon")

            schema = schema.extend(
                {
                    vol.Required(CONF_API_PROXY_URL, default=api_proxy_url): str,
                    vol.Required(CONF_API_PROXY_CERT, default=api_proxy_cert): str,
                    vol.Required(CONF_CLIENT_ID, default=client_id): str,
                }
            )
        return schema

    @callback
    def _async_entry_for_username(self, username):
        """Find an existing entry for a username."""
        for entry in self._async_current_entries():
            if entry.data.get(CONF_USERNAME) == username:
                return entry
        return None


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle a option flow for Tesla."""

    async def async_step_init(self, user_input=None):
        """Handle options flow."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_SCAN_INTERVAL,
                    default=self.config_entry.options.get(
                        CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                    ),
                ): vol.All(cv.positive_int, vol.Clamp(min=MIN_SCAN_INTERVAL)),
                vol.Optional(
                    CONF_WAKE_ON_START,
                    default=self.config_entry.options.get(
                        CONF_WAKE_ON_START, DEFAULT_WAKE_ON_START
                    ),
                ): bool,
                vol.Required(
                    CONF_POLLING_POLICY,
                    default=self.config_entry.options.get(
                        CONF_POLLING_POLICY, DEFAULT_POLLING_POLICY
                    ),
                ): vol.In(
                    [
                        ATTR_POLLING_POLICY_NORMAL,
                        ATTR_POLLING_POLICY_CONNECTED,
                        ATTR_POLLING_POLICY_ALWAYS,
                    ]
                ),
                vol.Optional(
                    CONF_ENABLE_TESLAMATE,
                    default=self.config_entry.options.get(
                        CONF_ENABLE_TESLAMATE, DEFAULT_ENABLE_TESLAMATE
                    ),
                ): bool,
            }
        )
        return self.async_show_form(step_id="init", data_schema=data_schema)


async def validate_input(hass: core.HomeAssistant, data) -> dict:
    """Validate the user input allows us to connect.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """

    config = {}
    async_client = httpx.AsyncClient(
        headers={USER_AGENT: SERVER_SOFTWARE}, timeout=60, verify=SSL_CONTEXT
    )

    try:
        controller = TeslaAPI(
            async_client,
            email=data[CONF_USERNAME],
            refresh_token=data[CONF_TOKEN],
            update_interval=DEFAULT_SCAN_INTERVAL,
            expiration=data.get(CONF_EXPIRATION, 0),
            auth_domain=data.get(CONF_DOMAIN, AUTH_DOMAIN),
            polling_policy=data.get(CONF_POLLING_POLICY, DEFAULT_POLLING_POLICY),
            api_proxy_cert=data.get(CONF_API_PROXY_CERT),
            api_proxy_url=data.get(CONF_API_PROXY_URL),
            client_id=data.get(CONF_CLIENT_ID),
        )
        result = await controller.connect(test_login=True)
        config[CONF_TOKEN] = result["refresh_token"]
        config[CONF_ACCESS_TOKEN] = result[CONF_ACCESS_TOKEN]
        config[CONF_EXPIRATION] = result[CONF_EXPIRATION]
        config[CONF_USERNAME] = data[CONF_USERNAME]
        config[CONF_DOMAIN] = data.get(CONF_DOMAIN, AUTH_DOMAIN)
        config[CONF_INCLUDE_VEHICLES] = data[CONF_INCLUDE_VEHICLES]
        config[CONF_INCLUDE_ENERGYSITES] = data[CONF_INCLUDE_ENERGYSITES]
        config[CONF_API_PROXY_URL] = data.get(CONF_API_PROXY_URL)
        config[CONF_API_PROXY_CERT] = data.get(CONF_API_PROXY_CERT)
        config[CONF_CLIENT_ID] = data.get(CONF_CLIENT_ID, "ownerapi")

    except IncompleteCredentials as ex:
        _LOGGER.error("Authentication error: %s %s", ex.message, ex)
        raise InvalidAuth() from ex
    except TeslaException as ex:
        if ex.code == HTTPStatus.UNAUTHORIZED or isinstance(ex, IncompleteCredentials):
            _LOGGER.error("Invalid credentials: %s", ex.message)
            raise InvalidAuth() from ex
        _LOGGER.error("Unable to communicate with Tesla API: %s", ex.message)
        raise CannotConnect() from ex
    finally:
        await async_client.aclose()
    _LOGGER.debug("Credentials successfully connected to the Tesla API")
    return config


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""
