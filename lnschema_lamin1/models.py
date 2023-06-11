from enum import Enum

from django.db import models
from django.db.models import PROTECT
from lnschema_bionty import CellLine, CellType, Disease, Species, Tissue
from lnschema_core.ids import Base62
from lnschema_core.models import BaseORM, File, User
from lnschema_core.types import ChoicesMixin
from lnschema_core.users import current_user_id


class ExperimentType(BaseORM):  # type: ignore
    """Experiment types."""

    id: str = models.CharField(max_length=4, default=Base62(n_char=4), primary_key=True)
    name: str = models.CharField(max_length=255, default=None, db_index=True)
    efo_id: str = models.CharField(max_length=30, default=None)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User,
        PROTECT,
        default=current_user_id,
        related_name="created_experiment_types",
    )
    """Creator of record, a :class:`~lamindb.User`."""


class TreatmentType(ChoicesMixin, Enum):
    genetic = "genetic"
    chemical = "chemical"


class TreatmentSystem(ChoicesMixin, Enum):
    CRISPR_Cas9 = "CRISPR Cas9"
    CRISPRi = "CRISPRi"
    CRISPRa = "CRISPRa"
    shRNA = "shRNA"
    siRNA = "siRNA"
    transgene = "transgene"
    transient_transfection = "transient transfection"


class Experiment(BaseORM):  # type: ignore
    """Experiments."""

    id: str = models.CharField(max_length=8, default=Base62(8), primary_key=True)
    name: str = models.CharField(max_length=255, default=None, db_index=True)
    date = models.DateTimeField(default=None, null=True, db_index=True)
    experiment_type = models.ForeignKey(ExperimentType, PROTECT, related_name="experiments")
    files = models.ManyToManyField(File, related_name="experiments")
    """Date on which the experiment is performed."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_experiments")
    """Creator of record, a :class:`~lamindb.User`."""


class Well(BaseORM):  # type: ignore
    """Wells in a experimental plate."""

    row = models.CharField(max_length=4, default=None)
    column = models.IntegerField()
    files = models.ManyToManyField(File, PROTECT, related_name="wells")

    class Meta:
        unique_together = (("row", "column"),)


class Treatment(BaseORM):  # type: ignore
    id = models.CharField(max_length=12, default=Base62(12), primary_key=True)
    name = models.CharField(max_length=255, default=None, db_index=True)
    description = models.CharField(max_length=255, default=None, db_index=True)
    type = models.CharField(max_length=20, choices=TreatmentType.choices(), nullable=False, db_index=True)
    system = models.CharField(max_length=20, choices=TreatmentSystem.choices(), default=None, db_index=True)
    target = models.CharField(max_length=60, default=None, db_index=True)
    sequence = models.TextField(default=None, db_index=True)
    on_target_score = models.FloatField(default=None, null=True, db_index=True)
    off_target_score = models.FloatField(default=None, null=True, db_index=True)
    ontology_id = models.CharField(max_length=20, default=None, db_index=True)
    pubchem_id = models.CharField(max_length=20, default=None, db_index=True)
    files = models.ManyToManyField(File, related_name="treatments")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, PROTECT, default=current_user_id, related_name="created_storages")
    """Creator of record, a :class:`~lamindb.User`."""


class Biosample(BaseORM):  # type: ignore
    """Biological samples that are registered in experiments."""

    id = models.CharField(max_length=12, default=Base62(12), primary_key=True)
    name = models.CharField(max_length=255, default=None, db_index=True, null=True)
    batch_name = models.CharField(max_length=60, default=None, null=True, db_index=True)
    species = models.ForeignKey(Species, PROTECT, related_name="biosamples")
    tissue = models.ManyToManyField(Tissue, PROTECT, related_name="biosamples")
    cell_line = models.ManyToManyField(CellLine, PROTECT, related_name="biosamples")
    cell_type = models.ManyToManyField(CellType, PROTECT, related_name="biosamples")
    disease = models.ManyToManyField(Disease, PROTECT, related_name="biosamples")
    files = models.ManyToManyField(File, PROTECT, related_name="biosamples")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User,
        PROTECT,
        default=current_user_id,
        related_name="created_storages",
    )
    """Creator of record, a :class:`~lamindb.User`."""


class Techsample(BaseORM):  # type: ignore
    id: str = models.CharField(max_length=12, default=Base62(12), primary_key=True)
    name = models.CharField(max_length=255, default=None, db_index=True)
    batch = models.CharField(max_length=60, default=None, db_index=True)
    biosamples = models.ManyToManyField(Biosample, related_name="techsamples")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User,
        PROTECT,
        default=current_user_id,
        related_name="created_storages",
    )
    """Creator of record, a :class:`~lamindb.User`."""
