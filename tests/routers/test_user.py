import importlib
import sys
import types
from types import SimpleNamespace

import pytest

from enums.StandardBusEnum import StandardBusinessEnum


class FakeJSONResponse:
    def __init__(self, content, status_code=200):
        self.content = content
        self.status_code = status_code


class FakeStandardResponse:
    def __init__(self, code, msg, data, path):
        self.code = code
        self.msg = msg
        self.data = data
        self.path = path

    @property
    def info(self):
        result = {"code": self.code, "msg": self.msg}
        if self.data is not None:
            result["data"] = self.data
        if self.path is not None:
            result["path"] = self.path
        return result


def load_router_module():
    sys.modules.pop("routers.User", None)

    fastapi_module = types.ModuleType("fastapi")

    class FakeAPIRouter:
        def __init__(self, prefix, tags):
            self.prefix = prefix
            self.tags = tags

        def post(self, _path):
            def decorator(func):
                return func
            return decorator

        def get(self, _path):
            def decorator(func):
                return func
            return decorator

    fastapi_module.APIRouter = FakeAPIRouter

    requests_module = types.ModuleType("fastapi.requests")
    requests_module.Request = object

    responses_module = types.ModuleType("fastapi.responses")
    responses_module.JSONResponse = FakeJSONResponse

    dantic_module = types.ModuleType("dantics.UserDantic")
    dantic_module.UserRegister = object
    dantic_module.UserLogin = object

    service_module = types.ModuleType("service.UserCenter")
    service_module.user_register = lambda request, data: None
    service_module.user_login = lambda request, data: None
    service_module.user_list_service = lambda request: None
    service_module.user_relevant_service = lambda request, req_id: None

    template_module = types.ModuleType("templates.StandardResTemplate")
    template_module.StandardResponse = FakeStandardResponse

    sys.modules["fastapi"] = fastapi_module
    sys.modules["fastapi.requests"] = requests_module
    sys.modules["fastapi.responses"] = responses_module
    sys.modules["dantics.UserDantic"] = dantic_module
    sys.modules["service.UserCenter"] = service_module
    sys.modules["templates.StandardResTemplate"] = template_module

    return importlib.import_module("routers.User")


router_module = load_router_module()


@pytest.mark.asyncio
async def test_register_returns_standard_response_without_data(monkeypatch):
    async def fake_user_register(request, data):
        return (StandardBusinessEnum.SUCCESS.value[0], "用户注册成功")

    monkeypatch.setattr(router_module, "user_register", fake_user_register)

    response = await router_module.register(SimpleNamespace(), SimpleNamespace())

    assert response.status_code == 200
    assert response.content == {"code": 1001, "msg": "用户注册成功"}


@pytest.mark.asyncio
async def test_login_returns_standard_response_with_token_data_on_success(monkeypatch):
    async def fake_user_login(request, data):
        return (StandardBusinessEnum.SUCCESS.value[0], "登录成功", {"token": "abc"})

    monkeypatch.setattr(router_module, "user_login", fake_user_login)

    response = await router_module.login(SimpleNamespace(), SimpleNamespace())

    assert response.status_code == 200
    assert response.content == {"code": 1001, "msg": "登录成功", "data": {"token": "abc"}}


@pytest.mark.asyncio
async def test_login_returns_standard_response_without_data_on_failure(monkeypatch):
    async def fake_user_login(request, data):
        return (StandardBusinessEnum.PWDERROR.value[0], "密码错误")

    monkeypatch.setattr(router_module, "user_login", fake_user_login)

    response = await router_module.login(SimpleNamespace(), SimpleNamespace())

    assert response.status_code == 200
    assert response.content == {"code": 4001, "msg": "密码错误"}
