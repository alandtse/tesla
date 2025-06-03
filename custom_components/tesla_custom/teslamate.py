"""TelsmaMate Module.

This listens to Teslamate MQTT topics, and updates their entites
with the latest data.
"""

import asyncio
import logging
import time
from typing import TYPE_CHECKING

from homeassistant.components.mqtt import mqtt_config_entry_enabled
from homeassistant.components.mqtt.models import ReceiveMessage
from homeassistant.components.mqtt.subscription import (
    async_prepare_subscribe_topics,
    async_subscribe_topics,
    async_unsubscribe_topics,
)
from homeassistant.const import UnitOfLength, UnitOfSpeed
from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store
from homeassistant.util.unit_conversion import DistanceConverter, SpeedConverter
from teslajsonpy.car import TeslaCar

from .const import TESLAMATE_STORAGE_KEY, TESLAMATE_STORAGE_VERSION

if TYPE_CHECKING:
    from . import TeslaDataUpdateCoordinator

logger = logging.getLogger(__name__)


def is_car_state_charging(car_state: str) -> bool:
    """Check if car_state is charging."""
    return car_state == "charging"


def cast_km_to_miles(km_to_convert: float) -> float:
    """Convert KM to Miles.

    The Tesla API natively returns properties in Miles.
    TeslaMate returns some properties in KMs.
    We need to convert to Miles so the home assistant sensor calculates
    properly.
    """
    km = float(km_to_convert)
    miles = DistanceConverter.convert(km, UnitOfLength.KILOMETERS, UnitOfLength.MILES)

    return miles


def cast_bool(val: str) -> bool:
    """Convert bool string to actual bool."""
    return val.lower() in ["true", "True"]


def cast_trunk_open(val: str) -> int:
    """Convert bool string to trunk/frunk open/close value."""
    return 255 if cast_bool(val) else 0


def cast_speed(speed: int) -> int:
    """Convert KM to Miles.

    The Tesla API natively returns the Speed in Miles M/H.
    TeslaMate returns the Speed in km/h.
    We need to convert to Miles so the speed calculates
    properly.
    """
    speed_km = int(speed)
    speed_miles = SpeedConverter.convert(
        speed_km, UnitOfSpeed.KILOMETERS_PER_HOUR, UnitOfSpeed.MILES_PER_HOUR
    )

    return int(speed_miles)


MAP_DRIVE_STATE = {
    "latitude": ("latitude", float),
    "longitude": ("longitude", float),
    "shift_state": ("shift_state", str),
    "speed": ("speed", cast_speed),
    "heading": ("heading", int),
}

MAP_CLIMATE_STATE = {
    "is_climate_on": ("is_climate_on", cast_bool),
    "inside_temp": ("inside_temp", float),
    "outside_temp": ("outside_temp", float),
    "is_preconditioning": ("is_preconditioning", cast_bool),
}

MAP_VEHICLE_STATE = {
    "tpms_pressure_fl": ("tpms_pressure_fl", float),
    "tpms_pressure_fr": ("tpms_pressure_fr", float),
    "tpms_pressure_rl": ("tpms_pressure_rl", float),
    "tpms_pressure_rr": ("tpms_pressure_rr", float),
    "locked": ("locked", cast_bool),
    "sentry_mode": ("sentry_mode", cast_bool),
    "odometer": ("odometer", cast_km_to_miles),
    "trunk_open": ("rt", cast_trunk_open),
    "frunk_open": ("ft", cast_trunk_open),
    "is_user_present": ("is_user_present", cast_bool),
}

MAP_CHARGE_STATE = {
    "battery_level": ("battery_level", float),
    "rated_battery_range_km": ("battery_range", cast_km_to_miles),
    "est_battery_range_km": ("est_battery_range", cast_km_to_miles),
    "ideal_battery_range_km": ("ideal_battery_range", cast_km_to_miles),
    "usable_battery_level": ("usable_battery_level", float),
    "charge_energy_added": ("charge_energy_added", float),
    "charger_actual_current": ("charger_actual_current", int),
    "charger_power": ("charger_power", int),
    "charger_voltage": ("charger_voltage", int),
    "time_to_full_charge": ("time_to_full_charge", float),
    "charge_limit_soc": ("charge_limit_soc", int),
    "charge_port_door_open": ("charge_port_door_open", cast_bool),
    "charge_current_request": ("charge_current_request", int),
    "charge_current_request_max": ("charge_current_request_max", int),
    "charging_state": ("charging_state", str),
}


class TeslaMate:
    """TeslaMate Connector.

    Manages connections to MQTT topics exposed by TeslaMate.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        coordinators: dict[str, "TeslaDataUpdateCoordinator"],
        cars: dict[str, TeslaCar],
    ) -> None:
        """Init Class."""
        self.cars = cars
        self.hass = hass
        self.coordinators = coordinators
        self._enabled = False
        self._data: dict = None

        self.watchers = []

        self._sub_state = None
        self._store = Store[dict[str, str]](
            hass, TESLAMATE_STORAGE_VERSION, TESLAMATE_STORAGE_KEY
        )

    async def unload(self):
        """Unload any MQTT watchers."""
        self._enabled = False

        if mqtt_config_entry_enabled(self.hass):
            await self._unsub_mqtt()
        else:
            logger.info("Cannot unsub from TeslaMate as MQTT has not been configured.")

        return True

    async def _unsub_mqtt(self):
        """Unsub from MQTT topics."""
        logger.info("Un-subbing from all MQTT Topics.")
        self._sub_state = async_unsubscribe_topics(self.hass, self._sub_state)
        logger.info("Un-subbed from all MQTT Topics.")

    async def async_load(self) -> None:
        """Load config."""
        if self._data is None:
            if stored := await self._store.async_load():
                self._data = stored

        # If still None, initialise it.
        if self._data is None:
            self._data = {}

    async def _async_save(self) -> None:
        """Save config."""
        await self._store.async_save(self._data)

    async def set_car_id(self, vin, teslamate_id):
        """Set the TeslaMate Car ID."""
        logger.debug("Setting car ID. VIN:%s TeslamateID: %s", vin, teslamate_id)
        await self.async_load()

        if "car_map" not in self._data:
            self._data["car_map"] = {}

        self._data["car_map"][vin] = teslamate_id

        await self._async_save()
        logger.debug("Successfully set car ID. Latest Car data")
        logger.debug(self._data)

    async def get_car_id(self, vin) -> str | None:
        """Get the TeslaMate Car ID."""
        await self.async_load()

        if "car_map" not in self._data:
            self._data["car_map"] = {}

        result = self._data["car_map"].get(vin)

        logger.debug("Got car ID. VIN:%s TeslamateID: %s", vin, result)

        return result

    async def get_car_from_id(self, teslamate_id: str) -> TeslaCar | None:
        """Get the TeslaCar from the TeslaMateID."""
        logger.debug("Getting TeslaCar for teslaMateID:%s", teslamate_id)

        await self.async_load()

        found_vin = None

        car_map = self._data.get("car_map", {})
        for vin, tm_id in car_map.items():
            if tm_id == teslamate_id:
                found_vin = vin
                break

        if found_vin is None:
            return None

        car = self.cars.get(found_vin)

        return car

    async def enable(self, enable=True):
        """Start Listening to MQTT topics."""

        if enable is False:
            return await self.unload()

        self._enabled = True
        return await self.watch_cars()

    async def watch_cars(self):
        """Start listening to MQTT for updates."""

        # Do nothing if TeslaMate or MQTT is not enabled
        if self._enabled is False:
            logger.info("Can't watch cars. TeslaMate is not enabled.")
            return None
        if not mqtt_config_entry_enabled(self.hass):
            logger.warning("Cannot enable TeslaMate as MQTT has not been configured.")
            return None

        logger.info("Setting up MQTT subs for TeslaMate")

        # Unsubscribe from all topics before creating new ones
        await self._unsub_mqtt()

        topics = {}

        # Generate topics for each car
        for vin in self.cars:
            car = self.cars[vin]
            teslamate_id = await self.get_car_id(vin=vin)

            if teslamate_id is not None:
                await self._get_car_topic(
                    car=car, teslamate_id=teslamate_id, topics=topics
                )

        # Subscribe to all topics
        self._sub_state = async_prepare_subscribe_topics(
            self.hass, self._sub_state, topics
        )
        await async_subscribe_topics(self.hass, self._sub_state)
        logger.debug("Subscribed to MQTT Topics")

        logger.debug("Completed watch_cars")

    async def _get_car_topic(self, car: TeslaCar, teslamate_id: str, topics: dict):
        """Create topics for MQTT subscription and add them to the topics dictionary."""
        logger.debug(
            "Setting up MQTT Sub for VIN:%s TelsaMateID:%s", car.vin, teslamate_id
        )

        def msg_recieved(msg: ReceiveMessage):
            return asyncio.run_coroutine_threadsafe(
                self.async_handle_new_data(msg), self.hass.loop
            ).result()

        sub_id = f"teslamate_{teslamate_id}"
        mqtt_topic = f"teslamate/cars/{teslamate_id}/#"
        logger.debug("MQTT Topic: %s", mqtt_topic)

        topics[sub_id] = {
            "topic": mqtt_topic,
            "msg_callback": msg_recieved,
            "qos": 0,
        }

        logger.info("Created mqtt Topic for: %s", mqtt_topic)

    async def async_handle_new_data(self, msg: ReceiveMessage):
        """Update Car Data from MQTT msg."""
        logger.debug("MQTT Topic Recieved: %s", msg.topic)

        mqtt_attr = msg.topic.split("/")[-1]
        teslamate_id = msg.topic.split("/")[2]
        car = await self.get_car_from_id(teslamate_id)

        if car is None:
            logger.debug("TeslaMate_id %s not found in config", teslamate_id)
            return

        coordinator = self.coordinators[car.vin]

        logger.debug(
            "Got %s from MQTT for VIN:%s | TeslsMateID:%s",
            mqtt_attr,
            car.vin,
            teslamate_id,
        )

        if mqtt_attr in MAP_DRIVE_STATE:
            attr, cast = MAP_DRIVE_STATE[mqtt_attr]
            self.update_car_state(car, "drive_state", attr, cast(msg.payload))

        elif mqtt_attr in MAP_VEHICLE_STATE:
            attr, cast = MAP_VEHICLE_STATE[mqtt_attr]
            self.update_car_state(car, "vehicle_state", attr, cast(msg.payload))

        elif mqtt_attr in MAP_CLIMATE_STATE:
            attr, cast = MAP_CLIMATE_STATE[mqtt_attr]
            self.update_car_state(car, "climate_state", attr, cast(msg.payload))

        elif mqtt_attr in MAP_CHARGE_STATE:
            attr, cast = MAP_CHARGE_STATE[mqtt_attr]
            self.update_car_state(car, "charge_state", attr, cast(msg.payload))

        elif mqtt_attr == "state":
            state = msg.payload
            self.update_car_state(car, None, "state", state)

        else:
            # Nothing matched. Return without updating listeners.
            return

        coordinator.last_update_time = round(time.time())
        coordinator.assumed_state = False
        coordinator.async_update_listeners_debounced()

    def update_charging_state(self, car: TeslaCar, val: str):
        """Update charging state."""
        self.update_car_state(car, "charge_state", "charging_state", val)

    @staticmethod
    def update_car_state(car: TeslaCar, sub_path: str, attr: str, value):
        """Update state safely."""
        # pylint: disable=protected-access

        if sub_path is not None:
            logger.debug(
                "Updating state '%s' to value '%s' in sub_path '%s' for VIN:%s",
                attr,
                value,
                sub_path,
                car.vin,
            )

            if sub_path not in car._vehicle_data:
                car._vehicle_data[sub_path] = {}

            state = car._vehicle_data[sub_path]
            state[attr] = value
        else:
            logger.debug(
                "Updating state '%s' to value '%s' in root for VIN:%s",
                attr,
                value,
                car.vin,
            )
            state = car._car
            state[attr] = value
