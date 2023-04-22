from lndb.test import (
    get_package_name,
    migrate_clones,
    migration_id_is_consistent,
    model_definitions_match_ddl,
)

package_name = get_package_name()


def test_migration_id_is_consistent():
    assert migration_id_is_consistent(package_name)


def test_model_definitions_match_ddl_postgres():
    model_definitions_match_ddl(package_name, dialect_name="postgresql")


def test_migrate_clones_sqlite():
    results = migrate_clones(package_name, n_instances=1, dialect_name="sqlite")
    if "migrate-failed" in results:
        raise RuntimeError("Migration e2e test failed.")


def test_migrate_clones_postgres():
    results = migrate_clones(package_name, n_instances=1, dialect_name="postgresql")
    if "migrate-failed" in results:
        raise RuntimeError("Migration e2e test failed.")
