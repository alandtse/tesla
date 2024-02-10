"""Tests for the Tesla button."""

from unittest.mock import patch

from homeassistant.components.button import DOMAIN as BUTTON_DOMAIN
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .common import setup_platform
from .mock_data import car as car_mock_data


async def test_registry_entries(hass: HomeAssistant) -> None:
    """Tests devices are registered in the entity registry."""
    await setup_platform(hass, BUTTON_DOMAIN)
    entity_registry = er.async_get(hass)

    entry = entity_registry.async_get("button.my_model_s_horn")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_horn"

    entry = entity_registry.async_get("button.my_model_s_flash_lights")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_flash_lights"

    entry = entity_registry.async_get("button.my_model_s_wake_up")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_wake_up"

    entry = entity_registry.async_get("button.my_model_s_force_data_update")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_force_data_update"

    entry = entity_registry.async_get("button.my_model_s_homelink")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_homelink"

    entry = entity_registry.async_get("button.my_model_s_remote_start")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_remote_start"

    entry = entity_registry.async_get("button.my_model_s_emissions_test")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_emissions_test"


async def test_enabled_by_default(hass: HomeAssistant) -> None:
    """Tests devices are enabled by default."""
    await setup_platform(hass, BUTTON_DOMAIN)
    entity_registry = er.async_get(hass)

    entry = entity_registry.async_get("button.my_model_s_horn")
    assert not entry.disabled

    entry = entity_registry.async_get("button.my_model_s_flash_lights")
    assert not entry.disabled

    entry = entity_registry.async_get("button.my_model_s_wake_up")
    assert not entry.disabled

    entry = entity_registry.async_get("button.my_model_s_force_data_update")
    assert not entry.disabled

    # Default mock data has homelink enabled
    entry = entity_registry.async_get("button.my_model_s_homelink")
    assert not entry.disabled

    entry = entity_registry.async_get("button.my_model_s_remote_start")
    assert not entry.disabled


async def test_disabled_by_default(hass: HomeAssistant) -> None:
    """Tests devices are disabled by default when appropriate."""
    # No garages paired, it should be disabled by default.
    car_mock_data.VEHICLE_DATA["vehicle_state"]["homelink_device_count"] = 0
    await setup_platform(hass, BUTTON_DOMAIN)
    entity_registry = er.async_get(hass)

    entry = entity_registry.async_get("button.my_model_s_homelink")
    assert entry.disabled


async def test_horn_press(hass: HomeAssistant) -> None:
    """Tests car horn button press."""
    await setup_platform(hass, BUTTON_DOMAIN)

    with patch("teslajsonpy.car.TeslaCar.honk_horn") as mock_honk_horn:
        await hass.services.async_call(
            BUTTON_DOMAIN,
            "press",
            {ATTR_ENTITY_ID: "button.my_model_s_horn"},
            blocking=True,
        )
        mock_honk_horn.assert_awaited_once()


async def test_flash_lights_press(hass: HomeAssistant) -> None:
    """Tests car flash lights button press."""
    await setup_platform(hass, BUTTON_DOMAIN)

    with patch("teslajsonpy.car.TeslaCar.flash_lights") as mock_flash_lights:
        await hass.services.async_call(
            BUTTON_DOMAIN,
            "press",
            {ATTR_ENTITY_ID: "button.my_model_s_flash_lights"},
            blocking=True,
        )
        mock_flash_lights.assert_awaited_once()


async def test_wake_up_press(hass: HomeAssistant) -> None:
    """Tests car wake up button press."""
    await setup_platform(hass, BUTTON_DOMAIN)

    with patch("teslajsonpy.car.TeslaCar.wake_up") as mock_wake_up:
        await hass.services.async_call(
            BUTTON_DOMAIN,
            "press",
            {ATTR_ENTITY_ID: "button.my_model_s_wake_up"},
            blocking=True,
        )
        mock_wake_up.assert_awaited_once()


async def test_force_data_update_press(hass: HomeAssistant) -> None:
    """Tests car force data button press."""
    await setup_platform(hass, BUTTON_DOMAIN)

    with patch(
        "custom_components.tesla_custom.base.TeslaCarEntity.update_controller"
    ) as mock_force_data_update:
        await hass.services.async_call(
            BUTTON_DOMAIN,
            "press",
            {ATTR_ENTITY_ID: "button.my_model_s_force_data_update"},
            blocking=True,
        )
        mock_force_data_update.assert_awaited_once_with(wake_if_asleep=True, force=True)


async def test_trigger_homelink_press(hass: HomeAssistant) -> None:
    """Tests car trigger homelink button press."""
    car_mock_data.VEHICLE_DATA["vehicle_state"]["homelink_device_count"] = 1
    car_mock_data.VEHICLE_DATA["vehicle_state"]["homelink_nearby"] = True
    await setup_platform(hass, BUTTON_DOMAIN)

    with patch("teslajsonpy.car.TeslaCar.trigger_homelink") as mock_trigger_homelink:
        await hass.services.async_call(
            BUTTON_DOMAIN,
            "press",
            {ATTR_ENTITY_ID: "button.my_model_s_homelink"},
            blocking=True,
        )
        mock_trigger_homelink.assert_awaited_once()


async def test_remote_start_press(hass: HomeAssistant) -> None:
    """Tests car remote start button press."""
    await setup_platform(hass, BUTTON_DOMAIN)

    with patch("teslajsonpy.car.TeslaCar.remote_start") as mock_remote_start:
        await hass.services.async_call(
            BUTTON_DOMAIN,
            "press",
            {ATTR_ENTITY_ID: "button.my_model_s_remote_start"},
            blocking=True,
        )
        mock_remote_start.assert_awaited_once()


async def test_emissions_test_press(hass: HomeAssistant) -> None:
    """Tests car emissions test button press."""
    await setup_platform(hass, BUTTON_DOMAIN)

    with patch("teslajsonpy.car.TeslaCar.remote_boombox") as mock_remote_boombox:
        await hass.services.async_call(
            BUTTON_DOMAIN,
            "press",
            {ATTR_ENTITY_ID: "button.my_model_s_emissions_test"},
            blocking=True,
        )
        mock_remote_boombox.assert_awaited_once()
