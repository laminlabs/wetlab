"""v0.7.0.post1.

Revision ID: e2507b7564f0
Revises: 01360b6492cc
Create Date: 2022-10-19 18:31:12.131732

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e2507b7564f0"
down_revision = "01360b6492cc"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("experiment", schema=None) as batch_op:
        batch_op.create_foreign_key(
            "fk_experiment_project_id_id",
            "project",
            ["project_id"],
            ["id"],
        )


def downgrade() -> None:
    pass
