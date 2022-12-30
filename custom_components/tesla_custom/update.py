"""Support for Tesla update."""
from typing import Any

from homeassistant.components.update import UpdateEntity, UpdateEntityFeature
from homeassistant.core import HomeAssistant
from teslajsonpy.car import TeslaCar

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarEntity
from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla update entities by config_entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    cars = hass.data[DOMAIN][config_entry.entry_id]["cars"]

    entities = [
        TeslaCarUpdate(
            hass,
            car,
            coordinator,
        )
        for car in cars.values()
    ]
    async_add_entities(entities, True)


INSTALLABLE_STATUSES = ["available", "scheduled"]

PRETTY_STATUS_STRINGS = {
    "downloading_wifi_wait": "Waiting on Wi-Fi",
    "downloading": "Downloading",
    "available": "Available to install",
    "scheduled": "Scheduled for install",
    "installing": "Installing",
}


class TeslaCarUpdate(TeslaCarEntity, UpdateEntity):
    """Representation of a Tesla car update."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize update entity."""
        super().__init__(hass, car, coordinator)
        self.type = "software update"

    @property
    def supported_features(self):
        """Return the list of supported features."""
        # Don't enable Install button until the update has downloaded
        if (
            self._car.software_update
            and self._car.software_update.get("status") in INSTALLABLE_STATUSES
        ):
            return UpdateEntityFeature.INSTALL | UpdateEntityFeature.PROGRESS
        return UpdateEntityFeature.PROGRESS

    @property
    def release_url(self) -> str:
        """Return release URL.

        Uses notateslaapp.com as Tesla doesn't have offical web based release Notes.
        """
        version_str = ""

        if self._car.software_update:
            # latest_version may include a status tag, so get the original version
            version_str: str = self._car.software_update.get("version", "").strip()
        if not version_str:
            version_str = self.installed_version

        if not version_str:
            return None

        return f"https://www.notateslaapp.com/software-updates/version/{version_str}/release-notes"

    @property
    def latest_version(self) -> str:
        """Get the latest version."""
        version_str = ""
        status_str = ""

        if self._car.software_update:
            version_str: str = self._car.software_update.get("version", "").strip()
            status_str: str = self._car.software_update.get("status", "").strip()
        # If we don't have a software_update version, then we're running the latest version.
        if not version_str:
            return self.installed_version

        # Append the status so users can tell if it's downloading or scheduled, etc
        if status_str:
            version_str += f" ({PRETTY_STATUS_STRINGS.get(status_str, status_str)})"
        return version_str

    @property
    def installed_version(self) -> str:
        """Get the installed version."""
        version_str = self._car.car_version
        # We will split out the version Hash, purely cause it looks nicer in the UI.
        if version_str is not None:
            version_str = version_str.split(" ")[0]

        return version_str

    @property
    def in_progress(self):
        """Get Progress, if updating."""
        update_status = None

        if self._car.software_update:
            update_status = self._car.software_update.get("status")
        # If the update is scheduled, don't consider in-progress so the
        # user can still install immediately if desired
        if update_status == "scheduled":
            return False
        # If its actually installing, we can use the install_perc
        if update_status == "installing":
            progress = self._car.software_update.get("install_perc")
            return progress
        # Otherwise, we're not updating, so return False
        return False

    async def async_install(self, version, backup: bool, **kwargs: Any) -> None:
        """Install an Update."""
        # Ask Tesla to start the update now.
        await self._car.schedule_software_update(offset_sec=0)
        # Do a controller refresh, to get the latest data from Tesla.
        await self.update_controller(force=True)
