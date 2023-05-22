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

Development tools:

.. autosummary::
   :toctree: .

   dev
   link

"""

_schema_id = "tvhn"
_name = "lamin1"
_migration = "93875ac1d3a4"
__version__ = "0.16.2"

# prints warning of python versions
from lamin_logger import py_version_warning

py_version_warning("3.8", "3.10")


from . import dev, link
from ._core import Biosample, Experiment, ExperimentType, Techsample, Treatment  # noqa
