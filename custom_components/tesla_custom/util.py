"""Utilities for tesla."""

import ssl

from homeassistant.helpers.httpx_client import SERVER_SOFTWARE, USER_AGENT
import httpx
from teslajsonpy.const import AUTH_DOMAIN

try:
    # Home Assistant 2023.4.x+
    from homeassistant.util.ssl import get_default_context

    SSL_CONTEXT = get_default_context()
except ImportError:
    from homeassistant.util.ssl import client_context

    SSL_CONTEXT = client_context()


def create_tesla_auth_ssl_context() -> ssl.SSLContext:
    """Create a TLS 1.3-only SSL context for Tesla auth requests."""
    context = ssl.create_default_context()
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    context.maximum_version = ssl.TLSVersion.TLSv1_3
    return context


def create_tesla_httpx_client(
    auth_ssl_context: ssl.SSLContext,
) -> httpx.AsyncClient:
    """Create a Tesla HTTP client with TLS 1.3 pinned to Tesla auth."""
    return httpx.AsyncClient(
        headers={USER_AGENT: SERVER_SOFTWARE},
        timeout=60,
        verify=SSL_CONTEXT,
        mounts={
            AUTH_DOMAIN: httpx.AsyncHTTPTransport(verify=auth_ssl_context),
        },
    )
