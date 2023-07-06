# Generated by Django 4.2.1 on 2023-07-06 14:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "lnschema_bionty",
            "0006_alter_biontysource_options_alter_cellline_options_and_more",
        ),
        ("lnschema_lamin1", "0006_remove_treatment_target_treatment_targets"),
    ]

    operations = [
        migrations.RenameField(
            model_name="biosample",
            old_name="batch_name",
            new_name="batch",
        ),
        migrations.RenameField(
            model_name="biosample",
            old_name="cell_line",
            new_name="cell_lines",
        ),
        migrations.RenameField(
            model_name="biosample",
            old_name="cell_type",
            new_name="cell_types",
        ),
        migrations.RenameField(
            model_name="biosample",
            old_name="disease",
            new_name="diseases",
        ),
        migrations.RenameField(
            model_name="biosample",
            old_name="tissue",
            new_name="tissues",
        ),
        migrations.RemoveField(
            model_name="experimenttype",
            name="efo_id",
        ),
        migrations.AddField(
            model_name="biosample",
            name="description",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AddField(
            model_name="experiment",
            name="description",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AddField(
            model_name="experimenttype",
            name="description",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AddField(
            model_name="experimenttype",
            name="ontology_id",
            field=models.CharField(db_index=True, default=None, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="techsample",
            name="description",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="biosample",
            name="species",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="biosamples",
                to="lnschema_bionty.species",
            ),
        ),
        migrations.AlterField(
            model_name="experiment",
            name="date",
            field=models.DateField(db_index=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="experiment",
            name="experiment_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="experiments",
                to="lnschema_lamin1.experimenttype",
            ),
        ),
    ]