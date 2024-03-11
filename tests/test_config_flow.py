"""Test the Tesla config flow."""

from http import HTTPStatus
import os
from unittest.mock import patch

from homeassistant import config_entries, data_entry_flow, setup
from homeassistant.const import (
    CONF_ACCESS_TOKEN,
    CONF_CLIENT_ID,
    CONF_DOMAIN,
    CONF_SCAN_INTERVAL,
    CONF_TOKEN,
    CONF_USERNAME,
)
from pytest_homeassistant_custom_component.common import MockConfigEntry
from teslajsonpy.const import AUTH_DOMAIN
from teslajsonpy.exceptions import IncompleteCredentials, TeslaException

from custom_components.tesla_custom.const import (
    ATTR_POLLING_POLICY_CONNECTED,
    CONF_API_PROXY_CERT,
    CONF_API_PROXY_ENABLE,
    CONF_API_PROXY_URL,
    CONF_ENABLE_TESLAMATE,
    CONF_EXPIRATION,
    CONF_INCLUDE_ENERGYSITES,
    CONF_INCLUDE_VEHICLES,
    CONF_POLLING_POLICY,
    CONF_WAKE_ON_START,
    DEFAULT_ENABLE_TESLAMATE,
    DEFAULT_POLLING_POLICY,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_WAKE_ON_START,
    DOMAIN,
    MIN_SCAN_INTERVAL,
)

from .const import (
    TEST_ACCESS_TOKEN,
    TEST_API_PROXY_CERT,
    TEST_API_PROXY_URL,
    TEST_CLIENT_ID,
    TEST_TOKEN,
    TEST_USERNAME,
    TEST_VALID_EXPIRATION,
)


async def test_form(hass):
    """Test we get the form if user chooses no proxy."""
    await setup.async_setup_component(hass, "persistent_notification", {})
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == "form"
    assert result["step_id"] == "user"

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_API_PROXY_ENABLE: False}
    )
    await hass.async_block_till_done()
    assert result2["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result2["step_id"] == "credentials"

    with (
        patch(
            "custom_components.tesla_custom.config_flow.TeslaAPI.connect",
            return_value={
                "refresh_token": TEST_TOKEN,
                CONF_ACCESS_TOKEN: TEST_ACCESS_TOKEN,
                CONF_EXPIRATION: TEST_VALID_EXPIRATION,
            },
        ),
        patch(
            "custom_components.tesla_custom.async_setup", return_value=True
        ) as mock_setup,
        patch(
            "custom_components.tesla_custom.async_setup_entry", return_value=True
        ) as mock_setup_entry,
    ):
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_TOKEN: TEST_TOKEN, CONF_USERNAME: TEST_USERNAME}
        )
        await hass.async_block_till_done()

    assert result3["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    assert result3["title"] == TEST_USERNAME
    assert result3["data"] == {
        CONF_USERNAME: TEST_USERNAME,
        CONF_TOKEN: TEST_TOKEN,
        CONF_ACCESS_TOKEN: TEST_ACCESS_TOKEN,
        CONF_EXPIRATION: TEST_VALID_EXPIRATION,
        CONF_DOMAIN: AUTH_DOMAIN,
        CONF_INCLUDE_VEHICLES: True,
        CONF_INCLUDE_ENERGYSITES: True,
        "initial_setup": True,
        CONF_API_PROXY_URL: None,
        CONF_API_PROXY_CERT: None,
        CONF_CLIENT_ID: None,
    }
    assert len(mock_setup.mock_calls) == 1
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_with_proxy(hass, httpx_mock):
    """Test we get the form if user chooses to use proxy."""

    os.environ["SUPERVISOR_TOKEN"] = "test-token"
    httpx_mock.add_response(
        url="http://supervisor/addons",
        json={
            "data": {
                "addons": [{"name": "Tesla HTTP Proxy", "slug": "tesla_http_proxy"}]
            }
        },
    )
    httpx_mock.add_response(
        url="http://supervisor/addons/tesla_http_proxy/info",
        json={"data": {"hostname": "http-proxy", "options": {"client_id": "test"}}},
    )

    await setup.async_setup_component(hass, "persistent_notification", {})
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == "form"
    assert result["step_id"] == "user"

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_API_PROXY_ENABLE: True}
    )
    await hass.async_block_till_done()
    assert result2["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result2["step_id"] == "credentials"

    with (
        patch(
            "custom_components.tesla_custom.config_flow.TeslaAPI.connect",
            return_value={
                "refresh_token": TEST_TOKEN,
                CONF_ACCESS_TOKEN: TEST_ACCESS_TOKEN,
                CONF_EXPIRATION: TEST_VALID_EXPIRATION,
            },
        ),
        patch(
            "custom_components.tesla_custom.async_setup", return_value=True
        ) as mock_setup,
        patch(
            "custom_components.tesla_custom.async_setup_entry", return_value=True
        ) as mock_setup_entry,
    ):
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_TOKEN: TEST_TOKEN,
                CONF_USERNAME: TEST_USERNAME,
                CONF_CLIENT_ID: TEST_CLIENT_ID,
                CONF_API_PROXY_CERT: TEST_API_PROXY_CERT,
                CONF_API_PROXY_URL: TEST_API_PROXY_URL,
            },
        )
        await hass.async_block_till_done()

    assert result3["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    assert result3["title"] == TEST_USERNAME
    assert result3["data"] == {
        CONF_USERNAME: TEST_USERNAME,
        CONF_TOKEN: TEST_TOKEN,
        CONF_ACCESS_TOKEN: TEST_ACCESS_TOKEN,
        CONF_EXPIRATION: TEST_VALID_EXPIRATION,
        CONF_DOMAIN: AUTH_DOMAIN,
        CONF_INCLUDE_VEHICLES: True,
        CONF_INCLUDE_ENERGYSITES: True,
        "initial_setup": True,
        CONF_API_PROXY_URL: TEST_API_PROXY_URL,
        CONF_API_PROXY_CERT: TEST_API_PROXY_CERT,
        CONF_CLIENT_ID: TEST_CLIENT_ID,
    }
    assert len(mock_setup.mock_calls) == 1
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_invalid_auth(hass):
    """Test we handle invalid auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input={CONF_API_PROXY_ENABLE: False}
    )
    await hass.async_block_till_done()

    with patch(
        "custom_components.tesla_custom.config_flow.TeslaAPI.connect",
        side_effect=TeslaException(401),
    ):
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_TOKEN: TEST_TOKEN, CONF_USERNAME: TEST_USERNAME},
        )

    assert result3["type"] == "form"
    assert result3["errors"] == {"base": "invalid_auth"}


async def test_form_invalid_auth_incomplete_credentials(hass):
    """Test we handle invalid auth with incomplete credentials."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input={CONF_API_PROXY_ENABLE: False}
    )
    await hass.async_block_till_done()

    with patch(
        "custom_components.tesla_custom.config_flow.TeslaAPI.connect",
        side_effect=IncompleteCredentials(401),
    ):
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_USERNAME: TEST_USERNAME, CONF_TOKEN: TEST_TOKEN},
        )

    assert result3["type"] == "form"
    assert result3["errors"] == {"base": "invalid_auth"}


async def test_form_cannot_connect(hass):
    """Test we handle cannot connect error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input={CONF_API_PROXY_ENABLE: False}
    )
    await hass.async_block_till_done()

    with patch(
        "custom_components.tesla_custom.config_flow.TeslaAPI.connect",
        side_effect=TeslaException(code=HTTPStatus.NOT_FOUND),
    ):
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_TOKEN: TEST_TOKEN, CONF_USERNAME: TEST_USERNAME},
        )

    assert result3["type"] == "form"
    assert result3["errors"] == {"base": "cannot_connect"}


async def test_form_repeat_identifier(hass):
    """Test we handle repeat identifiers."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title=TEST_USERNAME,
        data={CONF_USERNAME: TEST_USERNAME, CONF_TOKEN: TEST_TOKEN},
        options=None,
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input={CONF_API_PROXY_ENABLE: False}
    )
    await hass.async_block_till_done()

    with patch(
        "custom_components.tesla_custom.config_flow.TeslaAPI.connect",
        return_value={
            "refresh_token": TEST_TOKEN,
            CONF_ACCESS_TOKEN: TEST_ACCESS_TOKEN,
            CONF_EXPIRATION: TEST_VALID_EXPIRATION,
        },
    ):
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_USERNAME: TEST_USERNAME, CONF_TOKEN: TEST_TOKEN},
        )

    assert result3["type"] == "abort"
    assert result3["reason"] == "already_configured"


async def test_form_reauth(hass):
    """Test we handle reauth."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title=TEST_USERNAME,
        data={CONF_USERNAME: TEST_USERNAME, CONF_TOKEN: TEST_TOKEN},
        options=None,
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_REAUTH},
        data={CONF_USERNAME: TEST_USERNAME},
    )
    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input={CONF_API_PROXY_ENABLE: False}
    )
    await hass.async_block_till_done()

    with patch(
        "custom_components.tesla_custom.config_flow.TeslaAPI.connect",
        return_value={
            "refresh_token": TEST_TOKEN,
            CONF_ACCESS_TOKEN: TEST_ACCESS_TOKEN,
            CONF_EXPIRATION: TEST_VALID_EXPIRATION,
        },
    ):
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_USERNAME: TEST_USERNAME, CONF_TOKEN: "new-password"},
        )

    assert result3["type"] == "abort"
    assert result3["reason"] == "reauth_successful"


async def test_import(hass):
    """Test import step."""

    with patch(
        "custom_components.tesla_custom.config_flow.TeslaAPI.connect",
        return_value={
            "refresh_token": TEST_TOKEN,
            CONF_ACCESS_TOKEN: TEST_ACCESS_TOKEN,
            CONF_EXPIRATION: TEST_VALID_EXPIRATION,
        },
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_IMPORT},
            data={
                CONF_TOKEN: TEST_TOKEN,
                CONF_USERNAME: TEST_USERNAME,
                CONF_INCLUDE_VEHICLES: True,
                CONF_INCLUDE_ENERGYSITES: True,
                CONF_API_PROXY_ENABLE: False,
                CONF_API_PROXY_CERT: None,
                CONF_API_PROXY_URL: None,
                CONF_CLIENT_ID: None,
            },
        )
    assert result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    assert result["title"] == TEST_USERNAME
    assert result["data"][CONF_ACCESS_TOKEN] == TEST_ACCESS_TOKEN
    assert result["data"][CONF_TOKEN] == TEST_TOKEN
    assert result["description_placeholders"] is None


async def test_option_flow(hass):
    """Test config flow options."""
    entry = MockConfigEntry(domain=DOMAIN, data={}, options=None)
    entry.add_to_hass(hass)

    result = await hass.config_entries.options.async_init(entry.entry_id)

    assert result["type"] == "form"
    assert result["step_id"] == "init"

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={
            CONF_SCAN_INTERVAL: 350,
            CONF_WAKE_ON_START: True,
            CONF_POLLING_POLICY: ATTR_POLLING_POLICY_CONNECTED,
            CONF_ENABLE_TESLAMATE: True,
        },
    )
    assert result["type"] == "create_entry"
    assert result["data"] == {
        CONF_SCAN_INTERVAL: 350,
        CONF_WAKE_ON_START: True,
        CONF_POLLING_POLICY: ATTR_POLLING_POLICY_CONNECTED,
        CONF_ENABLE_TESLAMATE: True,
    }


async def test_option_flow_defaults(hass):
    """Test config flow options."""
    entry = MockConfigEntry(domain=DOMAIN, data={}, options=None)
    entry.add_to_hass(hass)

    result = await hass.config_entries.options.async_init(entry.entry_id)

    assert result["type"] == "form"
    assert result["step_id"] == "init"

    result = await hass.config_entries.options.async_configure(
        result["flow_id"], user_input={}
    )
    assert result["type"] == "create_entry"
    assert result["data"] == {
        CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
        CONF_WAKE_ON_START: DEFAULT_WAKE_ON_START,
        CONF_POLLING_POLICY: DEFAULT_POLLING_POLICY,
        CONF_ENABLE_TESLAMATE: DEFAULT_ENABLE_TESLAMATE,
    }


async def test_option_flow_input_floor(hass):
    """Test config flow options."""
    entry = MockConfigEntry(domain=DOMAIN, data={}, options=None)
    entry.add_to_hass(hass)

    result = await hass.config_entries.options.async_init(entry.entry_id)

    assert result["type"] == "form"
    assert result["step_id"] == "init"

    result = await hass.config_entries.options.async_configure(
        result["flow_id"], user_input={CONF_SCAN_INTERVAL: 1}
    )
    assert result["type"] == "create_entry"
    assert result["data"] == {
        CONF_SCAN_INTERVAL: MIN_SCAN_INTERVAL,
        CONF_WAKE_ON_START: DEFAULT_WAKE_ON_START,
        CONF_POLLING_POLICY: DEFAULT_POLLING_POLICY,
        CONF_ENABLE_TESLAMATE: DEFAULT_ENABLE_TESLAMATE,
    }
