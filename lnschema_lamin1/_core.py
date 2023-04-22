from typing import Optional

from lnbase_biolab import (
    BiosampleBase,
    ExperimentBase,
    ExperimentTypeBase,
    TechsampleBase,
)
from lnschema_bionty import CellType, Disease, Species, Tissue
from lnschema_core import File
from lnschema_core.dev.sqlmodel import add_relationship_keys, schema_sqlmodel
from sqlalchemy.orm import relationship
from sqlmodel import Field, Relationship

from . import _name as schema_name
from .link import BiosampleTechsample, FileBiosample, FileExperiment

_, prefix, schema_arg = schema_sqlmodel(schema_name)


class Experiment(ExperimentBase, table=True):  # type: ignore
    """Experiments."""

    experiment_type_id: str = Field(
        default=None, foreign_key="lamin1.experiment_type.id", index=True
    )
    files: File = Relationship(
        back_populates="experiments",
        sa_relationship_kwargs=dict(secondary=FileExperiment.__table__),
    )


File.experiments = relationship(
    Experiment, back_populates="files", secondary=FileExperiment.__table__
)
File.__sqlmodel_relationships__["experiments"] = None


class ExperimentType(ExperimentTypeBase, table=True):  # type: ignore
    """Experiment types."""

    __tablename__ = f"{prefix}experiment_type"


class Biosample(BiosampleBase, table=True):  # type: ignore
    """Biological samples that are registered in experiments."""

    batch: Optional[str] = None
    species_id: Optional[str] = Field(
        default=None, foreign_key="bionty.species.id", index=True
    )
    species: Species = Relationship()
    tissue_id: Optional[str] = Field(
        default=None, foreign_key="bionty.tissue.id", index=True
    )
    tissue: Tissue = Relationship()
    cell_type_id: Optional[str] = Field(
        default=None, foreign_key="bionty.cell_type.id", index=True
    )
    cell_type: CellType = Relationship()
    disease_id: Optional[str] = Field(
        default=None, foreign_key="bionty.disease.id", index=True
    )
    disease: Disease = Relationship()
    files: File = Relationship(
        back_populates="biosamples",
        sa_relationship_kwargs=dict(secondary=FileBiosample.__table__),
    )


File.biosamples = relationship(
    Biosample, back_populates="files", secondary=FileBiosample.__table__
)
File.__sqlmodel_relationships__["biosamples"] = None

add_relationship_keys(Biosample)


class Techsample(TechsampleBase, table=True):  # type: ignore
    biosamples: Biosample = Relationship(
        back_populates="techsamples",
        sa_relationship_kwargs=dict(secondary=BiosampleTechsample.__table__),
    )


Biosample.techsamples = relationship(
    Techsample, back_populates="biosamples", secondary=BiosampleTechsample.__table__
)
Biosample.__sqlmodel_relationships__["techsamples"] = None
