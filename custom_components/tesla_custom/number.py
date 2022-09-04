"""Support for Tesla numbers."""
from teslajsonpy.car import TeslaCar
from teslajsonpy.const import (
    BACKUP_RESERVE_MAX,
    BACKUP_RESERVE_MIN,
    CHARGE_CURRENT_MIN,
    RESOURCE_TYPE_BATTERY,
)
from teslajsonpy.energy import PowerwallSite

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.core import HomeAssistant

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarEntity, TeslaEnergyEntity
from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla numbers by config_entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    cars = hass.data[DOMAIN][config_entry.entry_id]["cars"]
    energysites = hass.data[DOMAIN][config_entry.entry_id]["energysites"]
    entities = []

    for car in cars.values():
        entities.append(TeslaCarChargeLimit(hass, car, coordinator))
        entities.append(TeslaCarCurrentLimit(hass, car, coordinator))

    for energysite in energysites.values():
        if energysite.resource_type == RESOURCE_TYPE_BATTERY:
            entities.append(TeslaEnergyBackupReserve(hass, energysite, coordinator))

    async_add_entities(entities, True)


class TeslaCarChargeLimit(TeslaCarEntity, NumberEntity):
    """Representation of a Tesla car charge limit number."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize charge limit entity."""
        super().__init__(hass, car, coordinator)
        self.type = "charge limit"
        self._attr_icon = "mdi:ev-station"
        self._attr_mode = NumberMode.AUTO
        self._attr_native_step = 1

    async def async_set_native_value(self, value: int) -> None:
        """Update charge limit."""
        await self._car.change_charge_limit(value)

    @property
    def native_value(self) -> int:
        """Return charge limit."""
        return self._car.charge_limit_soc

    @property
    def native_min_value(self) -> int:
        """Return min charge limit."""
        return self._car.charge_limit_soc_min

    @property
    def native_max_value(self) -> int:
        """Return max charge limit."""
        return self._car.charge_limit_soc_max


class TeslaCarCurrentLimit(TeslaCarEntity, NumberEntity):
    """Representation of a Tesla car current limit number."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize current limit entity."""
        super().__init__(hass, car, coordinator)
        self.type = "current limit"
        self._attr_icon = "mdi:ev-station"
        self._attr_mode = NumberMode.AUTO
        self._attr_native_step = 1

    async def async_set_native_value(self, value: int) -> None:
        """Update current limit."""
        await self._car.set_charging_amps(value)

    @property
    def native_value(self) -> int:
        """Return current limit."""
        return self._car.charge_current_request

    @property
    def native_min_value(self) -> int:
        """Return min current limitt."""
        # Not in API but Tesla app allows minimum of 5
        return CHARGE_CURRENT_MIN

    @property
    def native_max_value(self) -> int:
        """Return max current limit."""
        return self._car.charge_current_request_max


class TeslaEnergyBackupReserve(TeslaEnergyEntity, NumberEntity):
    """Representation of a Tesla energy backup reserve number."""

    def __init__(
        self,
        hass: HomeAssistant,
        energysite: PowerwallSite,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize backup reserve entity."""
        super().__init__(hass, energysite, coordinator)
        self.type = "backup reserve"
        self._attr_icon = "mdi:battery"
        self._attr_mode = NumberMode.AUTO
        self._attr_native_step = 1

    async def async_set_native_value(self, value: int) -> None:
        """Update backup reserve percentage."""
        await self._energysite.set_reserve_percent(value)

    @property
    def native_value(self) -> int:
        """Return backup reserve percentage."""
        return self._energysite.backup_reserve_percent

    @property
    def native_min_value(self) -> int:
        """Return min backup reserve percentage."""
        return BACKUP_RESERVE_MIN

    @property
    def native_max_value(self) -> int:
        """Return max backup reserve percentage."""
        return BACKUP_RESERVE_MAX
