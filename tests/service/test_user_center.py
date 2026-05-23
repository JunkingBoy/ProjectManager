import asyncio
import importlib
import sys
import types
from datetime import timezone, timedelta
from types import SimpleNamespace

import pytest

from enums.StandardBusEnum import StandardBusinessEnum
from utils.Excptions import DivExcep


class FakeHTTPException(Exception):
    def __init__(self, status_code, detail):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


class DummySessionContext:
    def __init__(self, session):
        self.session = session

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, exc_type, exc, tb):
        return False


class DummyPool:
    def __init__(self, session):
        self.session = session

    def get_session(self):
        return DummySessionContext(self.session)


class DummyRequest:
    def __init__(self, headers=None, session=None):
        self.headers = headers or {}
        self.app = SimpleNamespace(state=SimpleNamespace(db_pool=DummyPool(session or object())))


class DummyTokenInfo:
    def __init__(self, uid, exp):
        self.uid = uid
        self.exp = exp


def build_register_model():
    return SimpleNamespace(phone="enc-phone", email="enc-email", password="enc-password", password_confirm="enc-password")


def build_login_model():
    return SimpleNamespace(phone="enc-phone", password="enc-password")


def load_service_module():
    sys.modules.pop("service.UserCenter", None)

    fastapi_module = types.ModuleType("fastapi")
    fastapi_module.Request = object
    fastapi_module.HTTPException = FakeHTTPException

    models_module = types.ModuleType("models")
    models_module.CST = timezone(timedelta(hours=8))

    pool_module = types.ModuleType("utils.Pool")
    pool_module.StandardSQLiteDBConnectPool = DummyPool

    user_dantic_module = types.ModuleType("dantics.UserDantic")
    user_dantic_module.UserRegister = object
    user_dantic_module.UserLogin = object

    repository_module = types.ModuleType("repository.UserRepository")
    repository_module.user_alive = lambda session, data: asyncio.sleep(0, result=(StandardBusinessEnum.UNREGISTERED.value[0], "用户未注册"))
    repository_module.user_create = lambda session, template: asyncio.sleep(0, result=StandardBusinessEnum.SUCCESS.value[0])
    repository_module.email_repeat_check = lambda session, email: asyncio.sleep(0, result=False)

    jwt_module = types.ModuleType("utils.JWT")
    jwt_module.create_access_token = lambda token_info: asyncio.sleep(0, result="token")

    encry_module = types.ModuleType("utils.Encry")
    encry_module.decrypt = lambda value: asyncio.sleep(0, result=value)
    encry_module.encrypt = lambda value, iv="": asyncio.sleep(0, result=f"enc:{value}:{iv}")

    tools_files_module = types.ModuleType("tools.Files")
    tools_files_module.get_env_val = lambda key, env=None: "fixed-iv"

    tools_re_module = types.ModuleType("tools.Re")
    tools_re_module.generate_uid = lambda: "uid-default"
    tools_re_module.is_valid_email = lambda value: True
    tools_re_module.is_valid_phone = lambda value: True
    tools_re_module.is_valid_password = lambda value: True

    standard_sys_template_module = types.ModuleType("templates.StandardSysTemplate")
    standard_sys_template_module.StandardTokenInfoTemplate = DummyTokenInfo

    sys.modules["fastapi"] = fastapi_module
    sys.modules["models"] = models_module
    sys.modules["utils.Pool"] = pool_module
    sys.modules["dantics.UserDantic"] = user_dantic_module
    sys.modules["repository.UserRepository"] = repository_module
    sys.modules["utils.JWT"] = jwt_module
    sys.modules["utils.Encry"] = encry_module
    sys.modules["tools.Files"] = tools_files_module
    sys.modules["tools.Re"] = tools_re_module
    sys.modules["templates.StandardSysTemplate"] = standard_sys_template_module

    return importlib.import_module("service.UserCenter")


service_module = load_service_module()


@pytest.mark.asyncio
async def test_user_register_returns_fail_when_platform_header_missing():
    result = await service_module.user_register(DummyRequest(), build_register_model())

    assert result == (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")


@pytest.mark.asyncio
async def test_user_register_raises_when_phone_invalid(monkeypatch):
    async def fake_decrypt(value):
        return {"enc-phone": "bad-phone", "enc-email": "user@example.com", "enc-password": "Passw0rd!"}[value]

    monkeypatch.setattr(service_module, "decrypt", fake_decrypt)
    monkeypatch.setattr(service_module, "is_valid_phone", lambda value: False)

    with pytest.raises(DivExcep, match="手机号格式错误"):
        await service_module.user_register(DummyRequest(headers={"sec-ch-ua-platform": "Windows"}), build_register_model())


@pytest.mark.asyncio
async def test_user_register_returns_fail_when_email_exists(monkeypatch):
    async def fake_decrypt(value):
        return {"enc-phone": "13800000000", "enc-email": "user@example.com", "enc-password": "Passw0rd!"}[value]

    async def fake_encrypt(value, iv=""):
        return f"enc:{value}:{iv}"

    monkeypatch.setattr(service_module, "decrypt", fake_decrypt)
    monkeypatch.setattr(service_module, "encrypt", fake_encrypt)
    monkeypatch.setattr(service_module, "get_env_val", lambda key, env=None: "fixed-iv")
    monkeypatch.setattr(service_module, "email_repeat_check", lambda session, email: asyncio.sleep(0, result=True))

    result = await service_module.user_register(DummyRequest(headers={"sec-ch-ua-platform": "Windows"}), build_register_model())

    assert result == (StandardBusinessEnum.FAIL.value[0], "邮箱已存在")


@pytest.mark.asyncio
async def test_user_register_returns_fail_when_user_exists(monkeypatch):
    async def fake_decrypt(value):
        return {"enc-phone": "13800000000", "enc-email": "user@example.com", "enc-password": "Passw0rd!"}[value]

    async def fake_encrypt(value, iv=""):
        return f"enc:{value}:{iv}"

    monkeypatch.setattr(service_module, "decrypt", fake_decrypt)
    monkeypatch.setattr(service_module, "encrypt", fake_encrypt)
    monkeypatch.setattr(service_module, "get_env_val", lambda key, env=None: "fixed-iv")
    monkeypatch.setattr(service_module, "email_repeat_check", lambda session, email: asyncio.sleep(0, result=False))
    monkeypatch.setattr(service_module, "user_alive", lambda session, data: asyncio.sleep(0, result=(StandardBusinessEnum.SUCCESS.value[0], "uid-1")))

    result = await service_module.user_register(DummyRequest(headers={"sec-ch-ua-platform": "Windows"}), build_register_model())

    assert result == (StandardBusinessEnum.FAIL.value[0], "用户已存在")


@pytest.mark.asyncio
async def test_user_register_returns_success_when_create_succeeds(monkeypatch):
    captured = {}

    async def fake_decrypt(value):
        return {"enc-phone": "13800000000", "enc-email": "user@example.com", "enc-password": "Passw0rd!"}[value]

    async def fake_encrypt(value, iv=""):
        return f"enc:{value}:{iv}"

    async def fake_user_create(session, template):
        captured["template"] = template
        return StandardBusinessEnum.SUCCESS.value[0]

    monkeypatch.setattr(service_module, "decrypt", fake_decrypt)
    monkeypatch.setattr(service_module, "encrypt", fake_encrypt)
    monkeypatch.setattr(service_module, "get_env_val", lambda key, env=None: "fixed-iv")
    monkeypatch.setattr(service_module, "generate_uid", lambda: "uid-fixed")
    monkeypatch.setattr(service_module, "email_repeat_check", lambda session, email: asyncio.sleep(0, result=False))
    monkeypatch.setattr(service_module, "user_alive", lambda session, data: asyncio.sleep(0, result=(StandardBusinessEnum.UNREGISTERED.value[0], "用户未注册")))
    monkeypatch.setattr(service_module, "user_create", fake_user_create)

    result = await service_module.user_register(DummyRequest(headers={"sec-ch-ua-platform": "Windows"}), build_register_model())

    assert result == (StandardBusinessEnum.SUCCESS.value[0], "用户注册成功")
    assert captured["template"].uid == "uid-fixed"
    assert captured["template"].username == "用户13800000000"
    assert captured["template"].phone == "enc:13800000000:fixed-iv"


@pytest.mark.asyncio
async def test_user_login_returns_fail_when_platform_header_missing():
    result = await service_module.user_login(DummyRequest(), build_login_model())

    assert result == (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")


@pytest.mark.asyncio
async def test_user_login_returns_unregistered_when_repository_reports_unregistered(monkeypatch):
    async def fake_decrypt(value):
        return {"enc-phone": "13800000000", "enc-password": "Passw0rd!"}[value]

    async def fake_encrypt(value, iv=""):
        return f"enc:{value}:{iv}"

    monkeypatch.setattr(service_module, "decrypt", fake_decrypt)
    monkeypatch.setattr(service_module, "encrypt", fake_encrypt)
    monkeypatch.setattr(service_module, "get_env_val", lambda key, env=None: "fixed-iv")
    monkeypatch.setattr(service_module, "user_alive", lambda session, data: asyncio.sleep(0, result=(StandardBusinessEnum.UNREGISTERED.value[0], "用户未注册")))

    result = await service_module.user_login(DummyRequest(headers={"sec-ch-ua-platform": "Windows"}), build_login_model())

    assert result == (StandardBusinessEnum.UNREGISTERED.value[0], "用户未注册")


@pytest.mark.asyncio
async def test_user_login_returns_pwderror_when_repository_reports_wrong_password(monkeypatch):
    async def fake_decrypt(value):
        return {"enc-phone": "13800000000", "enc-password": "Passw0rd!"}[value]

    async def fake_encrypt(value, iv=""):
        return f"enc:{value}:{iv}"

    monkeypatch.setattr(service_module, "decrypt", fake_decrypt)
    monkeypatch.setattr(service_module, "encrypt", fake_encrypt)
    monkeypatch.setattr(service_module, "get_env_val", lambda key, env=None: "fixed-iv")
    monkeypatch.setattr(service_module, "user_alive", lambda session, data: asyncio.sleep(0, result=(StandardBusinessEnum.PWDERROR.value[0], "密码错误")))

    result = await service_module.user_login(DummyRequest(headers={"sec-ch-ua-platform": "Windows"}), build_login_model())

    assert result == (StandardBusinessEnum.PWDERROR.value[0], "密码错误")


@pytest.mark.asyncio
async def test_user_login_returns_success_and_token_when_credentials_valid(monkeypatch):
    captured = {}

    async def fake_decrypt(value):
        return {"enc-phone": "13800000000", "enc-password": "Passw0rd!"}[value]

    async def fake_encrypt(value, iv=""):
        return f"enc:{value}:{iv}"

    async def fake_create_access_token(token_info):
        captured["token_info"] = token_info
        return "signed-token"

    monkeypatch.setattr(service_module, "decrypt", fake_decrypt)
    monkeypatch.setattr(service_module, "encrypt", fake_encrypt)
    monkeypatch.setattr(service_module, "get_env_val", lambda key, env=None: "fixed-iv")
    monkeypatch.setattr(service_module, "user_alive", lambda session, data: asyncio.sleep(0, result=(StandardBusinessEnum.SUCCESS.value[0], "uid-1")))
    monkeypatch.setattr(service_module, "create_access_token", fake_create_access_token)

    result = await service_module.user_login(DummyRequest(headers={"sec-ch-ua-platform": "Windows"}), build_login_model())

    assert result == (StandardBusinessEnum.SUCCESS.value[0], "登录成功", {"token": "signed-token"})
    assert captured["token_info"].uid == "uid-1"
    assert captured["token_info"].exp > 0
