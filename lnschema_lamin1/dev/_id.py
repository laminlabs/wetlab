import lnschema_core


def donor() -> str:
    """Donor: 4 base62."""
    return lnschema_core.dev.id.base62(n_char=4)
