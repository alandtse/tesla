"""Support for Tesla binary sensor."""
import logging

from teslajsonpy.const import GRID_ACTIVE, RESOURCE_TYPE_BATTERY
from teslajsonpy.energy import PowerwallSite
from teslajsonpy.car import TeslaCar

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant

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
        entities.append(ParkingBrake(hass, car, coordinator))
        entities.append(CarOnline(hass, car, coordinator))
        entities.append(ChargerConnection(hass, car, coordinator))
        entities.append(Charging(hass, car, coordinator))

    for energysite in energysites.values():
        if energysite.resource_type == RESOURCE_TYPE_BATTERY:
            entities.append(TeslaEnergyCharging(hass, energysite, coordinator))
            entities.append(TeslaEnergyGridStatus(hass, energysite, coordinator))

    async_add_entities(entities, True)


class ParkingBrake(TeslaCarDevice, BinarySensorEntity):
    """Representation of the Tesla Battery Sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "parking brake"
        self._attr_icon = "mdi:car-brake-parking"
        self._attr_device_class = None

    @property
    def is_on(self):
        """Return the state of the binary sensor."""
        return self._car.shift_state == "P"


class ChargerConnection(TeslaCarDevice, BinarySensorEntity):
    """Representation of the Tesla Battery Sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "charger"
        self._attr_icon = "mdi:ev-station"
        self._attr_device_class = None

    @property
    def is_on(self):
        """Return the state of the binary sensor."""
        return self._car.charging_state != "Disconnected"

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        attrs = {
            "charging_state": self._car.charging_state,
            "conn_charge_cable": self._car.conn_charge_cable,
            "fast_charger_present": self._car.fast_charger_present,
            "fast_charger_brand": self._car.fast_charger_brand,
            "fast_charger_type": self._car.fast_charger_type,
        }

        return attrs


class Charging(TeslaCarDevice, BinarySensorEntity):
    """Representation of the Tesla Battery Sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "charging"
        self._attr_icon = None
        self._attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING

    @property
    def is_on(self):
        """Return the state of the binary sensor."""
        return self._car.charging_state == "Charging"


class CarOnline(TeslaCarDevice, BinarySensorEntity):
    """Representation of the Tesla Battery Sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "online"
        self._attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    @property
    def is_on(self):
        """Return the state of the binary sensor."""
        return self._car.is_on

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        attrs = {
            "vehicle_id": self._car.vehicle_id,
            "vin": self._car.vin,
            "id": self._car.id,
        }

        return attrs


class TeslaEnergyCharging(TeslaEnergyDevice, BinarySensorEntity):
    """Representation of the Tesla energy charging sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        energysite: PowerwallSite,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, energysite, coordinator)
        self.type = "charging"
        self._attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING

    @property
    def is_on(self) -> bool:
        """Return the state of battery charging."""
        return self._energysite.battery_power > 0


class TeslaEnergyGridStatus(TeslaEnergyDevice, BinarySensorEntity):
    """Representation of the Tesla energy grid status sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        energysite: PowerwallSite,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, energysite, coordinator)
        self.type = "grid status"
        self._attr_device_class = BinarySensorDeviceClass.POWER

    @property
    def is_on(self) -> bool:
        """Return the state of the grid status."""
        return self._energysite.grid_status == GRID_ACTIVE
