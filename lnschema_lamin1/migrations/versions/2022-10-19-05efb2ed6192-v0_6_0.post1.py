"""v0.6.0.post1.

Revision ID: 05efb2ed6192
Revises: 3ed88d3699fd
Create Date: 2022-10-19 12:30:17.936854

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "05efb2ed6192"
down_revision = "3ed88d3699fd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("biosample", schema=None) as batch_op:
        batch_op.create_foreign_key(
            "fk_biosample_cell_marker_id_id",
            "cell_marker",
            ["cell_marker_id"],
            ["id"],
        )


def downgrade() -> None:
    pass
