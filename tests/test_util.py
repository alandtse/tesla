"""Tests for Tesla utility helpers."""

import ssl
from unittest.mock import MagicMock, patch

from teslajsonpy.const import API_URL, AUTH_DOMAIN

from custom_components.tesla_custom import util


def test_create_tesla_auth_ssl_context_requires_tls13() -> None:
    """Tesla auth SSL context uses certificate verification and TLS 1.3."""
    context = util.create_tesla_auth_ssl_context()

    assert context.verify_mode == ssl.CERT_REQUIRED
    assert context.check_hostname is True
    assert context.minimum_version == ssl.TLSVersion.TLSv1_3
    assert context.maximum_version == ssl.TLSVersion.TLSv1_3


def test_create_tesla_httpx_client_mounts_auth_transport_only() -> None:
    """Tesla auth gets the TLS 1.3 transport; Owner API uses the default."""
    auth_ssl_context = MagicMock(spec=ssl.SSLContext)
    auth_transport = MagicMock()

    with (
        patch.object(
            util.httpx, "AsyncHTTPTransport", return_value=auth_transport
        ) as transport_cls,
        patch.object(util.httpx, "AsyncClient") as client_cls,
    ):
        client = util.create_tesla_httpx_client(auth_ssl_context)

    assert client is client_cls.return_value
    transport_cls.assert_called_once_with(verify=auth_ssl_context)

    client_cls.assert_called_once()
    kwargs = client_cls.call_args.kwargs
    assert kwargs["headers"] == {util.USER_AGENT: util.SERVER_SOFTWARE}
    assert kwargs["timeout"] == 60
    assert kwargs["verify"] is util.SSL_CONTEXT
    assert kwargs["mounts"] == {AUTH_DOMAIN: auth_transport}
    assert API_URL not in kwargs["mounts"]
