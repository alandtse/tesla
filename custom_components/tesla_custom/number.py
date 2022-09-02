"""Support for the Tesla sensors."""
from __future__ import annotations

from teslajsonpy.car import TeslaCar
from teslajsonpy.energy import PowerwallSite
from teslajsonpy.const import (
    BACKUP_RESERVE_MAX,
    BACKUP_RESERVE_MIN,
    CHARGE_CURRENT_MIN,
    RESOURCE_TYPE_BATTERY,
)

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.core import HomeAssistant

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarDevice, TeslaEnergyDevice
from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla Sensors by config_entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    cars = hass.data[DOMAIN][config_entry.entry_id]["cars"]
    energysites = hass.data[DOMAIN][config_entry.entry_id]["energysites"]
    entities = []

    for car in cars.values():
        entities.append(TeslaChargeLimit(hass, car, coordinator))
        entities.append(TeslaCurrentLimit(hass, car, coordinator))

    for energysite in energysites.values():
        if energysite.resource_type == RESOURCE_TYPE_BATTERY:
            entities.append(TeslaEnergyBackupReserve(hass, energysite, coordinator))

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
        self.type = "charge limit"
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
        self.type = "current limit"
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


class TeslaEnergyBackupReserve(TeslaEnergyDevice, NumberEntity):
    """Representation of the Tesla energy backup reserve percent."""

    def __init__(
        self,
        hass: HomeAssistant,
        energysite: PowerwallSite,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Number Entity."""
        super().__init__(hass, energysite, coordinator)
        self.type = "backup reserve"
        self._attr_icon = "mdi:battery"
        self._attr_mode = NumberMode.AUTO
        self._attr_native_step = 1

    async def async_set_native_value(self, value: int) -> None:
        """Update the backup reserve percentage."""
        await self._energysite.set_reserve_percent(value)

    @property
    def native_value(self) -> int:
        """Return the current value."""
        return self._energysite.backup_reserve_percent

    @property
    def native_min_value(self) -> int:
        """Return the min value for battery reserve."""
        return BACKUP_RESERVE_MIN

    @property
    def native_max_value(self) -> int:
        """Return the max value for battery reserve."""
        return BACKUP_RESERVE_MAX
