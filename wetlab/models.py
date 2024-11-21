from __future__ import annotations

from datetime import timedelta  # noqa
from typing import Literal, overload

from bionty import ids as bionty_ids
from bionty.models import (
    BioRecord,
    CellLine,
    CellType,
    Disease,
    Gene,
    Organism,
    Pathway,
    Protein,
    Source,
    Tissue,
)
from django.db import DatabaseError, models
from django.db.models import CASCADE, PROTECT, QuerySet
from lnschema_core import ids
from lnschema_core.fields import (
    BooleanField,
    CharField,
    DateField,
    DurationField,
    FloatField,
    ForeignKey,
    IntegerField,
    TextField,
)
from lnschema_core.models import (
    Artifact,
    CanCurate,
    Feature,
    LinkORM,
    Record,
    TracksRun,
    TracksUpdates,
)

GeneticTreatmentSystem = Literal[
    "CRISPR-Cas9",
    "CRISPRi",
    "CRISPRa",
    "shRNA",
    "siRNA",
    "transgene",
    "transient-transfection",
]


# def _get_related_repr(instance, related_name: str) -> str:
#     try:
#         related_manager = getattr(instance, related_name)
#         if instance.pk is not None and related_manager.exists():
#             related_count = related_manager.count()
#             related_repr = "\n".join(f"      {item}" for item in related_manager.all())
#             return f"  {related_name} ({related_count}):\n{related_repr}"
#     except (AttributeError, DatabaseError):
#         return ""
#     return ""


class Compound(BioRecord, TracksRun, TracksUpdates):
    """Models a (chemical) compound such as a drug.

    Examples:
        >>> compound = wl.Compound(
        ...    name="Navitoclax",
        ...    ontology_id="CHEMBL443684"
        ... ).save()
    """

    class Meta(BioRecord.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    _name_field: str = "name"
    _ontology_id_field: str = "ontology_id"

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: str = CharField(unique=True, max_length=8, default=bionty_ids.ontology)
    """A universal id (hash of selected field)."""
    name: str = CharField(max_length=256, db_index=True)
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


class ArtifactCompound(Record, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = ForeignKey(Artifact, CASCADE, related_name="links_compound")
    compound: Compound = ForeignKey(Compound, PROTECT, related_name="links_artifact")
    feature: Feature = ForeignKey(
        Feature, PROTECT, null=True, default=None, related_name="links_artifactcompound"
    )
    label_ref_is_name: bool | None = BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = BooleanField(null=True, default=None)


class Experiment(Record, CanCurate, TracksRun, TracksUpdates):
    """Models a wetlab experiment.

    Example:
        >>> experiment = wl.Experiment(
        ...     name="IPF mice vs control mice",
        ...     description="Analysis of gene expression levels in different cell types of IPF.",
        ... ).save()
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
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


class ArtifactExperiment(Record, LinkORM, TracksRun):
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


class Well(Record, CanCurate, TracksRun, TracksUpdates):
    """Models a well in a wetlab :class:`wetlab.Experiment` that is part of a microplate.

    Example:
        >>> well = wl.Well(
        ...    name="Well A1",
        ...    row="A",
        ...    column=1,
        ... ).save()
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
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


class ArtifactWell(Record, LinkORM, TracksRun):
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


class TreatmentTarget(Record, CanCurate, TracksRun, TracksUpdates):
    """Models treatment targets such as :class:`~bionty.Gene`, :class:`~bionty.Pathway`, and :class:`~bionty.Protein`.

    Examples:
        >>> gene_1 = bt.Gene.from_source(ensembl_gene_id="ENSG00000000003").save()
        >>> gene_2 = bt.Gene.from_source(ensembl_gene_id="ENSG00000000005").save()
        >>> targets = wl.TreatmentTarget(name="TSPAN6_TNMD").save()
        >>> targets.genes.set([gene_1, gene_2])
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: int = CharField(unique=True, max_length=8, default=ids.base62_8)
    """Universal id, valid across DB instances."""
    name: str = CharField(max_length=60, default=None, db_index=True)
    """Name of the treatment target."""
    description: str | None = TextField(null=True, default=None)
    """Description of the treatment target."""
    genes: Gene = models.ManyToManyField(
        "bionty.Gene", related_name="treatment_targets"
    )
    """Genes of the treatment target, link to :class:`~bionty.Gene` records."""
    pathways: Pathway = models.ManyToManyField(
        "bionty.Pathway", related_name="treatment_targets"
    )
    """Pathways of the treatment target, link to :class:`bionty.Pathway` records."""
    proteins: Protein = models.ManyToManyField(
        "bionty.Protein", related_name="treatment_targets"
    )
    artifacts: Artifact = models.ManyToManyField(
        Artifact, through="ArtifactTreatmentTarget", related_name="treatment_targets"
    )
    """Artifacts linked to the treatment target."""

    # def __repr__(self) -> str:
    #     result = [f"{super().__repr__()}"]

    #     result.append(_get_related_repr(self, "genes"))
    #     result.append(_get_related_repr(self, "pathways"))
    #     result.append(_get_related_repr(self, "proteins"))

    #     return "\n".join(filter(None, result))


class ArtifactTreatmentTarget(Record, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = ForeignKey(
        Artifact, CASCADE, related_name="links_treatment_target"
    )
    treatmenttarget: TreatmentTarget = ForeignKey(
        TreatmentTarget, PROTECT, related_name="links_artifact"
    )
    feature: Feature = ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="links_artifacttreatmenttarget",
    )
    label_ref_is_name: bool | None = BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = BooleanField(null=True, default=None)


class GeneticTreatment(Record, CanCurate, TracksRun, TracksUpdates):
    """Models Genetic perturbations such as CRISPR.

    Args:
        name: The name of the genetic treatment.
        system: The system used to apply the genetic treatment.
                Must be one of 'CRISPR Cas9', 'CRISPRi', 'CRISPRa', 'shRNA', 'siRNA', 'transgene', 'transient transfection'.
        on_target_score: The on-target score, indicating the likelihood of the guide RNA successfully targeting the intended DNA sequence.
        off_target_score: The off-target score, indicating the likelihood of the guide RNA targeting unintended DNA sequences.

    Examples:
        >>> sicke_cell_treatment = wl.GeneticTreatment(
        ...     system="CRISPR Cas9",
        ...     name="Hemoglobin Sickle Cell Treatment",
        ...     sequence="AGCTGACCGTGA",
        ...     on_target_score=85,
        ...     off_target_score=15
        ... ).save()
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: int = CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name: str = CharField(max_length=255, default=None, db_index=True)
    """Name of the Genetic treatment."""
    system: GeneticTreatmentSystem = CharField(
        max_length=32,
        default=None,
        db_index=True,
    )
    """System used for the genetic treatment."""
    sequence: str | None = TextField(null=True, default=None, db_index=True)
    """Sequence of the treatment."""
    on_target_score: float | None = FloatField(
        default=None, null=True, db_index=True, blank=True
    )
    """On-target score, indicating the likelihood of the guide RNA successfully targeting the intended DNA sequence."""
    off_target_score: float | None = FloatField(
        default=None, null=True, db_index=True, blank=True
    )
    """The off-target score, indicating the likelihood of the guide RNA targeting unintended DNA sequences.."""
    targets: TreatmentTarget = models.ManyToManyField(
        TreatmentTarget, related_name="genetic_targets"
    )
    """Targets of the treatment."""
    artifacts: Artifact = models.ManyToManyField(
        Artifact, through="ArtifactGeneticTreatment", related_name="genetic_treatments"
    )
    """Artifacts linked to the treatment."""

    # def __repr__(self) -> str:
    #     result = [f"{super().__repr__()}"]

    #     result.append(_get_related_repr(self, "targets"))

    #     return "\n".join(filter(None, result))


class ArtifactGeneticTreatment(Record, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = ForeignKey(
        Artifact, CASCADE, related_name="links_genetic_treatment"
    )
    genetictreatment: GeneticTreatment = ForeignKey(
        GeneticTreatment, PROTECT, related_name="links_artifact"
    )
    feature: Feature = ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="links_artifactgenetictreatment",
    )
    label_ref_is_name: bool | None = BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = BooleanField(null=True, default=None)


class CompoundTreatment(Record, CanCurate, TracksRun, TracksUpdates):
    """Models compound treatments such as drugs.

    Args:
        name: The name of the compound treatment.

    Examples:
        >>> aspirin_treatment = compound_treatment = wl.CompoundTreatment(
        ...    name="Antibiotic cocktail",
        ... ).save()
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: int = CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name: str = CharField(max_length=255, default=None, db_index=True)
    """Name of the compound treatment."""
    concentration: float = FloatField(null=True, default=None, blank=True)
    """Concentration of the compound."""
    concentration_unit: str = CharField(max_length=32, null=True, default=None)
    """Unit of the concentration."""
    duration: timedelta | None = DurationField(null=True, default=None)
    """Duration of the compound treatment."""
    targets: TreatmentTarget = models.ManyToManyField(
        TreatmentTarget, related_name="compound_targets"
    )
    """Targets of the treatment."""
    compounds: Compound = models.ManyToManyField(Compound, related_name="compounds")
    """Compounds linked to the treatment."""
    artifacts: Artifact = models.ManyToManyField(
        Artifact,
        through="ArtifactCompoundTreatment",
        related_name="compound_treatments",
    )
    """Artifacts linked to the treatment."""

    # def __repr__(self) -> str:
    #     result = [f"{super().__repr__()}"]

    #     result.append(_get_related_repr(self, "targets"))

    #     return "\n".join(filter(None, result))


class ArtifactCompoundTreatment(Record, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = ForeignKey(
        Artifact, CASCADE, related_name="links_compound_treatment"
    )
    compoundtreatment: CompoundTreatment = ForeignKey(
        CompoundTreatment, PROTECT, related_name="links_artifact"
    )
    feature: Feature = ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="links_artifactcompoundtreatment",
    )
    label_ref_is_name: bool | None = BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = BooleanField(null=True, default=None)


class EnvironmentalTreatment(Record, CanCurate, TracksRun, TracksUpdates):
    """Models environmental perturbations such as heat, acid, or smoke treatments.

    Args:
        name: Name of the environmental treatment.
        ontology_id: Ontology ID of the environmental treatment (EFO).
        value: A value such as a temperature.
        unit: A unit such as 'degrees celsius'.
        duration: Time duration of how long the treatment was applied.

    Examples:
        >>> acid_treatment = EnvironmentalTreatment(
        ...     name='Acid Treatment',
        ...     ontology_id='EFO:0004416',
        ...     value=1.5,
        ...     unit='pH',
        ... ).save()
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: int = CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name: str = CharField(max_length=255, default=None, db_index=True)
    """Name of the environmental treatment."""
    ontology_id = CharField(max_length=32, db_index=True, null=True, default=None)
    """Ontology ID (EFO) of the environmental treatment."""
    value: float | None = FloatField(null=True, default=None, blank=True)
    """The value of the environmental treatment such as a temperature."""
    unit: str | None = CharField(max_length=32, null=True, default=None)
    """Unit of the value such as 'degrees celsius'"""
    duration: timedelta | None = DurationField(null=True, default=None, blank=True)
    """Duration of the environmental treatment."""
    targets: TreatmentTarget = models.ManyToManyField(
        TreatmentTarget, related_name="environmental_targets"
    )
    """Targets of the environmental treatment."""
    artifacts: Artifact = models.ManyToManyField(
        Artifact,
        through="ArtifactEnvironmentalTreatment",
        related_name="environmental_treatments",
    )
    """Artifacts linked to the treatment."""

    # def __repr__(self) -> str:
    #     result = [f"{super().__repr__()}"]

    #     result.append(_get_related_repr(self, "targets"))

    #     return "\n".join(filter(None, result))


class ArtifactEnvironmentalTreatment(Record, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = ForeignKey(
        Artifact, CASCADE, related_name="links_environmental_treatment"
    )
    environmentaltreatment: EnvironmentalTreatment = ForeignKey(
        EnvironmentalTreatment, PROTECT, related_name="links_artifact"
    )
    feature: Feature = ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="links_artifactenvironmentaltreatment",
    )
    label_ref_is_name: bool | None = BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = BooleanField(null=True, default=None)


class CombinationTreatment(Record, CanCurate, TracksRun, TracksUpdates):
    """Combination of several Treatments.

    CombinationTreatments model several Treatments jointly such as one or more :class:`wetlab.GeneticTreatment`,
    :class:`wetlab.CompoundTreatment`, and :class:`wetlab.EnvironmentalTreatment` records.

    Args:
        name: A name of the CombinationTreatment that summarizes all applied Treatments.
        description: A description of the CombinationTreatment.
        ontology_id: An ontology ID of the CombinationTreatment.

    Examples:
        >>> sc_treatment = wl.GeneticTreatment(
        ...     system="CRISPR Cas9",
        ...     name="Hemoglobin Sickle Cell Treatment",
        ...     sequence="AGCTGACCGTGA",
        ... ).save()

        >>> cftr_treatment = wl.GeneticTreatment(
        ...     system="CRISPR Cas9",
        ...     name="Cystic Fibrosis CFTR Correction",
        ...     sequence="TTGGTGGTGAACT",
        ... ).save()

        >>> aspirin_treatment = compound_treatment = wl.CompoundTreatment(
        ...    name="Aspirin",
        ...    pubchem_id=2244
        ... ).save()

        >>> comb_treatment = wl.CombinationTreatment(name="Hemoglobin Sickle Cell and CFTR Correction with Aspirin",
        ...    description="Targets both sickle cell anemia and cystic fibrosis, using CRISPR Cas9 and Aspirin for anti-inflammatory support."
        ... ).save()
        >>> comb_treatment.genetics.set([sc_treatment, aspirin_treatment])
        >>> comb_treatment.compounds.add(aspirin_treatment)
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    id: int = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid: int = CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name: str | None = CharField(max_length=255, default=None, db_index=True)
    """Name of the treatment."""
    description: str | None = TextField(null=True, default=None)
    """Description of the combination treatment."""
    ontology_id: str | None = CharField(
        max_length=32, db_index=True, null=True, default=None
    )
    """Ontology ID of the treatment."""
    genetics: GeneticTreatment = models.ManyToManyField(
        GeneticTreatment, related_name="genetic_treatments"
    )
    """:class:`wetlab.GeneticTreatment` treatments."""
    compounds: CompoundTreatment = models.ManyToManyField(
        CompoundTreatment, related_name="compound_treatments"
    )
    """:class:`wetlab.CompoundTreatment` treatments."""
    environmentals: EnvironmentalTreatment = models.ManyToManyField(
        EnvironmentalTreatment, related_name="environmental_treatments"
    )
    """:class:`wetlab.EnvironmentalTreatment` treatments."""
    artifacts: Artifact = models.ManyToManyField(
        Artifact,
        through="ArtifactCombinationTreatment",
        related_name="combination_treatments",
    )
    """Artifacts linked to the treatment."""

    # def __repr__(self) -> str:
    #     result = [f"{super().__repr__()}"]

    #     result.append(_get_related_repr(self, "genetics"))
    #     result.append(_get_related_repr(self, "compounds"))
    #     result.append(_get_related_repr(self, "environmentals"))

    #     return "\n".join(filter(None, result))

    @property
    def members(self) -> QuerySet:
        """Retrieve all related GeneticTreatment, CompoundTreatment, and EnvironmentalTreatment instances."""
        if self._state.adding:
            return self.__class__.objects.none()

        return self.genetic.all().union(self.compound.all(), self.environmental.all())


class ArtifactCombinationTreatment(Record, LinkORM, TracksRun):
    id: int = models.BigAutoField(primary_key=True)
    artifact: Artifact = ForeignKey(
        Artifact, CASCADE, related_name="links_combination_treatment"
    )
    combinationtreatment: CombinationTreatment = ForeignKey(
        CombinationTreatment, PROTECT, related_name="links_artifact"
    )
    feature: Feature = ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="links_artifactcombinationtreatment",
    )
    label_ref_is_name: bool | None = BooleanField(null=True, default=None)
    feature_ref_is_name: bool | None = BooleanField(null=True, default=None)


class Biosample(Record, CanCurate, TracksRun, TracksUpdates):
    """Models a specimen derived from an organism, such as tissue, blood, or cells.

    Examples:
        >>> biosample = wl.Biosample(
        ...     name="control",
        ...     batch="ctrl_1"
        ... ).save()
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
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
    artifacts: Artifact = models.ManyToManyField(Artifact, related_name="biosamples")
    """Artifacts linked to the biosample."""


class ArtifactBiosample(Record, LinkORM, TracksRun):
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


class Techsample(Record, CanCurate, TracksRun, TracksUpdates):
    """Models technical samples which represent a processed or derived sample in a lab created from raw biological materials.

    Examples:
        >>> techsample = wl.Techsample(
        ...     name="tech_1",
        ...     batch="replicates_3"
        ... ).save()
    """

    class Meta(Record.Meta, TracksRun.Meta, TracksUpdates.Meta):
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
    artifacts: Artifact = models.ManyToManyField(Artifact, related_name="techsamples")
    """Artifacts linked to the techsample."""


class ArtifactTechsample(Record, LinkORM, TracksRun):
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
