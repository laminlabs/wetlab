"""Basic wetlab entities [`source <https://github.com/laminlabs/wetlab/blob/main/wetlab/models.py>`__].

Install and mount `wetlab` in a new instance:

>>> pip install wetlab
>>> lamin init --storage ./test-wetlab --schema bionty,wetlab

Import the package:

>>> import wetlab as wl

Create records:

>>> compound_treatment = wl.CompoundTreatment(
...    name="Aspirin treatment day 1",
... ).save()

Registries:

.. autosummary::
   :toctree: .

   Experiment
   Biosample
   Techsample
   CombinationTreatment
   CompoundTreatment
   EnvironmentalTreatment
   GeneticTreatment
   TreatmentTarget
   Well
   GeneticTreatmentSystem

"""

__version__ = "0.36.0"

from lamindb_setup import _check_instance_setup


def __getattr__(name):
    if name != "models":
        _check_instance_setup(from_module="wetlab")
    return globals()[name]


if _check_instance_setup():
    import lamindb

    del __getattr__  # delete so that imports work out
    from .models import (
        Biosample,
        CombinationTreatment,
        Compound,
        CompoundTreatment,
        EnvironmentalTreatment,
        Experiment,
        GeneticTreatment,
        Techsample,
        TreatmentTarget,
        Well,
    )
    from .types import GeneticTreatmentSystem
