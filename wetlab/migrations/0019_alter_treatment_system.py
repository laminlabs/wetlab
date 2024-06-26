# Generated by Django 5.0.6 on 2024-06-26 15:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wetlab", "0018_squashed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="treatment",
            name="system",
            field=models.CharField(
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
    ]
