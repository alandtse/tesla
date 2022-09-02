"""Support for Tesla cars."""
from teslajsonpy.car import TeslaCar
from teslajsonpy.energy import EnergySite

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from . import TeslaDataUpdateCoordinator
from .const import ATTRIBUTION, DOMAIN

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
        """Return device name."""
        return self.type.capitalize()

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Set entity registry to default."""
        return self._enabled_by_default

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return device state attributes."""
        attr = self._attributes
        return attr

    async def async_added_to_hass(self) -> None:
        """Register state update callback."""

        self.async_on_remove(self.coordinator.async_add_listener(self.refresh))


class TeslaCarDevice(TeslaBaseEntity):
    """Representation of a Tesla car device."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialise the Tesla car device."""
        super().__init__(hass, coordinator)
        self._car = car

    async def update_controller(
        self, *, wake_if_asleep: bool = False, force: bool = True, blocking: bool = True
    ) -> None:
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
            self._car.id, wake_if_asleep=wake_if_asleep, force=force
        )
        await self._coordinator.async_refresh()

    @property
    def available(self) -> bool:
        """Return availability of data."""
        return self._car.data_available != {}

    @property
    def vehicle_name(self) -> str:
        """Return vehicle name."""
        return (
            self._car.display_name
            if self._car.display_name is not None
            and self._car.display_name != self._car.vin[-6:]
            else f"Tesla Model {str(self._car.vin[3]).upper()}"
        )

    @property
    def unique_id(self) -> str:
        """Return unique id for car device."""
        return slugify(
            f"Tesla Model {str(self._car.vin[3]).upper()} {self._car.vin[-6:]} {self.type}"
        )

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._car.id)},
            name=self.vehicle_name,
            manufacturer="Tesla",
            model=self._car.car_type,
            sw_version=self._car.car_version,
        )

    @property
    def assumed_state(self) -> bool:
        # pylint: disable=protected-access
        """Return whether the data is from an online vehicle."""
        return not self._coordinator.controller.is_car_online(vin=self._car.vin) and (
            self._coordinator.controller.get_last_update_time(vin=self._car.vin)
            - self._coordinator.controller.get_last_wake_up_time(vin=self._car.vin)
            > self._coordinator.controller.update_interval
        )


class TeslaEnergyDevice(TeslaBaseEntity):
    """Representation of a Tesla energy device."""

    def __init__(
        self,
        hass: HomeAssistant,
        energysite: EnergySite,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialise the Tesla energy device."""
        super().__init__(hass, coordinator)
        self._energysite = energysite

    @property
    def unique_id(self) -> str:
        """Return unique id for energy site device."""
        return slugify(f"{self._energysite.energysite_id} {self.type}")

    @property
    def available(self) -> bool:
        """Return availability of data."""
        return self._energysite != {}

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        model = f"{self._energysite.resource_type.title()} {self._energysite.solar_type.replace('_', ' ')}"
        return DeviceInfo(
            identifiers={(DOMAIN, self._energysite.energysite_id)},
            manufacturer="Tesla",
            model=model,
            name=self._energysite.site_name,
        )
