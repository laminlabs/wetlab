"""Default `wetlab` schema.

This default wetlab schema module mostly serves to exemplify `how you define
costum registries on GitHub <https://github.com/laminlabs/wetlab/blob/main/wetlab/models.py>`__.

Most professional users create their custom schemas to map their operations or
leverage schema synching from Benchling. If you need help with this, please
`reach out <https://lamin.ai/contact>`__!

Install the module::

   pip install wetlab

Create your instance mounting the module::

   lamin init --storage ./test-wetlab --schema bionty,wetlab

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
