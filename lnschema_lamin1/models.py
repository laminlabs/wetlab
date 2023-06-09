from django.db import models
from lnschema_bionty import CellLine, CellType, Disease, Species, Tissue
from lnschema_core._users import current_user_id
from lnschema_core.models import BaseORM, User


class ExperimentType(BaseORM):  # type: ignore
    """Experiment types."""

    id: str = models.CharField(max_length=,default=idg.experiment_type, primary_key=True)
    name: str = models.CharField(max_length=,default=None, index=True)
    efo_id: str = models.CharField(max_length=,default=None, unique=True)
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


class Experiment(BaseORM):  # type: ignore
    """Experiments."""

    id: str = models.CharField(max_length=,default=idg.experiment, primary_key=True)
    name: str = models.CharField(max_length=,default=None, index=True)
    date: datetime = models.CharField(max_length=,default=None, index=True)
    """Date on which the experiment is performed."""
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt
    experiment_type_id: str = models.CharField(max_length=,default=None, foreign_key=ExperimentType.id, index=True)
    files: File = Relationship(
        back_populates="experiments",
        sa_relationship_kwargs=dict(secondary=FileExperiment.__table__),
    )


File.experiments = relationship(Experiment, back_populates="files", secondary=FileExperiment.__table__)


class Biosample(BaseORM):  # type: ignore
    """Biological samples that are registered in experiments."""

    id: str = models.CharField(max_length=,default=idg.biosample, primary_key=True)
    name: Optional[str] = models.CharField(max_length=,default=None, index=True)
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt
    batch: Optional[str] = None
    species_id: Optional[str] = models.CharField(max_length=,default=None, foreign_key=Species.id, index=True)
    species: Species = Relationship()
    tissue_id: Optional[str] = models.CharField(max_length=,default=None, foreign_key=Tissue.id, index=True)
    tissue: Tissue = Relationship()
    cell_type_id: Optional[str] = models.CharField(max_length=,default=None, foreign_key=CellType.id, index=True)
    cell_type: CellType = Relationship()
    disease_id: Optional[str] = models.CharField(max_length=,default=None, foreign_key=Disease.id, index=True)
    disease: Disease = Relationship()
    files: File = Relationship(
        back_populates="biosamples",
        sa_relationship_kwargs=dict(secondary=FileBiosample.__table__),
    )


File.biosamples = relationship(Biosample, back_populates="files", secondary=FileBiosample.__table__)


class Well(BaseORM):  # type: ignore
    """Wells in a experimental plate."""

    row: str = models.CharField(max_length=,primary_key=True)
    column: int = models.CharField(max_length=,primary_key=True)

    files: File = Relationship(
        back_populates="wells",
        sa_relationship_kwargs=dict(secondary=FileWell.__table__),
    )


File.wells = relationship(Well, secondary=FileWell.__table__)


class Treatment(BaseORM):  # type: ignore
    id: str = models.CharField(max_length=,default=idg.treatment, primary_key=True)
    name: Optional[str] = models.CharField(max_length=,default=None, index=True)
    description: Optional[str] = models.CharField(max_length=,default=None, index=True)
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt
    type: tp.treatment_type = models.CharField(max_length=,nullable=False, index=True)
    system: tp.treatment_system = models.CharField(max_length=,default=None, index=True)
    target: Optional[str] = models.CharField(max_length=,default=None, index=True)
    sequence: Optional[str] = models.CharField(max_length=,default=None, index=True)
    on_target_score: Optional[float] = models.CharField(max_length=,default=None, index=True)
    off_target_score: Optional[float] = models.CharField(max_length=,default=None, index=True)
    ontology_id: Optional[str] = models.CharField(max_length=,default=None, index=True)
    pubchem_id: Optional[str] = models.CharField(max_length=,default=None, index=True)
    files: File = Relationship(
        back_populates="treatments",
        sa_relationship_kwargs=dict(secondary=FileTreatment.__table__),
    )


File.treatments = relationship(Treatment, back_populates="files", secondary=FileTreatment.__table__)
File.cell_types = relationship(CellType, secondary=FileCellType.__table__)
File.cell_line = relationship(CellLine, secondary=FileCellLine.__table__)
add_relationship_keys(File)


class Techsample(BaseORM):  # type: ignore
    id: str = models.CharField(max_length=,default=idg.techsample, primary_key=True)
    name: Optional[str] = models.CharField(max_length=,default=None, index=True)
    batch: Optional[str] = None
    filepath_r1: Optional[str] = None
    filepath_r2: Optional[str] = None
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt
    biosamples: Biosample = Relationship(
        back_populates="techsamples",
        sa_relationship_kwargs=dict(secondary=BiosampleTechsample.__table__),
    )


Biosample.techsamples = relationship(Techsample, back_populates="biosamples", secondary=BiosampleTechsample.__table__)
Biosample.treatments = relationship(Treatment, secondary=BiosampleTreatment.__table__)
add_relationship_keys(Biosample)

Treatment.biosamples = relationship(Biosample, back_populates="treatments", secondary=BiosampleTreatment.__table__)
add_relationship_keys(Treatment)
