# Generated by Django 5.2 on 2025-01-11 16:44

import django.db.models.deletion
import lamindb.base.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("lamindb", "0072_remove_user__branch_code_remove_user_aux_and_more"),
        ("wetlab", "0030_lamindbv1"),
    ]

    operations = [
        migrations.AlterField(
            model_name="biologic",
            name="space",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="lamindb.space",
            ),
        ),
        migrations.AlterField(
            model_name="biosample",
            name="space",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="lamindb.space",
            ),
        ),
        migrations.AlterField(
            model_name="combinationperturbation",
            name="space",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="lamindb.space",
            ),
        ),
        migrations.AlterField(
            model_name="compound",
            name="space",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="lamindb.space",
            ),
        ),
        migrations.AlterField(
            model_name="compoundperturbation",
            name="space",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="lamindb.space",
            ),
        ),
        migrations.AlterField(
            model_name="donor",
            name="space",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="lamindb.space",
            ),
        ),
        migrations.AlterField(
            model_name="environmentalperturbation",
            name="space",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="lamindb.space",
            ),
        ),
        migrations.AlterField(
            model_name="experiment",
            name="space",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="lamindb.space",
            ),
        ),
        migrations.AlterField(
            model_name="geneticperturbation",
            name="space",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="lamindb.space",
            ),
        ),
        migrations.AlterField(
            model_name="perturbationtarget",
            name="space",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="lamindb.space",
            ),
        ),
        migrations.AlterField(
            model_name="techsample",
            name="space",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="lamindb.space",
            ),
        ),
        migrations.AlterField(
            model_name="well",
            name="space",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="lamindb.space",
            ),
        ),
    ]
