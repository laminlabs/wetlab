"""Lamin's `lamin1` lab schema (`tvhn`).

Import the package::

   import lnschema_lamin1

Examples of derived classes, typically configured:

.. autosummary::
   :toctree: .

   Experiment
   ExperimentType
   Biosample
   Techsample
   Treatment
   Well

Development tools:

.. autosummary::
   :toctree: .

   dev
   link

"""

_schema_id = "tvhn"
_name = "lamin1"
__version__ = "0.18a1"

from . import dev, link
from ._core import (  # noqa
    Biosample,
    Experiment,
    ExperimentType,
    Techsample,
    Treatment,
    Well,
)
