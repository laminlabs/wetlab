"""Basic wetlab entities [`source <https://github.com/laminlabs/wetlab/blob/main/wetlab/models.py>`__].

Install and mount `wetlab` in a new instance:

>>> pip install wetlab
>>> lamin init --storage ./test-wetlab --schema bionty,wetlab

Import the package:

>>> import wetlab as wl

Create records:

>>> compound_perturbation = wl.CompoundPerturbation(
...    name="Aspirin treatment day 1",
... ).save()

Registries:

.. autosummary::
   :toctree: .

   Experiment
   Biosample
   Techsample
   Well
   Donor
   CombinationPerturbation
   CompoundPerturbation
   EnvironmentalPerturbation
   GeneticPerturbation
   PerturbationTarget
   GeneticPerturbationSystem

"""

__version__ = "0.37.0"

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
        CombinationPerturbation,
        Compound,
        CompoundPerturbation,
        Donor,
        EnvironmentalPerturbation,
        Experiment,
        GeneticPerturbation,
        PerturbationTarget,
        Techsample,
        Well,
    )
    from .types import GeneticPerturbationSystem

    # backwards compatibility
    CombinationTreatment = CombinationPerturbation
    CompoundTreatment = CompoundPerturbation
    EnvironmentalTreatment = EnvironmentalPerturbation
    GeneticTreatment = GeneticPerturbation
    GeneticTreatmentSystem = GeneticPerturbationSystem
    TreatmentTarget = PerturbationTarget
