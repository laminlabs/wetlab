"""Basic wetlab entities [`source <https://github.com/laminlabs/wetlab/blob/main/wetlab/models.py>`__].

Install and mount `wetlab` in a new instance:

>>> pip install wetlab
>>> lamin init --storage ./test-wetlab --modules bionty,wetlab

Import the package:

>>> import wetlab as wl

Create records:

>>> biologic = wl.Biologic(name="IFNG").save()

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

   PerturbationTarget

Types:

.. autosummary::
   :toctree: .

   GeneticPerturbationSystem
   BiologicType

"""

__version__ = "2.0.0"

from lamindb_setup import _check_instance_setup

from .types import BiologicType, GeneticPerturbationSystem

_check_instance_setup(from_module="wetlab")


from .models import (
    Biologic,
    CombinationPerturbation,
    Compound,
    CompoundPerturbation,
    EnvironmentalPerturbation,
    GeneticPerturbation,
    PerturbationTarget,
)

__all__ = [
    # registries
    "Biologic",
    "CombinationPerturbation",
    "Compound",
    "CompoundPerturbation",
    "EnvironmentalPerturbation",
    "GeneticPerturbation",
    "PerturbationTarget",
    # helper types
    "BiologicType",
    "GeneticPerturbationSystem",
]
