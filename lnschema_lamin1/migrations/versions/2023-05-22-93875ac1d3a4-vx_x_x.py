"""vX.X.X."""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op
from lnschema_core.dev.sqlmodel import get_sqlite_prefix_schema_delim_from_alembic

revision = "93875ac1d3a4"
down_revision = "a0867fc8d6e5"


def upgrade() -> None:
    sqlite, prefix, schema, delim = get_sqlite_prefix_schema_delim_from_alembic()
    op.create_table(
        f"{prefix}well",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("row", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("column", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_lamin1{delim}well")),
        schema=schema,
    )
    with op.batch_alter_table(f"{prefix}well", schema=schema) as batch_op:
        batch_op.create_index(batch_op.f(f"ix_lamin1{delim}well_column"), ["column"], unique=False)
        batch_op.create_index(batch_op.f(f"ix_lamin1{delim}well_row"), ["row"], unique=False)

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
        sa.Column("well_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(
            ["file_id"],
            ["core.file.id"],
            name=op.f(f"fk_lamin1{delim}file_well_file_id_file"),
        ),
        sa.ForeignKeyConstraint(
            ["well_id"],
            ["lamin1.well.id"],
            name=op.f(f"fk_lamin1{delim}file_well_well_id_well"),
        ),
        sa.PrimaryKeyConstraint("file_id", "well_id", name=op.f(f"pk_lamin1{delim}file_well")),
        schema=schema,
    )


def downgrade() -> None:
    pass
