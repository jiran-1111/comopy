import pytest


def pytest_addoption(parser):
    parser.addini(
        "comopy_path",
        "ComoPy project path for test files configuration",
        default=".",
    )


@pytest.fixture
def project_path(pytestconfig):
    return pytestconfig.getini("comopy_path")
