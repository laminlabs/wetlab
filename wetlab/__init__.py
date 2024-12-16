"""Basic wetlab entities [`source <https://github.com/laminlabs/wetlab/blob/main/wetlab/models.py>`__].

Install and mount `wetlab` in a new instance:

>>> pip install wetlab
>>> lamin init --storage ./test-wetlab --schema bionty,wetlab

Import the package:

>>> import wetlab as wl

Create records:

>>> biosample = wl.Biosample(
...    name="Sample 1",
... ).save()

Basic registries:

.. autosummary::
   :toctree: .

   Experiment
   Biosample
   Techsample
   Donor

Perturbation registries:

.. autosummary::
   :toctree: .

   GeneticPerturbation
   Biologic
   Compound
   CompoundPerturbation
   EnvironmentalPerturbation
   CombinationPerturbation

Auxiliary registries:

.. autosummary::
   :toctree: .

   Well
   PerturbationTarget

Types:

.. autosummary::
   :toctree: .

   GeneticPerturbationSystem
   BiologicType

"""

__version__ = "0.39.1"

from lamindb_setup import _check_instance_setup


def __getattr__(name):
    if name != "models":
        _check_instance_setup(from_module="wetlab")
    return globals()[name]


if _check_instance_setup():
    import lamindb

    del __getattr__  # delete so that imports work out
    from .models import (
        Biologic,
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
    from .types import BiologicType, GeneticPerturbationSystem

    # backwards compatibility
    CombinationTreatment = CombinationPerturbation
    CompoundTreatment = CompoundPerturbation
    EnvironmentalTreatment = EnvironmentalPerturbation
    GeneticTreatment = GeneticPerturbation
    GeneticTreatmentSystem = GeneticPerturbationSystem
    TreatmentTarget = PerturbationTarget
