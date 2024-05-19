"""Lamin's default `wetlab` lab schema.

Import the package::

   import wetlab as wl

Registries:

.. autosummary::
   :toctree: .

   Experiment
   ExperimentType
   Biosample
   Techsample
   Treatment
   TreatmentTarget
   Well

"""

__version__ = "0.29.0"

from lamindb_setup import _check_instance_setup


# trigger instance loading if users
# want to access attributes
def __getattr__(name):
    if name not in {"models"}:
        _check_instance_setup(from_lamindb=True)
    return globals()[name]


if _check_instance_setup():
    del __getattr__  # delete so that imports work out
    from .models import (  # noqa
        Biosample,
        Experiment,
        ExperimentType,
        Techsample,
        Treatment,
        TreatmentTarget,
        Well,
    )
