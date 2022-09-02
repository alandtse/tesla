"""Support for Tesla charger switches."""
import logging

from teslajsonpy.car import TeslaCar
from teslajsonpy.energy import PowerwallSite
from teslajsonpy.const import RESOURCE_TYPE_BATTERY

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarDevice, TeslaEnergyDevice
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla selects by config_entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    cars = hass.data[DOMAIN][config_entry.entry_id]["cars"]
    energysites = hass.data[DOMAIN][config_entry.entry_id]["energysites"]
    entities = []

    for car in cars.values():
        if car.steering_wheel_heater:
            entities.append(HeatedSteeringWheel(hass, car, coordinator))
        if car.sentry_mode_available:
            entities.append(SentryMode(hass, car, coordinator))
        entities.append(Polling(hass, car, coordinator))
        entities.append(Charger(hass, car, coordinator))

    for energysite in energysites.values():
        if energysite.resource_type == RESOURCE_TYPE_BATTERY:
            entities.append(TeslaEnergyGridCharging(hass, energysite, coordinator))

    async_add_entities(entities, True)


class HeatedSteeringWheel(TeslaCarDevice, SwitchEntity):
    """Representation of the Tesla Battery Sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "heated steering"
        self._attr_icon = "mdi:steering"

    @property
    def is_on(self):
        """Return Heated Steering Wheel state."""
        return self._car.is_steering_wheel_heater_on

    async def async_turn_on(self, **kwargs):
        """Send the on command."""
        await self._car.set_heated_steering_wheel(True)

    async def async_turn_off(self, **kwargs):
        """Send the off command."""
        await self._car.set_heated_steering_wheel(False)


class Polling(TeslaCarDevice, SwitchEntity):
    """Representation of the Polling Switch."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "polling"
        self._attr_icon = "mdi:car-connected"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def is_on(self):
        """Return Heated Steering Wheel state."""
        if self._coordinator.controller.get_updates(vin=self._car.vin) is None:
            return None

        return bool(self._coordinator.controller.get_updates(vin=self._car.vin))

    async def async_turn_on(self, **kwargs):
        """Send the on command."""
        _LOGGER.debug("Enable polling: %s %s", self.name, self._car.vin)
        self._coordinator.controller.set_updates(vin=self._car.vin, value=True)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Send the off command."""
        _LOGGER.debug("Disable polling: %s %s", self.name, self._car.vin)
        self._coordinator.controller.set_updates(vin=self._car.vin, value=False)
        self.async_write_ha_state()


class Charger(TeslaCarDevice, SwitchEntity):
    """Representation of the Tesla Battery Sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Representation of a Tesla charger switch."""
        super().__init__(hass, car, coordinator)
        self.type = "charger"
        self._attr_icon = "mdi:battery-charging"

    @property
    def is_on(self):
        """Return charging state."""
        return self._car.charging_state == "Charging"

    async def async_turn_on(self, **kwargs):
        """Send the on command."""
        await self._car.start_charge()

    async def async_turn_off(self, **kwargs):
        """Send the off command."""
        await self._car.stop_charge()

        # Do a non-blocking update to get the latest Charging state.
        self.update_controller(wake_if_asleep=True, force=True, blocking=False)


class SentryMode(TeslaCarDevice, SwitchEntity):
    """Representation of the Tesla Battery Sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Representation of a Tesla Sentry Mode switch."""
        super().__init__(hass, car, coordinator)
        self.type = "sentry mode"
        self._attr_icon = "mdi:shield-car"

    @property
    def is_on(self):
        """Return Sentry Mode state."""
        sentry_mode_available = self._car.sentry_mode_available
        sentry_mode_status = self._car.sentry_mode

        if sentry_mode_available is True and sentry_mode_status is True:
            return True

        return False

    async def async_turn_on(self, **kwargs):
        """Send the on command."""
        await self._car.set_sentry_mode(True)

    async def async_turn_off(self, **kwargs):
        """Send the off command."""
        await self._car.set_sentry_mode(False)


class TeslaEnergyGridCharging(TeslaEnergyDevice, SwitchEntity):
    """Representation of a Tesla energy grid charging switch."""

    def __init__(
        self,
        hass: HomeAssistant,
        energysite: PowerwallSite,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize a Tesla energy grid charging switch."""
        super().__init__(hass, energysite, coordinator)
        self.type = "grid charging"

    @property
    def is_on(self):
        """Return grid charging enabled."""
        return self._energysite.grid_charging

    async def async_turn_on(self, **kwargs):
        """Send the on command."""
        await self._energysite.set_grid_charging(True)

    async def async_turn_off(self, **kwargs):
        """Send the off command."""
        await self._energysite.set_grid_charging(False)
