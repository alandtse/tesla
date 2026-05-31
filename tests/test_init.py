"""Tests for the Tesla integration setup and device removal."""

from unittest.mock import MagicMock

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
import pytest
from teslajsonpy.car import TeslaCar
from teslajsonpy.energy import SolarPowerwallSite, SolarSite

from custom_components.tesla_custom import async_remove_config_entry_device
from custom_components.tesla_custom.base import device_identifier
from custom_components.tesla_custom.const import DOMAIN

from .common import setup_platform
from .const import TEST_USERNAME
from .mock_data import car as car_mock_data, energysite as energysite_mock_data

# Mock data ids used across the helpers below.
CAR_ID = 12345678901234567  # car_mock_data.VEHICLE["id"]
SOLAR_SITE_ID = 12345
BATTERY_SITE_ID = 67890


def _make_car() -> TeslaCar:
    """Return a TeslaCar built from the shared mock data."""
    return TeslaCar(
        car_mock_data.VEHICLE,
        MagicMock(),
        car_mock_data.VEHICLE_DATA,
    )


def _make_solar_site() -> SolarSite:
    """Return a SolarSite built from the shared mock data."""
    return SolarSite(
        MagicMock(),
        energysite_mock_data.ENERGYSITE_SOLAR,
        energysite_mock_data.SITE_CONFIG_SOLAR,
        energysite_mock_data.SITE_DATA,
    )


def _make_battery_site() -> SolarPowerwallSite:
    """Return a SolarPowerwallSite built from the shared mock data."""
    return SolarPowerwallSite(
        MagicMock(),
        energysite_mock_data.ENERGYSITE_BATTERY,
        energysite_mock_data.SITE_CONFIG_POWERWALL,
        energysite_mock_data.BATTERY_DATA,
        energysite_mock_data.BATTERY_SUMMARY,
    )


def _device_entry(*identifiers) -> dr.DeviceEntry:
    """Build a minimal DeviceEntry-like object exposing only identifiers."""
    entry = MagicMock(spec=dr.DeviceEntry)
    entry.identifiers = set(identifiers)
    return entry


def _config_entry(entry_id: str = "test_entry") -> ConfigEntry:
    """Build a minimal ConfigEntry-like object exposing only entry_id."""
    entry = MagicMock(spec=ConfigEntry)
    entry.entry_id = entry_id
    return entry


def test_device_identifier_discriminates_by_type() -> None:
    """device_identifier uses car.id for cars and energysite_id for sites."""
    car = _make_car()
    solar = _make_solar_site()
    battery = _make_battery_site()

    assert device_identifier(car) == (DOMAIN, car.id)
    assert device_identifier(solar) == (DOMAIN, SOLAR_SITE_ID)
    assert device_identifier(battery) == (DOMAIN, BATTERY_SITE_ID)
    # Energy sites must not be identified by car-style ``id``.
    assert device_identifier(solar)[1] == solar.energysite_id
    assert device_identifier(battery)[1] == battery.energysite_id


def _entry_data():
    """Return an entry_data dict shaped like hass.data[DOMAIN][entry_id]."""
    return {
        "cars": {car_mock_data.VIN: _make_car()},
        "energysites": {
            SOLAR_SITE_ID: _make_solar_site(),
            BATTERY_SITE_ID: _make_battery_site(),
        },
    }


def _hass_with_entry(entry_id: str = "test_entry"):
    """Return a MagicMock hass whose data holds a loaded entry."""
    hass = MagicMock(spec=HomeAssistant)
    hass.data = {DOMAIN: {entry_id: _entry_data()}}
    return hass


async def test_remove_protects_live_car() -> None:
    """A device matching a live car must not be removable."""
    hass = _hass_with_entry()
    device = _device_entry((DOMAIN, CAR_ID))
    assert (
        await async_remove_config_entry_device(hass, _config_entry(), device) is False
    )


async def test_remove_protects_live_energy_site() -> None:
    """A device matching a live energy site must not be removable."""
    hass = _hass_with_entry()
    for site_id in (SOLAR_SITE_ID, BATTERY_SITE_ID):
        device = _device_entry((DOMAIN, site_id))
        assert (
            await async_remove_config_entry_device(hass, _config_entry(), device)
            is False
        )


async def test_remove_allows_orphan_device() -> None:
    """A device no longer provided by the integration is removable."""
    hass = _hass_with_entry()
    device = _device_entry((DOMAIN, 99999999999))
    assert await async_remove_config_entry_device(hass, _config_entry(), device) is True


async def test_remove_refuses_when_entry_not_loaded() -> None:
    """Removal must be refused while the config entry is not loaded."""
    hass = MagicMock(spec=HomeAssistant)
    hass.data = {DOMAIN: {}}
    device = _device_entry((DOMAIN, 99999999999))
    assert (
        await async_remove_config_entry_device(hass, _config_entry(), device) is False
    )

    # Also when DOMAIN itself is absent from hass.data.
    hass.data = {}
    assert (
        await async_remove_config_entry_device(hass, _config_entry(), device) is False
    )


async def test_remove_handles_id_coercion() -> None:
    """Identifier comparison is exact: a string id does not match an int id.

    The integration registers integer ids, so a device entry holding the
    string form is treated as an orphan (removable) rather than silently
    matching a live device.
    """
    hass = _hass_with_entry()
    device = _device_entry((DOMAIN, str(CAR_ID)))
    assert await async_remove_config_entry_device(hass, _config_entry(), device) is True


async def test_remove_protects_device_merged_with_foreign_domain() -> None:
    """A device with our live id plus a foreign-domain id stays protected.

    Device entries can carry identifiers from multiple integrations. As long
    as one of our live identifiers is present, the device must not be removed.
    """
    hass = _hass_with_entry()
    device = _device_entry((DOMAIN, CAR_ID), ("other_domain", "abc123"))
    assert (
        await async_remove_config_entry_device(hass, _config_entry(), device) is False
    )


async def test_remove_orphan_with_only_foreign_domain() -> None:
    """A device carrying only foreign-domain identifiers is removable."""
    hass = _hass_with_entry()
    device = _device_entry(("other_domain", "abc123"))
    assert await async_remove_config_entry_device(hass, _config_entry(), device) is True


@pytest.mark.parametrize("platform", ["binary_sensor"])
async def test_remove_with_real_loaded_entry(
    hass: HomeAssistant, platform: str
) -> None:
    """Integration test using the real setup fixture and device registry.

    Verifies the live car and energy-site devices created by setup are
    protected, while an orphaned device under the same entry is removable.
    """
    mock_entry, _ = await setup_platform(hass, platform)

    device_registry = dr.async_get(hass)

    # The car and both energy sites must be registered and protected.
    car_device = device_registry.async_get_device(identifiers={(DOMAIN, CAR_ID)})
    assert car_device is not None
    assert await async_remove_config_entry_device(hass, mock_entry, car_device) is False

    for site_id in (SOLAR_SITE_ID, BATTERY_SITE_ID):
        site_device = device_registry.async_get_device(identifiers={(DOMAIN, site_id)})
        assert site_device is not None
        assert (
            await async_remove_config_entry_device(hass, mock_entry, site_device)
            is False
        )

    # A stale device under the same entry (e.g. a car removed from the
    # account) is no longer provided and must be removable.
    orphan = device_registry.async_get_or_create(
        config_entry_id=mock_entry.entry_id,
        identifiers={(DOMAIN, 99999999999)},
    )
    assert await async_remove_config_entry_device(hass, mock_entry, orphan) is True


def test_config_entry_title_is_username() -> None:
    """Sanity check that the shared fixture username constant is wired."""
    assert TEST_USERNAME == "test-username"
