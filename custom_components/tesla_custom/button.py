"""Support for Tesla charger buttons."""
import logging

from homeassistant.components.button import ButtonDeviceClass, ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from teslajsonpy.exceptions import HomelinkError

from . import TeslaDataUpdateCoordinator
from .base import TeslaCarDevice
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Tesla selects by config_entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

    entities = []
    for car in hass.data[DOMAIN][config_entry.entry_id]["cars"]:
        entities.append(Horn(hass, car, coordinator))
        entities.append(FlashLights(hass, car, coordinator))
        entities.append(WakeUp(hass, car, coordinator))
        entities.append(ForceDataUpdate(hass, car, coordinator))
        entities.append(TriggerHomelink(hass, car, coordinator))

    async_add_entities(entities, True)


class Horn(TeslaCarDevice, ButtonEntity):
    """Representation of the Tesla Battery Sensor."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self._name = "horn"
        self._attr_icon = "mdi:bullhorn"

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._send_command(
            "HONK_HORN",
            path_vars={"vehicle_id": self.car.id},
            on=True,
            wake_if_asleep=True,
        )


class FlashLights(TeslaCarDevice, ButtonEntity):
    """Representation of the Tesla Battery Sensor."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self._name = "flash lights"
        self._attr_icon = "mdi:car-light-high"

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._send_command(
            "FLASH_LIGHTS",
            path_vars={"vehicle_id": self.car.id},
            on=True,
            wake_if_asleep=True,
        )


class WakeUp(TeslaCarDevice, ButtonEntity):
    """Representation of the Tesla Battery Sensor."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self._name = "wake up"
        self._attr_icon = "mdi:moon-waning-crescent"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._send_command(
            "WAKE_UP",
            path_vars={"vehicle_id": self.car.id},
            wake_if_asleep=True,
        )


class ForceDataUpdate(TeslaCarDevice, ButtonEntity):
    """Representation of the Tesla Battery Sensor."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialize the Sensor Entity."""
        super().__init__(hass, car, coordinator)
        self._name = "force Data update"
        self._attr_icon = "mdi:database-sync"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.update_controller(wake_if_asleep=True, force=True)

    @property
    def available(self) -> bool:
        """Return True."""
        return True


class TriggerHomelink(TeslaCarDevice, ButtonEntity):
    """Representation of a Tesla Homelink button."""

    def __init__(
        self, hass: HomeAssistant, car: dict, coordinator: TeslaDataUpdateCoordinator
    ) -> None:
        """Initialise the button."""
        super().__init__(hass, car, coordinator)
        self._name = "trigger homelink"
        self._attr_icon = "mdi:garage"
        self.__waiting = False
        self._enabled_by_default = False

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return super().available and not self.__waiting

    def _get_lat_long(self):
        """Get Car's current Lat and Long."""

        lat = None
        long = None

        data: dict = self.car.drive
        if data.get("native_location_supported"):
            long = data.get("native_longitude")
            lat = data.get("native_latitude")
        else:
            long = data.get("longitude")
            lat = data.get("latitude")

        return lat, long

    async def trigger_homelink(self):
        """Trigger Homeline on car."""
        await self.update_controller(wake_if_asleep=True, force=True, blocking=True)

        if self.car.state.get("homelink_device_count") is None:
            raise HomelinkError(f"No homelink devices added to {self.car_name}.")

        if self.car.state.get("homelink_nearby") is not True:
            raise HomelinkError(f"No homelink devices near {self.car_name}.")

        lat, long = self._get_lat_long()

        data = await self._send_command(
            "TRIGGER_HOMELINK",
            path_vars={"vehicle_id": self.car.id},
            lat=lat,
            lon=long,
            wake_if_asleep=True,
        )

        if data and data.get("response"):
            result = data["response"].get("result")
            reason = data["response"].get("reason")
            if result is False:
                raise HomelinkError(f"Error calling trigger_homelink: {reason}")

    async def async_press(self, **kwargs):
        """Send the command."""
        _LOGGER.debug("Trigger homelink: %s", self.name)
        self.__waiting = True
        self.async_write_ha_state()
        try:
            await self.trigger_homelink()
        except HomelinkError as ex:
            _LOGGER.error("%s", ex.message)
        finally:
            self.__waiting = False
            self.async_write_ha_state()
