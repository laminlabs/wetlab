from lnschema_core import dev


def biometa() -> str:
    """Biometa: 21 base62.

    Biometa consists of tuples of biosample, experiment, readout, featureset.

    There are about as many biometa rows as files.

    21 characters (62**21=4e+37 possibilities) outperform UUID (2*122=5e+36).
    """
    return dev.id.base62(n_char=21)


def biosample() -> str:
    """Bio sample: 20 base62."""
    return dev.id.base62(n_char=20)


def techsample() -> str:
    """Tech sample: 20 base62."""
    return dev.id.base62(n_char=20)


def readout() -> str:
    """Readout types: 5 base62.

    EFO ontology.
    """
    return dev.id.base62(n_char=5)


def experiment() -> str:
    """Experiments: 19 base62."""
    return dev.id.base62(n_char=19)


def experiment_type() -> str:
    """Experiments: 12 base62."""
    return dev.id.base62(n_char=12)


def treatment() -> str:
    """Projects: 12 base62."""
    return dev.id.base62(n_char=12)


def donor() -> str:
    """Donor: 4 base62."""
    return dev.id.base62(n_char=4)
