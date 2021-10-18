"""Support for Tesla services.

SPDX-License-Identifier: Apache-2.0
"""

import logging
from homeassistant.const import CONF_EMAIL

from teslajsonpy import Controller
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv
import voluptuous as vol

from homeassistant.const import ATTR_COMMAND
from .const import (
    ATTR_PARAMETERS,
    ATTR_PATH_VARS,
    DOMAIN,
    SERVICE_API,
)

_LOGGER = logging.getLogger(__name__)


API_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_EMAIL): vol.All(cv.string, vol.Length(min=1)),
        vol.Required(ATTR_COMMAND, default=""): vol.All(cv.string, vol.Length(min=1)),
        vol.Optional(ATTR_PARAMETERS, default={}): dict,
    }
)


@callback
def async_setup_services(hass) -> None:
    """Set up services for Tesla integration."""

    async def async_call_tesla_service(service_call) -> None:
        """Call correct Tesla service."""
        service = service_call.service

        if service == SERVICE_API:
            await api(service_call)

    hass.services.async_register(
        DOMAIN,
        SERVICE_API,
        async_call_tesla_service,
        schema=API_SCHEMA,
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
            controller = hass.data[DOMAIN].get(entry.entry_id)["coordinator"].controller
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
        path_vars = parameters.pop(ATTR_PATH_VARS)
        return await controller.api(name=command, path_vars=path_vars, **parameters)


@callback
def async_unload_services(hass) -> None:
    """Unload Tesla services."""
    hass.services.async_remove(DOMAIN, SERVICE_API)
