"""Support for Tesla binary sensor."""
import logging

from teslajsonpy.const import TESLA_RESOURCE_TYPE_BATTERY

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

    entities = []
    for car in hass.data[DOMAIN][config_entry.entry_id]["cars"]:
        entities.append(ParkingBrake(hass, car, coordinator))
        entities.append(CarOnline(hass, car, coordinator))
        entities.append(ChargerConnection(hass, car, coordinator))
        entities.append(Charging(hass, car, coordinator))

    for energysite in hass.data[DOMAIN][config_entry.entry_id]["energysites"]:
        if energysite["resource_type"] == TESLA_RESOURCE_TYPE_BATTERY:
            entities.append(TeslaEnergyCharging(hass, energysite, coordinator))

    async_add_entities(entities, True)


class ParkingBrake(TeslaCarDevice, BinarySensorEntity):
    """Representation of the Tesla Battery Sensor."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "parking brake"
        self._attr_icon = "mdi:car-brake-parking"
        self._attr_device_class = None

    @property
    def is_on(self):
        """Return the state of the binary sensor."""
        return self.car.drive.get("shift_state") == "P"


class ChargerConnection(TeslaCarDevice, BinarySensorEntity):
    """Representation of the Tesla Battery Sensor."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "charger"
        self._attr_icon = "mdi:ev-station"
        self._attr_device_class = None

    @property
    def is_on(self):
        """Return the state of the binary sensor."""
        return self.car.charging.get("charging_state") != "Disconnected"

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        attrs = {
            "charging_state": self.car.charging.get("charging_state"),
            "conn_charge_cable": self.car.charging.get("conn_charge_cable"),
            "fast_charger_present": self.car.charging.get("fast_charger_present"),
            "fast_charger_brand": self.car.charging.get("fast_charger_brand"),
            "fast_charger_type": self.car.charging.get("fast_charger_type"),
        }

        return attrs


class Charging(TeslaCarDevice, BinarySensorEntity):
    """Representation of the Tesla Battery Sensor."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "charging"
        self._attr_icon = None
        self._attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING

    @property
    def is_on(self):
        """Return the state of the binary sensor."""
        return self.car.charging.get("charging_state") == "Charging"


class CarOnline(TeslaCarDevice, BinarySensorEntity):
    """Representation of the Tesla Battery Sensor."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "online"
        self._attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    @property
    def is_on(self):
        """Return the state of the binary sensor."""
        return self._coordinator.controller.car_online[self.car.vin]

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the device."""
        attrs = {
            "vehicle_id": self.car.vehicle_id,
            "vin": self.car.vin,
            "id": self.car.id,
        }

        return attrs


class TeslaEnergyCharging(TeslaEnergyDevice, BinarySensorEntity):
    """Representation of the Tesla energy charging sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        energysite: dict,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, energysite, coordinator)
        self.type = "charging"
        self._attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING

    @property
    def is_on(self):
        """Return the state of the binary sensor."""

        return (
            self.coordinator.controller.get_power_params(self.energysite_id)[
                "battery_power"
            ]
            > 0
        )
