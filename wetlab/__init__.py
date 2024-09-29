"""Registries for wetlab entities.

See the `source code
<https://github.com/laminlabs/wetlab/blob/main/wetlab/models.py>`__.

>>> pip install wetlab
>>> lamin init --storage ./test-wetlab --schema bionty,wetlab

Import wetlab:

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

"""

__version__ = "0.34.0"

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
