"""v0.7.0.

Revision ID: 01360b6492cc
Revises: 05efb2ed6192
Create Date: 2022-10-19 12:54:37.784842

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "01360b6492cc"
down_revision = "05efb2ed6192"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("biosample", schema=None) as batch_op:
        batch_op.drop_index("ix_biosample_cell_marker_id")
        batch_op.drop_constraint("fk_biosample_cell_marker_id_id", type_="foreignkey")
        batch_op.drop_column("cell_marker_id")

    with op.batch_alter_table("experiment", schema=None) as batch_op:
        batch_op.create_unique_constraint(
            batch_op.f("uq_experiment_external_id"), ["external_id"]
        )

    with op.batch_alter_table("experiment_type", schema=None) as batch_op:
        batch_op.create_unique_constraint(
            batch_op.f("uq_experiment_type_efo_id"), ["efo_id"]
        )

    with op.batch_alter_table("featureset", schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f("uq_featureset_name"), ["name"])


def downgrade() -> None:
    pass
