"""v0.8.0.

Revision ID: bfda12fc80a8
Revises: a5d6b07f1401
Create Date: 2022-11-03
"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

revision = "bfda12fc80a8"
down_revision = "a5d6b07f1401"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    if bind.engine.name == "sqlite":
        op.rename_table(old_table_name="biometa", new_table_name="wetlab.biometa")
        op.rename_table(
            old_table_name="dobject_biometa", new_table_name="wetlab.dobject_biometa"
        )
        op.rename_table(old_table_name="biosample", new_table_name="wetlab.biosample")
        op.rename_table(old_table_name="techsample", new_table_name="wetlab.techsample")
        op.rename_table(
            old_table_name="biosample_techsample",
            new_table_name="wetlab.biosample_techsample",
        )
        op.rename_table(old_table_name="readout", new_table_name="wetlab.readout")
        op.rename_table(old_table_name="treatment", new_table_name="wetlab.treatment")
        op.rename_table(
            old_table_name="project_experiment",
            new_table_name="wetlab.project_experiment",
        )
        op.rename_table(old_table_name="experiment", new_table_name="wetlab.experiment")
        op.rename_table(
            old_table_name="experiment_type",
            new_table_name="wetlab.experiment_type",
        )
    else:
        op.execute("alter table public.biometa set schema wetlab")
        op.execute("alter table public.dobject_biometa set schema wetlab")
        op.execute("alter table public.biosample set schema wetlab")
        op.execute("alter table public.techsample set schema wetlab")
        op.execute("alter table public.biosample_techsample set schema wetlab")
        op.execute("alter table public.readout set schema wetlab")
        op.execute("alter table public.treatment set schema wetlab")
        op.execute("alter table public.project_experiment set schema wetlab")
        op.execute("alter table public.experiment set schema wetlab")
        op.execute("alter table public.experiment_type set schema wetlab")


def downgrade() -> None:
    pass
