import pytest


@pytest.mark.unit
def test_package_import():
    import app

    assert app.__name__ == "app"
