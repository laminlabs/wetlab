from __future__ import annotations

from datetime import timedelta  # noqa
from typing import overload

from bionty import ids as bionty_ids
from bionty.models import (
    BioRecord,
    CellLine,
    CellType,
    Disease,
    Ethnicity,
    Gene,
    Organism,
    Pathway,
    Phenotype,
    Protein,
    Source,
    Tissue,
)
from django.db import models
from django.db.models import CASCADE, PROTECT, QuerySet
from lamindb.base import ids
from lamindb.base.fields import (
    BooleanField,
    CharField,
    DateField,
    DurationField,
    FloatField,
    ForeignKey,
    IntegerField,
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


class Compound(BioRecord, TracksRun, TracksUpdates):
    """Models a (chemical) compound such as a drug.

    Example::

        import wetlab as wl

        compound = wl.Compound(
            name="Navitoclax",
            ontology_id="CHEMBL443684"
        ).save()
    """

    class Meta(BioRecord.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    _name_field: str = "name"
    _ontology_id_field: str = "ontology_id"

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: str = CharField(unique=True, max_length=8, default=bionty_ids.ontology)
    """A universal id (hash of selected field)."""
    name: str = TextField(db_index=True)
    """Name of the compound."""
    ontology_id: str | None = CharField(
        max_length=32, db_index=True, null=True, default=None
    )
    """Ontology ID of the compound."""
    chembl_id: str | None = CharField(
        max_length=32, db_index=True, null=True, default=None
    )
    """Chembl ontology ID of the compound"""
    abbr: str | None = CharField(
        max_length=32, db_index=True, unique=True, null=True, default=None
    )
    """A unique abbreviation of compound."""
    synonyms: str | None = TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this compound."""
    description: str | None = TextField(null=True, default=None)
    """Description of the compound."""
    parents: Compound = models.ManyToManyField(
        "self", symmetrical=False, related_name="children"
    )
    """Parent compound records."""
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
        super().__init__(*args, **kwargs)


class ArtifactCompound(BaseSQLRecord, IsLink, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = ForeignKey(Artifact, CASCADE, related_name="links_compound")
    compound: Compound = ForeignKey(Compound, PROTECT, related_name="links_artifact")
    feature: Feature = ForeignKey(
        Feature, PROTECT, null=True, default=None, related_name="links_artifactcompound"
    )
    label_ref_is_name: bool | None = BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = BooleanField(null=True, default=None)


class Experiment(SQLRecord, CanCurate, TracksRun, TracksUpdates):
    """Models a wetlab experiment.

    Example::

        import wetlab as wl

        experiment = wl.Experiment(
            name="IPF mice vs control mice",
            description="Analysis of gene expression levels in different cell types of IPF.",
        ).save()
    """

    class Meta(SQLRecord.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: str = CharField(unique=True, max_length=8, default=ids.base62_8)
    """Universal id, valid across DB instances."""
    name: str | None = CharField(max_length=255, default=None, db_index=True)
    """Name of the experiment."""
    description: str | None = TextField(null=True, default=None)
    """Description of the experiment."""
    date: DateField | None = DateField(
        default=None, null=True, db_index=True, blank=True
    )
    """Date of the experiment."""
    artifacts: Artifact = models.ManyToManyField(
        Artifact, through="ArtifactExperiment", related_name="experiments"
    )
    """Artifacts linked to the experiment."""


class ArtifactExperiment(BaseSQLRecord, IsLink, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = ForeignKey(Artifact, CASCADE, related_name="links_experiment")
    experiment: Experiment = ForeignKey(
        Experiment, PROTECT, related_name="links_artifact"
    )
    feature: Feature = ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="links_artifactexperiment",
    )
    label_ref_is_name: bool | None = BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = BooleanField(null=True, default=None)


class Well(SQLRecord, CanCurate, TracksRun, TracksUpdates):
    """Models a well in a wetlab :class:`wetlab.Experiment` that is part of a microplate.

    Example::

        import wetlab as wl

        well = wl.Well(
            name="Well A1",
            row="A",
            column=1,
        ).save()
    """

    class Meta(SQLRecord.Meta, TracksRun.Meta, TracksUpdates.Meta):
        unique_together = (("row", "column"),)
        abstract = False

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: int = CharField(unique=True, max_length=4, default=ids.base62_4)
    """Universal id, valid across DB instances."""
    name: str | None = CharField(
        max_length=32, default=None, null=True, unique=True, db_index=True
    )
    """Name of the well."""
    row: str = CharField(max_length=4, default=None)
    """Horizontal position of the well in the microplate."""
    column: int = IntegerField()
    """Vertical position of the well in the microplate."""
    artifacts: Artifact = models.ManyToManyField(
        Artifact, through="ArtifactWell", related_name="wells"
    )
    """Artifacts linked to the well."""


class ArtifactWell(BaseSQLRecord, IsLink, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = ForeignKey(Artifact, CASCADE, related_name="links_well")
    well: Well = ForeignKey(Well, PROTECT, related_name="links_artifact")
    feature: Feature = ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="links_artifactwell",
    )
    label_ref_is_name: bool | None = BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = BooleanField(null=True, default=None)


class PerturbationTarget(SQLRecord, CanCurate, TracksRun, TracksUpdates):
    """Models perturbation targets such as :class:`~bionty.Gene`, :class:`~bionty.Pathway`, and :class:`~bionty.Protein`.

    Example::

        import bionty as bt
        import wetlab as wl

        gene_1 = bt.Gene.from_source(ensembl_gene_id="ENSG00000000003").save()
        gene_2 = bt.Gene.from_source(ensembl_gene_id="ENSG00000000005").save()
        targets = wl.PerturbationTarget(name="TSPAN6_TNMD").save()
        targets.genes.set([gene_1, gene_2])
    """

    class Meta(SQLRecord.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: int = CharField(unique=True, max_length=8, default=ids.base62_8)
    """Universal id, valid across DB instances."""
    name: str = CharField(max_length=60, default=None, db_index=True)
    """Name of the perturbation target."""
    description: str | None = TextField(null=True, default=None)
    """Description of the perturbation target."""
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

    # def __repr__(self) -> str:
    #     result = [f"{super().__repr__()}"]

    #     result.append(_get_related_repr(self, "genes"))
    #     result.append(_get_related_repr(self, "pathways"))
    #     result.append(_get_related_repr(self, "proteins"))

    #     return "\n".join(filter(None, result))


class ArtifactPerturbationTarget(BaseSQLRecord, IsLink, TracksRun):
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
    label_ref_is_name: bool | None = BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = BooleanField(null=True, default=None)


class GeneticPerturbation(SQLRecord, CanCurate, TracksRun, TracksUpdates):
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

    class Meta(SQLRecord.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: int = CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name: str = CharField(max_length=255, default=None, db_index=True)
    """Name of the Genetic perturbation."""
    system: GeneticPerturbationSystem = models.CharField(
        max_length=32,
        default=None,
        db_index=True,
    )
    """:class:`~wetlab.GeneticPerturbationSystem` used for the genetic perturbation."""
    description: str | None = TextField(null=True, default=None)
    """Description of the genetic perturbation."""
    sequence: str | None = models.TextField(null=True, default=None, db_index=True)
    """Sequence of the perturbation."""
    on_target_score: float | None = FloatField(
        default=None, null=True, db_index=True, blank=True
    )
    """On-target score, indicating the likelihood of the guide RNA successfully targeting the intended DNA sequence."""
    off_target_score: float | None = FloatField(
        default=None, null=True, db_index=True, blank=True
    )
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

    # def __repr__(self) -> str:
    #     result = [f"{super().__repr__()}"]

    #     result.append(_get_related_repr(self, "targets"))

    #     return "\n".join(filter(None, result))


class ArtifactGeneticPerturbation(BaseSQLRecord, IsLink, TracksRun):
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
    label_ref_is_name: bool | None = BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = BooleanField(null=True, default=None)


class Biologic(SQLRecord, CanCurate, TracksRun, TracksUpdates):
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

    _name_field: str = "name"

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: str = CharField(unique=True, max_length=12, default=ids.base62_12)
    """A universal id (hash of selected field)."""
    name: str = CharField(unique=True, db_index=True)
    """Name of the compound."""
    type: BiologicType = CharField(max_length=32, db_index=True, default=None)
    """The type."""
    abbr: str | None = CharField(
        max_length=32, db_index=True, unique=True, null=True, default=None
    )
    """A unique abbreviation."""
    synonyms: str | None = TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this compound."""
    description: str | None = TextField(null=True, default=None)
    """Description of the compound."""
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
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = ForeignKey(Artifact, CASCADE, related_name="links_biologic")
    biologic: Biologic = ForeignKey(Biologic, PROTECT, related_name="links_artifact")
    feature: Feature = ForeignKey(
        Feature, PROTECT, null=True, default=None, related_name="links_artifactbiologic"
    )
    label_ref_is_name: bool | None = BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = BooleanField(null=True, default=None)


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

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: int = CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name: str = CharField(max_length=255, default=None, db_index=True)
    """Name of the compound perturbation."""
    description: str | None = TextField(null=True, default=None)
    """Description of the compound perturbation."""
    concentration: float = FloatField(null=True, default=None, blank=True)
    """Concentration of the compound."""
    concentration_unit: str = CharField(max_length=32, null=True, default=None)
    """Unit of the concentration."""
    duration: timedelta | None = DurationField(null=True, default=None)
    """Duration of the compound perturbation."""
    targets: PerturbationTarget = models.ManyToManyField(
        PerturbationTarget, related_name="compound_perturbations"
    )
    """Targets of the perturbation."""
    compound: Compound | None = ForeignKey("Compound", PROTECT, null=True, default=None)
    """Compounds linked to the perturbation."""
    artifacts: Artifact = models.ManyToManyField(
        Artifact,
        through="ArtifactCompoundPerturbation",
        related_name="compound_perturbations",
    )
    """Artifacts linked to the perturbation."""

    # def __repr__(self) -> str:
    #     result = [f"{super().__repr__()}"]

    #     result.append(_get_related_repr(self, "targets"))

    #     return "\n".join(filter(None, result))


class ArtifactCompoundPerturbation(BaseSQLRecord, IsLink, TracksRun):
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
    label_ref_is_name: bool | None = BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = BooleanField(null=True, default=None)


class EnvironmentalPerturbation(SQLRecord, CanCurate, TracksRun, TracksUpdates):
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

    class Meta(SQLRecord.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: int = CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name: str = CharField(max_length=255, default=None, db_index=True)
    """Name of the environmental perturbation."""
    ontology_id = CharField(max_length=32, db_index=True, null=True, default=None)
    """Ontology ID (EFO) of the environmental perturbation."""
    description: str | None = TextField(null=True, default=None)
    """Description of the environmental perturbation."""
    value: float | None = FloatField(null=True, default=None, blank=True)
    """The value of the environmental perturbation such as a temperature."""
    unit: str | None = CharField(max_length=32, null=True, default=None)
    """Unit of the value such as 'degrees celsius'"""
    duration: timedelta | None = DurationField(null=True, default=None, blank=True)
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

    # def __repr__(self) -> str:
    #     result = [f"{super().__repr__()}"]

    #     result.append(_get_related_repr(self, "targets"))

    #     return "\n".join(filter(None, result))


class ArtifactEnvironmentalPerturbation(BaseSQLRecord, IsLink, TracksRun):
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
    label_ref_is_name: bool | None = BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = BooleanField(null=True, default=None)


class CombinationPerturbation(SQLRecord, CanCurate, TracksRun, TracksUpdates):
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

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: int = CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name: str | None = CharField(max_length=255, default=None, db_index=True)
    """Name of the perturbation."""
    description: str | None = TextField(null=True, default=None)
    """Description of the combination perturbation."""
    ontology_id: str | None = CharField(
        max_length=32, db_index=True, null=True, default=None
    )
    """Ontology ID of the perturbation."""
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

    # def __repr__(self) -> str:
    #     result = [f"{super().__repr__()}"]

    #     result.append(_get_related_repr(self, "genetics"))
    #     result.append(_get_related_repr(self, "compounds"))
    #     result.append(_get_related_repr(self, "environmentals"))

    #     return "\n".join(filter(None, result))

    @property
    def members(self) -> QuerySet:
        """Retrieve all related GeneticPerturbation, CompoundPerturbation, and EnvironmentalPerturbation instances."""
        if self._state.adding:
            return self.__class__.objects.none()

        return self.genetic.all().union(self.compound.all(), self.environmental.all())


class ArtifactCombinationPerturbation(BaseSQLRecord, IsLink, TracksRun):
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
    label_ref_is_name: bool | None = BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = BooleanField(null=True, default=None)


class Biosample(SQLRecord, CanCurate, TracksRun, TracksUpdates):
    """Models a specimen derived from an organism, such as tissue, blood, or cells.

    Example::

        import wetlab as wl

        biosample = wl.Biosample(
            name="control",
            batch="ctrl_1"
        ).save()
    """

    class Meta(SQLRecord.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: int = CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name: str | None = CharField(max_length=255, default=None, db_index=True, null=True)
    """Name of the biosample."""
    batch: str | None = CharField(max_length=60, default=None, null=True, db_index=True)
    """Batch label of the biosample."""
    description: str | None = TextField(null=True, default=None)
    """Description of the biosample."""
    organism: Organism | None = ForeignKey(
        Organism, PROTECT, null=True, related_name="biosamples"
    )
    """Organism of the biosample."""
    tissues: Tissue = models.ManyToManyField(Tissue, related_name="biosamples")
    """Tissues linked to the biosample."""
    cell_lines: CellLine = models.ManyToManyField(CellLine, related_name="biosamples")
    """Cell lines linked to the biosample."""
    cell_types: CellType = models.ManyToManyField(CellType, related_name="biosamples")
    """Cell types linked to the biosample."""
    diseases: Disease = models.ManyToManyField(Disease, related_name="biosamples")
    """Diseases linked to the biosample."""
    artifacts: Artifact = models.ManyToManyField(
        Artifact, through="ArtifactBiosample", related_name="biosamples"
    )
    """Artifacts linked to the biosample."""


class ArtifactBiosample(BaseSQLRecord, IsLink, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = ForeignKey(Artifact, CASCADE, related_name="links_biosample")
    biosample: Biosample = ForeignKey(Biosample, PROTECT, related_name="links_artifact")
    feature: Feature = ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="links_artifactbiosample",
    )
    label_ref_is_name: bool | None = BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = BooleanField(null=True, default=None)


class Techsample(SQLRecord, CanCurate, TracksRun, TracksUpdates):
    """Models technical samples which represent a processed or derived sample in a lab created from raw biological materials.

    Example::

        import wetlab as wl

        techsample = wl.Techsample(
            name="tech_1",
            batch="replicates_3"
        ).save()
    """

    class Meta(SQLRecord.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: int = CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name: str | None = CharField(max_length=255, default=None, db_index=True)
    """Name of the techsample."""
    batch: str | None = CharField(max_length=60, default=None, db_index=True)
    """Batch label of the techsample."""
    description: str | None = TextField(null=True, default=None)
    """Description of the techsample."""
    biosamples: Biosample = models.ManyToManyField(
        Biosample, related_name="techsamples"
    )
    """Linked biosamples."""
    artifacts: Artifact = models.ManyToManyField(
        Artifact, through="ArtifactTechsample", related_name="techsamples"
    )
    """Artifacts linked to the techsample."""


class ArtifactTechsample(BaseSQLRecord, IsLink, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = ForeignKey(Artifact, CASCADE, related_name="links_techsample")
    techsample: Techsample = ForeignKey(
        Techsample, PROTECT, related_name="links_artifact"
    )
    feature: Feature = ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="links_artifacttechsample",
    )
    label_ref_is_name: bool | None = BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = BooleanField(null=True, default=None)


class Donor(SQLRecord, CanCurate, TracksRun, TracksUpdates):
    """Models a donor that provides biospecimens for research.

    Example::

        import wetlab as wl

        donor = wl.Donor(
            name="donor_001",
            age=45,
            sex="M"
        ).save()
        donor.diseases.add(disease)
    """

    class Meta(SQLRecord.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: int = CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name: str | None = CharField(max_length=255, default=None, db_index=True)
    """Name/identifier of the donor."""
    batch: str | None = CharField(max_length=60, default=None, db_index=True)
    """Batch label for the donor."""
    description: str | None = TextField(null=True, default=None)
    """Description of the donor."""
    age: int | None = IntegerField(null=True, db_index=True, default=None)
    """Age of the donor in years."""
    bmi: float | None = FloatField(null=True, default=None)
    """Body mass index (BMI) of the donor."""
    ethnicity: Ethnicity = ForeignKey(
        Ethnicity, PROTECT, null=True, related_name="donors"
    )
    """Race or ethnicity of the donor."""
    sex: Phenotype = ForeignKey(Phenotype, PROTECT, null=True, related_name="donors")
    """Biological sex of the donor."""
    organism: Organism | None = ForeignKey(
        Organism, PROTECT, null=True, related_name="donors"
    )
    """Organism of the donor."""
    diseases: Disease = models.ManyToManyField(Disease, related_name="donors")
    """Diseases associated with the donor."""
    artifacts: Artifact = models.ManyToManyField(
        Artifact, through="ArtifactDonor", related_name="donors"
    )
    """Artifacts linked to the donor."""


class ArtifactDonor(BaseSQLRecord, IsLink, TracksRun):
    """Link table between Artifacts and Donors."""

    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = ForeignKey(Artifact, CASCADE, related_name="links_donor")
    donor: Donor = ForeignKey(Donor, PROTECT, related_name="links_artifact")
    feature: Feature = ForeignKey(
        Feature, PROTECT, null=True, default=None, related_name="links_artifactdonor"
    )
    label_ref_is_name: bool | None = BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = BooleanField(null=True, default=None)
