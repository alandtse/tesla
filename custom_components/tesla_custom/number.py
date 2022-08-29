"""Support for the Tesla sensors."""
from __future__ import annotations

from teslajsonpy.car import TeslaCar
from teslajsonpy.const import CHARGE_CURRENT_MIN

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.core import HomeAssistant

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarDevice
from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla Sensors by config_entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    cars = hass.data[DOMAIN][config_entry.entry_id]["cars"]
    entities = []

    for car in cars.values():
        entities.append(TeslaChargeLimit(hass, car, coordinator))
        entities.append(TeslaCurrentLimit(hass, car, coordinator))

    async_add_entities(entities, True)


class TeslaChargeLimit(TeslaCarDevice, NumberEntity):
    """Representation of the Tesla Charge Limit Number."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Number Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "charge limit number"
        self._attr_icon = "mdi:battery"
        self._attr_mode = NumberMode.AUTO
        self._attr_native_step = 1

    async def async_set_native_value(self, value: int) -> None:
        """Update the current value."""
        await self._car.change_charge_limit(value)

    @property
    def native_value(self) -> int:
        """Return the current value."""
        return self._car.charge_limit_soc

    @property
    def native_min_value(self) -> int:
        """Return the Min value for Charge Limit."""
        return self._car.charge_limit_soc_min

    @property
    def native_max_value(self) -> int:
        """Return the Max value for Charge Limit."""
        return self._car.charge_limit_soc_max


class TeslaCurrentLimit(TeslaCarDevice, NumberEntity):
    """Representation of the Tesla Current Limit Number."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Number Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "current limit number"
        self._attr_icon = "mdi:battery"
        self._attr_mode = NumberMode.AUTO
        self._attr_native_step = 1

    async def async_set_native_value(self, value: int) -> None:
        """Update the charging amps value."""
        await self._car.set_charging_amps(value)

    @property
    def native_value(self) -> int:
        """Return the current value."""
        return self._car.charge_current_request

    @property
    def native_min_value(self) -> int:
        """Return the Min value for Charge Limit."""
        # Not in API but Tesla app allows minimum of 5
        return CHARGE_CURRENT_MIN

    @property
    def native_max_value(self) -> int:
        """Return the Max value for Charge Limit."""
        return self._car.charge_current_request_max
