"""Support for Tesla cars."""
import asyncio
from datetime import timedelta
from functools import partial
from http import HTTPStatus
import logging

import async_timeout
from homeassistant.config_entries import SOURCE_IMPORT
from homeassistant.const import (
    CONF_ACCESS_TOKEN,
    CONF_DOMAIN,
    CONF_SCAN_INTERVAL,
    CONF_TOKEN,
    CONF_USERNAME,
    EVENT_HOMEASSISTANT_CLOSE,
)
from homeassistant.core import callback
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers.httpx_client import SERVER_SOFTWARE, USER_AGENT
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import httpx
from teslajsonpy import Controller as TeslaAPI
from teslajsonpy.const import AUTH_DOMAIN
from teslajsonpy.exceptions import IncompleteCredentials, TeslaException

from .config_flow import CannotConnect, InvalidAuth, validate_input
from .const import (
    CONF_ENABLE_TESLAMATE,
    CONF_EXPIRATION,
    CONF_INCLUDE_ENERGYSITES,
    CONF_INCLUDE_VEHICLES,
    CONF_POLLING_POLICY,
    CONF_WAKE_ON_START,
    DATA_LISTENER,
    DEFAULT_ENABLE_TESLAMATE,
    DEFAULT_POLLING_POLICY,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_WAKE_ON_START,
    DOMAIN,
    MIN_SCAN_INTERVAL,
    PLATFORMS,
)
from .services import async_setup_services, async_unload_services
from .teslamate import TeslaMate
from .util import SSL_CONTEXT

_LOGGER = logging.getLogger(__name__)


@callback
def _async_save_tokens(hass, config_entry, access_token, refresh_token, expiration):
    hass.config_entries.async_update_entry(
        config_entry,
        data={
            **config_entry.data,
            CONF_ACCESS_TOKEN: access_token,
            CONF_TOKEN: refresh_token,
            CONF_EXPIRATION: expiration,
        },
    )


@callback
def _async_configured_emails(hass):
    """Return a set of configured Tesla emails."""
    return {
        entry.data[CONF_USERNAME]
        for entry in hass.config_entries.async_entries(DOMAIN)
        if CONF_USERNAME in entry.data
    }


async def async_setup(hass, base_config):
    """Set up of Tesla component."""

    def _update_entry(email, data=None, options=None):
        data = data or {}
        options = options or {
            CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
            CONF_WAKE_ON_START: DEFAULT_WAKE_ON_START,
            CONF_POLLING_POLICY: DEFAULT_POLLING_POLICY,
        }
        for entry in hass.config_entries.async_entries(DOMAIN):
            if email != entry.title:
                continue
            hass.config_entries.async_update_entry(entry, data=data, options=options)

    config = base_config.get(DOMAIN)

    if not config:
        return True

    email = config[CONF_USERNAME]
    token = config[CONF_TOKEN]
    scan_interval = config[CONF_SCAN_INTERVAL]

    if email in _async_configured_emails(hass):
        try:
            info = await validate_input(hass, config)
        except (CannotConnect, InvalidAuth):
            return False
        _update_entry(
            email,
            data={
                CONF_USERNAME: email,
                CONF_ACCESS_TOKEN: info[CONF_ACCESS_TOKEN],
                CONF_TOKEN: info[CONF_TOKEN],
                CONF_EXPIRATION: info[CONF_EXPIRATION],
            },
            options={CONF_SCAN_INTERVAL: scan_interval},
        )
    else:
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN,
                context={"source": SOURCE_IMPORT},
                data={CONF_USERNAME: email, CONF_TOKEN: token},
            )
        )
        hass.data.setdefault(DOMAIN, {})
        hass.data[DOMAIN][email] = {CONF_SCAN_INTERVAL: scan_interval}

    return True


async def async_setup_entry(hass, config_entry):
    """Set up Tesla as config entry."""
    # pylint: disable=too-many-locals,too-many-statements
    hass.data.setdefault(DOMAIN, {})
    config = config_entry.data
    # Because users can have multiple accounts, we always
    # create a new session so they have separate cookies
    async_client = httpx.AsyncClient(
        headers={USER_AGENT: SERVER_SOFTWARE}, timeout=60, verify=SSL_CONTEXT
    )
    email = config_entry.title

    if not hass.data[DOMAIN]:
        async_setup_services(hass)

    if email in hass.data[DOMAIN] and CONF_SCAN_INTERVAL in hass.data[DOMAIN][email]:
        scan_interval = hass.data[DOMAIN][email][CONF_SCAN_INTERVAL]
        hass.config_entries.async_update_entry(
            config_entry, options={CONF_SCAN_INTERVAL: scan_interval}
        )
        hass.data[DOMAIN].pop(email)

    try:
        controller = TeslaAPI(
            async_client,
            email=config.get(CONF_USERNAME),
            refresh_token=config[CONF_TOKEN],
            access_token=config[CONF_ACCESS_TOKEN],
            expiration=config.get(CONF_EXPIRATION, 0),
            auth_domain=config.get(CONF_DOMAIN, AUTH_DOMAIN),
            update_interval=config_entry.options.get(
                CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
            ),
            polling_policy=config_entry.options.get(
                CONF_POLLING_POLICY, DEFAULT_POLLING_POLICY
            ),
        )
        result = await controller.connect(
            include_vehicles=config.get(CONF_INCLUDE_VEHICLES),
            include_energysites=config.get(CONF_INCLUDE_ENERGYSITES),
        )
        refresh_token = result["refresh_token"]
        access_token = result["access_token"]
        expiration = result["expiration"]

    except IncompleteCredentials as ex:
        await async_client.aclose()
        raise ConfigEntryAuthFailed from ex

    except (httpx.ConnectTimeout, httpx.ConnectError) as ex:
        await async_client.aclose()
        raise ConfigEntryNotReady from ex

    except TeslaException as ex:
        await async_client.aclose()

        if ex.code == HTTPStatus.UNAUTHORIZED:
            raise ConfigEntryAuthFailed from ex

        if ex.message in [
            "TOO_MANY_REQUESTS",
            "UPSTREAM_TIMEOUT",
        ]:
            raise ConfigEntryNotReady(
                f"Temporarily unable to communicate with Tesla API: {ex.message}"
            ) from ex

        _LOGGER.error("Unable to communicate with Tesla API: %s", ex.message)

        return False

    async def _async_close_client(*_):
        await async_client.aclose()

    @callback
    def _async_create_close_task():
        # Background tasks are tracked in HA to prevent them from
        # being garbage collected in the middle of the task since
        # asyncio only holds a weak reference to them.
        #
        # https://docs.python.org/3/library/asyncio-task.html#creating-tasks

        if hasattr(hass, "async_create_background_task"):
            hass.async_create_background_task(
                _async_close_client(), "tesla_close_client"
            )
        else:
            asyncio.create_task(_async_close_client())

    config_entry.async_on_unload(
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_CLOSE, _async_close_client)
    )
    config_entry.async_on_unload(_async_create_close_task)

    _async_save_tokens(hass, config_entry, access_token, refresh_token, expiration)

    try:
        if config_entry.data.get("initial_setup"):
            wake_if_asleep = True
        else:
            wake_if_asleep = config_entry.options.get(
                CONF_WAKE_ON_START, DEFAULT_WAKE_ON_START
            )

        cars = await controller.generate_car_objects(wake_if_asleep=wake_if_asleep)

        hass.config_entries.async_update_entry(
            config_entry, data={**config_entry.data, "initial_setup": False}
        )

    except TeslaException as ex:
        await async_client.aclose()

        if ex.message in [
            "TOO_MANY_REQUESTS",
            "SERVICE_MAINTENANCE",
            "UPSTREAM_TIMEOUT",
        ]:
            raise ConfigEntryNotReady(
                f"Temporarily unable to communicate with Tesla API: {ex.message}"
            ) from ex

        _LOGGER.error("Unable to communicate with Tesla API: %s", ex.message)

        return False

    try:
        energysites = await controller.generate_energysite_objects()

    except TeslaException as ex:
        await async_client.aclose()

        if ex.message in [
            "TOO_MANY_REQUESTS",
            "SERVICE_MAINTENANCE",
            "UPSTREAM_TIMEOUT",
        ]:
            raise ConfigEntryNotReady(
                f"Temporarily unable to communicate with Tesla API: {ex.message}"
            ) from ex

        _LOGGER.error("Unable to communicate with Tesla API: %s", ex.message)

        return False

    reload_lock = asyncio.Lock()
    _partial_coordinator = partial(
        TeslaDataUpdateCoordinator,
        hass,
        config_entry=config_entry,
        controller=controller,
        reload_lock=reload_lock,
        energy_site_ids=set(),
        vins=set(),
        update_vehicles=False,
    )
    coordinators = {
        "update_vehicles": _partial_coordinator(update_vehicles=True),
        **{
            energy_site_id: _partial_coordinator(energy_site_ids={energy_site_id})
            for energy_site_id in energysites
        },
        **{vin: _partial_coordinator(vins={vin}) for vin in cars},
    }

    teslamate = TeslaMate(hass=hass, cars=cars, coordinators=coordinators)

    enable_teslamate = config_entry.options.get(
        CONF_ENABLE_TESLAMATE, DEFAULT_ENABLE_TESLAMATE
    )

    await teslamate.enable(enable_teslamate)

    hass.data[DOMAIN][config_entry.entry_id] = {
        "controller": controller,
        "coordinators": coordinators,
        "cars": cars,
        "energysites": energysites,
        "teslamate": teslamate,
        DATA_LISTENER: [config_entry.add_update_listener(update_listener)],
    }
    _LOGGER.debug("Connected to the Tesla API")

    # We do not do a first refresh as we already know the API is working
    # from above. Each platform will schedule a refresh via update_before_add
    # for the sites/vehicles they are interested in.

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_unload_entry(hass, config_entry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    )
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    controller: TeslaAPI = entry_data["controller"]
    await controller.disconnect()

    for listener in entry_data[DATA_LISTENER]:
        listener()
    username = config_entry.title

    await entry_data["teslamate"].unload()

    if unload_ok:
        hass.data[DOMAIN].pop(config_entry.entry_id)
        _LOGGER.debug("Unloaded entry for %s", username)

        if not hass.data[DOMAIN]:
            async_unload_services(hass)

        return True

    return False


async def update_listener(hass, config_entry):
    """Update when config_entry options update."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    controller: TeslaAPI = entry_data["controller"]
    old_update_interval = controller.update_interval
    controller.update_interval = config_entry.options.get(
        CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
    )
    if old_update_interval != controller.update_interval:
        _LOGGER.debug(
            "Changing scan_interval from %s to %s",
            old_update_interval,
            controller.update_interval,
        )

    enable_teslamate = config_entry.options.get(
        CONF_ENABLE_TESLAMATE, DEFAULT_ENABLE_TESLAMATE
    )

    await entry_data["teslamate"].enable(enable_teslamate)


class TeslaDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Tesla data."""

    def __init__(
        self,
        hass,
        *,
        config_entry,
        controller: TeslaAPI,
        reload_lock: asyncio.Lock,
        vins: set[str],
        energy_site_ids: set[str],
        update_vehicles: bool,
    ):
        """Initialize global Tesla data updater."""
        self.controller = controller
        self.config_entry = config_entry
        self.reload_lock = reload_lock
        self.vins = vins
        self.energy_site_ids = energy_site_ids
        self.update_vehicles = update_vehicles

        update_interval = timedelta(seconds=MIN_SCAN_INTERVAL)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        if self.controller.is_token_refreshed():
            # It doesn't matter which coordinator calls this, as long as there
            # are no awaits in the below code, it will be called only once.
            result = self.controller.get_tokens()
            refresh_token = result["refresh_token"]
            access_token = result["access_token"]
            expiration = result["expiration"]
            _async_save_tokens(
                self.hass, self.config_entry, access_token, refresh_token, expiration
            )
            _LOGGER.debug("Saving new tokens in config_entry")

        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(30):
                _LOGGER.debug("Running controller.update()")
                return await self.controller.update(
                    vins=self.vins,
                    energy_site_ids=self.energy_site_ids,
                    update_vehicles=self.update_vehicles,
                )
        except IncompleteCredentials:
            if self.reload_lock.locked():
                # Any of the coordinators can trigger a reload, but we only
                # want to do it once. If the lock is already locked, we know
                # another coordinator is already reloading.
                _LOGGER.debug("Config entry is already being reloaded")
                return
            async with self.reload_lock:
                await self.hass.config_entries.async_reload(self.config_entry.entry_id)
        except TeslaException as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
