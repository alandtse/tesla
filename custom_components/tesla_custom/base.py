"""Support for Tesla cars and energy sites."""

from homeassistant.core import callback
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
            if display_name is not None
            and display_name != vin[-6:]
            and display_name != ""
            else f"Tesla Model {str(vin[3]).upper()}"
        )
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, car.id)},
            name=vehicle_name,
            manufacturer="Tesla",
            model=car.car_type,
            sw_version=car.car_version,
        )
        self._last_update_success: bool | None = None
        self.last_update_time: float | None = None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        prev_last_update_success = self._last_update_success
        prev_last_update_time = self.last_update_time
        coordinator = self.coordinator
        current_last_update_success = coordinator.last_update_success
        current_last_update_time = coordinator.last_update_time
        self._last_update_success = current_last_update_success
        self.last_update_time = current_last_update_time
        if (
            prev_last_update_success == current_last_update_success
            and prev_last_update_time == current_last_update_time
        ):
            # If there was no change in the last update success or time,
            # avoid writing state to prevent unnecessary entity updates.
            return
        super()._handle_coordinator_update()

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
        return self.coordinator.assumed_state


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
