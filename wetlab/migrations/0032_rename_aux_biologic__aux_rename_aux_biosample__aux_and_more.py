# Generated by Django 5.2 on 2025-01-13 11:15

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("wetlab", "0031_alter_biologic_space_alter_biosample_space_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="biologic",
            old_name="aux",
            new_name="_aux",
        ),
        migrations.RenameField(
            model_name="biosample",
            old_name="aux",
            new_name="_aux",
        ),
        migrations.RenameField(
            model_name="combinationperturbation",
            old_name="aux",
            new_name="_aux",
        ),
        migrations.RenameField(
            model_name="compound",
            old_name="aux",
            new_name="_aux",
        ),
        migrations.RenameField(
            model_name="compoundperturbation",
            old_name="aux",
            new_name="_aux",
        ),
        migrations.RenameField(
            model_name="donor",
            old_name="aux",
            new_name="_aux",
        ),
        migrations.RenameField(
            model_name="environmentalperturbation",
            old_name="aux",
            new_name="_aux",
        ),
        migrations.RenameField(
            model_name="experiment",
            old_name="aux",
            new_name="_aux",
        ),
        migrations.RenameField(
            model_name="geneticperturbation",
            old_name="aux",
            new_name="_aux",
        ),
        migrations.RenameField(
            model_name="perturbationtarget",
            old_name="aux",
            new_name="_aux",
        ),
        migrations.RenameField(
            model_name="techsample",
            old_name="aux",
            new_name="_aux",
        ),
        migrations.RenameField(
            model_name="well",
            old_name="aux",
            new_name="_aux",
        ),
    ]
