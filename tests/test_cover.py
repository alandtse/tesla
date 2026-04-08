"""Tests for the Tesla cover."""

from unittest.mock import patch

from homeassistant.components.cover import DOMAIN as COVER_DOMAIN
from homeassistant.const import ATTR_ENTITY_ID, SERVICE_CLOSE_COVER, SERVICE_OPEN_COVER
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .common import setup_platform
from .mock_data import car as car_mock_data


async def test_registry_entries(hass: HomeAssistant) -> None:
    """Tests devices are registered in the entity registry."""
    await setup_platform(hass, COVER_DOMAIN)
    entity_registry = er.async_get(hass)

    entry = entity_registry.async_get("cover.my_model_s_charger_door")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_charger_door"

    entry = entity_registry.async_get("cover.my_model_s_frunk")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_frunk"

    entry = entity_registry.async_get("cover.my_model_s_trunk")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_trunk"

    entry = entity_registry.async_get("cover.my_model_s_windows")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_windows"

    entry = entity_registry.async_get("cover.my_model_s_sunroof")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_sunroof"


async def test_charger_door(hass: HomeAssistant) -> None:
    """Tests charger door cover."""
    await setup_platform(hass, COVER_DOMAIN)

    with patch("teslajsonpy.car.TeslaCar.charge_port_door_open") as mock_open_cover:
        await hass.services.async_call(
            COVER_DOMAIN,
            SERVICE_OPEN_COVER,
            {ATTR_ENTITY_ID: "cover.my_model_s_charger_door"},
            blocking=True,
        )
        mock_open_cover.assert_awaited_once()

    with patch("teslajsonpy.car.TeslaCar.charge_port_door_close") as mock_close_cover:
        await hass.services.async_call(
            COVER_DOMAIN,
            SERVICE_CLOSE_COVER,
            {ATTR_ENTITY_ID: "cover.my_model_s_charger_door"},
            blocking=True,
        )
        mock_close_cover.assert_awaited_once()


async def test_frunk(hass: HomeAssistant) -> None:
    """Tests frunk cover."""
    await setup_platform(hass, COVER_DOMAIN)

    with patch("teslajsonpy.car.TeslaCar.toggle_frunk") as mock_toggle_frunk:
        await hass.services.async_call(
            COVER_DOMAIN,
            SERVICE_OPEN_COVER,
            {ATTR_ENTITY_ID: "cover.my_model_s_frunk"},
            blocking=True,
        )
        mock_toggle_frunk.assert_awaited_once()


async def test_trunk(hass: HomeAssistant) -> None:
    """Tests trunk cover."""
    await setup_platform(hass, COVER_DOMAIN)

    with patch("teslajsonpy.car.TeslaCar.toggle_trunk") as mock_toggle_trunk:
        await hass.services.async_call(
            COVER_DOMAIN,
            SERVICE_OPEN_COVER,
            {ATTR_ENTITY_ID: "cover.my_model_s_trunk"},
            blocking=True,
        )
        mock_toggle_trunk.assert_awaited_once()


async def test_windows(hass: HomeAssistant) -> None:
    """Tests windows cover."""
    await setup_platform(hass, COVER_DOMAIN)

    with patch("teslajsonpy.car.TeslaCar.close_windows") as mock_close_cover:
        await hass.services.async_call(
            COVER_DOMAIN,
            SERVICE_CLOSE_COVER,
            {ATTR_ENTITY_ID: "cover.my_model_s_windows"},
            blocking=True,
        )
        mock_close_cover.assert_not_awaited()

    with patch("teslajsonpy.car.TeslaCar.vent_windows") as mock_open_cover:
        await hass.services.async_call(
            COVER_DOMAIN,
            SERVICE_OPEN_COVER,
            {ATTR_ENTITY_ID: "cover.my_model_s_windows"},
            blocking=True,
        )
        mock_open_cover.assert_awaited_once()

    car_mock_data.VEHICLE_DATA["vehicle_state"]["fd_window"] = 1
    car_mock_data.VEHICLE_DATA["vehicle_state"]["fp_window"] = 1
    car_mock_data.VEHICLE_DATA["vehicle_state"]["rd_window"] = 1
    car_mock_data.VEHICLE_DATA["vehicle_state"]["rp_window"] = 1

    with patch("teslajsonpy.car.TeslaCar.vent_windows") as mock_open_cover:
        await hass.services.async_call(
            COVER_DOMAIN,
            SERVICE_OPEN_COVER,
            {ATTR_ENTITY_ID: "cover.my_model_s_windows"},
            blocking=True,
        )
        mock_close_cover.assert_not_awaited()

    with patch("teslajsonpy.car.TeslaCar.close_windows") as mock_close_cover:
        await hass.services.async_call(
            COVER_DOMAIN,
            SERVICE_CLOSE_COVER,
            {ATTR_ENTITY_ID: "cover.my_model_s_windows"},
            blocking=True,
        )
        mock_close_cover.assert_awaited_once()


async def test_sunroof_registry_entry(hass: HomeAssistant) -> None:
    """Tests sunroof is registered in the entity registry."""
    await setup_platform(hass, COVER_DOMAIN)
    entity_registry = er.async_get(hass)

    entry = entity_registry.async_get("cover.my_model_s_sunroof")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_sunroof"


async def test_sunroof_vent(hass: HomeAssistant) -> None:
    """Tests sunroof vent (open) command."""
    await setup_platform(hass, COVER_DOMAIN)

    with patch(
        "teslajsonpy.car.TeslaCar._send_command",
        return_value={"response": {"result": True}},
    ) as mock_send_command:
        await hass.services.async_call(
            COVER_DOMAIN,
            SERVICE_OPEN_COVER,
            {ATTR_ENTITY_ID: "cover.my_model_s_sunroof"},
            blocking=True,
        )
        mock_send_command.assert_awaited_once_with("CHANGE_SUNROOF_STATE", state="vent")
        assert car_mock_data.VEHICLE_DATA["vehicle_state"]["sun_roof_state"] == "vent"

    car_mock_data.VEHICLE_DATA["vehicle_state"]["sun_roof_state"] = "closed"


async def test_sunroof_close(hass: HomeAssistant) -> None:
    """Tests sunroof close command."""
    await setup_platform(hass, COVER_DOMAIN)

    car_mock_data.VEHICLE_DATA["vehicle_state"]["sun_roof_state"] = "vent"

    with patch(
        "teslajsonpy.car.TeslaCar._send_command",
        return_value={"response": {"result": True}},
    ) as mock_send_command:
        await hass.services.async_call(
            COVER_DOMAIN,
            SERVICE_CLOSE_COVER,
            {ATTR_ENTITY_ID: "cover.my_model_s_sunroof"},
            blocking=True,
        )
        mock_send_command.assert_awaited_once_with("CHANGE_SUNROOF_STATE", state="close")
        assert car_mock_data.VEHICLE_DATA["vehicle_state"]["sun_roof_state"] == "closed"


async def test_sunroof_no_duplicate_command_when_already_open(hass: HomeAssistant) -> None:
    """Tests that vent command is not sent when sunroof is already vented."""
    await setup_platform(hass, COVER_DOMAIN)

    car_mock_data.VEHICLE_DATA["vehicle_state"]["sun_roof_state"] = "vent"

    with patch("teslajsonpy.car.TeslaCar._send_command") as mock_send_command:
        await hass.services.async_call(
            COVER_DOMAIN,
            SERVICE_OPEN_COVER,
            {ATTR_ENTITY_ID: "cover.my_model_s_sunroof"},
            blocking=True,
        )
        mock_send_command.assert_not_awaited()

    car_mock_data.VEHICLE_DATA["vehicle_state"]["sun_roof_state"] = "closed"


async def test_sunroof_no_duplicate_command_when_already_closed(hass: HomeAssistant) -> None:
    """Tests that close command is not sent when sunroof is already closed."""
    await setup_platform(hass, COVER_DOMAIN)

    with patch("teslajsonpy.car.TeslaCar._send_command") as mock_send_command:
        await hass.services.async_call(
            COVER_DOMAIN,
            SERVICE_CLOSE_COVER,
            {ATTR_ENTITY_ID: "cover.my_model_s_sunroof"},
            blocking=True,
        )
        mock_send_command.assert_not_awaited()
