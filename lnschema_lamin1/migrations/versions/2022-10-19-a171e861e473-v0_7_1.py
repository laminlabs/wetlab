"""v0.7.1.

Revision ID: a171e861e473
Revises: e2507b7564f0
Create Date: 2022-10-19 18:33:50.266432

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "a171e861e473"
down_revision = "e2507b7564f0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("experiment", schema=None) as batch_op:
        batch_op.drop_index("ix_experiment_project_id")
        batch_op.drop_constraint("fk_experiment_project_id_id", type_="foreignkey")
        batch_op.drop_column("project_id")

    with op.batch_alter_table("project", schema=None) as batch_op:
        batch_op.drop_index("ix_project_created_at")
        batch_op.drop_index("ix_project_created_by")
        batch_op.drop_index("ix_project_external_id")
        batch_op.drop_index("ix_project_name")
    op.drop_table("project")


def downgrade() -> None:
    pass
