import pytest

from .helpers import register_stub_python


@pytest.fixture(autouse=True, scope="session")
def _register_stub_python():
    register_stub_python()
