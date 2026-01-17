import shutil

import lamindb as ln
import pytest


def pytest_sessionstart():
    # Set up a test instance of LaminDB
    ln.setup.init(storage="./test-pertdb-unit", schema="bionty,pertdb")


def pytest_sessionfinish(session: pytest.Session):
    shutil.rmtree("test-pertdb-unit")
    # Tear down the test instance after all tests are done
    ln.setup.delete("test-pertdb-unit", force=True)
