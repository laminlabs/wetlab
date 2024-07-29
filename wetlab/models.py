from enum import Enum

from django.db import models
from django.db.models import PROTECT, QuerySet
from lnschema_bionty.models import (
    CellLine,
    CellType,
    Disease,
    Tissue,
)
from lnschema_core import ids
from lnschema_core.models import (
    Artifact,
    CanValidate,
    Collection,
    Registry,
    User,
)
from lnschema_core.types import ChoicesMixin
from lnschema_core.users import current_user_id


class GeneticTreatmentSystem(ChoicesMixin, Enum):
    CRISPR_Cas9 = "CRISPR Cas9"
    CRISPRi = "CRISPRi"
    CRISPRa = "CRISPRa"
    shRNA = "shRNA"
    siRNA = "siRNA"
    transgene = "transgene"
    transient_transfection = "transient transfection"


class DurationUnit(ChoicesMixin, Enum):
    SECOND = "second"
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


class ExperimentType(Registry, CanValidate):
    """Models the type of wetlab experiment and is associated with :class:`wetlab.Experiment`.

    Examples:
        >>> experiment_type = wl.ExperimentType(
        ...    name="single-cell RNA sequencing",
        ...    ontology_id="0008913"
        ... ).save()
    """

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=4, default=ids.base62_4)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, default=None, db_index=True)
    """Name of the experiment type."""
    description = models.TextField(null=True, default=None)
    """Description of the experiment."""
    ontology_id = models.CharField(
        max_length=32, db_index=True, null=True, default=None
    )
    """Ontology ID (EFO) of the experiment type."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User, PROTECT, default=current_user_id, related_name="created_experiment_types"
    )
    """Creator of record, a :class:`~lamindb.User`."""


class Experiment(Registry, CanValidate):
    """Models a wetlab experiment of :class:`wetlab.ExperimentType`..

    Example:
        >>> experiment = wl.Experiment(
        ...     name="IPF mice vs control mice",
        ...     description="Analysis of gene expression levels in different cell types of IPF.",
        ... ).save()
    """

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.base62_8)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, default=None, db_index=True)
    """Name of the experiment."""
    description = models.TextField(null=True, default=None)
    """Description of the experiment."""
    date = models.DateField(default=None, null=True, db_index=True)
    """Date of the experiment."""
    experiment_type = models.ForeignKey(
        ExperimentType, PROTECT, null=True, related_name="experiments"
    )
    """Type of the experiment."""
    artifacts = models.ManyToManyField(Artifact, related_name="experiments")
    """Artifacts linked to the experiment."""
    collections = models.ManyToManyField(Collection, related_name="experiments")
    """Collections linked to the experiment."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User, PROTECT, default=current_user_id, related_name="created_experiments"
    )
    """Creator of record, a :class:`~lamindb.User`."""


class Well(Registry, CanValidate):
    """Wells.

    Models a well in a wetlab :class:`wetlab.Experiment` that is part of a microplate.

    Example:
        >>> well = wl.Well(
        ...    name="Well A1",
        ...    row="A",
        ...    column=1,
        ... ).save()
    """

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=4, default=ids.base62_4)
    """Universal id, valid across DB instances."""
    name = models.CharField(
        max_length=32, default=None, null=True, unique=True, db_index=True
    )
    """Name of the well."""
    row = models.CharField(max_length=4, default=None)
    """Horizontal position of the well in the microplate."""
    column = models.IntegerField()
    """Vertical position of the well in the microplate."""
    artifacts = models.ManyToManyField(Artifact, related_name="wells")
    """Artifacts linked to the well."""
    collections = models.ManyToManyField(Collection, related_name="wells")
    """Collections linked to the well."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User, PROTECT, default=current_user_id, related_name="created_wells"
    )
    """Creator of record, a :class:`~lamindb.User`."""

    class Meta:
        unique_together = (("row", "column"),)


class TreatmentTarget(Registry, CanValidate):
    """Treatment targets.

    Models targets of a :class:`wetlab.Treatment` such as :class:`~bionty.Gene`, :class:`~bionty.Pathway`, and :class:`~bionty.Protein`.

    Examples:
        >>> gene_1 = bt.Gene.from_public(ensembl_gene_id="ENSG00000000003").save()
        >>> gene_2 = bt.Gene.from_public(ensembl_gene_id="ENSG00000000005").save()
        >>> targets = wl.TreatmentTarget(name="TSPAN6_TNMD")
        >>> targets.genes.set([gene_1, gene_2])
    """

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.base62_8)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=60, default=None, db_index=True)
    """Name of the treatment target."""
    description = models.TextField(null=True, default=None)
    """Description of the treatment target."""
    genes = models.ManyToManyField(
        "lnschema_bionty.Gene", related_name="treatment_targets"
    )
    """Genes of the treatment target, link to :class:`~bionty.Gene` records."""
    pathways = models.ManyToManyField(
        "lnschema_bionty.Pathway", related_name="treatment_targets"
    )
    """Pathways of the treatment target, link to :class:`bionty.Pathway` records."""
    proteins = models.ManyToManyField(
        "lnschema_bionty.Protein", related_name="treatment_targets"
    )
    artifacts = models.ManyToManyField(Artifact, related_name="treatment_targets")
    """Artifacts linked to the treatment target."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User,
        PROTECT,
        default=current_user_id,
        related_name="created_treatment_targets",
    )
    """Creator of record, a :class:`~lamindb.User`."""

    def __repr__(self) -> str:
        genes_repr = "\n".join(f"      {gene}" for gene in self.genes.all())
        pathways_repr = "\n".join(f"      {pathway}" for pathway in self.pathways.all())
        proteins_repr = "\n".join(f"      {protein}" for protein in self.proteins.all())

        result = [f"{super().__repr__()}"]

        if self.genes.count() > 0:
            result.append(f"  genes ({self.genes.count()}):\n{genes_repr}")
        if self.pathways.count() > 0:
            result.append(f"  pathways ({self.pathways.count()}):\n{pathways_repr}")
        if self.proteins.count() > 0:
            result.append(f"  proteins ({self.proteins.count()}):\n{proteins_repr}")

        return "\n".join(result)


class GeneticTreatment(Registry, CanValidate):
    """Genetic treatments.

    Models Genetic perturbations such as CRISPR.

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

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, default=None, db_index=True)
    """Name of the Genetic treatment."""
    system = models.CharField(
        max_length=32,
        choices=GeneticTreatmentSystem.choices(),
        default=None,
        db_index=True,
    )
    """System used for the genetic treatment."""
    sequence = models.TextField(null=True, default=None, db_index=True)
    """Sequence of the treatment."""
    on_target_score = models.FloatField(default=None, null=True, db_index=True)
    """On-target score, indicating the likelihood of the guide RNA successfully targeting the intended DNA sequence."""
    off_target_score = models.FloatField(default=None, null=True, db_index=True)
    """The off-target score, indicating the likelihood of the guide RNA targeting unintended DNA sequences.."""
    targets = models.ManyToManyField(TreatmentTarget, related_name="genetic_targets")
    """Targets of the treatment."""
    artifacts = models.ManyToManyField(Artifact, related_name="genetic_treatments")
    """Artifacts linked to the treatment."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User, PROTECT, default=current_user_id, related_name="created_genetics"
    )
    """Creator of record, a :class:`~lamindb.User`."""

    def __repr__(self) -> str:
        original_repr = super().__repr__()
        if self.targets.count() > 0:
            targets_repr = "\n".join(f"      {target}" for target in self.targets.all())
            return (
                f"{original_repr}\n  targets ({self.targets.count()}):\n{targets_repr}"
            )
        return original_repr


class CompoundTreatment(Registry, CanValidate):
    """Compound treatments.

    Models compound treatments such as drugs.

    Args:
        name: The name of the compound treatment.
        ontology_id: Ontology ID of the compound by the Drug ontology (DROD).
        pubchem_id: Pubchem ID of the compound.
        concentration: The concentration of the compound. Strictly positive.
        duration: Time duration of how long the treatment was applied.
        duration_unit: The unit for the duration.
            Must be one of 'second', 'minute', 'hour', 'day', 'week', 'month', 'year'.

    Examples:
        >>> aspirin_treatment = compound_treatment = wl.CompoundTreatment(
        ...    name="Aspirin 325 MG Enteric Coated Tablet",
        ...    ontology_id="00076148",
        ...    pubchem_id=2244
        ... ).save()
    """

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, default=None, db_index=True)
    """Name of the Genetic treatment."""
    ontology_id = models.CharField(
        max_length=32, db_index=True, null=True, default=None
    )
    """Ontology ID (DRON) of the compound."""
    pubchem_id = models.CharField(max_length=32, db_index=True, null=True, default=None)
    """Pubchem ID of the compound."""
    concentration = models.PositiveIntegerField(null=True)
    """Concentration of the compound."""
    duration = models.PositiveBigIntegerField(null=True)
    """Duration of the compound treatment."""
    duration_unit = models.CharField(
        max_length=32, choices=DurationUnit.choices(), null=True
    )
    """Unit of the duration."""
    targets = models.ManyToManyField(TreatmentTarget, related_name="compound_targets")
    """Targets of the treatment."""
    artifacts = models.ManyToManyField(Artifact, related_name="compound_treatments")
    """Artifacts linked to the treatment."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User, PROTECT, default=current_user_id, related_name="created_compounds"
    )
    """Creator of record, a :class:`~lamindb.User`."""

    def __repr__(self) -> str:
        original_repr = super().__repr__()
        if self.targets.count() > 0:
            targets_repr = "\n".join(f"      {target}" for target in self.targets.all())
            return (
                f"{original_repr}\n  targets ({self.targets.count()}):\n{targets_repr}"
            )
        return original_repr


class EnvironmentalTreatment(Registry, CanValidate):
    """Environmental treatments.

    Models environmental perturbations such as heat, acid, or smoke treatments.

    Args:
        name: Name of the environmental treatment.
        ontology_id: Ontology ID of the environmental treatment (EFO).
        value: A value such as a temperature.
        unit: A unit such as 'degrees celsius'.
        duration: Time duration of how long the treatment was applied.
        duration_unit: The unit for the duration.
            Must be one of 'second', 'minute', 'hour', 'day', 'week', 'month', 'year'.

    Examples:
        >>> acid_treatment = EnvironmentalTreatment(
        ...     name='Acid Treatment',
        ...     ontology_id='EFO:0004416',
        ...     value=1.5,
        ...     unit='pH',
        ...     duration=30,
        ...     duration_unit='minute'
        ... ).save()
    """

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, default=None, db_index=True)
    """Name of the environmental treatment."""
    ontology_id = models.CharField(
        max_length=32, db_index=True, null=True, default=None
    )
    """Ontology ID (EFO) of the environmental treatment."""
    value = models.IntegerField(null=True)
    """The value of the environmental treatment such as a temperature"""
    unit = models.CharField(max_length=32, null=True)
    """Unit of the value such as 'degrees celius'"""
    duration = models.PositiveBigIntegerField(null=True)
    """Duration of the environmental treatment."""
    duration_unit = models.CharField(
        max_length=32, choices=DurationUnit.choices(), null=True
    )
    """Unit of the duration."""
    targets = models.ManyToManyField(
        TreatmentTarget, related_name="environmental_targets"
    )
    """Targets of the environmental treatment."""
    artifacts = models.ManyToManyField(
        Artifact, related_name="environmental_treatments"
    )
    """Artifacts linked to the treatment."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User, PROTECT, default=current_user_id, related_name="created_environmental"
    )
    """Creator of record, a :class:`~lamindb.User`."""

    def __repr__(self) -> str:
        original_repr = super().__repr__()
        if self.targets.count() > 0:
            targets_repr = "\n".join(f"      {target}" for target in self.targets.all())
            return (
                f"{original_repr}\n  targets ({self.targets.count()}):\n{targets_repr}"
            )
        return original_repr


class CombinationTreatment(Registry, CanValidate):
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

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, default=None, db_index=True)
    """Name of the treatment."""
    description = models.TextField(null=True, default=None)
    """Description of the combination treatment."""
    ontology_id = models.CharField(
        max_length=32, db_index=True, null=True, default=None
    )
    """Ontology ID of the treatment."""
    genetics = models.ManyToManyField(
        GeneticTreatment, related_name="genetic_treatments"
    )
    """:class:`wetlab.GeneticTreatment` treatments."""
    compounds = models.ManyToManyField(
        CompoundTreatment, related_name="compound_treatments"
    )
    """:class:`wetlab.CompoundTreatment` treatments."""
    environmentals = models.ManyToManyField(
        EnvironmentalTreatment, related_name="environmental_treatments"
    )
    """:class:`wetlab.EnvironmentalTreatment` treatments."""
    artifacts = models.ManyToManyField(Artifact, related_name="combination_treatments")
    """Artifacts linked to the treatment."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User,
        PROTECT,
        default=current_user_id,
        related_name="created_combination_treatments",
    )
    """Creator of record, a :class:`~lamindb.User`."""

    def __repr__(self) -> str:
        genetics_repr = "\n".join(f"      {genetic}" for genetic in self.genetics.all())
        compounds_repr = "\n".join(
            f"      {compound}" for compound in self.compounds.all()
        )
        environmentals_repr = "\n".join(
            f"      {environmental}" for environmental in self.environmentals.all()
        )

        result = [f"{super().__repr__()}"]
        if self.genetics.count() > 0:
            result.append(f"  genetics ({self.genetics.count()}):\n{genetics_repr}")
        if self.compounds.count() > 0:
            result.append(f"  compounds ({self.compounds.count()}):\n{compounds_repr}")
        if self.environmentals.count() > 0:
            result.append(
                f"  environmentals ({self.environmentals.count()}):\n{environmentals_repr}"
            )

        return "\n".join(result)

    @property
    def members(self) -> QuerySet:
        """Retrieve all related GeneticTreatment, CompoundTreatment, and EnvironmentalTreatment instances."""
        if self._state.adding:
            return self.__class__.objects.none()

        return self.genetic.all().union(self.compound.all(), self.environmental.all())


class Biosample(Registry, CanValidate):
    """Biological samples.

    Examples:
        >>> biosample = wl.Biosample(
        ...     name="control",
        ...     batch="ctrl_1"
        ... ).save()
    """

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, default=None, db_index=True, null=True)
    """Name of the biosample."""
    batch = models.CharField(max_length=60, default=None, null=True, db_index=True)
    """Batch label of the biosample."""
    description = models.TextField(null=True, default=None)
    """Description of the biosample."""
    # organism = models.ForeignKey(
    #     Organism, PROTECT, null=True, related_name="biosamples"
    # )
    """Organism of the biosample."""
    tissues = models.ManyToManyField(Tissue, related_name="biosamples")
    """Tissues linked to the biosample."""
    cell_lines = models.ManyToManyField(CellLine, related_name="biosamples")
    """Cell lines linked to the biosample."""
    cell_types = models.ManyToManyField(CellType, related_name="biosamples")
    """Cell types linked to the biosample."""
    diseases = models.ManyToManyField(Disease, related_name="biosamples")
    """Diseases linked to the biosample."""
    # artifacts = models.ManyToManyField(Artifact, related_name="biosamples")
    """Artifacts linked to the biosample."""
    collections = models.ManyToManyField(Collection, related_name="biosamples")
    """Collections linked to the biosample."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    # created_by = models.ForeignKey(
    #     User, PROTECT, default=current_user_id, related_name="created_biosamples"
    # )
    """Creator of record, a :class:`~lamindb.User`."""


class Techsample(Registry, CanValidate):
    """Technical samples.

    Models technical samples which represent a processed or derived sample in a lab,
    often created from raw biological materials and used for specific assays.

    Examples:
        >>> techsample = wl.Techsample(
        ...     name="tech_1",
        ...     batch="replicates_3"
        ... ).save()
    """

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, default=None, db_index=True)
    """Name of the techsample."""
    batch = models.CharField(max_length=60, default=None, db_index=True)
    """Batch label of the techsample."""
    description = models.TextField(null=True, default=None)
    """Description of the techsample."""
    biosamples = models.ManyToManyField(Biosample, related_name="techsamples")
    """Linked biosamples."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User, PROTECT, default=current_user_id, related_name="created_techsamples"
    )
    """Creator of record, a :class:`~lamindb.User`."""
