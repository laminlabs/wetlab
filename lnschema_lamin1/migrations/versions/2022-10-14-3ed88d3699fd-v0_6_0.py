"""v0.6.0.

Revision ID: 3ed88d3699fd
Revises:
Create Date: 2022-10-14 23:48:42.242156

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3ed88d3699fd"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("project", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString(), nullable=False)
        )
        batch_op.create_index(
            batch_op.f("ix_project_created_by"), ["created_by"], unique=False
        )
        batch_op.create_foreign_key(
            "fk_created_by_user_id", "user", ["created_by"], ["id"]
        )

    with op.batch_alter_table("version_vvhc", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_version_vvhc_user_id"), ["user_id"], unique=False
        )


def downgrade() -> None:
    pass
