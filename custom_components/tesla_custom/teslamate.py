"""TelsmaMate Module.

This listens to Teslamate MQTT topics, and updates their entites
with the latest data.
"""

import asyncio
import logging
from typing import TYPE_CHECKING

from homeassistant.components.mqtt.models import ReceiveMessage
from homeassistant.components.mqtt.subscription import (
    async_prepare_subscribe_topics,
    async_subscribe_topics,
    async_unsubscribe_topics,
)
from homeassistant.components.mqtt import (
    mqtt_config_entry_enabled,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store
from teslajsonpy.car import TeslaCar

from .const import TESLAMATE_STORAGE_KEY, TESLAMATE_STORAGE_VERSION

if TYPE_CHECKING:
    from . import TeslaDataUpdateCoordinator

logger = logging.getLogger(__name__)

MAP_DRIVE_STATE = {
    "latitude": ("latitude", float),
    "longitude": ("longitude", float),
    "shift_state": ("shift_state", str),
    "speed": ("speed", int),
    "heading": ("heading", int),
}

MAP_CLIMATE_STATE = {
    "is_climate_on": ("is_climate_on", bool),
    "inside_temp": ("inside_temp", float),
    "outside_temp": ("outside_temp", float),
}

MAP_VEHICLE_STATE = {
    "tpms_pressure_fl": ("tpms_pressure_fl", float),
    "tpms_pressure_fr": ("tpms_pressure_fr", float),
    "tpms_pressure_rl": ("tpms_pressure_rl", float),
    "tpms_pressure_rr": ("tpms_pressure_rr", float),
}


class TeslaMate:
    def __init__(
        self,
        hass: HomeAssistant,
        coordinators: list["TeslaDataUpdateCoordinator"],
        cars: dict[str, TeslaCar],
    ):
        self.cars = cars
        self.hass = hass
        self.coordinators = coordinators
        self._enabled = False

        self.watchers = []

        self._sub_state = None
        self._store = Store[dict[str, str]](
            hass, TESLAMATE_STORAGE_VERSION, TESLAMATE_STORAGE_KEY
        )

    async def unload(self):
        """Unload any MQTT watchers."""
        self._enabled = False

        if not mqtt_config_entry_enabled(self.hass):
            logger.warning(
                "Cannot unsub from TeslaMate as MQTT has not been configured."
            )
            return None
        else:
            await self._unsub_mqtt()

        return True

    async def _unsub_mqtt(self):
        """Unsub from MQTT topics."""
        logger.info("Un-subbing from MQTT Topics.")
        self._sub_state = async_unsubscribe_topics(self.hass, self._sub_state)

    async def set_car_id(self, vin, teslamate_id):
        """Set the TeslaMate Car ID."""
        if (data := await self._store.async_load()) is None:
            data = {}

        if "car_map" not in data:
            data["car_map"] = {}

        data["car_map"][vin] = teslamate_id

        await self._store.async_save(data)

    async def get_car_id(self, vin) -> str | None:
        """Get the TeslaMate Car ID."""
        if (data := await self._store.async_load()) is None:
            data = {}

        if "car_map" not in data:
            data["car_map"] = {}

        result = data["car_map"].get(vin)

        return result

    async def enable(self, enable=True):
        """Start Listening to MQTT topics."""

        if enable is False:
            return await self.unload()

        self._enabled = True
        return await self.watch_cars()

    async def watch_cars(self):
        """Start listening to MQTT for updates."""

        if self._enabled is False:
            logger.info("Can't watch cars. teslaMate is not enabled.")
            return None

        if not mqtt_config_entry_enabled(self.hass):
            logger.warning("Cannot enable TeslaMate as MQTT has not been configured.")
            return None

        logger.info("Setting up MQTT subs for Teslamate")

        # We'll unsub from all topics before we create new ones.
        await self._unsub_mqtt()

        for vin in self.cars:
            car = self.cars[vin]
            teslamate_id = await self.get_car_id(vin=vin)

            if teslamate_id is not None:
                await self._watch_car(car=car, teslamate_id=teslamate_id)

    async def _watch_car(self, car: TeslaCar, teslamate_id: str):
        """Set up MQTT watchers for a car."""

        topics = {}

        def msg_recieved(msg: ReceiveMessage):
            return asyncio.run_coroutine_threadsafe(
                self.async_handle_new_data(car, msg), self.hass.loop
            ).result()

        sub_id = f"teslamate_{car.vin}"
        topics[sub_id] = {
            "topic": f"teslamate/cars/{teslamate_id}/#",
            "msg_callback": msg_recieved,
            "qos": 0,
        }

        self._sub_state = async_prepare_subscribe_topics(
            self.hass, self._sub_state, topics
        )

        await async_subscribe_topics(self.hass, self._sub_state)

    async def async_handle_new_data(self, car: TeslaCar, msg: ReceiveMessage):
        """Update Car Data from MQTT msg."""

        mqtt_attr = msg.topic.split("/")[-1]
        coordinator = self.coordinators[car.vin]

        if mqtt_attr in MAP_DRIVE_STATE:
            logger.info("Setting %s from MQTT", mqtt_attr)
            attr, cast = MAP_DRIVE_STATE[mqtt_attr]
            self.update_drive_state(car, attr, cast(msg.payload))
            coordinator.async_update_listeners()

        elif mqtt_attr in MAP_VEHICLE_STATE:
            logger.info("Setting %s from MQTT", mqtt_attr)
            attr, cast = MAP_VEHICLE_STATE[mqtt_attr]
            self.update_vehicle_state(car, attr, cast(msg.payload))
            coordinator.async_update_listeners()

        elif mqtt_attr in MAP_CLIMATE_STATE:
            logger.info("Setting %s from MQTT", mqtt_attr)
            attr, cast = MAP_CLIMATE_STATE[mqtt_attr]
            self.update_climate_state(car, attr, cast(msg.payload))
            coordinator.async_update_listeners()

    @staticmethod
    def update_drive_state(car, attr, value):
        """Update Drive State Safely."""

        if "drive_state" not in car._vehicle_data:
            car._vehicle_data["drive_state"] = {}

        drive_state = car._vehicle_data["drive_state"]
        drive_state[attr] = value

    @staticmethod
    def update_vehicle_state(car, attr, value):
        """Update Vehicle State Safely."""

        if "vehicle_state" not in car._vehicle_data:
            car._vehicle_data["vehicle_state"] = {}

        vehicle_state = car._vehicle_data["vehicle_state"]
        vehicle_state[attr] = value

    @staticmethod
    def update_climate_state(car, attr, value):
        """Update Climate State Safely."""

        if "climate_state" not in car._vehicle_data:
            car._vehicle_data["climate_state"] = {}

        climate_state = car._vehicle_data["climate_state"]
        climate_state[attr] = value
