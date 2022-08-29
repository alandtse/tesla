"""Common methods used across tests for Tesla."""
from datetime import datetime
from unittest.mock import patch

from homeassistant.const import (
    CONF_ACCESS_TOKEN,
    CONF_DOMAIN,
    CONF_TOKEN,
    CONF_USERNAME,
)
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry
from teslajsonpy.car import TeslaCar
from teslajsonpy.energy import SolarSite
from teslajsonpy.const import AUTH_DOMAIN

from custom_components.tesla_custom.const import CONF_EXPIRATION, DOMAIN as TESLA_DOMIN

from .const import TEST_ACCESS_TOKEN, TEST_TOKEN, TEST_USERNAME, TEST_VALID_EXPIRATION
from .mock_data import car as car_mock_data
from .mock_data import energysite as energysite_mock_data


def setup_mock_controller(mock_controller):
    """Setup a mock controller with mock data."""
    instance = mock_controller.return_value

    instance.get_state_params.return_value = car_mock_data.VEHICLE_STATE
    instance.get_config_params.return_value = car_mock_data.VEHICLE_CONFIG
    instance.get_charging_params.return_value = car_mock_data.CHARGE_STATE
    instance.get_climate_params.return_value = car_mock_data.CLIMATE_STATE
    instance.get_gui_params.return_value = car_mock_data.GUI_SETTINGS
    instance.get_drive_params.return_value = car_mock_data.DRIVE_STATE
    instance.is_car_online.return_value = True
    instance.get_last_update_time.return_value = datetime.now()
    instance.get_last_update_time.return_value = datetime.now()
    instance.update_interval.return_value = 660

    instance.get_tokens.return_value = {
        "refresh_token": TEST_TOKEN,
        "access_token": TEST_ACCESS_TOKEN,
        "expiration": TEST_VALID_EXPIRATION,
    }

    instance.generate_car_objects.return_value = {
        car_mock_data.VIN: TeslaCar(
            car_mock_data.SAMPLE_VEHICLE, mock_controller.return_value
        )
    }

    instance.generate_energysite_objects.return_value = {
        1234567890: SolarSite(
            mock_controller.api,
            energysite_mock_data.ENERGYSITE,
            energysite_mock_data.SITE_DATA,
        )
    }


async def setup_platform(hass: HomeAssistant, platform: str) -> MockConfigEntry:
    """Set up the Abode platform."""

    mock_entry = MockConfigEntry(
        domain=TESLA_DOMIN,
        title=TEST_USERNAME,
        data={
            CONF_USERNAME: TEST_USERNAME,
            CONF_ACCESS_TOKEN: TEST_ACCESS_TOKEN,
            CONF_TOKEN: TEST_TOKEN,
            CONF_EXPIRATION: TEST_VALID_EXPIRATION,
            CONF_DOMAIN: AUTH_DOMAIN,
        },
        options=None,
    )

    mock_entry.add_to_hass(hass)

    with patch("custom_components.tesla_custom.PLATFORMS", [platform]), patch(
        "custom_components.tesla_custom.TeslaAPI", autospec=True
    ) as mock_controller:
        setup_mock_controller(mock_controller)
        assert await async_setup_component(hass, TESLA_DOMIN, {})
    await hass.async_block_till_done()

    return mock_entry, mock_controller
