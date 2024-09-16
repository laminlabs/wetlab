"""Registries for wetlab related entities.

Generally, the wetlab schema is designed to model experimental covariates and perturbations including their targets.

This default wetlab schema module mostly serves to exemplify `how you define
costum registries on GitHub <https://github.com/laminlabs/wetlab/blob/main/wetlab/models.py>`__.

Most professional users create their custom schemas to map their operations or
leverage schema synching from Benchling. If you need help with this, please `reach out <https://lamin.ai/contact>`__!

>>> pip install wetlab

>>> lamin init --storage ./test-wetlab --schema bionty,wetlab

Import wetlab:

>>> import wetlab as wl

Create records:

>>> aspirin_treatment = compound_treatment = wl.CompoundTreatment(
...    name="Aspirin 325 MG Enteric Coated Tablet",
...    ontology_id="00076148",
...    pubchem_id=2244
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

__version__ = "0.31.1"

from lamindb_setup import _check_instance_setup


# trigger instance loading if users
# want to access attributes
def __getattr__(name):
    if name not in {"models"}:
        _check_instance_setup(from_lamindb=True)
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
