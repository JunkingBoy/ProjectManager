import importlib
import runpy
import sys
import types


def install_fake_runtime(calls):
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

    uvicorn_module = types.ModuleType("uvicorn")

    def fake_run(app, host, port, reload):
        calls.append({
            "app": app,
            "host": host,
            "port": port,
            "reload": reload,
        })

    uvicorn_module.run = fake_run

    sys.modules["fastapi"] = fastapi_module
    sys.modules["fastapi.exceptions"] = exceptions_module
    sys.modules["uvicorn"] = uvicorn_module

    config_module = importlib.import_module("config")
    return config_module.ProjectServer


def test_main_module_calls_uvicorn_run():
    calls = []
    project_server = install_fake_runtime(calls)

    runpy.run_module("main", run_name="__main__")

    assert calls == [{
        "app": project_server,
        "host": "127.0.0.1",
        "port": 8000,
        "reload": False,
    }]
