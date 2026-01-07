from __future__ import annotations

from datetime import timedelta  # noqa
from typing import overload

try:
    from rdkit import Chem, rdBase
    from rdkit.Chem import Descriptors
    from rdkit.Chem.MolStandardize import rdMolStandardize
    from rdkit.Chem.rdMolDescriptors import CalcMolFormula

    rdBase.DisableLog("rdApp.info")
    rdBase.DisableLog("rdApp.warning")
    RDKIT_AVAILABLE = True
except ImportError:
    RDKIT_AVAILABLE = False

from bionty import uids as bionty_ids
from bionty.models import (
    BioRecord,
    Gene,
    HasOntologyId,
    Pathway,
    Protein,
    Source,
)
from django.db import models
from django.db.models import CASCADE, PROTECT, QuerySet
from lamin_utils import logger
from lamindb.base import ids
from lamindb.base.fields import (
    CharField,
    DurationField,
    FloatField,
    ForeignKey,
    TextField,
)
from lamindb.models import (
    Artifact,
    BaseSQLRecord,
    CanCurate,
    Feature,
    IsLink,
    SQLRecord,
    TracksRun,
    TracksUpdates,
)

from .types import BiologicType, GeneticPerturbationSystem  # noqa


class Compound(BioRecord, HasOntologyId, TracksRun, TracksUpdates):
    """Models a (chemical) compound such as a drug.

    Example::

        import wetlab as wl

        compound = wl.Compound(
            name="Navitoclax",
            ontology_id="CHEMBL443684",
            smiles="[H][C@@](CCN1CCOCC1)(CSC1=CC=CC=C1)NC1=C(C=C(C=C1)S(=O)(=O)NC(=O)C1=CC=C(C=C1)N1CCN(CC2=C(CCC(C)(C)C2)C2=CC=C(Cl)C=C2)CC1)S(=O)(=O)C(F)(F)F"
        ).save()
    """

    class Meta(BioRecord.Meta, HasOntologyId.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False
        app_label = "wetlab"

    id: int = models.BigAutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: str = CharField(
        unique=True, max_length=14, db_index=True, default=bionty_ids.ontology
    )
    """A universal id (hash of selected field)."""
    name: str = TextField(db_index=True)
    """Name of the compound."""
    type: str | None = CharField(max_length=32, db_index=True, null=True)
    """Type of the compound."""
    chembl_id: str | None = CharField(null=True, max_length=32, db_index=True)
    """Chembl ontology ID of the compound"""
    smiles: str | None = TextField(null=True, db_index=True)
    """Raw SMILES string as provided by user."""
    canonical_smiles: str | None = TextField(null=True, db_index=True)
    """Normalized and standardized canonical SMILES string."""
    inchikey: str | None = TextField(null=True, db_index=True)
    """InChIKey of the compound from the canonical SMILES."""
    molweight: float | None = FloatField(null=True, default=None, db_index=True)
    """MolWeight of the compound from the canonical SMILES."""
    molformula: str | None = TextField(null=True, db_index=True)
    """MolFormula of the compound from the canonical SMILES."""
    moa: str | None = TextField(null=True, db_index=True)
    """Mechanism of action of the compound."""
    targets: PerturbationTarget = models.ManyToManyField(
        "PerturbationTarget", related_name="compounds"
    )
    """Targets of the compound."""
    artifacts: Artifact = models.ManyToManyField(
        Artifact, through="ArtifactCompound", related_name="compounds"
    )
    """Artifacts linked to the compound."""

    @overload
    def __init__(
        self,
        name: str,
        ontology_id: str | None,
        abbr: str | None,
        synonyms: str | None,
        description: str | None,
        chembl_id: str | None,
        smiles: str | None,
        canonical_smiles: str | None,
        inchikey: str | None,
        molweight: float | None,
        molformula: str | None,
        parents: list[Compound],
        source: Source | None,
    ): ...

    @overload
    def __init__(
        self,
        *db_args,
    ): ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        smiles = kwargs.get("smiles")
        super().__init__(*args, **kwargs)
        if smiles and self._state.adding:  # Only process for new instances
            self._process_smiles(smiles)

    def _process_smiles(self, smiles_string: str) -> None:
        """Process and normalize SMILES string.

        Args:
            smiles_string: Raw SMILES string to process
        """
        if not RDKIT_AVAILABLE:
            raise ImportError(
                "RDKit is not available. Please install: pip install rdkit"
            )
        try:
            # Store the original SMILES
            self.smiles = smiles_string
            # Normalize and store canonical SMILES
            self.canonical_smiles = Compound.standardize_smiles(smiles_string)
            self.inchikey = Chem.MolToInchiKey(
                Chem.MolFromSmiles(self.canonical_smiles)
            )
            self.molweight = Descriptors.MolWt(
                Chem.MolFromSmiles(self.canonical_smiles)
            )
            self.molformula = CalcMolFormula(Chem.MolFromSmiles(self.canonical_smiles))

        except ValueError as e:
            self.smiles = smiles_string
            self.canonical_smiles = None
            self.inchikey = None
            self.molweight = None
            self.molformula = None
            logger.warning(
                f"could not normalize SMILES for compound '{self.name}': {str(e)}"
            )

    def save(self, *args, **kwargs):
        """Override save to ensure SMILES processing happens before database save."""
        # If SMILES was set but not processed yet, process it now
        if self.smiles and not self.canonical_smiles:
            self._process_smiles(self.smiles)

        super().save(*args, **kwargs)

    def update_smiles(self, new_smiles: str) -> None:
        """Update the SMILES string and reprocess normalization.

        Args:
            new_smiles: New SMILES string to set
        """
        self._process_smiles(new_smiles)
        self.save()

    @staticmethod
    def standardize_smiles(smiles: str) -> str | None:
        """Generates a standardized, canonical SMILES string from an input SMILES.

        This function follows the best-practice standardization workflow recommended by
        Greg Landrum, the creator of RDKit. The steps are:
        1. Parse the SMILES string.
        2. Use rdMolStandardize.Cleanup() to apply a series of standard cleanups
        (e.g., remove Hs, disconnect metal atoms, normalize, reionize).
        3. Use rdMolStandardize.FragmentParent() to select the largest covalent
        fragment, effectively removing salts and solvents.
        4. Use rdMolStandardize.Uncharger() to neutralize the molecule.
        5. Use rdMolStandardize.TautomerEnumerator().Canonicalize() to generate the
        canonical tautomer.
        6. Convert the final molecule object back to a canonical SMILES string.

        Args:
            smiles: The input SMILES string to standardize.

        Returns:
            The canonical, standardized SMILES string, or None if the input
            SMILES is invalid.
        """
        # Step 1: Parse SMILES
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise ValueError(f"Could not parse SMILES: {smiles}")

        # Step 2: General cleanup
        # removeHs, disconnect metal atoms, normalize the molecule, reionize the molecule
        clean_mol = rdMolStandardize.Cleanup(mol)

        # Step 3: Get the parent fragment
        parent_mol = rdMolStandardize.FragmentParent(clean_mol)

        # Step 4: Neutralize
        # Note: The Uncharger class must be instantiated.
        uncharger = rdMolStandardize.Uncharger()
        uncharged_mol = uncharger.uncharge(parent_mol)

        # Step 5: Generate canonical tautomer
        # Note: The TautomerEnumerator class must be instantiated.
        te = rdMolStandardize.TautomerEnumerator()
        canonical_tautomer = te.Canonicalize(uncharged_mol)

        # Step 6: Convert back to canonical SMILES string for output
        canonical_smiles = Chem.MolToSmiles(canonical_tautomer, canonical=True)

        return canonical_smiles


class ArtifactCompound(BaseSQLRecord, IsLink, TracksRun):
    class Meta:
        app_label = "wetlab"

    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = ForeignKey(Artifact, CASCADE, related_name="links_compound")
    compound: Compound = ForeignKey(Compound, PROTECT, related_name="links_artifact")
    feature: Feature = ForeignKey(
        Feature, PROTECT, null=True, default=None, related_name="links_artifactcompound"
    )


class PerturbationTarget(BioRecord, TracksRun, TracksUpdates):
    """Models perturbation targets such as :class:`~bionty.Gene`, :class:`~bionty.Pathway`, and :class:`~bionty.Protein`.

    Example::

        import bionty as bt
        import wetlab as wl

        gene_1 = bt.Gene.from_source(ensembl_gene_id="ENSG00000000003").save()
        gene_2 = bt.Gene.from_source(ensembl_gene_id="ENSG00000000005").save()
        targets = wl.PerturbationTarget(name="TSPAN6_TNMD").save()
        targets.genes.set([gene_1, gene_2])
    """

    class Meta(BioRecord.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False
        app_label = "wetlab"

    uid: str = CharField(unique=True, max_length=8, default=ids.base62_8, db_index=True)
    """Universal id, valid across DB instances."""
    name: str = CharField(db_index=True)
    """Name of the perturbation target."""
    genes: Gene = models.ManyToManyField(
        "bionty.Gene", related_name="perturbation_targets"
    )
    """Genes of the perturbation target, link to :class:`~bionty.Gene` records."""
    pathways: Pathway = models.ManyToManyField(
        "bionty.Pathway", related_name="perturbation_targets"
    )
    """Pathways of the perturbation target, link to :class:`bionty.Pathway` records."""
    proteins: Protein = models.ManyToManyField(
        "bionty.Protein", related_name="perturbation_targets"
    )
    """Proteins of the perturbation target, link to :class:`bionty.Protein` records."""
    artifacts: Artifact = models.ManyToManyField(
        Artifact,
        through="ArtifactperturbationTarget",
        related_name="perturbation_targets",
    )
    """Artifacts linked to the perturbation target."""


class ArtifactPerturbationTarget(BaseSQLRecord, IsLink, TracksRun):
    class Meta:
        app_label = "wetlab"
        indexes = [
            models.Index(fields=["artifact", "perturbationtarget"]),
        ]

    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = ForeignKey(
        Artifact, CASCADE, related_name="links_perturbation_target"
    )
    perturbationtarget: PerturbationTarget = ForeignKey(
        PerturbationTarget, PROTECT, related_name="links_artifact"
    )
    feature: Feature = ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="links_artifactperturbationtarget",
    )


class GeneticPerturbation(BioRecord, TracksRun, TracksUpdates):
    """Models genetic perturbations such as CRISPR.

    Args:
        name: The name of the genetic perturbation.
        system: The :class:`~wetlab.GeneticPerturbationSystem` used to apply the genetic perturbation.
                Must be one of 'CRISPR Cas9', 'CRISPRi', 'CRISPRa', 'shRNA', 'siRNA', 'transgene', 'transient transfection'.
        on_target_score: The on-target score, indicating the likelihood of the guide RNA successfully targeting the intended DNA sequence.
        off_target_score: The off-target score, indicating the likelihood of the guide RNA targeting unintended DNA sequences.

    Example::

        import wetlab as wl

        sicke_cell_perturbation = wl.GeneticPerturbation(
            system="CRISPR Cas9",
            name="Hemoglobin Sickle Cell Perturbation",
            sequence="AGCTGACCGTGA",
            on_target_score=85,
            off_target_score=15
        ).save()
    """

    class Meta(BioRecord.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False
        app_label = "wetlab"

    uid: str = CharField(
        unique=True, max_length=12, default=ids.base62_12, db_index=True
    )
    """Universal id, valid across DB instances."""
    name: str = CharField(db_index=True)
    """Name of the Genetic perturbation."""
    type: GeneticPerturbationSystem = models.CharField(
        max_length=32,
        db_index=True,
        null=True,
    )
    """:class:`~wetlab.GeneticPerturbationSystem` used for the genetic perturbation."""
    sequence: str | None = models.TextField(null=True, db_index=True)
    """Sequence of the perturbation."""
    on_target_score: float | None = FloatField(null=True, default=None, db_index=True)
    """On-target score, indicating the likelihood of the guide RNA successfully targeting the intended DNA sequence."""
    off_target_score: float | None = FloatField(null=True, default=None, db_index=True)
    """The off-target score, indicating the likelihood of the guide RNA targeting unintended DNA sequences.."""
    targets: PerturbationTarget = models.ManyToManyField(
        PerturbationTarget, related_name="genetic_perturbations"
    )
    """Targets of the perturbation."""
    artifacts: Artifact = models.ManyToManyField(
        Artifact,
        through="ArtifactGeneticPerturbation",
        related_name="genetic_perturbations",
    )
    """Artifacts linked to the perturbation."""


class ArtifactGeneticPerturbation(BaseSQLRecord, IsLink, TracksRun):
    class Meta:
        app_label = "wetlab"
        # see https://laminlabs.slack.com/archives/C03P6D8U1PC/p1761756966506899
        indexes = [
            models.Index(fields=["artifact", "geneticperturbation"]),
        ]

    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = ForeignKey(
        Artifact, CASCADE, related_name="links_genetic_perturbation"
    )
    geneticperturbation: GeneticPerturbation = ForeignKey(
        GeneticPerturbation, PROTECT, related_name="links_artifact"
    )
    feature: Feature = ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="links_artifactgeneticperturbation",
    )


class Biologic(BioRecord, TracksRun, TracksUpdates):
    """Proteins, peptides, antibodies, enzymes, growth factors, etc.

    Example::

        import wetlab as wl

        biologic = wl.Biologic(
            name="IFNG",
            type="cytokine",
        ).save()
    """

    class Meta(BioRecord.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False
        app_label = "wetlab"

    _name_field: str = "name"

    uid: str = CharField(
        unique=True, max_length=12, default=ids.base62_12, db_index=True
    )
    """A universal id (hash of selected field)."""
    name: str = CharField(db_index=True)
    """Name of the compound."""
    type: BiologicType = CharField(max_length=32, db_index=True)
    """The type."""
    proteins: Protein = models.ManyToManyField(
        "bionty.Protein", related_name="biologics"
    )
    """Proteins associated with this biologic."""
    targets: PerturbationTarget = models.ManyToManyField(
        PerturbationTarget, related_name="biologics"
    )
    """Targets of the perturbation."""
    artifacts: Artifact = models.ManyToManyField(
        Artifact, through="ArtifactBiologic", related_name="biologics"
    )
    """Artifacts linked to the compound."""

    @overload
    def __init__(
        self,
        name: str,
        abbr: str | None,
        synonyms: str | None,
        description: str | None,
    ): ...

    @overload
    def __init__(
        self,
        *db_args,
    ): ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)


class ArtifactBiologic(BaseSQLRecord, IsLink, TracksRun):
    class Meta:
        app_label = "wetlab"

    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = ForeignKey(Artifact, CASCADE, related_name="links_biologic")
    biologic: Biologic = ForeignKey(Biologic, PROTECT, related_name="links_artifact")
    feature: Feature = ForeignKey(
        Feature, PROTECT, null=True, default=None, related_name="links_artifactbiologic"
    )


class CompoundPerturbation(SQLRecord, CanCurate, TracksRun, TracksUpdates):
    """Models compound perturbations such as drugs.

    Args:
        name: The name of the compound perturbation.

    Example::

        import wetlab as wl

        aspirin_perturbation = compound_perturbation = wl.CompoundPerturbation(
            name="Antibiotic cocktail",
        ).save()
    """

    class Meta(SQLRecord.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False
        app_label = "wetlab"

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: str = CharField(
        unique=True, max_length=12, default=ids.base62_12, db_index=True
    )
    """Universal id, valid across DB instances."""
    name: str = CharField(db_index=True)
    """Name of the compound perturbation."""
    description: str | None = TextField(null=True, db_index=True)
    """Description of the compound perturbation."""
    concentration: float = FloatField(null=True, default=None)
    """Concentration of the compound."""
    concentration_unit: str = CharField(max_length=32, null=True)
    """Unit of the concentration."""
    duration: timedelta | None = DurationField(null=True, default=None)
    """Duration of the compound perturbation."""
    compound: Compound | None = ForeignKey("Compound", PROTECT, null=True, default=None)
    """Compounds linked to the perturbation."""
    artifacts: Artifact = models.ManyToManyField(
        Artifact,
        through="ArtifactCompoundPerturbation",
        related_name="compound_perturbations",
    )
    """Artifacts linked to the perturbation."""


class ArtifactCompoundPerturbation(BaseSQLRecord, IsLink, TracksRun):
    class Meta:
        app_label = "wetlab"

    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = ForeignKey(
        Artifact, CASCADE, related_name="links_compound_perturbation"
    )
    compoundperturbation: CompoundPerturbation = ForeignKey(
        CompoundPerturbation, PROTECT, related_name="links_artifact"
    )
    feature: Feature = ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="links_artifactcompoundperturbation",
    )


class EnvironmentalPerturbation(BioRecord, TracksRun, TracksUpdates):
    """Models environmental perturbations such as heat, acid, or smoke perturbations.

    Args:
        name: Name of the environmental perturbation.
        ontology_id: Ontology ID of the environmental perturbation (EFO).
        value: A value such as a temperature.
        unit: A unit such as 'degrees celsius'.
        duration: Time duration of how long the perturbation was applied.

    Example::

        import wetlab as wl

        acid_perturbation = EnvironmentalPerturbation(
            name='Acid perturbation',
            ontology_id='EFO:0004416',
            value=1.5,
            unit='pH',
        ).save()
    """

    class Meta(BioRecord.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False
        app_label = "wetlab"

    uid: str = CharField(
        unique=True, max_length=12, default=ids.base62_12, db_index=True
    )
    """Universal id, valid across DB instances."""
    name: str = CharField(db_index=True)
    """Name of the environmental perturbation."""
    ontology_id = CharField(max_length=32, db_index=True, null=True)
    """Ontology ID (EFO) of the environmental perturbation."""
    value: float | None = FloatField(null=True, default=None)
    """The value of the environmental perturbation such as a temperature."""
    unit: str | None = CharField(max_length=32, null=True)
    """Unit of the value such as 'degrees celsius'"""
    duration: timedelta | None = DurationField(null=True, default=None)
    """Duration of the environmental perturbation."""
    targets: PerturbationTarget = models.ManyToManyField(
        PerturbationTarget, related_name="environmental_perturbations"
    )
    """Targets of the environmental perturbation."""
    artifacts: Artifact = models.ManyToManyField(
        Artifact,
        through="ArtifactEnvironmentalperturbation",
        related_name="environmental_perturbations",
    )
    """Artifacts linked to the perturbation."""


class ArtifactEnvironmentalPerturbation(BaseSQLRecord, IsLink, TracksRun):
    class Meta:
        app_label = "wetlab"

    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = ForeignKey(
        Artifact, CASCADE, related_name="links_environmental_perturbation"
    )
    environmentalperturbation: EnvironmentalPerturbation = ForeignKey(
        EnvironmentalPerturbation, PROTECT, related_name="links_artifact"
    )
    feature: Feature = ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="links_artifactenvironmentalperturbation",
    )


class CombinationPerturbation(BioRecord, TracksRun, TracksUpdates):
    """Combination of several perturbations.

    CombinationPerturbations model several perturbations jointly such as one or more :class:`wetlab.GeneticPerturbation`,
    :class:`wetlab.CompoundPerturbation`, and :class:`wetlab.EnvironmentalPerturbation` records.

    Args:
        name: A name of the CombinationPerturbation that summarizes all applied perturbations.
        description: A description of the CombinationPerturbation.
        ontology_id: An ontology ID of the CombinationPerturbation.

    Example::

        import wetlab as wl

        sc_perturbation = wl.GeneticPerturbation(
            system="CRISPR Cas9",
            name="Hemoglobin Sickle Cell perturbation",
            sequence="AGCTGACCGTGA",
        ).save()

        cftr_perturbation = wl.GeneticPerturbation(
            system="CRISPR Cas9",
            name="Cystic Fibrosis CFTR Correction",
            sequence="TTGGTGGTGAACT",
        ).save()

        aspirin_perturbation = compound_perturbation = wl.CompoundPerturbation(
            name="Aspirin",
            pubchem_id=2244
        ).save()

        comb_perturbation = wl.CombinationPerturbation(name="Hemoglobin Sickle Cell and CFTR Correction with Aspirin",
            description="Targets both sickle cell anemia and cystic fibrosis, using CRISPR Cas9 and Aspirin for anti-inflammatory support."
        ).save()
        comb_perturbation.genetics.set([sc_perturbation, cftr_perturbation])
        comb_perturbation.compounds.add(aspirin_perturbation)
    """

    class Meta(SQLRecord.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False
        app_label = "wetlab"

    uid: str = CharField(
        unique=True, max_length=12, default=ids.base62_12, db_index=True
    )
    """Universal id, valid across DB instances."""
    name: str | None = CharField(db_index=True)
    """Name of the perturbation."""
    genetic_perturbations: GeneticPerturbation = models.ManyToManyField(
        GeneticPerturbation, related_name="combination_perturbations"
    )
    """:class:`wetlab.GeneticPerturbation` perturbations."""
    compound_perturbations: CompoundPerturbation = models.ManyToManyField(
        CompoundPerturbation, related_name="combination_perturbations"
    )
    """:class:`wetlab.CompoundPerturbation` perturbations."""
    environmental_perturbations: EnvironmentalPerturbation = models.ManyToManyField(
        EnvironmentalPerturbation, related_name="combination_perturbations"
    )
    """:class:`wetlab.EnvironmentalPerturbation` perturbations."""
    artifacts: Artifact = models.ManyToManyField(
        Artifact,
        through="ArtifactCombinationperturbation",
        related_name="combination_perturbations",
    )
    """Artifacts linked to the perturbation."""

    @property
    def members(self) -> QuerySet:
        """Retrieve all related GeneticPerturbation, CompoundPerturbation, and EnvironmentalPerturbation instances."""
        if self._state.adding:
            return self.__class__.objects.none()

        return self.genetic.all().union(self.compound.all(), self.environmental.all())


class ArtifactCombinationPerturbation(BaseSQLRecord, IsLink, TracksRun):
    class Meta:
        app_label = "wetlab"

    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = ForeignKey(
        Artifact, CASCADE, related_name="links_combination_perturbation"
    )
    combinationperturbation: CombinationPerturbation = ForeignKey(
        CombinationPerturbation, PROTECT, related_name="links_artifact"
    )
    feature: Feature = ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="links_artifactcombinationperturbation",
    )
