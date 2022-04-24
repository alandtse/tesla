"""Helpers module.

A collection of functions which may be used accross entities
"""
from .const import DOMAIN as TESLA_DOMAIN

import asyncio
import async_timeout
import logging

from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


async def get_device(
    hass: HomeAssistant,
    config_entry_id: str,
    device_category: str,
    device_type: str,
):
    """Get a tesla Device for a Config Entry ID."""

    entry_data = hass.data[TESLA_DOMAIN][config_entry_id]
    devices = entry_data["devices"].get(device_category, [])

    for device in devices:
        if device.type == device_type:
            return device

    return None


async def wait_for_climate(
    hass: HomeAssistant, config_entry_id: str, timeout: int = 30
):
    """Wait for HVac.

    Optional Timeout. defaults to 30 seconds
    """
    climate_device = await get_device(
        hass, config_entry_id, "climate", "HVAC (climate) system"
    )

    if climate_device is None:
        return None

    async with async_timeout.timeout(timeout):
        while True:
            hvac_mode = climate_device.is_hvac_enabled()

            if hvac_mode is True:
                _LOGGER.debug("HVAC Enabled")
                return True
            else:
                _LOGGER.info("Enabing Climate to activate Heated Steering Wheel")

                # The below is a blocking funtion (it waits for a reponse from the API).
                # So it could eat into our timeout, and this is fine.
                # We'll try to turn the set the status, and check again
                try:
                    await climate_device.set_status(True)
                    continue
                except:
                    # If we get an error, we'll just loop around and try again
                    pass

            # Wait two second between API calls, in case we get an error like car unavail,
            # or any other random thing tesla throws at us
            await asyncio.sleep(2)

    # we'll return false if the timeout is reached.
    return False
