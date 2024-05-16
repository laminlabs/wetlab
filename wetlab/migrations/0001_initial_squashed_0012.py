# Generated by Django 4.2.5 on 2023-10-12 11:19

import django.db.models.deletion
import lnschema_core.ids
import lnschema_core.users
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("lnschema_bionty", "0022_rename_datasets_cellline_collections_and_more.py"),
    ]

    operations = []  # type: ignore

    operations = [
        migrations.CreateModel(
            name="Biosample",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "uid",
                    models.CharField(unique=True, default=lnschema_core.ids.base62_12, max_length=12),
                ),
                (
                    "name",
                    models.CharField(db_index=True, default=None, max_length=255, null=True),
                ),
                (
                    "batch",
                    models.CharField(db_index=True, default=None, max_length=60, null=True),
                ),
                ("description", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "cell_lines",
                    models.ManyToManyField(related_name="biosamples", to="lnschema_bionty.cellline"),
                ),
                (
                    "cell_types",
                    models.ManyToManyField(related_name="biosamples", to="lnschema_bionty.celltype"),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_biosamples",
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "datasets",
                    models.ManyToManyField(related_name="biosamples", to="lnschema_core.collection"),
                ),
                (
                    "diseases",
                    models.ManyToManyField(related_name="biosamples", to="lnschema_bionty.disease"),
                ),
                (
                    "files",
                    models.ManyToManyField(related_name="biosamples", to="lnschema_core.artifact"),
                ),
                (
                    "species",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="biosamples",
                        to="lnschema_bionty.organism",
                    ),
                ),
                (
                    "tissues",
                    models.ManyToManyField(related_name="biosamples", to="lnschema_bionty.tissue"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TreatmentTarget",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "uid",
                    models.CharField(unique=True, default=lnschema_core.ids.base62_8, max_length=8),
                ),
                ("name", models.CharField(db_index=True, default=None, max_length=60)),
                ("description", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_treatment_targets",
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "files",
                    models.ManyToManyField(related_name="treatment_targets", to="lnschema_core.artifact"),
                ),
                (
                    "genes",
                    models.ManyToManyField(related_name="treatment_targets", to="lnschema_bionty.gene"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Treatment",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "uid",
                    models.CharField(unique=True, default=lnschema_core.ids.base62_12, max_length=12),
                ),
                ("name", models.CharField(db_index=True, default=None, max_length=255)),
                (
                    "type",
                    models.CharField(
                        choices=[("genetic", "genetic"), ("chemical", "chemical")],
                        db_index=True,
                        max_length=20,
                    ),
                ),
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
                        max_length=20,
                    ),
                ),
                ("description", models.TextField(default=None, null=True)),
                ("sequence", models.TextField(db_index=True, default=None, null=True)),
                (
                    "on_target_score",
                    models.FloatField(db_index=True, default=None, null=True),
                ),
                (
                    "off_target_score",
                    models.FloatField(db_index=True, default=None, null=True),
                ),
                (
                    "ontology_id",
                    models.CharField(db_index=True, default=None, max_length=32, null=True),
                ),
                (
                    "pubchem_id",
                    models.CharField(db_index=True, default=None, max_length=32, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_treatments",
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "datasets",
                    models.ManyToManyField(related_name="treatments", to="lnschema_core.collection"),
                ),
                (
                    "files",
                    models.ManyToManyField(related_name="treatments", to="lnschema_core.artifact"),
                ),
                (
                    "targets",
                    models.ManyToManyField(related_name="treatments", to="wetlab.treatmenttarget"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Techsample",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "uid",
                    models.CharField(unique=True, default=lnschema_core.ids.base62_12, max_length=12),
                ),
                ("name", models.CharField(db_index=True, default=None, max_length=255)),
                ("batch", models.CharField(db_index=True, default=None, max_length=60)),
                ("description", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "biosamples",
                    models.ManyToManyField(related_name="techsamples", to="wetlab.biosample"),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_techsamples",
                        to="lnschema_core.user",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ExperimentType",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "uid",
                    models.CharField(default=lnschema_core.ids.base62_4, max_length=4, unique=True),
                ),
                ("name", models.CharField(db_index=True, default=None, max_length=255)),
                ("description", models.TextField(default=None, null=True)),
                (
                    "ontology_id",
                    models.CharField(db_index=True, default=None, max_length=32, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_experiment_types",
                        to="lnschema_core.user",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Experiment",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "uid",
                    models.CharField(unique=True, default=lnschema_core.ids.base62_8, max_length=8),
                ),
                ("name", models.CharField(db_index=True, default=None, max_length=255)),
                ("description", models.TextField(default=None, null=True)),
                ("date", models.DateField(db_index=True, default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_experiments",
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "datasets",
                    models.ManyToManyField(related_name="experiments", to="lnschema_core.collection"),
                ),
                (
                    "experiment_type",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="experiments",
                        to="wetlab.experimenttype",
                    ),
                ),
                (
                    "files",
                    models.ManyToManyField(related_name="experiments", to="lnschema_core.artifact"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Well",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "uid",
                    models.CharField(unique=True, default=lnschema_core.ids.base62_4, max_length=4),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        default=None,
                        max_length=32,
                        null=True,
                        unique=True,
                    ),
                ),
                ("row", models.CharField(default=None, max_length=4)),
                ("column", models.IntegerField()),
                (
                    "datasets",
                    models.ManyToManyField(related_name="wells", to="lnschema_core.collection"),
                ),
                (
                    "files",
                    models.ManyToManyField(related_name="wells", to="lnschema_core.artifact"),
                ),
            ],
            options={
                "unique_together": {("row", "column")},
            },
        ),
    ]
