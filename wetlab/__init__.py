"""Basic wetlab entities [`source <https://github.com/laminlabs/wetlab/blob/main/wetlab/models.py>`__].

Install and mount `wetlab` in a new instance:

>>> pip install wetlab
>>> lamin init --storage ./test-wetlab --modules bionty,wetlab

Import the package:

>>> import wetlab as wl

Create records:

>>> biosample = wl.Biosample(name="Sample 1").save()

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

__version__ = "1.3.1"

from lamindb_setup import _check_instance_setup

from .types import BiologicType, GeneticPerturbationSystem


def __getattr__(name):
    if name != "models":
        _check_instance_setup(from_module="wetlab")
    return globals()[name]


if _check_instance_setup():
    del __getattr__  # delete so that imports work out
    from lamindb.curators import PertAnnDataCatManager as PertCurator

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
