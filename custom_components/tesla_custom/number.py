"""Support for the Tesla sensors."""
from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.core import HomeAssistant

from . import TeslaDataUpdateCoordinator
from .base import TeslaBaseEntity
from .const import DOMAIN

CHARGE_CURRENT_MIN = 1


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla Sensors by config_entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

    entities = []
    for car in hass.data[DOMAIN][config_entry.entry_id]["cars"]:
        entities.append(TeslaChargeLimit(hass, car, coordinator))
        entities.append(TeslaCurrentLimit(hass, car, coordinator))

    async_add_entities(entities, True)


class TeslaChargeLimit(TeslaBaseEntity, NumberEntity):
    """Representation of the Tesla Charge Limit Number."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Number Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "charge limit number"
        self._attr_icon = "mdi:battery"
        self._attr_mode = NumberMode.AUTO
        self._attr_step = 1

    async def async_set_value(self, value: float) -> None:
        """Update the current value."""

        data = await self._send_command(
            "CHANGE_CHARGE_LIMIT",
            path_vars={"vehicle_id": self.car.id},
            percent=int(value),
            wake_if_asleep=True,
        )

        if data and data["response"]["result"] is True:
            self.car.climate["charge_limit_soc"] = int(value)
            self.async_write_ha_state()

    @property
    def value(self):
        """Return the current value."""

        return self.car.charging.get("charge_limit_soc")

    @property
    def min_value(self):
        """Return the Min value for Charge Limit."""

        return self.car.charging.get("charge_limit_soc_min")

    @property
    def max_value(self):
        """Return the Max value for Charge Limit."""

        return self.car.charging.get("charge_limit_soc_max")


class TeslaCurrentLimit(TeslaBaseEntity, NumberEntity):
    """Representation of the Tesla Current Limit Number."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Number Entity."""
        super().__init__(hass, car, coordinator)
        self.type = "current limit number"
        self._attr_icon = "mdi:battery"
        self._attr_mode = NumberMode.AUTO
        self._attr_step = 1

    async def async_set_value(self, value: float) -> None:
        """Update the current value."""

        data = await self._send_command(
            "CHARGING_AMPS",
            path_vars={"vehicle_id": self.car.id},
            charging_amps=int(value),
            wake_if_asleep=True,
        )

        if data and data["response"]["result"] is True:
            self.car.climate["charge_limit_soc"] = int(value)
            self.async_write_ha_state()

    @property
    def value(self):
        """Return the current value."""

        return self.car.charging.get("charge_current_request")

    @property
    def min_value(self):
        """Return the Min value for Charge Limit."""

        # I can't find anything in the API that
        # sets the min_value for current requests.
        # So i've just set it to 1 amp 🤷‍♂️
        return CHARGE_CURRENT_MIN

    @property
    def max_value(self):
        """Return the Max value for Charge Limit."""

        return self.car.charging.get("charge_current_request_max")
