# Generated by Django 5.2 on 2024-12-03 19:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0069_squashed"),
        ("wetlab", "0025_squashed"),
    ]

    operations = [
        migrations.RunSQL(
            f"""
            INSERT INTO wetlab_artifactbiosample (artifact_id, biosample_id, feature_id, created_by_id, created_at)
            SELECT artifact_id, biosample_id, NULL, {1}, CURRENT_TIMESTAMP
            FROM wetlab_biosample_artifacts;
            """
        ),
        migrations.RunSQL(
            f"""
            INSERT INTO wetlab_artifacttechsample (artifact_id, techsample_id, feature_id, created_by_id, created_at)
            SELECT artifact_id, techsample_id, NULL, {1}, CURRENT_TIMESTAMP
            FROM wetlab_techsample_artifacts;
            """
        ),
        migrations.RemoveField(
            model_name="biosample",
            name="artifacts",
        ),
        migrations.AddField(
            model_name="biosample",
            name="artifacts",
            field=models.ManyToManyField(
                related_name="biosamples",
                through="wetlab.ArtifactBiosample",
                to="lnschema_core.artifact",
            ),
        ),
        migrations.RemoveField(
            model_name="techsample",
            name="artifacts",
        ),
        migrations.AlterField(
            model_name="techsample",
            name="artifacts",
            field=models.ManyToManyField(
                related_name="techsamples",
                through="wetlab.ArtifactTechsample",
                to="lnschema_core.artifact",
            ),
        ),
    ]
