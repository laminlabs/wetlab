from datetime import datetime
from typing import Optional

from lnschema_bionty import CellLine, CellType, Disease, Species, Tissue
from lnschema_core import File
from lnschema_core._timestamps import CreatedAt, UpdatedAt
from lnschema_core._users import CreatedBy
from lnschema_core.dev.sqlmodel import add_relationship_keys, get_orm, schema_sqlmodel
from sqlalchemy.orm import relationship
from sqlmodel import Field, Relationship

from lnschema_lamin1.dev import id as idg
from lnschema_lamin1.dev import type as tp

from . import __name__ as module_name
from . import _name as schema_name
from .link import (
    BiosampleTechsample,
    BiosampleTreatment,
    FileBiosample,
    FileCellLine,
    FileCellType,
    FileExperiment,
    FileTreatment,
    FileWell,
)

# this is for backward compat
schema_sqlmodel(schema_name)

# this is the current way
SQLModel = get_orm(module_name)


class ExperimentType(SQLModel, table=True):  # type: ignore
    """Experiment types."""

    id: str = Field(default_factory=idg.experiment_type, primary_key=True)
    name: str = Field(default=None, index=True)
    efo_id: str = Field(default=None, unique=True)
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


class Experiment(SQLModel, table=True):  # type: ignore
    """Experiments."""

    id: str = Field(default_factory=idg.experiment, primary_key=True)
    name: str = Field(default=None, index=True)
    date: datetime = Field(default=None, index=True)
    """Date on which the experiment is performed."""
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt
    experiment_type_id: str = Field(default=None, foreign_key=ExperimentType.id, index=True)
    files: File = Relationship(
        back_populates="experiments",
        sa_relationship_kwargs=dict(secondary=FileExperiment.__table__),
    )


File.experiments = relationship(Experiment, back_populates="files", secondary=FileExperiment.__table__)


class Biosample(SQLModel, table=True):  # type: ignore
    """Biological samples that are registered in experiments."""

    id: str = Field(default_factory=idg.biosample, primary_key=True)
    name: Optional[str] = Field(default=None, index=True)
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt
    batch: Optional[str] = None
    species_id: Optional[str] = Field(default=None, foreign_key=Species.id, index=True)
    species: Species = Relationship()
    tissue_id: Optional[str] = Field(default=None, foreign_key=Tissue.id, index=True)
    tissue: Tissue = Relationship()
    cell_type_id: Optional[str] = Field(default=None, foreign_key=CellType.id, index=True)
    cell_type: CellType = Relationship()
    disease_id: Optional[str] = Field(default=None, foreign_key=Disease.id, index=True)
    disease: Disease = Relationship()
    files: File = Relationship(
        back_populates="biosamples",
        sa_relationship_kwargs=dict(secondary=FileBiosample.__table__),
    )


File.biosamples = relationship(Biosample, back_populates="files", secondary=FileBiosample.__table__)


class Well(SQLModel, table=True):  # type: ignore
    """Wells in a experimental plate."""

    row: str = Field(primary_key=True)
    column: int = Field(primary_key=True)

    files: File = Relationship(
        back_populates="wells",
        sa_relationship_kwargs=dict(secondary=FileWell.__table__),
    )


File.wells = relationship(Well, secondary=FileWell.__table__)


class Treatment(SQLModel, table=True):  # type: ignore
    id: str = Field(default_factory=idg.treatment, primary_key=True)
    name: Optional[str] = Field(default=None, index=True)
    description: Optional[str] = Field(default=None, index=True)
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt
    type: tp.treatment_type = Field(nullable=False, index=True)
    system: tp.treatment_system = Field(default=None, index=True)
    target: Optional[str] = Field(default=None, index=True)
    sequence: Optional[str] = Field(default=None, index=True)
    on_target_score: Optional[float] = Field(default=None, index=True)
    off_target_score: Optional[float] = Field(default=None, index=True)
    ontology_id: Optional[str] = Field(default=None, index=True)
    pubchem_id: Optional[str] = Field(default=None, index=True)
    files: File = Relationship(
        back_populates="treatments",
        sa_relationship_kwargs=dict(secondary=FileTreatment.__table__),
    )


File.treatments = relationship(Treatment, back_populates="files", secondary=FileTreatment.__table__)
File.cell_types = relationship(CellType, secondary=FileCellType.__table__)
File.cell_line = relationship(CellLine, secondary=FileCellLine.__table__)
add_relationship_keys(File)


class Techsample(SQLModel, table=True):  # type: ignore
    id: str = Field(default_factory=idg.techsample, primary_key=True)
    name: Optional[str] = Field(default=None, index=True)
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
