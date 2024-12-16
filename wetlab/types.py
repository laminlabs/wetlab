from typing import Literal

GeneticPerturbationSystem = Literal[
    "CRISPR-Cas9",
    "CRISPRi",
    "CRISPRa",
    "shRNA",
    "siRNA",
    "transgene",
    "transient-transfection",
]

BiologicType = Literal[
    "protein",
    "peptide",
    "antibody",
    "enzyme",
    "growth-factor",
    "cytokine",
    "hormone",
    "vaccine",
    "oligonucleotide",
]
