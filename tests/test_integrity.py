import lamindb_setup as ln_setup
import pytest


@pytest.fixture
def setup_instance():
    ln_setup.init(storage="./testdb", schema="bionty,wetlab")
    yield
    ln_setup.delete("testdb", force=True)


def test_migrate_check(setup_instance):
    assert ln_setup.migrate.check()
