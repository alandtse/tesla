"""Support for Tesla charger switches."""
import logging

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarDevice
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla selects by config_entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

    entities = []
    for car in hass.data[DOMAIN][config_entry.entry_id]["cars"]:
        entities.append(HeatedSteeringWheel(hass, car, coordinator))
        entities.append(Polling(hass, car, coordinator))
        entities.append(Charger(hass, car, coordinator))
        entities.append(SentryMode(hass, car, coordinator))

    async_add_entities(entities, True)


class HeatedSteeringWheel(TeslaCarDevice, SwitchEntity):
    """Representation of the Tesla Battery Sensor."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self._name = "heated steering switch"
        self._attr_icon = "mdi:steering"

    @property
    def is_on(self):
        """Return Heated Steering Wheel state."""

        return self.car.climate.get("steering_wheel_heater")

    async def set_heated_steering_wheel(self, value: bool) -> None:
        """Set the Heated Steering Wheel to the desired state."""
        _LOGGER.info("Setting Heated Steering Wheel to: %s", value)
        data = await self._send_command(
            "REMOTE_STEERING_WHEEL_HEATER_REQUEST",
            path_vars={"vehicle_id": self.car.id},
            on=value,
            wake_if_asleep=True,
        )

        if data and data["response"]["result"]:
            self.car.climate["steering_wheel_heater"] = value
            self.async_write_ha_state()

    async def async_turn_on(self, **kwargs):
        """Send the on command."""
        await self.set_heated_steering_wheel(True)

    async def async_turn_off(self, **kwargs):
        """Send the off command."""
        await self.set_heated_steering_wheel(False)


class Polling(TeslaCarDevice, SwitchEntity):
    """Representation of the Polling Switch."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self._name = "polling switch"
        self._attr_icon = "mdi:car-connected"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def is_on(self):
        """Return Heated Steering Wheel state."""
        if self._coordinator.controller.get_updates(vin=self.car.vin) is None:
            return None

        return bool(self._coordinator.controller.get_updates(vin=self.car.vin))

    async def async_turn_on(self, **kwargs):
        """Send the on command."""
        _LOGGER.debug("Enable polling: %s %s", self.name, self.car.vin)
        self._coordinator.controller.set_updates(vin=self.car.vin, value=True)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Send the off command."""
        _LOGGER.debug("Disable polling: %s %s", self.name, self.car.vin)
        self._coordinator.controller.set_updates(vin=self.car.vin, value=False)
        self.async_write_ha_state()


class Charger(TeslaCarDevice, SwitchEntity):
    """Representation of the Tesla Battery Sensor."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Representation of a Tesla charger switch."""
        super().__init__(hass, car, coordinator)
        self._name = "charger switch"
        self._attr_icon = "mdi:battery-charging"

    @property
    def is_on(self):
        """Return Heated Steering Wheel state."""
        charging_state = self.car.charging.get("charging_state")

        return charging_state == "Charging"

    async def async_turn_on(self, **kwargs):
        """Send the on command."""
        data = await self._send_command(
            "START_CHARGE",
            path_vars={"vehicle_id": self.car.id},
            wake_if_asleep=True,
        )

        if data and data["response"]["result"]:
            self.car.charging["charging_state"] = "Charging"
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Send the off command."""
        data = await self._send_command(
            "STOP_CHARGE",
            path_vars={"vehicle_id": self.car.id},
            wake_if_asleep=True,
        )

        if data and data["response"]["result"]:
            self.car.charging["charging_state"] = None
            self.async_write_ha_state()

            # Do a non-blocking update to get the latest Charging state.
            self.update_controller(wake_if_asleep=True, force=True, blocking=False)


class SentryMode(TeslaCarDevice, SwitchEntity):
    """Representation of the Tesla Battery Sensor."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Representation of a Tesla Sentry Mode switch."""
        super().__init__(hass, car, coordinator)
        self._name = "sentry mode switch"
        self._attr_icon = "mdi:shield-car"

    @property
    def is_on(self):
        """Return Sentry Mode state."""
        sentry_mode_available = self.car.state.get("sentry_mode_available")
        sentry_mode_status = self.car.state.get("sentry_mode")

        if sentry_mode_available is True and sentry_mode_status is True:
            return True

        return False

    async def set_sentry_mode(self, value: bool) -> None:
        """Set Sentry Mode to the desired value."""
        data = await self._send_command(
            "SET_SENTRY_MODE",
            path_vars={"vehicle_id": self.car.id},
            on=value,
            wake_if_asleep=True,
        )

        if data and data["response"]["result"]:
            self.car.state["sentry_mode"] = value
            self.async_write_ha_state()

    async def async_turn_on(self, **kwargs):
        """Send the on command."""
        await self.set_sentry_mode(True)

    async def async_turn_off(self, **kwargs):
        """Send the off command."""
        await self.set_sentry_mode(False)
