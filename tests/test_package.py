import ts_forecasting


def test_package_importable() -> None:
    assert ts_forecasting is not None


def test_version_defined() -> None:
    assert isinstance(ts_forecasting.__version__, str)
    assert ts_forecasting.__version__ != ""
