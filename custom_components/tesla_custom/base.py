"""Support for Tesla cars."""
import logging
from xxlimited import Str

from teslajsonpy.const import TESLA_DEFAULT_ENERGY_SITE_NAME

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from . import TeslaDataUpdateCoordinator
from .const import ATTRIBUTION, DOMAIN

_LOGGER = logging.getLogger(__name__)

DEFAULT_DEVICE = "device"


class TeslaBaseEntity(CoordinatorEntity):
    """Representation of a Tesla device."""

    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True

    def __init__(
        self, hass: HomeAssistant, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialise the Tesla device."""
        super().__init__(coordinator)
        self._coordinator = coordinator
        self.hass = hass
        # reset the device type. If its not already set, it sets it to the
        # default device.
        self.type: str = getattr(self, "type", DEFAULT_DEVICE)

        self.attrs: dict[str, str] = {}
        self._enabled_by_default: bool = True
        self.config_entry_id = None
        self._unique_id = None
        self._attributes = {}

    def refresh(self) -> None:
        """Refresh the device data.

        This is called by the DataUpdateCoodinator when new data is available.

        This assumes the controller has already been updated. This should be
        called by inherited classes so the overall device information is updated.
        """

        self.async_write_ha_state()

    @property
    def name(self) -> str:
        """Return name of entity."""
        # TeslaEnergyPowerSensors self.type contains an underscore
        # since we use it
        return self.type.replace("_", " ").capitalize()

    @property
    def entity_registry_enabled_default(self):
        """Set entity registry to default."""
        return self._enabled_by_default

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        attr = self._attributes
        return attr

    async def async_added_to_hass(self):
        """Register state update callback."""

        self.async_on_remove(self.coordinator.async_add_listener(self.refresh))

    async def _send_command(
        self, name: str, *, path_vars: dict, wake_if_asleep: bool = False, **kwargs
    ):
        """Wrapper for Sending Commands to the Tesla API.

        Just cleans up command functions throughout the codebase.
        """
        _LOGGER.debug("Sending Command: %s", name)
        data = await self._coordinator.controller.api(
            name, path_vars=path_vars, wake_if_asleep=wake_if_asleep, **kwargs
        )

        return data


class TeslaCarDevice(TeslaBaseEntity):
    """Representation of a Tesla car device."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialise the Tesla car device."""
        super().__init__(hass, coordinator)
        self.car = TeslaCar(car, coordinator)

    async def update_controller(
        self, *, wake_if_asleep: bool = False, force: bool = True, blocking: bool = True
    ):
        """Get the latest data from Tesla.

        This does a controller update,
        then a coordinator update.
        the coordinator triggers a call to the refresh function.

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

    @property
    def available(self) -> str:
        """Return the Availability of Data."""
        return self.car.state != {}

    @property
    def unique_id(self) -> str:
        """Return entity unique id."""
        if self._unique_id is None:
            self._unique_id = slugify(
                f"Tesla Model {str(self.car.vin[3]).upper()} {self.car.vin[-6:]} {self.type}"
            )

        return self._unique_id

    @property
    def device_info(self):
        """Return the device_info of the device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.car.id)},
            name=self.car.name,
            manufacturer="Tesla",
            model=self.car.type,
            sw_version=self.car.version,
        )

    @property
    def assumed_state(self) -> bool:
        # pylint: disable=protected-access
        """Return whether the data is from an online vehicle."""
        return not self._coordinator.controller.is_car_online(vin=self.car.vin) and (
            self._coordinator.controller.get_last_update_time(vin=self.car.vin)
            - self._coordinator.controller.get_last_wake_up_time(vin=self.car.vin)
            > self._coordinator.controller.update_interval
        )


class TeslaCar:
    """Data Holder for all Car Data.

    Exists simply so we don't have a bunch of attributes on the top level Entity.
    """

    def __init__(self, car: dict, coordinator: TeslaDataUpdateCoordinator) -> None:
        """Initialize TeslaCard Data Holder."""
        self.coordinator: TeslaDataUpdateCoordinator = coordinator
        self.raw: dict = car

    def set_car_data(self, new_data: dict) -> None:
        """Update Car Data."""
        self.raw = new_data

    @property
    def state(self) -> dict:
        """Return State Data."""
        return self.coordinator.controller.get_state_params(vin=self.vin)

    @property
    def config(self) -> dict:
        """Return State Data."""
        return self.coordinator.controller.get_config_params(vin=self.vin)

    @property
    def charging(self) -> dict:
        """Return State Data."""
        return self.coordinator.controller.get_charging_params(vin=self.vin)

    @property
    def climate(self) -> dict:
        """Return State Data."""
        return self.coordinator.controller.get_climate_params(vin=self.vin)

    @property
    def gui(self) -> dict:
        """Return State Data."""
        return self.coordinator.controller.get_gui_params(vin=self.vin)

    @property
    def drive(self) -> dict:
        """Return State Data."""
        return self.coordinator.controller.get_drive_params(vin=self.vin)

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


class TeslaEnergyDevice(TeslaBaseEntity):
    """Representation of a Tesla energy device."""

    def __init__(
        self,
        hass: HomeAssistant,
        energysite: list,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialise the Tesla energy device."""
        super().__init__(hass, coordinator)
        self.energysite = energysite

    @property
    def unique_id(self) -> str:
        """Return a unique ID for energy site device."""
        return f"{self.energysite_id}-{self.type}"

    @property
    def available(self) -> str:
        """Return the Availability of Data."""
        return self.energysite != []

    @property
    def energysite_id(self) -> str:
        """Return the id of this energy site."""
        return self.energysite["energy_site_id"]

    @property
    def site_name(self) -> str:
        """Return the energy site name."""
        return self.energysite.get("site_name", TESLA_DEFAULT_ENERGY_SITE_NAME)

    @property
    def site_type(self) -> str:
        """Return the type of energy site."""
        _resource_type = self.energysite["resource_type"].title()
        _solar_type = self.energysite["components"]["solar_type"].replace("_", " ")

        return f"{_resource_type} {_solar_type}"

    @property
    def device_info(self):
        """Return the device_info of the device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.energysite_id)},
            manufacturer="Tesla",
            model=self.site_type,
            name=self.site_name,
        )

    @property
    def power_data(self):
        """Return the coordinator controller power data."""
        return self.coordinator.controller.get_power_params(self.energysite_id)
