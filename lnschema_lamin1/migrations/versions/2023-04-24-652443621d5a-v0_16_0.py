"""v0.16.0."""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op
from lnschema_core.dev.sqlmodel import (  # noqa
    get_sqlite_prefix_schema_delim_from_alembic,
)

revision = "652443621d5a"
down_revision = None


def upgrade() -> None:
    sqlite, prefix, schema, delim = get_sqlite_prefix_schema_delim_from_alembic()

    op.create_table(
        f"{prefix}file_cell_type",
        sa.Column("file_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("cell_type_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(
            ["cell_type_id"],
            ["bionty.cell_type.id"],
            name=op.f("fk_file_cell_type_cell_type_id_cell_type"),
        ),
        sa.ForeignKeyConstraint(["file_id"], ["core.file.id"], name=op.f("fk_file_cell_type_file_id_file")),
        sa.PrimaryKeyConstraint("file_id", "cell_type_id", name=op.f("pk_file_cell_type")),
        schema=schema,
    )


def downgrade() -> None:
    op.drop_table("file_cell_type", schema="lamin1")
