"""Support for Tesla cars."""
from functools import wraps
import logging
from typing import Any, Dict, Optional

from homeassistant.const import ATTR_BATTERY_CHARGING, ATTR_BATTERY_LEVEL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_registry import async_get_registry
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify
from teslajsonpy.exceptions import IncompleteCredentials

from .const import DOMAIN, ICONS
from . import TeslaDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

DEFAULT_DEVICE = "device"


class TeslaBaseEntity(CoordinatorEntity):
    """Representation of a Tesla device."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ):
        """Initialise the Tesla device."""
        super().__init__(coordinator)
        self._coordinator = coordinator
        self.hass = hass

        self.car = TeslaCar(car, coordinator)

        # reset the device type. If its not already set, it sets it to the
        # default device.
        self.type: str = getattr(self, "type", DEFAULT_DEVICE)

        self.attrs: Dict[str, str] = {}
        self._enabled_by_default: bool = True
        self.config_entry_id = None

        self._name = None
        self._unique_id = None
        self._attributes = {}

    @property
    def name(self) -> str:
        if self._name is None:
            self._name = (
                f"{self.car.display_name} {self.type}"
                if self.car.display_name is not None
                and self.car.display_name != self.car.vin[-6:]
                else f"Tesla Model {str(self.car.vin[3]).upper()} {self.type}"
            )

        return self._name

    @property
    def unique_id(self) -> str:
        if self._unique_id is None:
            self._unique_id = slugify(
                f"Tesla Model {str(self.car.vin[3]).upper()} {self.car.vin[-6:]} {self.type}"
            )

        return self._unique_id

    async def update_controller(
        self, *, wake_if_asleep: bool = False, force: bool = True, blocking: bool = True
    ):
        """Get the latest data from Tesla.

        This does a controller update,
        then a coordinator update.
        This also triggers a async_write_ha_state

        Setting the Blocking param to False will create a background task for the update.
        """

        if blocking is False:
            await self.hass.async_create_task(
                self.update_controller(wake_if_asleep=wake_if_asleep, force=force)
            )
            return

        await self._coordinator.controller.update(
            self.car.id, wake_if_asleep=wake_if_asleep, force=force
        )
        await self._coordinator.async_refresh()
        self.refresh()

    def refresh(self) -> None:
        """Refresh the vehicle data.
        This assumes the controller has already been updated. This should be
        called by inherited classes so the overall vehicle information is updated.
        """
        self.car.refresh()
        self.async_write_ha_state()

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return None

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        attr = self._attributes
        ### This can probably be removed. it was a stub from this
        # if self.car.charging != {}:
        #     attr[ATTR_BATTERY_LEVEL] = self.car.charging.get("battery_level")
        #     attr[ATTR_BATTERY_CHARGING] = (
        #         self.car.charging.get("charging_state") == "Charging"
        #     )
        return attr

    @property
    def entity_registry_enabled_default(self):
        return self._enabled_by_default

    @property
    def device_info(self):
        """Return the device_info of the device."""
        return {
            "identifiers": {(DOMAIN, self.car.id)},
            "name": self.car.name,
            "manufacturer": "Tesla",
            "model": self.car.type,
            "sw_version": self.car.version,
        }

    @property
    def assumed_state(self) -> bool:
        # pylint: disable=protected-access
        """Return whether the data is from an online vehicle."""
        return not self._coordinator.controller.car_online[self.car.vin] and (
            self._coordinator.controller._last_update_time[self.car.vin]
            - self._coordinator.controller._last_wake_up_time[self.car.vin]
            > self._coordinator.controller.update_interval
        )

    @property
    def attribution(self) -> bool:
        """Return Data Attribution."""
        return "Data provided by Tesla"

    async def async_added_to_hass(self):
        """Register state update callback."""
        self.async_on_remove(self.coordinator.async_add_listener(self.refresh))
        registry = await async_get_registry(self.hass)
        # self.config_entry_id = registry.entities.get(self.entity_id).config_entry_id

    async def _send_command(
        self, name: str, *, path_vars: dict, wake_if_asleep: bool = False, **kwargs
    ):
        """Wrapper for Sending Commands to the Tesla API.

        Just cleans up command functions throughout the codebase.
        """
        data = await self._coordinator.controller.api(
            name, path_vars=path_vars, wake_if_asleep=wake_if_asleep, **kwargs
        )

        return data


class TeslaCar:
    """Data Holder for all Car Data.

    Exists simply so we don't have a bunch of attributes on the top level Entity.
    """

    def __init__(self, car: dict, coordinator: TeslaDataUpdateCoordinator):
        self.coordinator: TeslaDataUpdateCoordinator = coordinator
        self.raw: dict = car

        self.state = {}
        self.config = {}
        self.climate = {}
        self.charging = {}

    def set_car_data(self, new_data: dict) -> None:
        """Update Car Data."""
        self.raw = new_data

    def refresh(self):
        """Refresh Car Data from the controller."""
        self.state = self.coordinator.controller.get_state_params(vin=self.vin)
        self.config = self.coordinator.controller.get_config_params(vin=self.vin)
        self.climate = self.coordinator.controller.get_climate_params(vin=self.vin)
        self.charging = self.coordinator.controller.get_charging_params(vin=self.vin)

    @property
    def sentry_mode_available(self) -> bool:
        """Return True if sentry mode is available on this Vehicle."""
        return (
            "vehicle_state" in self.raw
            and "sentry_mode_available" in self.raw["vehicle_state"]
            and self.raw["vehicle_state"]["sentry_mode_available"]
        )

    @property
    def type(self) -> str:
        """Return the car_type of this Vehicle."""
        return f"Model {str(self.vin[3]).upper()}"

    @property
    def display_name(self) -> str:
        """Return the display_name of this Vehicle."""
        return self.raw.get("display_name")

    @property
    def vehicle_id(self) -> str:
        """Return the vehicle_id of this Vehicle."""
        return self.raw.get("vehicle_id")

    @property
    def id(self) -> str:
        """Return the id of this Vehicle."""
        return self.raw.get("id")

    @property
    def vin(self) -> str:
        """Return the vin of this Vehicle."""
        return self.raw.get("vin")

    @property
    def name(self) -> str:
        """Return the car name of this Vehicle."""
        return (
            self.display_name
            if self.display_name is not None and self.display_name != self.vin[-6:]
            else f"Tesla Model {str(self.vin[3]).upper()}"
        )

    @property
    def version(self) -> str:
        """Return the Software Version of this Vehicle."""
        return self.state.get("car_version")
