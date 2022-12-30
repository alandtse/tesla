"""Support for Tesla cars and energy sites."""
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify
from homeassistant.util.unit_system import METRIC_SYSTEM, US_CUSTOMARY_SYSTEM
from teslajsonpy.car import TeslaCar
from teslajsonpy.const import RESOURCE_TYPE_BATTERY
from teslajsonpy.energy import EnergySite

from . import TeslaDataUpdateCoordinator
from .const import ATTRIBUTION, DOMAIN


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
        self._enabled_by_default: bool = True
        self.hass = hass
        self.type = None

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

    async def async_added_to_hass(self) -> None:
        """Register state update callback."""
        self.async_on_remove(self.coordinator.async_add_listener(self.refresh))


class TeslaCarEntity(TeslaBaseEntity):
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
        self._unit_system = (
            METRIC_SYSTEM
            if self.hass.config.units is METRIC_SYSTEM
            else US_CUSTOMARY_SYSTEM
        )

    async def update_controller(
        self, *, wake_if_asleep: bool = False, force: bool = True, blocking: bool = True
    ) -> None:
        """Get the latest data from Tesla.

        This does a controller update then a coordinator update.
        The coordinator triggers a call to the refresh function.

        Setting the blocking param to False will create a background task for the update.
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
        """Return unique id for car entity."""
        return slugify(f"{self._car.vin} {self.type}")

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
        """Return whether the data is from an online vehicle."""
        return not self._coordinator.controller.is_car_online(vin=self._car.vin) and (
            self._coordinator.controller.get_last_update_time(vin=self._car.vin)
            - self._coordinator.controller.get_last_wake_up_time(vin=self._car.vin)
            > self._coordinator.controller.update_interval
        )


class TeslaEnergyEntity(TeslaBaseEntity):
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
    def sw_version(self) -> bool:
        """Return firmware version."""
        if self._energysite.resource_type == RESOURCE_TYPE_BATTERY:
            return self._energysite.version
        # Non-Powerwall sites do not provide version info
        return "Unavailable"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        model = f"{self._energysite.resource_type.title()}"
        return DeviceInfo(
            identifiers={(DOMAIN, self._energysite.energysite_id)},
            manufacturer="Tesla",
            model=model,
            name=self._energysite.site_name,
            sw_version=self.sw_version,
        )
