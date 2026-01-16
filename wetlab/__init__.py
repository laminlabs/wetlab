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

from lamin_utils import logger
from pertdb import *  # noqa:F403

logger.warning(
    "please `import pertdb` instead of `import wetlab`. The wetlab module was renamed. Everything else stays the same."
)
