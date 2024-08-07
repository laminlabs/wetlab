# Generated by Django 5.2 on 2024-08-01 13:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wetlab", "0020_treatmenttarget_pathways_treatmenttarget_proteins_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="compoundtreatment",
            name="duration_unit",
            field=models.CharField(default=None, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name="environmentaltreatment",
            name="duration_unit",
            field=models.CharField(default=None, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name="genetictreatment",
            name="system",
            field=models.CharField(db_index=True, default=None, max_length=32),
        ),
    ]
