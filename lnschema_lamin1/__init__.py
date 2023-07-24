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
   PlateWell

"""

_schema_id = "tvhn"
_name = "lamin1"
__version__ = "0.22a2"

from lamindb_setup import _check_instance_setup

if _check_instance_setup():
    from .models import (  # noqa
        Biosample,
        Experiment,
        ExperimentType,
        PlateWell,
        Techsample,
        Treatment,
        TreatmentTarget,
    )
