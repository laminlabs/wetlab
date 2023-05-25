from lnschem_core.dev.sqlmodel import get_orm
from sqlmodel import Field, ForeignKeyConstraint

from . import __name__ as module_name

SQLModel = get_orm(module_name)


class ProjectExperiment(SQLModel, table=True):  # type: ignore
    """Links `Project` and `Experiment`."""

    project_id: str = Field(foreign_key="lnschema_core_project.id", primary_key=True)
    experiment_id: str = Field(foreign_key="lnschema_lamin1_experiment.id", primary_key=True)


class FileExperiment(SQLModel, table=True):  # type: ignore
    """Links for `File` and `Experiment`."""

    file_id: str = Field(foreign_key="lnschema_core_file.id", primary_key=True)
    experiment_id: str = Field(foreign_key="lnschema_lamin1_experiment.id", primary_key=True)


class FileTreatment(SQLModel, table=True):  # type: ignore
    """Links for `File` and `Treatment`."""

    file_id: str = Field(foreign_key="lnschema_core_file.id", primary_key=True)
    treatment_id: str = Field(foreign_key="lnschema_lamin1_treatment.id", primary_key=True)


class BiosampleTreatment(SQLModel, table=True):  # type: ignore
    """Links for `Biosample` and `Treatment`."""

    biosample_id: str = Field(foreign_key="lnschema_lamin1_biosample.id", primary_key=True)
    treatment_id: str = Field(foreign_key="lnschema_lamin1_treatment.id", primary_key=True)


class BiosampleTechsample(SQLModel, table=True):  # type: ignore
    """Links for `Biosample` and `Techsample`."""

    biosample_id: str = Field(foreign_key="lnschema_lamin1_biosample.id", primary_key=True)
    techsample_id: str = Field(foreign_key="lnschema_lamin1_techsample.id", primary_key=True)


class FileBiosample(SQLModel, table=True):  # type: ignore
    """Links for `File` and `Biosample`."""

    file_id: str = Field(foreign_key="lnschema_core_file.id", primary_key=True)
    biosample_id: str = Field(foreign_key="lnschema_lamin1_biosample.id", primary_key=True)


class FileCellType(SQLModel, table=True):  # type: ignore
    """Links for `File` and `CellType`."""

    file_id: str = Field(foreign_key="lnschema_core_file.id", primary_key=True)
    cell_type_id: str = Field(foreign_key="lnschema_bionty_cell_type.id", primary_key=True)


class FileCellLine(SQLModel, table=True):  # type: ignore
    """Links for `File` and `CellLine`."""

    file_id: str = Field(foreign_key="lnschema_core_file.id", primary_key=True)
    cell_line_id: str = Field(foreign_key="lnschema_bionty_cell_line.id", primary_key=True)


class FileWell(SQLModel, table=True):  # type: ignore
    """Links for `File` and `Well`."""

    file_id: str = Field(foreign_key="lnschema_core_file.id", primary_key=True)
    well_row: str = Field(primary_key=True)
    well_column: int = Field(primary_key=True)

    __table_args__ = ForeignKeyConstraint(
        ["well_row", "well_column"],
        ["lnschema_lamin1_well.row", "lnschema_lamin1_well.column"],
    )
