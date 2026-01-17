"""Registries for perturbations and their targets [`source <https://github.com/laminlabs/pertdb/blob/main/pertdb/models.py>`__].

Install and mount `pertdb` in a new instance::

    pip install pertdb
    lamin init --storage ./test-pertdb --modules bionty,pertdb

Import the package and create an object::

    import pertdb
    biologic = pertdb.Biologic(name="IFNG").save()

Main registries:

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

Helper types:

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
