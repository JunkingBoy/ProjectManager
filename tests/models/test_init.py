import importlib
import sys
import types


def load_models_package():
    sys.modules.pop("models", None)

    pytz_module = types.ModuleType("pytz")

    class FakeTimezone:
        def __init__(self, zone):
            self.zone = zone

    pytz_module.timezone = lambda zone: FakeTimezone(zone)

    declarative_module = types.ModuleType("sqlalchemy.ext.declarative")
    declarative_module.declarative_base = lambda: type("FakeBase", (), {"metadata": object()})

    sys.modules["pytz"] = pytz_module
    sys.modules["sqlalchemy.ext.declarative"] = declarative_module

    return importlib.import_module("models")


def test_base_model_has_metadata_attribute():
    models_module = load_models_package()

    assert hasattr(models_module.BaseModel, "metadata")


def test_base_time_uses_asia_shanghai_timezone():
    models_module = load_models_package()

    assert models_module.BaseTime.zone == "Asia/Shanghai"
