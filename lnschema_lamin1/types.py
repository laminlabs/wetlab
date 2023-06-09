"""Custom types.

.. autosummary::
   :toctree: .

    treatment_type
    treatment_system
"""
from enum import Enum


class treatment_type(str, Enum):
    genetic = "genetic"
    chemical = "chemical"


class treatment_system(str, Enum):
    CRISPR_Cas9 = "CRISPR Cas9"
    CRISPRi = "CRISPRi"
    CRISPRa = "CRISPRa"
    shRNA = "shRNA"
    siRNA = "siRNA"
    transgene = "transgene"
    transient_transfection = "transient transfection"
