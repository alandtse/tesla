"""Helpers module.

A collection of functions which may be used accross entities
"""
import logging
import asyncio
import async_timeout

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_registry import async_get, RegistryEntryDisabler

from .const import DOMAIN as TESLA_DOMAIN

_LOGGER = logging.getLogger(__name__)


async def get_device(
    hass: HomeAssistant,
    config_entry_id: str,
    device_category: str,
    device_type: str,
    vin: str,
):
    """Get a tesla Device for a Config Entry ID."""

    entry_data = hass.data[TESLA_DOMAIN][config_entry_id]
    devices = entry_data["devices"].get(device_category, [])

    for device in devices:
        if device.type == device_type and device.vin() == vin:
            return device

    return None


def enable_entity(
    hass: HomeAssistant,
    domain: str,
    platform: str,
    unique_id: str,
):
    """Enable provided entity if disabled by integration."""

    # Get Entity Registry
    entity_registry = async_get(hass)

    entity_id = entity_registry.async_get_entity_id(domain, platform, unique_id)
    if entity_id is None:
        _LOGGER.debug(
            "Entity for domain %s, platform %s with unique id %s "
            "was never registered.",
            domain,
            platform,
            unique_id,
        )
        return

    # Now get the entity itself.
    entity = entity_registry.entities[entity_id]

    if entity.disabled_by == RegistryEntryDisabler.INTEGRATION:
        # Entity was disabled by us, now we can enable it.
        _LOGGER.debug("Enabling entity %s", entity)
        entity_registry.async_update_entity(entity.entity_id, disabled_by=None)
    elif entity.disabled_by is None:
        _LOGGER.debug("Entity %s already enabled", entity_id)
    else:
        _LOGGER.debug("Entity %s was disabled by %s", entity_id, entity.disabled_by)


async def wait_for_climate(
    hass: HomeAssistant, config_entry_id: str, vin: str, timeout: int = 30
):
    """Wait for HVac.

    Optional Timeout. defaults to 30 seconds
    """
    climate_device = await get_device(
        hass, config_entry_id, "climate", "HVAC (climate) system", vin
    )

    if climate_device is None:
        return None

    async with async_timeout.timeout(timeout):
        while True:
            hvac_mode = climate_device.is_hvac_enabled()

            if hvac_mode is True:
                _LOGGER.debug("HVAC Enabled")
                return True

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

            # Wait two second between API calls, in case we get an error like
            # car unavailable,or any other random thing tesla throws at us
            await asyncio.sleep(2)

    # we'll return false if the timeout is reached.
    return False
