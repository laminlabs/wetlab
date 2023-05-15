from lnschema_core.dev.sqlmodel import schema_sqlmodel
from sqlmodel import Field

from . import _name as schema_name

SQLModel, prefix, schema_arg = schema_sqlmodel(schema_name)


class ProjectExperiment(SQLModel, table=True):  # type: ignore
    """Links `Project` and `Experiment`."""

    __tablename__ = f"{prefix}project_experiment"

    project_id: str = Field(foreign_key="core.project.id", primary_key=True)
    experiment_id: str = Field(foreign_key="lamin1.experiment.id", primary_key=True)


class FileExperiment(SQLModel, table=True):  # type: ignore
    """Links for `File` and `Experiment`."""

    __tablename__ = f"{prefix}file_experiment"

    file_id: str = Field(foreign_key="core.file.id", primary_key=True)
    experiment_id: str = Field(foreign_key="lamin1.experiment.id", primary_key=True)


class FileTreatment(SQLModel, table=True):  # type: ignore
    """Links for `File` and `Treatment`."""

    __tablename__ = f"{prefix}file_treatment"

    file_id: str = Field(foreign_key="core.file.id", primary_key=True)
    treatment_id: str = Field(foreign_key="lamin1.treatment.id", primary_key=True)


class BiosampleTreatment(SQLModel, table=True):  # type: ignore
    """Links for `Biosample` and `Treatment`."""

    __tablename__ = f"{prefix}biosample_treatment"

    biosample_id: str = Field(foreign_key="lamin1.biosample.id", primary_key=True)
    treatment_id: str = Field(foreign_key="lamin1.treatment.id", primary_key=True)


class BiosampleTechsample(SQLModel, table=True):  # type: ignore
    """Links for `Biosample` and `Techsample`."""

    __tablename__ = f"{prefix}biosample_techsample"

    biosample_id: str = Field(foreign_key="lamin1.biosample.id", primary_key=True)
    techsample_id: str = Field(foreign_key="lamin1.techsample.id", primary_key=True)


class FileBiosample(SQLModel, table=True):  # type: ignore
    """Links for `File` and `Biosample`."""

    __tablename__ = f"{prefix}file_biosample"

    file_id: str = Field(foreign_key="core.file.id", primary_key=True)
    biosample_id: str = Field(foreign_key="lamin1.biosample.id", primary_key=True)


class FileCellType(SQLModel, table=True):  # type: ignore
    """Links for `File` and `CellType`."""

    __tablename__ = f"{prefix}file_cell_type"

    file_id: str = Field(foreign_key="core.file.id", primary_key=True)
    cell_type_id: str = Field(foreign_key="bionty.cell_type.id", primary_key=True)
