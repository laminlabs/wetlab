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

Development tools:

.. autosummary::
   :toctree: .

   dev
   link

"""

_schema_id = "tvhn"
_name = "lamin1"
_migration = None
__version__ = "0.15.1"

# prints warning of python versions
from lamin_logger import py_version_warning

py_version_warning("3.8", "3.10")


from . import dev, link
from ._core import Biosample, Experiment, ExperimentType, Techsample  # noqa
