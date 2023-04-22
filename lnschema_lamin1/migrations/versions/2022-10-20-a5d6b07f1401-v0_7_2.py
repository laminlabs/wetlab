"""v0.7.2.

Revision ID: a5d6b07f1401
Revises: a171e861e473
Create Date: 2022-10-20 10:48:15.014883

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "a5d6b07f1401"
down_revision = "a171e861e473"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "project_experiment",
        sa.Column("project_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("experiment_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(
            ["experiment_id"],
            ["experiment.id"],
            name=op.f("fk_project_experiment_experiment_id_experiment"),
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["project.id"],
            name=op.f("fk_project_experiment_project_id_project"),
        ),
        sa.PrimaryKeyConstraint(
            "project_id", "experiment_id", name=op.f("pk_project_experiment")
        ),
    )

    with op.batch_alter_table("biometa", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString(), nullable=False)
        )
        batch_op.create_index(
            batch_op.f("ix_biometa_created_by"), ["created_by"], unique=False
        )
        batch_op.create_foreign_key(
            batch_op.f("fk_biometa_created_by_user"), "user", ["created_by"], ["id"]
        )

    with op.batch_alter_table("experiment", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString(), nullable=False)
        )
        batch_op.create_index(
            batch_op.f("ix_experiment_created_by"), ["created_by"], unique=False
        )
        batch_op.create_foreign_key(
            batch_op.f("fk_experiment_created_by_user"), "user", ["created_by"], ["id"]
        )

    with op.batch_alter_table("experiment_type", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_experiment_type_name"), ["name"], unique=False
        )


def downgrade() -> None:
    pass
