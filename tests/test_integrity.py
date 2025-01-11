import lamindb_setup as ln_setup
import pytest


@pytest.fixture(scope="module")
def setup_instance():
    ln_setup.init(storage="./testdb", modules="bionty,wetlab")
    yield
    ln_setup.delete("testdb", force=True)


def test_migrate_check(setup_instance):
    assert ln_setup.migrate.check()


def test_system_check(setup_instance):
    ln_setup.django("check")
