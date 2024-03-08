# Generated by Django 4.2.5 on 2023-10-12 08:21

from django.db import connection, migrations, models

import wetlab.models

CORE_MODELS = {
    "ExperimentType": False,
    "Experiment": False,
    "Well": False,
    "TreatmentTarget": False,
    "Treatment": False,
    "Biosample": False,
    "Techsample": False,
}


def create_new_ids(apps, schema_editor):
    for model_name in CORE_MODELS.keys():
        model_class = apps.get_model("wetlab", model_name)
        new_id = 1
        for record in model_class.objects.all().iterator(chunk_size=50):
            record.id = new_id
            record.save()
            new_id += 1


class Migration(migrations.Migration):
    dependencies = [
        ("wetlab", "0010_rename_platewell_well"),
        ("lnschema_core", "0023_export_legacy_data"),
        ("lnschema_bionty", "0016_export_legacy_data"),
    ]

    operations = []  # type: ignore


# repurpose old primary key
for model_name in CORE_MODELS.keys():
    Migration.operations.append(
        migrations.RenameField(
            model_name=model_name,
            old_name="id",
            new_name="uid",
        )
    )


# add new primary key field
for model_name, big in CORE_MODELS.items():
    Migration.operations.append(
        migrations.AddField(
            model_name=model_name,
            name="id",
            field=(models.BigIntegerField(editable=False, null=True) if big else models.IntegerField(editable=False, null=True)),
            preserve_default=False,
        )
    )

# fill in new id values in entity tables
Migration.operations.append(migrations.RunPython(create_new_ids, reverse_code=migrations.RunPython.noop))

# make them unique
for model_name, big in CORE_MODELS.items():
    Migration.operations.append(
        migrations.AlterField(
            model_name=model_name,
            name="id",
            field=(models.BigIntegerField(editable=False, unique=True) if big else models.IntegerField(editable=False, unique=True)),
            preserve_default=False,
        )
    )


def add_new_column_foreign_keys(apps, schema_editor):
    def add_new_column_foreign_keys_orm(orm):
        foreign_key_names = [field.name for field in orm._meta.fields if isinstance(field, (models.ForeignKey, models.OneToOneField))]
        for foreign_key_name in foreign_key_names:
            command1 = f"ALTER TABLE {orm._meta.db_table} RENAME COLUMN {foreign_key_name}_id TO {foreign_key_name}_id_old"
            command2 = f"ALTER TABLE {orm._meta.db_table} ADD {foreign_key_name}_id int"
            with connection.cursor() as cursor:
                cursor.execute(command1)
                cursor.execute(command2)
        many_to_many_names = [field.name for field in orm._meta.many_to_many]
        for many_to_many_name in many_to_many_names:
            link_orm = getattr(orm, many_to_many_name).through
            add_new_column_foreign_keys_orm(link_orm)

    for model_name in CORE_MODELS.keys():
        registry = getattr(wetlab.models, model_name)
        add_new_column_foreign_keys_orm(registry)


# add temporary ID fields
Migration.operations.append(migrations.RunPython(add_new_column_foreign_keys, reverse_code=migrations.RunPython.noop))


def populate_tmp_column_foreign_keys(orm):
    migrations_list = []
    foreign_key_names = [field.name for field in orm._meta.fields if isinstance(field, (models.ForeignKey, models.OneToOneField))]
    for foreign_key_name in foreign_key_names:
        related_table = orm._meta.get_field(foreign_key_name).related_model._meta.db_table
        table = orm._meta.db_table
        # need to use an alias below, otherwise self-referential foreign keys will be omitted
        command = f"UPDATE {table} SET {foreign_key_name}_id=(SELECT id FROM {related_table} b WHERE {table}.{foreign_key_name}_id_old=b.uid)"
        migrations_list.append(migrations.RunSQL(command))
    many_to_many_names = [field.name for field in orm._meta.many_to_many]
    for many_to_many_name in many_to_many_names:
        link_orm = getattr(orm, many_to_many_name).through
        migrations_list += populate_tmp_column_foreign_keys(link_orm)
    return migrations_list


# populate temporary fields
for model_name in CORE_MODELS.keys():
    registry = getattr(wetlab.models, model_name)
    Migration.operations += populate_tmp_column_foreign_keys(registry)
