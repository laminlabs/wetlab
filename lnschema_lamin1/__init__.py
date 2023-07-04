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
__version__ = "0.20a3"

from lamindb_setup import _check_instance_setup

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
