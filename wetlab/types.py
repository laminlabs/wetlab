from typing import Literal

GeneticPerturbationSystem = Literal[
    "control",
    "CRISPR-Cas9",
    "CRISPR-Cas13",
    "CRISPRi",
    "CRISPRa",
    "overexpression",
    "mutant overexpression",
    "shRNA",
    "siRNA",
    "transgene",
    "transient-transfection",
]

BiologicType = Literal[
    "control",
    "protein",
    "peptide",
    "antibody",
    "enzyme",
    "growth-factor",
    "cytokine",
    "hormone",
    "vaccine",
    "oligonucleotide",
    "co-culture",
    "ligand",
]
