"""Support for Tesla door locks."""
import logging
from typing import Any

from homeassistant.components.update import UpdateEntity, UpdateEntityFeature

from .const import DOMAIN
from .base import TeslaBaseEntity
from . import TeslaDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Tesla binary_sensors by config_entry."""
    entities = [
        TeslaUpdate(
            car,
            hass.data[DOMAIN][config_entry.entry_id]["coordinator"],
        )
        for car in hass.data[DOMAIN][config_entry.entry_id]["cars"]
    ]
    async_add_entities(entities, True)


class TeslaUpdate(TeslaBaseEntity, UpdateEntity):
    """Tesla Update Entity."""

    def __init__(self, car: Any, coordinator: TeslaDataUpdateCoordinator):
        """Initialize the Update Entity."""
        super().__init__(car, coordinator)
        self.type = "Software Update"

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return UpdateEntityFeature.INSTALL | UpdateEntityFeature.PROGRESS

    @property
    def release_url(self):
        """Return Release URL.

        Uses notateslaapp.com as Tesla doesn't have offical web based release Notes.
        """
        version_str = self.latest_version
        if version_str is None:
            version_str = self.installed_version

        if version_str is None:
            return None

        return f"https://www.notateslaapp.com/software-updates/version/{version_str}/release-notes"

    @property
    def latest_version(self):
        version_str = self.car.state.get("software_update", {}).get("version")

        return version_str

    @property
    def installed_version(self):
        version_str = self.car.state.get("car_version")

        if version_str is not None:
            version_str = version_str.split(" ")[0]

        return version_str

    @property
    def in_progress(self):
        update_status = self.car.state.get("software_update", {}).get("status")

        if update_status == "available":
            return None

        progress = self.car.state.get("software_update", {}).get("install_perc")

        return progress
