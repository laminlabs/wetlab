# Generated by Django 5.2 on 2025-06-03 09:45

import django.db.models.deletion
import lamindb.base.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("lamindb", "0104_alter_branch_uid"),
        ("wetlab", "0037_rename__branch_code_biologic_branch_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="biologic",
            name="branch",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_column="_branch_code",
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="lamindb.branch",
            ),
        ),
        migrations.AlterField(
            model_name="biologic",
            name="space",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="lamindb.space",
            ),
        ),
        migrations.AlterField(
            model_name="biosample",
            name="branch",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_column="_branch_code",
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="lamindb.branch",
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
                related_name="+",
                to="lamindb.space",
            ),
        ),
        migrations.AlterField(
            model_name="combinationperturbation",
            name="branch",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_column="_branch_code",
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="lamindb.branch",
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
                related_name="+",
                to="lamindb.space",
            ),
        ),
        migrations.AlterField(
            model_name="compound",
            name="branch",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_column="_branch_code",
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="lamindb.branch",
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
                related_name="+",
                to="lamindb.space",
            ),
        ),
        migrations.AlterField(
            model_name="compoundperturbation",
            name="branch",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_column="_branch_code",
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="lamindb.branch",
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
                related_name="+",
                to="lamindb.space",
            ),
        ),
        migrations.AlterField(
            model_name="donor",
            name="branch",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_column="_branch_code",
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="lamindb.branch",
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
                related_name="+",
                to="lamindb.space",
            ),
        ),
        migrations.AlterField(
            model_name="environmentalperturbation",
            name="branch",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_column="_branch_code",
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="lamindb.branch",
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
                related_name="+",
                to="lamindb.space",
            ),
        ),
        migrations.AlterField(
            model_name="experiment",
            name="branch",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_column="_branch_code",
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="lamindb.branch",
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
                related_name="+",
                to="lamindb.space",
            ),
        ),
        migrations.AlterField(
            model_name="geneticperturbation",
            name="branch",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_column="_branch_code",
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="lamindb.branch",
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
                related_name="+",
                to="lamindb.space",
            ),
        ),
        migrations.AlterField(
            model_name="perturbationtarget",
            name="branch",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_column="_branch_code",
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="lamindb.branch",
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
                related_name="+",
                to="lamindb.space",
            ),
        ),
        migrations.AlterField(
            model_name="techsample",
            name="branch",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_column="_branch_code",
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="lamindb.branch",
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
                related_name="+",
                to="lamindb.space",
            ),
        ),
        migrations.AlterField(
            model_name="well",
            name="branch",
            field=lamindb.base.fields.ForeignKey(
                blank=True,
                db_column="_branch_code",
                db_default=1,
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="lamindb.branch",
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
                related_name="+",
                to="lamindb.space",
            ),
        ),
    ]
