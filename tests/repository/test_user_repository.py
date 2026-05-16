import asyncio
import importlib
import sys
import types

import pytest

from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardDBTemplate import TbUserTemplate
from templates.StandardRepositoryTemplate import StandardUserRepositoryTemplate


class FakeHTTPException(Exception):
    def __init__(self, status_code, detail):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


class FakeSQLAlchemyError(Exception):
    pass


class DummyColumn:
    def __eq__(self, other):
        return other


class DummyUser:
    phone = DummyColumn()
    email = DummyColumn()
    active = DummyColumn()
    deleted = DummyColumn()

    def __init__(self, uid="uid-1", password="stored"):
        self.uid = uid
        self.password = password
        self.info = {"uid": uid}


class FakeResult:
    def __init__(self, value):
        self.value = value

    def scalar_one_or_none(self):
        return self.value


class FakeSession:
    def __init__(self, result=None, error=None, commit_error=None):
        self.result = result
        self.error = error
        self.commit_error = commit_error
        self.rollback_called = False
        self.added = []
        self.refreshed = []

    async def execute(self, _query):
        if self.error:
            raise self.error
        return FakeResult(self.result)

    def add(self, item):
        self.added.append(item)

    async def commit(self):
        if self.commit_error:
            raise self.commit_error

    async def refresh(self, item):
        self.refreshed.append(item)

    async def rollback(self):
        self.rollback_called = True


class DummyLogger:
    def __init__(self):
        self.messages = []

    def error(self, message):
        self.messages.append(message)

    def info(self, message):
        self.messages.append(message)


class DummyExceptionLog:
    @staticmethod
    def get_instance():
        return DummyLogger()


class DummyQuery:
    def where(self, *_args, **_kwargs):
        return self


def load_repository_module():
    sys.modules.pop("repository.UserRepository", None)
    sys.modules.pop("utils.Excptions", None)

    fastapi_module = types.ModuleType("fastapi")
    fastapi_module.HTTPException = FakeHTTPException

    sqlalchemy_module = types.ModuleType("sqlalchemy")
    sqlalchemy_module.select = lambda *_args, **_kwargs: DummyQuery()
    sqlalchemy_module.and_ = lambda *args, **kwargs: (args, kwargs)

    sqlalchemy_sql_module = types.ModuleType("sqlalchemy.sql")
    sqlalchemy_sql_module.Select = DummyQuery

    sqlalchemy_engine_module = types.ModuleType("sqlalchemy.engine")
    sqlalchemy_engine_module.Result = FakeResult

    sqlalchemy_exc_module = types.ModuleType("sqlalchemy.exc")
    sqlalchemy_exc_module.SQLAlchemyError = FakeSQLAlchemyError

    sqlalchemy_ext_module = types.ModuleType("sqlalchemy.ext")
    sqlalchemy_asyncio_module = types.ModuleType("sqlalchemy.ext.asyncio")
    sqlalchemy_asyncio_module.AsyncSession = FakeSession

    models_tb_user_module = types.ModuleType("models.TbUser")
    models_tb_user_module.User = DummyUser

    encry_module = types.ModuleType("utils.Encry")
    encry_module.decrypt = lambda password: asyncio.sleep(0, result=password)

    logs_module = types.ModuleType("utils.Logs")
    logs_module.ExceptionLog = DummyExceptionLog

    sys.modules["fastapi"] = fastapi_module
    sys.modules["sqlalchemy"] = sqlalchemy_module
    sys.modules["sqlalchemy.sql"] = sqlalchemy_sql_module
    sys.modules["sqlalchemy.engine"] = sqlalchemy_engine_module
    sys.modules["sqlalchemy.exc"] = sqlalchemy_exc_module
    sys.modules["sqlalchemy.ext"] = sqlalchemy_ext_module
    sys.modules["sqlalchemy.ext.asyncio"] = sqlalchemy_asyncio_module
    sys.modules["models.TbUser"] = models_tb_user_module
    sys.modules["utils.Encry"] = encry_module
    sys.modules["utils.Logs"] = logs_module

    repository_module = importlib.import_module("repository.UserRepository")
    div_excep = importlib.import_module("utils.Excptions").DivExcep
    return repository_module, div_excep


repository_module, DivExcep = load_repository_module()


@pytest.mark.asyncio
async def test_email_repeat_check_returns_true_when_user_exists():
    session = FakeSession(result=DummyUser())

    result = await repository_module.email_repeat_check(session, "email")

    assert result is True


@pytest.mark.asyncio
async def test_email_repeat_check_returns_false_when_user_missing():
    session = FakeSession(result=None)

    result = await repository_module.email_repeat_check(session, "email")

    assert result is False


@pytest.mark.asyncio
async def test_email_repeat_check_raises_divexcep_on_sqlalchemy_error(monkeypatch):
    logger = DummyLogger()
    monkeypatch.setattr(repository_module.ExceptionLog, "get_instance", staticmethod(lambda: logger))
    session = FakeSession(error=FakeSQLAlchemyError("boom"))

    with pytest.raises(DivExcep, match="邮箱数据查询异常"):
        await repository_module.email_repeat_check(session, "email")

    assert logger.messages == ["邮箱数据查询异常boom"]


@pytest.mark.asyncio
async def test_user_alive_returns_unregistered_when_user_missing():
    session = FakeSession(result=None)
    payload = StandardUserRepositoryTemplate(uid=None, phone="phone", email=None, password="pwd")

    result = await repository_module.user_alive(session, payload)

    assert result == (StandardBusinessEnum.UNREGISTERED.value[0], StandardBusinessEnum.UNREGISTERED.value[1])


@pytest.mark.asyncio
async def test_user_alive_returns_pwderror_when_password_mismatch(monkeypatch):
    monkeypatch.setattr(repository_module, "decrypt", lambda password: asyncio.sleep(0, result="other-pwd"))
    session = FakeSession(result=DummyUser(password="stored"))
    payload = StandardUserRepositoryTemplate(uid=None, phone="phone", email=None, password="pwd")

    result = await repository_module.user_alive(session, payload)

    assert result == (StandardBusinessEnum.PWDERROR.value[0], StandardBusinessEnum.PWDERROR.value[1])


@pytest.mark.asyncio
async def test_user_alive_returns_success_and_uid_when_password_matches(monkeypatch):
    monkeypatch.setattr(repository_module, "decrypt", lambda password: asyncio.sleep(0, result="pwd"))
    session = FakeSession(result=DummyUser(uid="uid-9", password="stored"))
    payload = StandardUserRepositoryTemplate(uid=None, phone="phone", email=None, password="pwd")

    result = await repository_module.user_alive(session, payload)

    assert result == (StandardBusinessEnum.SUCCESS.value[0], "uid-9")


@pytest.mark.asyncio
async def test_user_create_returns_success_and_persists_user(monkeypatch):
    monkeypatch.setattr(repository_module, "User", lambda user: DummyUser(uid=user.uid, password=user.password))
    session = FakeSession()
    template = TbUserTemplate(uid="uid-1", username="name", phone="phone", email="mail", password="pwd")

    result = await repository_module.user_create(session, template)

    assert result == StandardBusinessEnum.SUCCESS.value[0]
    assert len(session.added) == 1
    assert session.refreshed == session.added


@pytest.mark.asyncio
async def test_user_create_rolls_back_and_raises_divexcep_on_sqlalchemy_error(monkeypatch):
    logger = DummyLogger()
    monkeypatch.setattr(repository_module.ExceptionLog, "get_instance", staticmethod(lambda: logger))
    monkeypatch.setattr(repository_module, "User", lambda user: DummyUser(uid=user.uid, password=user.password))
    session = FakeSession(commit_error=FakeSQLAlchemyError("commit failed"))
    template = TbUserTemplate(uid="uid-1", username="name", phone="phone", email="mail", password="pwd")

    with pytest.raises(DivExcep, match="用户创建数据库异常"):
        await repository_module.user_create(session, template)

    assert session.rollback_called is True
    assert logger.messages == ["用户创建数据库异常commit failed"]
