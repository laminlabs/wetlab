"""Lamin's `lamin1` exemplary lab schema.

Import the package::

   import lnschema_lamin1

ORMs:

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

_schema_id = "tvhn"
_name = "lamin1"
__version__ = "0.24.0"

from lamindb_setup import _check_instance_setup


# trigger instance loading if users
# want to access attributes
def __getattr__(name):
    if name not in {"models"}:
        _check_instance_setup(from_lamindb=True)
    return globals()[name]


if _check_instance_setup():
    from .models import (  # noqa
        Biosample,
        Experiment,
        ExperimentType,
        Techsample,
        Treatment,
        TreatmentTarget,
        Well,
    )
