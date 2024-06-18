"""Tests for the Tesla climate."""

from unittest.mock import patch

from homeassistant.components.climate import DOMAIN as CLIMATE_DOMAIN
from homeassistant.const import ATTR_ENTITY_ID, ATTR_TEMPERATURE, STATE_OFF
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .common import setup_platform
from .mock_data import car as car_mock_data

DEVICE_ID = "climate.my_model_s_hvac_climate_system"


async def test_registry_entries(hass: HomeAssistant) -> None:
    """Tests devices are registered in the entity registry."""
    await setup_platform(hass, CLIMATE_DOMAIN)
    entity_registry = er.async_get(hass)

    entry = entity_registry.async_get(DEVICE_ID)
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_hvac_climate_system"


async def test_climate_properties(hass: HomeAssistant) -> None:
    """Tests car climate properties."""
    await setup_platform(hass, CLIMATE_DOMAIN)

    state = hass.states.get(DEVICE_ID)

    assert state.state == STATE_OFF

    assert (
        state.attributes.get("min_temp")
        == car_mock_data.VEHICLE_DATA["climate_state"]["min_avail_temp"]
    )
    assert (
        state.attributes.get("max_temp")
        == car_mock_data.VEHICLE_DATA["climate_state"]["max_avail_temp"]
    )
    assert (
        state.attributes.get("current_temperature")
        == car_mock_data.VEHICLE_DATA["climate_state"]["inside_temp"]
    )
    assert (
        state.attributes.get("temperature")
        == car_mock_data.VEHICLE_DATA["climate_state"]["driver_temp_setting"]
    )


async def test_set_temperature(hass: HomeAssistant) -> None:
    """Tests car setting temperature."""
    await setup_platform(hass, CLIMATE_DOMAIN)

    with patch("teslajsonpy.car.TeslaCar.set_temperature") as mock_set_temperature:
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            "set_temperature",
            {
                ATTR_ENTITY_ID: DEVICE_ID,
                ATTR_TEMPERATURE: 21.0,
            },
            blocking=True,
        )
        mock_set_temperature.assert_awaited_once_with(21.0)


async def test_set_hvac_mode(hass: HomeAssistant) -> None:
    """Tests car setting HVAC mode."""
    await setup_platform(hass, CLIMATE_DOMAIN)

    with patch("teslajsonpy.car.TeslaCar.set_hvac_mode") as mock_set_hvac_mode:
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            "set_hvac_mode",
            {
                ATTR_ENTITY_ID: DEVICE_ID,
                "hvac_mode": "heat_cool",
            },
            blocking=True,
        )
        mock_set_hvac_mode.assert_awaited_once_with("on")


async def test_set_fan_mode(hass: HomeAssistant) -> None:
    """Tests car setting Bioweapon mode."""
    await setup_platform(hass, CLIMATE_DOMAIN)

    with patch("teslajsonpy.car.TeslaCar.set_bioweapon_mode") as mock_set_fan_mode:
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            "set_fan_mode",
            {
                ATTR_ENTITY_ID: DEVICE_ID,
                "fan_mode": "bioweapon",
            },
            blocking=True,
        )
        mock_set_fan_mode.assert_awaited_once_with(True)


async def test_set_preset_mode(hass: HomeAssistant) -> None:
    """Tests car setting HVAC mode."""
    await setup_platform(hass, CLIMATE_DOMAIN)

    with (
        patch("teslajsonpy.car.TeslaCar.set_max_defrost") as mock_set_max_defrost,
        patch("teslajsonpy.car.TeslaCar.defrost_mode", return_value=1),
    ):
        # Test set preset_mode "Normal" with defrost_mode != 0
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            "set_preset_mode",
            {
                ATTR_ENTITY_ID: DEVICE_ID,
                "preset_mode": "normal",
            },
            blocking=True,
        )
        mock_set_max_defrost.assert_awaited_once_with(False)

    with (
        patch(
            "teslajsonpy.car.TeslaCar.set_climate_keeper_mode"
        ) as mock_set_climate_keeper_mode,
        patch("teslajsonpy.car.TeslaCar.climate_keeper_mode", return_value="on"),
    ):
        # Test set preset_mode "Normal" with climate_keeper_mode != 0
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            "set_preset_mode",
            {
                ATTR_ENTITY_ID: DEVICE_ID,
                "preset_mode": "normal",
            },
            blocking=True,
        )
        mock_set_climate_keeper_mode.assert_awaited_once_with(0)

    with patch("teslajsonpy.car.TeslaCar.set_max_defrost") as mock_set_max_defrost:
        # Test set preset_mode "Defrost"
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            "set_preset_mode",
            {
                ATTR_ENTITY_ID: DEVICE_ID,
                "preset_mode": "defrost",
            },
            blocking=True,
        )
        mock_set_max_defrost.assert_awaited_once_with(2)

    with patch(
        "teslajsonpy.car.TeslaCar.set_climate_keeper_mode"
    ) as mock_set_climate_keeper_mode:
        # Test set preset_mode "Dog Mode"
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            "set_preset_mode",
            {
                ATTR_ENTITY_ID: DEVICE_ID,
                "preset_mode": "dog",
            },
            blocking=True,
        )
        mock_set_climate_keeper_mode.assert_awaited_once_with(2)
