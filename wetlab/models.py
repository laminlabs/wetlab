from enum import Enum
from typing import Iterable

from django.db import models
from django.db.models import PROTECT, QuerySet
from lnschema_bionty.models import (
    CellLine,
    CellType,
    Disease,
    Gene,
    Pathway,
    Protein,
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


class ExperimentType(Registry, CanValidate):
    """Experiment types."""

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


class GeneticTreatmentSystem(ChoicesMixin, Enum):
    CRISPR_Cas9 = "CRISPR Cas9"
    CRISPRi = "CRISPRi"
    CRISPRa = "CRISPRa"
    shRNA = "shRNA"
    siRNA = "siRNA"
    transgene = "transgene"
    transient_transfection = "transient transfection"


class Experiment(Registry, CanValidate):
    """Experiments."""

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
    """Wells."""

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
    """Treatment targets."""

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


def _create_targets_for_biomolecules(
    cls: Registry, targets: TreatmentTarget | Gene | Protein | Pathway
) -> None:
    if targets is not None:
        valid_targets = []
        for target in targets:
            if isinstance(target, TreatmentTarget):
                valid_targets.append(target)
            elif isinstance(target, (Gene, Protein, Pathway)):
                treatment_target = TreatmentTarget.objects.create(
                    name=target.name,
                    description=f"Automatically created for {target.__class__.__name__}",
                )
                if isinstance(target, Gene):
                    treatment_target.genes.add(target)
                elif isinstance(target, Pathway):
                    treatment_target.pathways.add(target)
                elif isinstance(target, Protein):
                    treatment_target.proteins.add(target)
                treatment_target.save()
                valid_targets.append(treatment_target)
            else:
                raise ValueError("Invalid target type")

        cls.targets.set(valid_targets)


class GeneticTreatment(Registry, CanValidate):
    """Genetic perturbations such as CRISPR."""

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
    targets = models.ManyToManyField(TreatmentTarget, related_name="genetic_targets")
    """Targets of the treatment."""
    sequence = models.TextField(null=True, default=None, db_index=True)
    """Sequence of the treatment."""
    on_target_score = models.FloatField(default=None, null=True, db_index=True)
    """On-target score of the treatment."""
    off_target_score = models.FloatField(default=None, null=True, db_index=True)
    """Off-target score of the treatment."""
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

    def __init__(
        self,
        *args,
        targets: TreatmentTarget | Gene | Protein | Pathway = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        _create_targets_for_biomolecules(self, targets)


class CompoundTreatment(Registry, CanValidate):
    """Compound perturbations such as drugs."""

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, default=None, db_index=True)
    """Name of the Genetic treatment."""
    ontology_id = models.CharField(
        max_length=32, db_index=True, null=True, default=None
    )
    """Ontology ID of the compound."""
    targets = models.ManyToManyField(TreatmentTarget, related_name="compound_targets")
    """Targets of the combination treatment."""
    pubchem_id = models.CharField(max_length=32, db_index=True, null=True, default=None)
    """Pubchem ID of the compound treatment."""
    concentration = models.PositiveIntegerField(null=True)
    """Concentration of the compound treatment."""
    duration = models.PositiveBigIntegerField(null=True)
    """Duration of the compound treatment."""
    duration_unit = models.CharField(max_length=12, null=True)
    """Unit of the duration."""
    artifacts = models.ManyToManyField(Artifact, related_name="compound_treatments")
    """Artifacts linked to the treatment."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User, PROTECT, default=current_user_id, related_name="created_compounds"
    )

    def __init__(
        self,
        *args,
        targets: TreatmentTarget | Gene | Protein | Pathway = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        _create_targets_for_biomolecules(self, targets)


class EnvironmentalTreatment(Registry, CanValidate):
    """Environmental perturbations such as acid."""

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=12, default=ids.base62_12)
    """Universal id, valid across DB instances."""
    name = models.CharField(max_length=255, default=None, db_index=True)
    """Name of the Genetic treatment."""
    ontology_id = models.CharField(
        max_length=32, db_index=True, null=True, default=None
    )
    """Ontology ID of the environmental treatment."""
    targets = models.ManyToManyField(
        TreatmentTarget, related_name="environmental_targets"
    )
    """Targets of the combination treatment."""
    value = models.IntegerField(null=True)
    """The value of the environmental treatment such as a temperature"""
    unit = models.CharField(max_length=32, null=True)
    """Unit of the value such as 'degrees celius'"""
    duration = models.PositiveBigIntegerField(null=True)
    """Duration of the environmental treatment in seconds."""
    duration_unit = models.CharField(max_length=12, null=True)
    """Unit of the duration."""
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


class CombinationTreatment(Registry, CanValidate):
    """Treatments."""

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

    def __init__(
        self,
        *args,
        genetics: GeneticTreatment | Iterable[GeneticTreatment] | None = None,
        compounds: CompoundTreatment | Iterable[CompoundTreatment] | None = None,
        environmentals: EnvironmentalTreatment
        | Iterable[EnvironmentalTreatment]
        | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._genetics = (
            [genetics] if isinstance(genetics, GeneticTreatment) else genetics
        )
        self._compounds = (
            [compounds] if isinstance(compounds, CompoundTreatment) else compounds
        )
        self._environmentals = (
            [environmentals]
            if isinstance(environmentals, EnvironmentalTreatment)
            else environmentals
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._genetics:
            self.genetics.set(self._genetics)
        if self._compounds:
            self.compounds.set(self._compounds)
        if self._environmentals:
            self.environmentals.set(self._environmentals)
        self._genetics = None
        self._compounds = None
        self._environmentals = None

    @property
    def members(self) -> QuerySet:
        """Retrieve all related GeneticTreatment, CompoundTreatment, and EnvironmentalTreatment instances."""
        if self._state.adding:
            return self.__class__.objects.none()

        return self.genetic.all().union(self.compound.all(), self.environmental.all())


class Biosample(Registry, CanValidate):
    """Biological samples."""

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
    """Technical samples."""

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
