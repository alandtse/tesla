"""Support for Tesla door locks."""
import logging
from typing import Any

from homeassistant.components.update import UpdateEntity, UpdateEntityFeature
from homeassistant.core import HomeAssistant

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarDevice
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla binary_sensors by config_entry."""
    entities = [
        TeslaUpdate(
            hass,
            car,
            hass.data[DOMAIN][config_entry.entry_id]["coordinator"],
        )
        for car in hass.data[DOMAIN][config_entry.entry_id]["cars"]
    ]
    async_add_entities(entities, True)


class TeslaUpdate(TeslaCarDevice, UpdateEntity):
    """Tesla Update Entity."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Update Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "software update"

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return UpdateEntityFeature.INSTALL | UpdateEntityFeature.PROGRESS

    @property
    def release_url(self) -> str:
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
    def latest_version(self) -> str:
        """Get the latest Version."""
        version_str: str = self.car.state.get("software_update", {}).get("version")

        # If we don't have a software_update version, then we're running the latest version.
        if version_str is None or version_str.strip() == "":
            version_str = self.installed_version

        return version_str

    @property
    def installed_version(self) -> str:
        """Get the Installed Version."""
        version_str = self.car.state.get("car_version")

        # We will split out the version Hash, purely cause it looks nicer in the UI.
        if version_str is not None:
            version_str = version_str.split(" ")[0]

        return version_str

    @property
    def in_progress(self):
        """Get Progress, if updating."""
        update_status = self.car.state.get("software_update", {}).get("status")

        # If the update is scheduled, then its Simply In Progress
        if update_status == "scheduled":
            return True

        # If its actually installing, we can use the install_perc
        if update_status == "installing":
            progress = self.car.state.get("software_update", {}).get("install_perc")
            return progress

        # Otherwise, we're not updating, so return False
        return False

    async def async_install(self, version, backup: bool, **kwargs: Any) -> None:
        """Install an Update."""

        # Ask Tesla to start the update now.
        await self._coordinator.controller.api(
            "SCHEDULE_SOFTWARE_UPDATE",
            path_vars={"vehicle_id": self.car.id},
            offset_sec=0,
            wake_if_asleep=True,
        )

        # Do a controller refresh, to get the latest data from Tesla.
        await self.update_controller(force=True)
