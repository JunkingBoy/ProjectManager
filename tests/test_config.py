import importlib
import sys
import types


def load_config_module():
    sys.modules.pop("config", None)

    fastapi_module = types.ModuleType("fastapi")

    class FakeFastAPI:
        def __init__(self, title, description, version):
            self.title = title
            self.description = description
            self.version = version

    fastapi_module.FastAPI = FakeFastAPI

    exceptions_module = types.ModuleType("fastapi.exceptions")
    exceptions_module.RequestValidationError = type("RequestValidationError", (), {})
    exceptions_module.ResponseValidationError = type("ResponseValidationError", (), {})
    exceptions_module.HTTPException = type("HTTPException", (), {})

    sys.modules["fastapi"] = fastapi_module
    sys.modules["fastapi.exceptions"] = exceptions_module

    return importlib.import_module("config"), FakeFastAPI


def test_create_app_returns_fastapi_instance():
    config_module, fake_fastapi = load_config_module()

    app = config_module.create_app()

    assert isinstance(app, fake_fastapi)


def test_create_app_uses_expected_metadata():
    config_module, _ = load_config_module()

    app = config_module.create_app()

    assert app.title == "Project Manager Server Py"
    assert app.description == "A Backend Server for Project Manager"
    assert app.version == "1.0.0"


def test_project_server_is_fastapi_instance():
    config_module, fake_fastapi = load_config_module()

    assert isinstance(config_module.ProjectServer, fake_fastapi)
