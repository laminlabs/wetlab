"""v0.17.0."""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

revision = "c3f38ffe9e05"
down_revision = "f9f58cf3ab38"


def upgrade() -> None:
    bind = op.get_bind()
    if bind.engine.name == "sqlite":
        op.rename_table(old_table_name="lamin1.experiment_type", new_table_name="lnschema_lamin1_experimenttype")
        op.rename_table(old_table_name="lamin1.experiment", new_table_name="lnschema_lamin1_experiment")
        op.rename_table(old_table_name="lamin1.biosample", new_table_name="lnschema_lamin1_biosample")
        op.rename_table(old_table_name="lamin1.well", new_table_name="lnschema_lamin1_well")
        op.rename_table(old_table_name="lamin1.treatment", new_table_name="lnschema_lamin1_treatment")
        op.rename_table(old_table_name="lamin1.techsample", new_table_name="lnschema_lamin1_techsample")
        op.rename_table(old_table_name="lamin1.project_experiment", new_table_name="lnschema_lamin1_projectexperiment")
        op.rename_table(old_table_name="lamin1.file_experiment", new_table_name="lnschema_lamin1_fileexperiment")
        op.rename_table(old_table_name="lamin1.file_treatment", new_table_name="lnschema_lamin1_filetreatment")
        op.rename_table(old_table_name="lamin1.biosample_treatment", new_table_name="lnschema_lamin1_biosampletreatment")
        op.rename_table(old_table_name="lamin1.biosample_techsample", new_table_name="lnschema_lamin1_biosampletechsample")
        op.rename_table(old_table_name="lamin1.file_biosample", new_table_name="lnschema_lamin1_filebiosample")
        op.rename_table(old_table_name="lamin1.file_cell_type", new_table_name="lnschema_lamin1_filecelltype")
        op.rename_table(old_table_name="lamin1.file_cell_line", new_table_name="lnschema_lamin1_filecellline")
        op.rename_table(old_table_name="lamin1.file_well", new_table_name="lnschema_lamin1_filewell")
    else:
        op.rename_table(old_table_name="experiment_type", new_table_name="lnschema_lamin1_experimenttype", schema="lamin1")
        op.rename_table(old_table_name="experiment", new_table_name="lnschema_lamin1_experiment", schema="lamin1")
        op.rename_table(old_table_name="biosample", new_table_name="lnschema_lamin1_biosample", schema="lamin1")
        op.rename_table(old_table_name="well", new_table_name="lnschema_lamin1_well", schema="lamin1")
        op.rename_table(old_table_name="treatment", new_table_name="lnschema_lamin1_treatment", schema="lamin1")
        op.rename_table(old_table_name="techsample", new_table_name="lnschema_lamin1_techsample", schema="lamin1")
        op.rename_table(old_table_name="project_experiment", new_table_name="lnschema_lamin1_projectexperiment", schema="lamin1")
        op.rename_table(old_table_name="file_experiment", new_table_name="lnschema_lamin1_fileexperiment", schema="lamin1")
        op.rename_table(old_table_name="file_treatment", new_table_name="lnschema_lamin1_filetreatment", schema="lamin1")
        op.rename_table(old_table_name="biosample_treatment", new_table_name="lnschema_lamin1_biosampletreatment", schema="lamin1")
        op.rename_table(old_table_name="biosample_techsample", new_table_name="lnschema_lamin1_biosampletechsample", schema="lamin1")
        op.rename_table(old_table_name="file_biosample", new_table_name="lnschema_lamin1_filebiosample", schema="lamin1")
        op.rename_table(old_table_name="file_cell_type", new_table_name="lnschema_lamin1_filecelltype", schema="lamin1")
        op.rename_table(old_table_name="file_cell_line", new_table_name="lnschema_lamin1_filecellline", schema="lamin1")
        op.rename_table(old_table_name="file_well", new_table_name="lnschema_lamin1_filewell", schema="lamin1")
        # there seems to be a bug in alembic autoexperimentrate that doesn't pick this up
        op.execute("alter table lamin1.lnschema_lamin1_experimenttype set schema public")
        op.execute("alter table lamin1.lnschema_lamin1_experiment set schema public")
        op.execute("alter table lamin1.lnschema_lamin1_biosample set schema public")
        op.execute("alter table lamin1.lnschema_lamin1_well set schema public")
        op.execute("alter table lamin1.lnschema_lamin1_treatment set schema public")
        op.execute("alter table lamin1.lnschema_lamin1_techsample set schema public")
        op.execute("alter table lamin1.lnschema_lamin1_projectexperiment set schema public")
        op.execute("alter table lamin1.lnschema_lamin1_fileexperiment set schema public")
        op.execute("alter table lamin1.lnschema_lamin1_filetreatment set schema public")
        op.execute("alter table lamin1.lnschema_lamin1_biosampletreatment set schema public")
        op.execute("alter table lamin1.lnschema_lamin1_biosampletechsample set schema public")
        op.execute("alter table lamin1.lnschema_lamin1_filebiosample set schema public")
        op.execute("alter table lamin1.lnschema_lamin1_filecelltype set schema public")
        op.execute("alter table lamin1.lnschema_lamin1_filecellline set schema public")
        op.execute("alter table lamin1.lnschema_lamin1_filewell set schema public")


def downgrade() -> None:
    pass
