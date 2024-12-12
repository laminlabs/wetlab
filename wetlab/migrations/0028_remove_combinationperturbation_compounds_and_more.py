# Generated by Django 5.2 on 2024-12-12 16:23

import django.db.models.deletion
import lnschema_core.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wetlab", "0027_rename_treatment_add_donor"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="compoundperturbation",
            name="compounds",
        ),
        migrations.AddField(
            model_name="compoundperturbation",
            name="compound",
            field=lnschema_core.fields.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="wetlab.compound",
            ),
        ),
        migrations.RenameField(
            model_name="combinationperturbation",
            old_name="environmentals",
            new_name="environmental_perturbations",
        ),
        migrations.AlterField(
            model_name="combinationperturbation",
            name="environmental_perturbations",
            field=models.ManyToManyField(
                related_name="combination_perturbations",
                to="wetlab.environmentalperturbation",
            ),
        ),
        migrations.RenameField(
            model_name="combinationperturbation",
            old_name="genetics",
            new_name="genetic_perturbations",
        ),
        migrations.AlterField(
            model_name="combinationperturbation",
            name="genetic_perturbations",
            field=models.ManyToManyField(
                related_name="combination_perturbations",
                to="wetlab.geneticperturbation",
            ),
        ),
        migrations.RenameField(
            model_name="combinationperturbation",
            old_name="compounds",
            new_name="compound_perturbations",
        ),
        migrations.AlterField(
            model_name="combinationperturbation",
            name="compound_perturbations",
            field=models.ManyToManyField(
                related_name="combination_perturbations",
                to="wetlab.compoundperturbation",
            ),
        ),
        migrations.AddField(
            model_name="compoundperturbation",
            name="description",
            field=lnschema_core.fields.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="environmentalperturbation",
            name="description",
            field=lnschema_core.fields.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="geneticperturbation",
            name="description",
            field=lnschema_core.fields.TextField(blank=True, default=None, null=True),
        ),
    ]
