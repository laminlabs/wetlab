import lamindb as ln
import pytest


@pytest.fixture(scope="session")
def lamindb_test_instance():
    # Set up a test instance of LaminDB
    ln.setup.init(storage="./test-pertdb-unit", schema="bionty,pertdb")
    yield
    # Tear down the test instance after all tests are done
    ln.setup.delete("test-pertdb-unit", force=True)
