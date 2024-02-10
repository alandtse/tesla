"""Support for Tesla switches."""

import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from teslajsonpy.car import TeslaCar

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla switches by config_entry."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinators = entry_data["coordinators"]
    cars = entry_data["cars"]
    entities = []

    for vin, car in cars.items():
        coordinator = coordinators[vin]
        entities.append(TeslaCarHeatedSteeringWheel(car, coordinator))
        entities.append(TeslaCarSentryMode(car, coordinator))
        entities.append(TeslaCarPolling(car, coordinator))
        entities.append(TeslaCarCharger(car, coordinator))
        entities.append(TeslaCarValetMode(car, coordinator))

    async_add_entities(entities, update_before_add=True)


class TeslaCarHeatedSteeringWheel(TeslaCarEntity, SwitchEntity):
    """Representation of a Tesla car heated steering wheel switch."""

    type = "heated steering"
    _attr_icon = "mdi:steering"

    def __init__(
        self,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize heated steering wheel entity."""
        # Entity is disabled for cars with variable heated steering wheel.
        self._enabled_by_default = car.get_heated_steering_wheel_level() is not None
        super().__init__(car, coordinator)

    @property
    def available(self) -> bool:
        """Return True if steering wheel heater is available."""
        return super().available and self._car.steering_wheel_heater

    @property
    def is_on(self):
        """Return True if steering wheel heater is on."""
        return self._car.is_steering_wheel_heater_on

    async def async_turn_on(self, **kwargs):
        """Send the on command."""
        await self._car.set_heated_steering_wheel(True)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Send the off command."""
        await self._car.set_heated_steering_wheel(False)
        self.async_write_ha_state()


class TeslaCarPolling(TeslaCarEntity, SwitchEntity):
    """Representation of a polling switch."""

    type = "polling"
    _attr_icon = "mdi:car-connected"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def is_on(self) -> bool | None:
        """Return True if updates available."""
        controller = self.coordinator.controller
        get_updates = controller.get_updates(vin=self._car.vin)
        if get_updates is None:
            return None
        return bool(get_updates)

    async def async_turn_on(self, **kwargs):
        """Send the on command."""
        _LOGGER.debug("Enable polling: %s %s", self.name, self._car.vin)
        self.coordinator.controller.set_updates(vin=self._car.vin, value=True)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Send the off command."""
        _LOGGER.debug("Disable polling: %s %s", self.name, self._car.vin)
        self.coordinator.controller.set_updates(vin=self._car.vin, value=False)
        self.async_write_ha_state()


class TeslaCarCharger(TeslaCarEntity, SwitchEntity):
    """Representation of a Tesla car charger switch."""

    type = "charger"
    _attr_icon = "mdi:ev-station"

    @property
    def is_on(self):
        """Return charging state."""
        return self._car.charging_state == "Charging"

    async def async_turn_on(self, **kwargs):
        """Send the on command."""
        await self._car.start_charge()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Send the off command."""
        await self._car.stop_charge()
        self.async_write_ha_state()


class TeslaCarSentryMode(TeslaCarEntity, SwitchEntity):
    """Representation of a Tesla car sentry mode switch."""

    type = "sentry mode"
    _attr_icon = "mdi:shield-car"

    def __init__(
        self,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize sentry mode entity."""
        # Entity is only enabled upon first install if sentry mode is available
        self._enabled_by_default = car.sentry_mode_available
        super().__init__(car, coordinator)

    @property
    def available(self) -> bool:
        """Return True if sentry mode switch is available."""
        return super().available and self._car.sentry_mode_available

    @property
    def is_on(self):
        """Return True if sentry mode is on."""
        sentry_mode_available = self._car.sentry_mode_available
        sentry_mode_status = self._car.sentry_mode
        return bool(sentry_mode_available and sentry_mode_status)

    async def async_turn_on(self, **kwargs):
        """Send the on command."""
        await self._car.set_sentry_mode(True)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Send the off command."""
        await self._car.set_sentry_mode(False)
        self.async_write_ha_state()


class TeslaCarValetMode(TeslaCarEntity, SwitchEntity):
    """Representation of a Tesla car valet mode switch."""

    type = "valet mode"
    _attr_icon = "mdi:room-service"

    @property
    def is_on(self):
        """Return valet mode state."""
        return self._car.is_valet_mode

    async def async_turn_on(self, **kwargs):
        """Send the on command."""
        # pylint: disable=protected-access
        if self._car._vehicle_data.get("vehicle_state", {}).get("valet_pin_needed"):
            _LOGGER.debug("Pin required for valet mode, set pin in vehicle or app.")
        else:
            await self._car.valet_mode(True)
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Send the off command."""
        # pylint: disable=protected-access
        if self._car._vehicle_data.get("vehicle_state", {}).get("valet_pin_needed"):
            _LOGGER.debug("Pin required for valet mode, set pin in vehicle or app.")
        else:
            await self._car.valet_mode(False)
            self.async_write_ha_state()
