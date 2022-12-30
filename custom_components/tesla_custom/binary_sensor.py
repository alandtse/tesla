"""Support for Tesla binary sensors."""
import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.core import HomeAssistant
from teslajsonpy.car import TeslaCar
from teslajsonpy.const import GRID_ACTIVE, RESOURCE_TYPE_BATTERY
from teslajsonpy.energy import PowerwallSite

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarEntity, TeslaEnergyEntity
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla selects by config_entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    cars = hass.data[DOMAIN][config_entry.entry_id]["cars"]
    energysites = hass.data[DOMAIN][config_entry.entry_id]["energysites"]
    entities = []

    for car in cars.values():
        entities.append(TeslaCarParkingBrake(hass, car, coordinator))
        entities.append(TeslaCarOnline(hass, car, coordinator))
        entities.append(TeslaCarAsleep(hass, car, coordinator))
        entities.append(TeslaCarChargerConnection(hass, car, coordinator))
        entities.append(TeslaCarCharging(hass, car, coordinator))
        entities.append(TeslaCarDoors(hass, car, coordinator))
        entities.append(TeslaCarScheduledCharging(hass, car, coordinator))
        entities.append(TeslaCarScheduledDeparture(hass, car, coordinator))
        entities.append(TeslaCarUserPresent(hass, car, coordinator))

    for energysite in energysites.values():
        if energysite.resource_type == RESOURCE_TYPE_BATTERY:
            entities.append(TeslaEnergyBatteryCharging(hass, energysite, coordinator))
            entities.append(TeslaEnergyGridStatus(hass, energysite, coordinator))

    async_add_entities(entities, True)


class TeslaCarParkingBrake(TeslaCarEntity, BinarySensorEntity):
    """Representation of a Tesla car parking brake binary sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize parking brake entity."""
        super().__init__(hass, car, coordinator)
        self.type = "parking brake"
        self._attr_icon = "mdi:car-brake-parking"
        self._attr_device_class = None

    @property
    def is_on(self):
        """Return True if car shift state in park or None."""
        # When car is parked and off, Tesla API reports shift_state None
        return self._car.shift_state == "P" or self._car.shift_state is None


class TeslaCarChargerConnection(TeslaCarEntity, BinarySensorEntity):
    """Representation of a Tesla car charger connection binary sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize charger connection entity."""
        super().__init__(hass, car, coordinator)
        self.type = "charger"
        self._attr_icon = "mdi:ev-station"
        self._attr_device_class = BinarySensorDeviceClass.PLUG

    @property
    def is_on(self):
        """Return True if charger connected."""
        return self._car.charging_state != "Disconnected"

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        return {
            "charging_state": self._car.charging_state,
            "conn_charge_cable": self._car.conn_charge_cable,
            "fast_charger_present": self._car.fast_charger_present,
            "fast_charger_brand": self._car.fast_charger_brand,
            "fast_charger_type": self._car.fast_charger_type,
        }


class TeslaCarCharging(TeslaCarEntity, BinarySensorEntity):
    """Representation of Tesla car charging binary sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize charging entity."""
        super().__init__(hass, car, coordinator)
        self.type = "charging"
        self._attr_icon = "mdi:ev-station"
        self._attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING

    @property
    def is_on(self):
        """Return the state of the binary sensor."""
        return self._car.charging_state == "Charging"


class TeslaCarOnline(TeslaCarEntity, BinarySensorEntity):
    """Representation of a Tesla car online binary sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize car online entity."""
        super().__init__(hass, car, coordinator)
        self.type = "online"
        self._attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    @property
    def is_on(self):
        """Return True if car is online."""
        return self._car.is_on

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        return {
            "vehicle_id": str(self._car.vehicle_id),
            "vin": self._car.vin,
            "id": str(self._car.id),
            "state": self._car.state,
        }


class TeslaCarAsleep(TeslaCarEntity, BinarySensorEntity):
    """Representation of a Tesla car asleep binary sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize car asleep entity."""
        super().__init__(hass, car, coordinator)
        self.type = "asleep"
        self._attr_device_class = None
        self._attr_icon = "mdi:sleep"

    @property
    def is_on(self):
        """Return True if car is asleep."""
        return self._car.state == "asleep"


class TeslaEnergyBatteryCharging(TeslaEnergyEntity, BinarySensorEntity):
    """Representation of a Tesla energy charging binary sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        energysite: PowerwallSite,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize battery charging entity."""
        super().__init__(hass, energysite, coordinator)
        self.type = "battery charging"
        self._attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING
        self._attr_icon = "mdi:battery-charging"

    @property
    def is_on(self) -> bool:
        """Return True if battery charging."""
        return self._energysite.battery_power < -100


class TeslaEnergyGridStatus(TeslaEnergyEntity, BinarySensorEntity):
    """Representation of the Tesla energy grid status binary sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        energysite: PowerwallSite,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize grid status entity."""
        super().__init__(hass, energysite, coordinator)
        self.type = "grid status"
        self._attr_device_class = BinarySensorDeviceClass.POWER

    @property
    def is_on(self) -> bool:
        """Return True if grid status is active."""
        return self._energysite.grid_status == GRID_ACTIVE


class TeslaCarDoors(TeslaCarEntity, BinarySensorEntity):
    """Representation of a Tesla car door sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize car door entity."""
        super().__init__(hass, car, coordinator)
        self.type = "doors"
        self._attr_device_class = BinarySensorDeviceClass.DOOR
        self._attr_icon = "mdi:car-door"

    @property
    def is_on(self):
        """Return True if a car door is open."""
        return (
            self._car.door_df
            or self._car.door_dr
            or self._car.door_pf
            or self._car.door_pr
        )

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        return {
            "Driver Front": self._open_or_closed(self._car.door_df),
            "Driver Rear": self._open_or_closed(self._car.door_dr),
            "Passenger Front": self._open_or_closed(self._car.door_pf),
            "Passenger Rear": self._open_or_closed(self._car.door_pr),
        }

    def _open_or_closed(self, door):
        """Return string of 'Open' or 'Closed' when passed a door integer state."""
        if door:
            return "Open"
        return "Closed"


class TeslaCarScheduledCharging(TeslaCarEntity, BinarySensorEntity):
    """Representation of a Tesla car scheduled charging binary sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize scheduled charging entity."""
        super().__init__(hass, car, coordinator)
        self.type = "scheduled charging"
        self._attr_icon = "mdi:calendar-plus"
        self._attr_device_class = None

    @property
    def is_on(self):
        """Return True if scheduled charging enebaled."""
        if self._car.scheduled_charging_mode == "StartAt":
            return True
        return False

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        # pylint: disable=protected-access
        timestamp = self._car._vehicle_data.get("charge_state", {}).get(
            "scheduled_charging_start_time"
        )
        return {
            "Scheduled charging time": self._car.scheduled_charging_start_time_app,
            "Scheduled charging timestamp": timestamp,
        }


class TeslaCarScheduledDeparture(TeslaCarEntity, BinarySensorEntity):
    """Representation of a Tesla car scheduled departure binary sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize scheduled departure entity."""
        super().__init__(hass, car, coordinator)
        self.type = "scheduled departure"
        self._attr_icon = "mdi:calendar-plus"
        self._attr_device_class = None

    @property
    def is_on(self):
        """Return True if scheduled departure enebaled."""
        if (
            self._car.scheduled_charging_mode == "DepartBy"
            or self._car.is_preconditioning_enabled
            or self._car.is_off_peak_charging_enabled
        ):
            return True
        return False

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        # pylint: disable=protected-access
        timestamp = self._car._vehicle_data.get("charge_state", {}).get(
            "scheduled_departure_time"
        )
        return {
            "Departure time": self._car.scheduled_departure_time_minutes,
            "Preconditioning enabled": self._car.is_preconditioning_enabled,
            "Preconditioning weekdays only": self._car.is_preconditioning_weekday_only,
            "Off peak charging enabled": self._car.is_off_peak_charging_enabled,
            "Off peak charging weekdays only": self._car.is_off_peak_charging_weekday_only,
            "End off peak time": self._car.off_peak_hours_end_time,
            "Departure timestamp": timestamp,
        }


class TeslaCarUserPresent(TeslaCarEntity, BinarySensorEntity):
    """Representation of a Tesla car user present binary sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        car: TeslaCar,
        coordinator: TeslaDataUpdateCoordinator,
    ) -> None:
        """Initialize user present entity."""
        super().__init__(hass, car, coordinator)
        self.type = "user present"
        self._attr_icon = "mdi:account-check"
        self._attr_device_class = None

    @property
    def is_on(self):
        """Return True if user present enebaled."""
        # pylint: disable=protected-access
        return self._car._vehicle_data.get("vehicle_state", {}).get("is_user_present")

    @property
    def extra_state_attributes(self):
        """Return device state attributes."""
        # pylint: disable=protected-access
        user_id = str(self._car._vehicle_data.get("user_id"))

        return {"user_id": user_id}
