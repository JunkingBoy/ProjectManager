import importlib
import sys
import time
import types

import pytest

from enums.StandardBusEnum import StandardBusinessEnum


class DummyLogger:
    def __init__(self):
        self.messages = []

    def error(self, message):
        self.messages.append(message)


class FakeJWTError(Exception):
    pass


class FakeExpiredSignatureError(FakeJWTError):
    pass


class FakeJWTModule:
    @staticmethod
    def encode(data, secret):
        if secret == "boom":
            raise RuntimeError("encode failed")
        return f"token::{data['uid']}::{data['exp']}::{secret}"

    @staticmethod
    def decode(token, secret):
        if token == "bad.token":
            raise FakeJWTError("bad token")
        if token == "expired.token":
            raise FakeExpiredSignatureError("expired")
        if token == "boom.token":
            raise RuntimeError("decode boom")
        _, uid, exp, used_secret = token.split("::")
        if used_secret != secret:
            raise FakeJWTError("wrong secret")
        return {"uid": uid, "exp": int(exp)}


class FakeHTTPException(Exception):
    def __init__(self, status_code, detail):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


def load_jwt_module():
    sys.modules.pop("utils.JWT", None)
    sys.modules.pop("utils.Excptions", None)

    jose_module = types.ModuleType("jose")
    jose_module.jwt = FakeJWTModule
    jose_module.JWTError = FakeJWTError
    jose_module.ExpiredSignatureError = FakeExpiredSignatureError

    fastapi_module = types.ModuleType("fastapi")
    fastapi_module.HTTPException = FakeHTTPException

    sys.modules["jose"] = jose_module
    sys.modules["fastapi"] = fastapi_module

    jwt_module = importlib.import_module("utils.JWT")
    exceptions_module = importlib.import_module("utils.Excptions")
    return jwt_module, exceptions_module.DivExcep


jwt_module, DivExcep = load_jwt_module()
StandardTokenInfoTemplate = importlib.import_module("templates.StandardSysTemplate").StandardTokenInfoTemplate


@pytest.mark.asyncio
async def test_create_access_token_returns_encoded_token(monkeypatch):
    monkeypatch.setattr(jwt_module, "get_env_val", lambda key, env=None: "secret-key")
    token_info = StandardTokenInfoTemplate(uid="uid-1", exp=int(time.time()) + 3600)

    token = await jwt_module.create_access_token(token_info)
    decoded = jwt_module.jwt.decode(token, "secret-key")

    assert isinstance(token, str)
    assert decoded["uid"] == "uid-1"


@pytest.mark.asyncio
async def test_verify_access_token_returns_success_and_payload_for_valid_token(monkeypatch):
    monkeypatch.setattr(jwt_module, "get_env_val", lambda key, env=None: "secret-key")
    token = jwt_module.jwt.encode({"uid": "uid-1", "exp": int(time.time()) + 3600}, "secret-key")

    code, payload = await jwt_module.verify_access_token(token)

    assert code == StandardBusinessEnum.SUCCESS.value[0]
    assert payload["uid"] == "uid-1"


@pytest.mark.asyncio
async def test_verify_access_token_returns_invalid_for_malformed_token(monkeypatch):
    monkeypatch.setattr(jwt_module, "get_env_val", lambda key, env=None: "secret-key")

    result = await jwt_module.verify_access_token("bad.token")

    assert result == (StandardBusinessEnum.INVALID.value[0], StandardBusinessEnum.INVALID.value[1])


@pytest.mark.asyncio
async def test_verify_access_token_returns_expired_for_expired_token(monkeypatch):
    monkeypatch.setattr(jwt_module, "get_env_val", lambda key, env=None: "secret-key")

    result = await jwt_module.verify_access_token("expired.token")

    assert result == (StandardBusinessEnum.EXPIRED.value[0], StandardBusinessEnum.EXPIRED.value[1])


@pytest.mark.asyncio
async def test_create_access_token_raises_divexcep_when_secret_lookup_fails(monkeypatch):
    logger = DummyLogger()
    monkeypatch.setattr(jwt_module.ExceptionLog, "get_instance", classmethod(lambda cls: logger))
    monkeypatch.setattr(jwt_module, "get_env_val", lambda key, env=None: "boom")

    with pytest.raises(DivExcep, match="创建token失败"):
        await jwt_module.create_access_token(StandardTokenInfoTemplate(uid="uid-1", exp=int(time.time()) + 3600))

    assert logger.messages == ["创建token失败: encode failed"]


@pytest.mark.asyncio
async def test_verify_access_token_raises_divexcep_on_unexpected_decode_error(monkeypatch):
    logger = DummyLogger()
    monkeypatch.setattr(jwt_module.ExceptionLog, "get_instance", classmethod(lambda cls: logger))
    monkeypatch.setattr(jwt_module, "get_env_val", lambda key, env=None: "secret-key")

    with pytest.raises(DivExcep, match="验证token失败"):
        await jwt_module.verify_access_token("boom.token")

    assert logger.messages == ["验证token失败: decode boom"]
