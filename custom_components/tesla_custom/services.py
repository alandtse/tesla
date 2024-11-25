"""Support for Tesla services.

SPDX-License-Identifier: Apache-2.0
"""

import logging

from homeassistant.const import ATTR_COMMAND, CONF_EMAIL, CONF_SCAN_INTERVAL
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv
from teslajsonpy import Controller
import voluptuous as vol

from .const import (
    ATTR_PARAMETERS,
    ATTR_PATH_VARS,
    ATTR_VIN,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    SERVICE_API,
    SERVICE_SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


API_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_EMAIL): vol.All(cv.string, vol.Length(min=1)),
        vol.Required(ATTR_COMMAND, default=""): vol.All(cv.string, vol.Length(min=1)),
        vol.Optional(ATTR_PARAMETERS, default={}): dict,
    }
)

SCAN_INTERVAL_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_EMAIL): vol.All(cv.string, vol.Length(min=1)),
        vol.Optional(ATTR_VIN): vol.All(cv.string, vol.Length(min=1)),
        vol.Required(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
            vol.Coerce(int), vol.Range(min=-1, max=3600)
        ),
    }
)


@callback
def async_setup_services(hass) -> None:
    """Set up services for Tesla integration."""

    async def async_call_tesla_service(service_call) -> None:
        """Call correct Tesla service."""
        service = service_call.service
        response = None

        if service == SERVICE_API:
            response = await api(service_call)
        elif service == SERVICE_SCAN_INTERVAL:
            response = await set_update_interval(service_call)

        return response

    hass.services.async_register(
        DOMAIN,
        SERVICE_API,
        async_call_tesla_service,
        schema=API_SCHEMA,
        supports_response=True,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_SCAN_INTERVAL,
        async_call_tesla_service,
        schema=SCAN_INTERVAL_SCHEMA,
        supports_response=True,
    )

    async def api(call):
        """Handle api service request.

        Arguments
            call.CONF_EMAIL {str: ""} -- email, optional
            call.ATTR_COMMAND {str: ""} -- Command
            call.ATTR_PARAMETERS {dict:} -- Parameters dictionary

        Returns
            bool -- True if api called successfully

        """
        _LOGGER.debug("call %s", call)
        service_data = call.data
        email = service_data.get(CONF_EMAIL, "")

        if len(hass.config_entries.async_entries(DOMAIN)) > 1 and not email:
            raise ValueError("Email address missing")
        controller: Controller = None
        for entry in hass.config_entries.async_entries(DOMAIN):
            if (
                len(hass.config_entries.async_entries(DOMAIN)) > 1
                and entry.title != email
            ):
                continue
            entry_data = hass.data[DOMAIN][entry.entry_id]
            controller = entry_data["controller"]
        if controller is None:
            raise ValueError(f"No Tesla controllers found for email {email}")
        command = call.data.get(ATTR_COMMAND)
        parameters: dict = call.data.get(ATTR_PARAMETERS, {})
        _LOGGER.debug(
            "Service api called with email: %s command: %s parameters: %s",
            email,
            command,
            parameters,
        )
        path_vars = parameters.pop(ATTR_PATH_VARS, {})
        response = await controller.api(name=command, path_vars=path_vars, **parameters)
        return response

    async def set_update_interval(call):
        """Handle api service request.

        Arguments
            call.CONF_EMAIL {str: ""} -- email, optional
            call.ATTR_VIN {str: ""} -- vehicle VIN, optional
            call.CONF_SCAN_INTERVAL {int: 660} -- New scan interval

        Returns
            bool -- True if new interval is set

        """
        _LOGGER.debug("call %s", call)
        service_data = call.data
        email = service_data.get(CONF_EMAIL, "")

        if len(hass.config_entries.async_entries(DOMAIN)) > 1 and not email:
            raise ValueError("Email address missing")
        controller: Controller = None
        for entry in hass.config_entries.async_entries(DOMAIN):
            if (
                len(hass.config_entries.async_entries(DOMAIN)) > 1
                and entry.title != email
            ):
                continue
            entry_data = hass.data[DOMAIN][entry.entry_id]
            controller = entry_data["controller"]
        if controller is None:
            raise ValueError(f"No Tesla controllers found for email {email}")

        vin = service_data.get(ATTR_VIN, "")
        update_interval = service_data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        _LOGGER.debug(
            "Service %s called with email: %s vin %s interval %s",
            SERVICE_SCAN_INTERVAL,
            email,
            vin,
            update_interval,
        )
        old_update_interval = controller.get_update_interval_vin(vin=vin)
        if old_update_interval != update_interval:
            _LOGGER.debug(
                "Changing update_interval from %s to %s for %s",
                old_update_interval,
                update_interval,
                vin,
            )
            controller.set_update_interval_vin(vin=vin, value=update_interval)
        return {
            "result": True,
            "message": f"Update interval set to {update_interval} for VIN {vin}",
        }


@callback
def async_unload_services(hass) -> None:
    """Unload Tesla services."""
    hass.services.async_remove(DOMAIN, SERVICE_API)
    hass.services.async_remove(DOMAIN, SERVICE_SCAN_INTERVAL)
