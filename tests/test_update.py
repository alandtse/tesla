"""Tests for the Tesla update."""
from unittest.mock import patch
import pytest

from homeassistant.components.update import DOMAIN as UPDATE_DOMAIN

from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import entity_registry as er

from .common import setup_platform
from .mock_data import car as car_mock_data


async def test_registry_entries(hass: HomeAssistant) -> None:
    """Tests devices are registered in the entity registry."""
    await setup_platform(hass, UPDATE_DOMAIN)
    entity_registry = er.async_get(hass)

    entry = entity_registry.async_get("update.my_model_s_software_update")
    assert entry.unique_id == f"{car_mock_data.VIN.lower()}_software_update"


async def test_status_download_wait_wifi(hass: HomeAssistant) -> None:
    """Tests waiting on wifi status"""
    car_mock_data.VEHICLE_DATA["vehicle_state"]["software_update"] = {
        "download_perc": 0,
        "expected_duration_sec": 2700,
        "install_perc": 1,
        "status": "downloading_wifi_wait",
        "version": "2022.36.20",
    }
    await setup_platform(hass, UPDATE_DOMAIN)

    state = hass.states.get("update.my_model_s_software_update")
    assert state.state == "on"
    assert state.attributes.get("latest_version") == "2022.36.20 (Waiting on Wi-Fi)"
    assert state.attributes.get("installed_version") == "2022.8.10.1"
    assert state.attributes.get("in_progress") is False
    assert (
        state.attributes.get("release_url")
        == "https://www.notateslaapp.com/software-updates/version/2022.36.20/release-notes"
    )
    with pytest.raises(HomeAssistantError):
        await hass.services.async_call(
            UPDATE_DOMAIN,
            "install",
            {ATTR_ENTITY_ID: "update.my_model_s_software_update"},
            blocking=True,
        )


async def test_status_downloading(hass: HomeAssistant) -> None:
    """Tests downloading status"""
    car_mock_data.VEHICLE_DATA["vehicle_state"]["software_update"] = {
        "download_perc": 50,
        "expected_duration_sec": 2700,
        "install_perc": 1,
        "status": "downloading",
        "version": "2022.36.20",
    }
    await setup_platform(hass, UPDATE_DOMAIN)

    state = hass.states.get("update.my_model_s_software_update")
    assert state.state == "on"
    assert state.attributes.get("latest_version") == "2022.36.20 (Downloading)"
    assert state.attributes.get("installed_version") == "2022.8.10.1"
    assert state.attributes.get("in_progress") is False
    assert (
        state.attributes.get("release_url")
        == "https://www.notateslaapp.com/software-updates/version/2022.36.20/release-notes"
    )
    with pytest.raises(HomeAssistantError):
        await hass.services.async_call(
            UPDATE_DOMAIN,
            "install",
            {ATTR_ENTITY_ID: "update.my_model_s_software_update"},
            blocking=True,
        )


async def test_status_available(hass: HomeAssistant) -> None:
    """Tests available status"""
    car_mock_data.VEHICLE_DATA["vehicle_state"]["software_update"] = {
        "download_perc": 100,
        "expected_duration_sec": 2700,
        "install_perc": 10,
        "status": "available",
        "version": "2022.36.20",
    }
    await setup_platform(hass, UPDATE_DOMAIN)

    state = hass.states.get("update.my_model_s_software_update")
    assert state.state == "on"
    assert state.attributes.get("latest_version") == "2022.36.20 (Available to install)"
    assert state.attributes.get("installed_version") == "2022.8.10.1"
    assert state.attributes.get("in_progress") is False
    assert (
        state.attributes.get("release_url")
        == "https://www.notateslaapp.com/software-updates/version/2022.36.20/release-notes"
    )
    with patch(
        "teslajsonpy.car.TeslaCar.schedule_software_update"
    ) as mock_schedule_software_update:

        assert await hass.services.async_call(
            UPDATE_DOMAIN,
            "install",
            {ATTR_ENTITY_ID: "update.my_model_s_software_update"},
            blocking=True,
        )
        mock_schedule_software_update.assert_awaited_once()


async def test_status_scheduled(hass: HomeAssistant) -> None:
    """Tests scheduled status"""
    car_mock_data.VEHICLE_DATA["vehicle_state"]["software_update"] = {
        "download_perc": 100,
        "expected_duration_sec": 2700,
        "install_perc": 10,
        "scheduled_time_ms": 1669209103248,
        "status": "scheduled",
        "version": "2022.36.20",
        "warning_time_remaining_ms": 70509,
    }
    await setup_platform(hass, UPDATE_DOMAIN)

    state = hass.states.get("update.my_model_s_software_update")
    assert state.state == "on"
    assert (
        state.attributes.get("latest_version") == "2022.36.20 (Scheduled for install)"
    )
    assert state.attributes.get("installed_version") == "2022.8.10.1"
    assert state.attributes.get("in_progress") is False
    assert (
        state.attributes.get("release_url")
        == "https://www.notateslaapp.com/software-updates/version/2022.36.20/release-notes"
    )
    with patch(
        "teslajsonpy.car.TeslaCar.schedule_software_update"
    ) as mock_schedule_software_update:

        assert await hass.services.async_call(
            UPDATE_DOMAIN,
            "install",
            {ATTR_ENTITY_ID: "update.my_model_s_software_update"},
            blocking=True,
        )
        mock_schedule_software_update.assert_awaited_once()


async def test_status_installing(hass: HomeAssistant) -> None:
    """Tests installing status"""
    car_mock_data.VEHICLE_DATA["vehicle_state"]["software_update"] = {
        "download_perc": 100,
        "expected_duration_sec": 2700,
        "install_perc": 30,
        "status": "installing",
        "version": "2022.36.20",
    }
    await setup_platform(hass, UPDATE_DOMAIN)

    state = hass.states.get("update.my_model_s_software_update")
    assert state.state == "on"
    assert state.attributes.get("latest_version") == "2022.36.20 (Installing)"
    assert state.attributes.get("installed_version") == "2022.8.10.1"
    assert state.attributes.get("in_progress") == 30
    assert (
        state.attributes.get("release_url")
        == "https://www.notateslaapp.com/software-updates/version/2022.36.20/release-notes"
    )
    with pytest.raises(HomeAssistantError):
        await hass.services.async_call(
            UPDATE_DOMAIN,
            "install",
            {ATTR_ENTITY_ID: "update.my_model_s_software_update"},
            blocking=True,
        )


async def test_status_none(hass: HomeAssistant) -> None:
    """Tests no update"""
    car_mock_data.VEHICLE_DATA["vehicle_state"]["software_update"] = {
        "download_perc": 0,
        "expected_duration_sec": 2700,
        "install_perc": 1,
        "status": "",
        "version": "2022.8.10.1",
    }
    await setup_platform(hass, UPDATE_DOMAIN)

    state = hass.states.get("update.my_model_s_software_update")
    assert state.state == "off"
    assert state.attributes.get("latest_version") == "2022.8.10.1"
    assert state.attributes.get("installed_version") == "2022.8.10.1"
    assert state.attributes.get("in_progress") is False
    assert (
        state.attributes.get("release_url")
        == "https://www.notateslaapp.com/software-updates/version/2022.8.10.1/release-notes"
    )
    with pytest.raises(HomeAssistantError):
        await hass.services.async_call(
            UPDATE_DOMAIN,
            "install",
            {ATTR_ENTITY_ID: "update.my_model_s_software_update"},
            blocking=True,
        )
