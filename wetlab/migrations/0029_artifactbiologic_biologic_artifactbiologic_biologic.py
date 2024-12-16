# Generated by Django 5.1.3 on 2024-12-16 21:32

import django.db.models.deletion
import lnschema_core.fields
import lnschema_core.ids
import lnschema_core.models
import lnschema_core.users
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bionty", "0041_squashed"),
        ("lnschema_core", "0069_squashed"),
        ("wetlab", "0028_remove_combinationperturbation_compounds_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ArtifactBiologic",
            fields=[
                (
                    "created_at",
                    lnschema_core.fields.DateTimeField(
                        auto_now_add=True, db_index=True
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "label_ref_is_name",
                    lnschema_core.fields.BooleanField(
                        blank=True, default=None, null=True
                    ),
                ),
                (
                    "feature_ref_is_name",
                    lnschema_core.fields.BooleanField(
                        blank=True, default=None, null=True
                    ),
                ),
                (
                    "artifact",
                    lnschema_core.fields.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="links_biologic",
                        to="lnschema_core.artifact",
                    ),
                ),
                (
                    "created_by",
                    lnschema_core.fields.ForeignKey(
                        blank=True,
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "feature",
                    lnschema_core.fields.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="links_artifactbiologic",
                        to="lnschema_core.feature",
                    ),
                ),
                (
                    "run",
                    lnschema_core.fields.ForeignKey(
                        blank=True,
                        default=lnschema_core.models.current_run,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lnschema_core.run",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(lnschema_core.models.LinkORM, models.Model),
        ),
        migrations.CreateModel(
            name="Biologic",
            fields=[
                (
                    "created_at",
                    lnschema_core.fields.DateTimeField(
                        auto_now_add=True, db_index=True
                    ),
                ),
                (
                    "updated_at",
                    lnschema_core.fields.DateTimeField(auto_now=True, db_index=True),
                ),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "uid",
                    lnschema_core.fields.CharField(
                        blank=True,
                        default=lnschema_core.ids.base62_12,
                        max_length=12,
                        unique=True,
                    ),
                ),
                (
                    "name",
                    lnschema_core.fields.CharField(
                        blank=True, db_index=True, default=None, max_length=256
                    ),
                ),
                (
                    "abbr",
                    lnschema_core.fields.CharField(
                        blank=True,
                        db_index=True,
                        default=None,
                        max_length=32,
                        null=True,
                        unique=True,
                    ),
                ),
                (
                    "synonyms",
                    lnschema_core.fields.TextField(blank=True, default=None, null=True),
                ),
                (
                    "description",
                    lnschema_core.fields.TextField(blank=True, default=None, null=True),
                ),
                (
                    "_previous_runs",
                    models.ManyToManyField(related_name="+", to="lnschema_core.run"),
                ),
                (
                    "artifacts",
                    models.ManyToManyField(
                        related_name="biologics",
                        through="wetlab.ArtifactBiologic",
                        to="lnschema_core.artifact",
                    ),
                ),
                (
                    "created_by",
                    lnschema_core.fields.ForeignKey(
                        blank=True,
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "proteins",
                    models.ManyToManyField(
                        related_name="biologics", to="bionty.protein"
                    ),
                ),
                (
                    "run",
                    lnschema_core.fields.ForeignKey(
                        blank=True,
                        default=lnschema_core.models.current_run,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lnschema_core.run",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(lnschema_core.models.CanCurate, models.Model),
        ),
        migrations.AddField(
            model_name="artifactbiologic",
            name="biologic",
            field=lnschema_core.fields.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="links_artifact",
                to="wetlab.biologic",
            ),
        ),
    ]
