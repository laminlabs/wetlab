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

__version__ = "1.5a1"

from lamindb_setup import _check_instance_setup

from .types import BiologicType, GeneticPerturbationSystem

_check_instance_setup(from_module="wetlab")


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

__all__ = [
    # registries
    "Biologic",
    "Biosample",
    "CombinationPerturbation",
    "Compound",
    "CompoundPerturbation",
    "Donor",
    "EnvironmentalPerturbation",
    "Experiment",
    "GeneticPerturbation",
    "PerturbationTarget",
    "Techsample",
    "Well",
    # helper types
    "BiologicType",
    "GeneticPerturbationSystem",
]
