# Generated by Django 5.0.3 on 2024-07-29 06:51

import django.db.models.deletion
import lnschema_core.ids
import lnschema_core.models
import lnschema_core.users
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bionty", "0029_alter_cellline_previous_runs_and_more"),
        ("lnschema_core", "0055_artifact_type_artifactparamvalue_and_more"),
        ("wetlab", "0019_alter_treatment_system"),
    ]

    operations = [
        migrations.AddField(
            model_name="treatmenttarget",
            name="pathways",
            field=models.ManyToManyField(
                related_name="treatment_targets", to="bionty.pathway"
            ),
        ),
        migrations.AddField(
            model_name="treatmenttarget",
            name="proteins",
            field=models.ManyToManyField(
                related_name="treatment_targets", to="bionty.protein"
            ),
        ),
        migrations.CreateModel(
            name="CompoundTreatment",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "uid",
                    models.CharField(
                        default=lnschema_core.ids.base62_12, max_length=12, unique=True
                    ),
                ),
                ("name", models.CharField(db_index=True, default=None, max_length=255)),
                (
                    "ontology_id",
                    models.CharField(
                        db_index=True, default=None, max_length=32, null=True
                    ),
                ),
                (
                    "pubchem_id",
                    models.CharField(
                        db_index=True, default=None, max_length=32, null=True
                    ),
                ),
                ("concentration", models.FloatField(default=None, null=True)),
                ("duration", models.FloatField(default=None, null=True)),
                (
                    "duration_unit",
                    models.CharField(
                        choices=[
                            ("second", "SECOND"),
                            ("minute", "MINUTE"),
                            ("hour", "HOUR"),
                            ("day", "DAY"),
                            ("week", "WEEK"),
                            ("month", "MONTH"),
                            ("year", "YEAR"),
                        ],
                        default=None,
                        max_length=32,
                        null=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "artifacts",
                    models.ManyToManyField(
                        related_name="compound_treatments", to="lnschema_core.artifact"
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_compounds",
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "targets",
                    models.ManyToManyField(
                        related_name="compound_targets", to="wetlab.treatmenttarget"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, lnschema_core.models.CanCurate),
        ),
        migrations.CreateModel(
            name="EnvironmentalTreatment",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "uid",
                    models.CharField(
                        default=lnschema_core.ids.base62_12, max_length=12, unique=True
                    ),
                ),
                ("name", models.CharField(db_index=True, default=None, max_length=255)),
                (
                    "ontology_id",
                    models.CharField(
                        db_index=True, default=None, max_length=32, null=True
                    ),
                ),
                ("value", models.FloatField(default=None, null=True)),
                ("unit", models.CharField(default=None, max_length=32, null=True)),
                ("duration", models.FloatField(default=None, null=True)),
                (
                    "duration_unit",
                    models.CharField(
                        choices=[
                            ("second", "SECOND"),
                            ("minute", "MINUTE"),
                            ("hour", "HOUR"),
                            ("day", "DAY"),
                            ("week", "WEEK"),
                            ("month", "MONTH"),
                            ("year", "YEAR"),
                        ],
                        default=None,
                        max_length=32,
                        null=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "artifacts",
                    models.ManyToManyField(
                        related_name="environmental_treatments",
                        to="lnschema_core.artifact",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_environmental",
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "targets",
                    models.ManyToManyField(
                        related_name="environmental_targets",
                        to="wetlab.treatmenttarget",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, lnschema_core.models.CanCurate),
        ),
        migrations.CreateModel(
            name="GeneticTreatment",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "uid",
                    models.CharField(
                        default=lnschema_core.ids.base62_12, max_length=12, unique=True
                    ),
                ),
                ("name", models.CharField(db_index=True, default=None, max_length=255)),
                (
                    "system",
                    models.CharField(
                        choices=[
                            ("CRISPR Cas9", "CRISPR_Cas9"),
                            ("CRISPRi", "CRISPRi"),
                            ("CRISPRa", "CRISPRa"),
                            ("shRNA", "shRNA"),
                            ("siRNA", "siRNA"),
                            ("transgene", "transgene"),
                            ("transient transfection", "transient_transfection"),
                        ],
                        db_index=True,
                        default=None,
                        max_length=32,
                    ),
                ),
                ("sequence", models.TextField(db_index=True, default=None, null=True)),
                (
                    "on_target_score",
                    models.FloatField(db_index=True, default=None, null=True),
                ),
                (
                    "off_target_score",
                    models.FloatField(db_index=True, default=None, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "artifacts",
                    models.ManyToManyField(
                        related_name="genetic_treatments", to="lnschema_core.artifact"
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_genetics",
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "targets",
                    models.ManyToManyField(
                        related_name="genetic_targets", to="wetlab.treatmenttarget"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, lnschema_core.models.CanCurate),
        ),
        migrations.CreateModel(
            name="CombinationTreatment",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "uid",
                    models.CharField(
                        default=lnschema_core.ids.base62_12, max_length=12, unique=True
                    ),
                ),
                ("name", models.CharField(db_index=True, default=None, max_length=255)),
                ("description", models.TextField(default=None, null=True)),
                (
                    "ontology_id",
                    models.CharField(
                        db_index=True, default=None, max_length=32, null=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "artifacts",
                    models.ManyToManyField(
                        related_name="combination_treatments",
                        to="lnschema_core.artifact",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_combination_treatments",
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "compounds",
                    models.ManyToManyField(
                        related_name="compound_treatments",
                        to="wetlab.compoundtreatment",
                    ),
                ),
                (
                    "environmentals",
                    models.ManyToManyField(
                        related_name="environmental_treatments",
                        to="wetlab.environmentaltreatment",
                    ),
                ),
                (
                    "genetics",
                    models.ManyToManyField(
                        related_name="genetic_treatments", to="wetlab.genetictreatment"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, lnschema_core.models.CanCurate),
        ),
        migrations.DeleteModel(
            name="Treatment",
        ),
        migrations.AddField(
            model_name="compoundtreatment",
            name="concentration_unit",
            field=models.CharField(default=None, max_length=32, null=True),
        ),
    ]
