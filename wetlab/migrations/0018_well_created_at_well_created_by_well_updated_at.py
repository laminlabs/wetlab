# Generated by Django 5.1 on 2024-04-25 14:41

import django.db.models.deletion
import django.utils.timezone
import lnschema_core.users
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wetlab", "0017_remove_biosample_artifacts"),
    ]

    operations = [
        migrations.AddField(
            model_name="well",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, db_index=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="well",
            name="created_by",
            field=models.ForeignKey(
                default=lnschema_core.users.current_user_id,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="created_wells",
                to="lnschema_core.user",
            ),
        ),
        migrations.AddField(
            model_name="well",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
    ]
