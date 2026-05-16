import importlib
import sys
import types


class DummyLogger:
    def __init__(self):
        self.messages = []

    def info(self, message):
        self.messages.append(message)


class FakeValidationError(Exception):
    def __init__(self, errors):
        self._errors = errors

    def errors(self):
        return self._errors


class FakeJSONResponse:
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content


def load_global_dantic_module():
    sys.modules.pop("dantics.GlobalDantic", None)

    fastapi_module = types.ModuleType("fastapi")
    fastapi_module.Request = type("Request", (), {})

    responses_module = types.ModuleType("fastapi.responses")
    responses_module.JSONResponse = FakeJSONResponse

    pydantic_module = types.ModuleType("pydantic")
    pydantic_module.BaseModel = type("BaseModel", (), {})
    pydantic_module.ValidationError = FakeValidationError

    logs_module = types.ModuleType("utils.Logs")
    logs_module.ExceptionLog = type("ExceptionLog", (), {"get_instance": classmethod(lambda cls: DummyLogger())})

    sys.modules["fastapi"] = fastapi_module
    sys.modules["fastapi.responses"] = responses_module
    sys.modules["pydantic"] = pydantic_module
    sys.modules["utils.Logs"] = logs_module

    return importlib.import_module("dantics.GlobalDantic")


def test_Global_Model_Error_Catch_returns_400_with_simplified_errors(monkeypatch):
    global_dantic_module = load_global_dantic_module()
    logger = DummyLogger()
    monkeypatch.setattr(
        global_dantic_module.ExceptionLog,
        "get_instance",
        classmethod(lambda cls: logger),
    )
    error = FakeValidationError([
        {"type": "int_parsing", "msg": "bad int", "loc": ("age",), "input": "x", "ctx": {"field": "age"}},
        {"type": "missing", "msg": "required", "loc": ("name",), "input": {}},
    ])

    response = global_dantic_module.CoreModel.Global_Model_Error_Catch(error)

    assert response.status_code == 400
    assert response.content == [
        {"typ": "int_parsing", "msg": "bad int"},
        {"typ": "missing", "msg": "required"},
    ]


def test_Global_Model_Error_Catch_logs_full_error_details(monkeypatch):
    global_dantic_module = load_global_dantic_module()
    logger = DummyLogger()
    monkeypatch.setattr(
        global_dantic_module.ExceptionLog,
        "get_instance",
        classmethod(lambda cls: logger),
    )
    error = FakeValidationError([
        {"type": "int_parsing", "msg": "bad int", "loc": ("age",), "input": "x", "ctx": {"field": "age"}},
        {"type": "missing", "msg": "required", "loc": ("name",), "input": {}},
    ])

    global_dantic_module.CoreModel.Global_Model_Error_Catch(error)

    assert len(logger.messages) == 1
    assert "请求失败,完整响应结构体为" in logger.messages[0]
    assert "int_parsing" in logger.messages[0]
    assert "missing" in logger.messages[0]
    assert "('age',)" in logger.messages[0]
    assert "('name',)" in logger.messages[0]
    assert "None" in logger.messages[0]
