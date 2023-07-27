"""Support for Tesla cars and energy sites."""

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify
from teslajsonpy.car import TeslaCar
from teslajsonpy.const import RESOURCE_TYPE_BATTERY
from teslajsonpy.energy import EnergySite

from . import TeslaDataUpdateCoordinator
from .const import ATTRIBUTION, DOMAIN


class TeslaBaseEntity(CoordinatorEntity[TeslaDataUpdateCoordinator]):
    """Representation of a Tesla device."""

    type: str
    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True
    _enabled_by_default: bool = True
    _memorized_unique_id: str | None = None

    def __init__(
        self, base_unique_id: str, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialise the Tesla device."""
        super().__init__(coordinator)
        self._attr_unique_id = slugify(f"{base_unique_id} {self.type}")
        self._attr_name = self.type.capitalize()
        self._attr_entity_registry_enabled_default = self._enabled_by_default

    async def async_added_to_hass(self) -> None:
        """Register state update callback."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )


class TeslaCarEntity(TeslaBaseEntity):
    """Representation of a Tesla car device."""

    def __init__(
        self,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialise the Tesla car device."""
        vin = car.vin
        super().__init__(vin, coordinator)
        self._car = car
        display_name = car.display_name
        vehicle_name = (
            display_name
            if display_name is not None and display_name != vin[-6:]
            else f"Tesla Model {str(vin[3]).upper()}"
        )
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, car.id)},
            name=vehicle_name,
            manufacturer="Tesla",
            model=car.car_type,
            sw_version=car.car_version,
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

        await self.coordinator.controller.update(
            self._car.id, wake_if_asleep=wake_if_asleep, force=force
        )
        await self.coordinator.async_refresh()

    @property
    def assumed_state(self) -> bool:
        """Return whether the data is from an online vehicle."""
        vin = self._car.vin
        controller = self.coordinator.controller
        return not controller.is_car_online(vin=vin) and (
            controller.get_last_update_time(vin=vin)
            - controller.get_last_wake_up_time(vin=vin)
            > controller.update_interval
        )


class TeslaEnergyEntity(TeslaBaseEntity):
    """Representation of a Tesla energy device."""

    def __init__(
        self,
        energysite: EnergySite,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialise the Tesla energy device."""
        energysite_id = energysite.energysite_id
        super().__init__(energysite_id, coordinator)
        self._energysite = energysite
        if energysite.resource_type == RESOURCE_TYPE_BATTERY:
            sw_version = energysite.version
        else:
            # Non-Powerwall sites do not provide version info
            sw_version = "Unavailable"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, energysite_id)},
            manufacturer="Tesla",
            model=energysite.resource_type.title(),
            name=energysite.site_name,
            sw_version=sw_version,
        )
