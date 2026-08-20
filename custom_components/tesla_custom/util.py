"""Utilities for tesla."""

import ssl

from homeassistant.util.ssl import get_default_context


def create_tesla_ssl_context() -> ssl.SSLContext:
    """Return a fresh SSL context capped at TLS 1.2 for each caller.

    A module-level shared context would be mutated by every async_setup_entry
    call, causing the last loaded CA certificate to overwrite all earlier
    entries. Using a factory ensures each account gets its own isolated
    context object.
    """
    # get_default_context() retourne un nouveau contexte à chaque appel,
    # ce qui respecte la logique d'isolation voulue par l'intégration.
    ctx = get_default_context()
    ctx.maximum_version = ssl.TLSVersion.TLSv1_2
    return ctx
