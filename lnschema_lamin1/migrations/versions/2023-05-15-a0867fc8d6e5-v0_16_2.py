"""v0.16.2."""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op
from lnschema_core.dev.sqlmodel import get_sqlite_prefix_schema_delim_from_alembic

revision = "a0867fc8d6e5"
down_revision = "652443621d5a"


def upgrade() -> None:
    sqlite, prefix, schema, delim = get_sqlite_prefix_schema_delim_from_alembic()
    op.create_table(
        f"{prefix}treatment",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("type", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("system", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("target", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("sequence", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("on_target_score", sqlmodel.sql.sqltypes.types.Float(), nullable=True),
        sa.Column("off_target_score", sqlmodel.sql.sqltypes.types.Float(), nullable=True),
        sa.Column("ontology_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("pubchem_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["core.user.id"],
            name=op.f(f"fk_lamin1{delim}treatment_created_by_user"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f(f"pk_lamin1{delim}treatment")),
        schema=schema,
    )

    with op.batch_alter_table(f"{prefix}treatment", schema=schema) as batch_op:
        for field in [
            "name",
            "description",
            "type",
            "system",
            "target",
            "sequence",
            "on_target_score",
            "off_target_score",
            "ontology_id",
            "pubchem_id",
            "created_by",
            "created_at",
            "updated_at",
        ]:
            batch_op.create_index(
                batch_op.f(f"ix_lamin1{delim}treatment_{field}"),
                [field],
                unique=False,
            )

    op.create_table(
        f"{prefix}file_treatment",
        sa.Column("file_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("treatment_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(
            ["file_id"],
            ["core.file.id"],
            name=op.f(f"fk_lamin1{delim}file_treatment_file_id_file"),
        ),
        sa.ForeignKeyConstraint(
            ["treatment_id"],
            ["lamin1.treatment.id"],
            name=op.f(f"fk_lamin1{delim}file_treatment_treatment_id_treatment"),
        ),
        sa.PrimaryKeyConstraint("file_id", "treatment_id", name=op.f(f"pk_lamin1{delim}file_treatment")),
        schema=schema,
    )

    op.create_table(
        f"{prefix}biosample_treatment",
        sa.Column("biosample_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("treatment_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(
            ["biosample_id"],
            ["lamin1.biosample.id"],
            name=op.f(f"fk_lamin1{delim}biosample_treatment_biosample_id_biosample"),
        ),
        sa.ForeignKeyConstraint(
            ["treatment_id"],
            ["lamin1.treatment.id"],
            name=op.f(f"fk_lamin1{delim}biosample_treatment_treatment_id_treatment"),
        ),
        sa.PrimaryKeyConstraint(
            "biosample_id",
            "treatment_id",
            name=op.f(f"pk_lamin1{delim}biosample_treatment"),
        ),
        schema=schema,
    )


def downgrade() -> None:
    pass
