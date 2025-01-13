# Generated by Django 5.2 on 2025-01-13 11:55

import lamindb.base.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("wetlab", "0032_rename_aux_biologic__aux_rename_aux_biosample__aux_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="biologic",
            name="_aux",
            field=lamindb.base.fields.JSONField(
                blank=True, db_default=None, default=None, null=True
            ),
        ),
        migrations.AlterField(
            model_name="biosample",
            name="_aux",
            field=lamindb.base.fields.JSONField(
                blank=True, db_default=None, default=None, null=True
            ),
        ),
        migrations.AlterField(
            model_name="combinationperturbation",
            name="_aux",
            field=lamindb.base.fields.JSONField(
                blank=True, db_default=None, default=None, null=True
            ),
        ),
        migrations.AlterField(
            model_name="compound",
            name="_aux",
            field=lamindb.base.fields.JSONField(
                blank=True, db_default=None, default=None, null=True
            ),
        ),
        migrations.AlterField(
            model_name="compoundperturbation",
            name="_aux",
            field=lamindb.base.fields.JSONField(
                blank=True, db_default=None, default=None, null=True
            ),
        ),
        migrations.AlterField(
            model_name="donor",
            name="_aux",
            field=lamindb.base.fields.JSONField(
                blank=True, db_default=None, default=None, null=True
            ),
        ),
        migrations.AlterField(
            model_name="environmentalperturbation",
            name="_aux",
            field=lamindb.base.fields.JSONField(
                blank=True, db_default=None, default=None, null=True
            ),
        ),
        migrations.AlterField(
            model_name="experiment",
            name="_aux",
            field=lamindb.base.fields.JSONField(
                blank=True, db_default=None, default=None, null=True
            ),
        ),
        migrations.AlterField(
            model_name="geneticperturbation",
            name="_aux",
            field=lamindb.base.fields.JSONField(
                blank=True, db_default=None, default=None, null=True
            ),
        ),
        migrations.AlterField(
            model_name="perturbationtarget",
            name="_aux",
            field=lamindb.base.fields.JSONField(
                blank=True, db_default=None, default=None, null=True
            ),
        ),
        migrations.AlterField(
            model_name="techsample",
            name="_aux",
            field=lamindb.base.fields.JSONField(
                blank=True, db_default=None, default=None, null=True
            ),
        ),
        migrations.AlterField(
            model_name="well",
            name="_aux",
            field=lamindb.base.fields.JSONField(
                blank=True, db_default=None, default=None, null=True
            ),
        ),
    ]
