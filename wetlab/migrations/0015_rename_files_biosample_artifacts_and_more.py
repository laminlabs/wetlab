# Generated by Django 4.2.5 on 2023-12-12 07:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("wetlab", "0014_rename_species_biosample_organism"),
    ]

    operations = [
        migrations.RenameField(
            model_name="biosample",
            old_name="files",
            new_name="artifacts",
        ),
        migrations.RenameField(
            model_name="experiment",
            old_name="files",
            new_name="artifacts",
        ),
        migrations.RenameField(
            model_name="treatment",
            old_name="files",
            new_name="artifacts",
        ),
        migrations.RenameField(
            model_name="treatmenttarget",
            old_name="files",
            new_name="artifacts",
        ),
        migrations.RenameField(
            model_name="well",
            old_name="files",
            new_name="artifacts",
        ),
    ]
