"""Basic pertdb entities [`source <https://github.com/laminlabs/pertdb/blob/main/pertdb/models.py>`__].

Install and mount `pertdb` in a new instance:

>>> pip install pertdb
>>> lamin init --storage ./test-pertdb --modules bionty,pertdb

Import the package:

>>> import pertdb as wl

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

_check_instance_setup(from_module="pertdb")


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
