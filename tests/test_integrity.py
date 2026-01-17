import lamindb_setup as ln_setup
import pytest


def test_migrate_check():
    assert ln_setup.migrate.check()


def test_system_check():
    ln_setup.django("check")
