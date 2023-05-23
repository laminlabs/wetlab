"""v0.16.3."""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op
from lnschema_core.dev.sqlmodel import get_sqlite_prefix_schema_delim_from_alembic

revision = "f9f58cf3ab38"
down_revision = "a0867fc8d6e5"


def upgrade() -> None:
    sqlite, prefix, schema, delim = get_sqlite_prefix_schema_delim_from_alembic()

    op.create_table(
        f"{prefix}well",
        sa.Column("row", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("column", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("row", "column", name=op.f(f"pk_lamin1{delim}well")),
        schema=schema,
    )
    op.create_table(
        f"{prefix}file_cell_line",
        sa.Column("file_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("cell_line_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(
            ["cell_line_id"],
            ["bionty.cell_line.id"],
            name=op.f(f"fk_lamin1{delim}file_cell_line_cell_line_id_cell_line"),
        ),
        sa.ForeignKeyConstraint(
            ["file_id"],
            ["core.file.id"],
            name=op.f(f"fk_lamin1{delim}file_cell_line_file_id_file"),
        ),
        sa.PrimaryKeyConstraint("file_id", "cell_line_id", name=op.f(f"pk_lamin1{delim}file_cell_line")),
        schema=schema,
    )
    op.create_table(
        f"{prefix}file_well",
        sa.Column("file_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("well_row", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("well_column", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["file_id"],
            ["core.file.id"],
            name=op.f(f"fk_lamin1{delim}file_well_file_id_file"),
        ),
        sa.ForeignKeyConstraint(
            ["well_row", "well_column"],
            ["lamin1.well.row", "lamin1.well.column"],
            name=op.f(f"fk_lamin1{delim}file_well_well_row_well"),
        ),
        sa.PrimaryKeyConstraint(
            "file_id",
            "well_row",
            "well_column",
            name=op.f(f"pk_lamin1{delim}file_well"),
        ),
        schema=schema,
    )


def downgrade() -> None:
    pass
