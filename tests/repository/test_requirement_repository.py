import asyncio
import importlib
import sys
import types

import pytest

from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardDBTemplate import TbRequirementTemplate


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

    def ilike(self, other):
        return other


class DummyRequirement:
    requirement_id = DummyColumn()
    status = DummyColumn()
    title = DummyColumn()
    project = DummyColumn()
    person = DummyColumn()
    c_time = DummyColumn()

    def __init__(self, requirement_id="req-1", status=0):
        self.requirement_id = requirement_id
        self.status = status
        self.info = {"requirement_id": requirement_id, "status": status}


class FakeResult:
    def __init__(self, value=None, all_values=None):
        self.value = value
        self.all_values = all_values or []

    def scalar_one_or_none(self):
        return self.value

    def scalars(self):
        return FakeScalars(self.all_values)


class FakeScalars:
    def __init__(self, values):
        self.values = values

    def all(self):
        return self.values


class FakeSession:
    def __init__(self, result=None, all_results=None, error=None, commit_error=None):
        self.result = result
        self.all_results = all_results or []
        self.error = error
        self.commit_error = commit_error
        self.rollback_called = False
        self.added = []
        self.refreshed = []

    async def execute(self, _query):
        if self.error:
            raise self.error
        return FakeResult(self.result, self.all_results)

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

    def order_by(self, *_args, **_kwargs):
        return self


def load_repository_module():
    sys.modules.pop("repository.RequirementRepository", None)
    sys.modules.pop("utils.Excptions", None)

    fastapi_module = types.ModuleType("fastapi")
    fastapi_module.HTTPException = FakeHTTPException

    sqlalchemy_module = types.ModuleType("sqlalchemy")
    sqlalchemy_module.select = lambda *_args, **_kwargs: DummyQuery()
    sqlalchemy_module.and_ = lambda *args, **kwargs: (args, kwargs)
    sqlalchemy_module.or_ = lambda *args, **kwargs: (args, kwargs)
    sqlalchemy_module.desc = lambda col: col

    sqlalchemy_sql_module = types.ModuleType("sqlalchemy.sql")
    sqlalchemy_sql_module.Select = DummyQuery

    sqlalchemy_engine_module = types.ModuleType("sqlalchemy.engine")
    sqlalchemy_engine_module.Result = FakeResult

    sqlalchemy_exc_module = types.ModuleType("sqlalchemy.exc")
    sqlalchemy_exc_module.SQLAlchemyError = FakeSQLAlchemyError

    sqlalchemy_ext_module = types.ModuleType("sqlalchemy.ext")
    sqlalchemy_asyncio_module = types.ModuleType("sqlalchemy.ext.asyncio")
    sqlalchemy_asyncio_module.AsyncSession = FakeSession

    models_module = types.ModuleType("models.TbRequirement")
    models_module.Requirement = DummyRequirement

    logs_module = types.ModuleType("utils.Logs")
    logs_module.ExceptionLog = DummyExceptionLog

    sys.modules["fastapi"] = fastapi_module
    sys.modules["sqlalchemy"] = sqlalchemy_module
    sys.modules["sqlalchemy.sql"] = sqlalchemy_sql_module
    sys.modules["sqlalchemy.engine"] = sqlalchemy_engine_module
    sys.modules["sqlalchemy.exc"] = sqlalchemy_exc_module
    sys.modules["sqlalchemy.ext"] = sqlalchemy_ext_module
    sys.modules["sqlalchemy.ext.asyncio"] = sqlalchemy_asyncio_module
    sys.modules["models.TbRequirement"] = models_module
    sys.modules["utils.Logs"] = logs_module

    repository_module = importlib.import_module("repository.RequirementRepository")
    div_excep = importlib.import_module("utils.Excptions").DivExcep
    return repository_module, div_excep


repository_module, DivExcep = load_repository_module()


@pytest.mark.asyncio
async def test_requirement_list_returns_results():
    session = FakeSession(all_results=[DummyRequirement("req-1", 0), DummyRequirement("req-2", 1)])
    result = await repository_module.requirement_list(session, status=0)
    assert len(result) == 2


@pytest.mark.asyncio
async def test_requirement_get_returns_requirement_when_exists():
    session = FakeSession(result=DummyRequirement("req-1", 0))
    result = await repository_module.requirement_get(session, "req-1")
    assert result is not None
    assert result.requirement_id == "req-1"


@pytest.mark.asyncio
async def test_requirement_get_returns_none_when_missing():
    session = FakeSession(result=None)
    result = await repository_module.requirement_get(session, "req-1")
    assert result is None


@pytest.mark.asyncio
async def test_requirement_create_returns_success(monkeypatch):
    monkeypatch.setattr(repository_module, "Requirement", lambda data: DummyRequirement(data.requirement_id, 0))
    session = FakeSession()
    template = TbRequirementTemplate(
        requirement_id="req-1",
        number="R001",
        title="测试需求",
        description=None,
        source=0,
        status=0,
        person=None,
        relevant=None,
        total=None,
        develop=None,
        test=None,
        priority=2,
        iteration=None,
        project=None,
        scheme=None,
    )
    result = await repository_module.requirement_create(session, template)
    assert result == StandardBusinessEnum.SUCCESS.value[0]
    assert len(session.added) == 1


@pytest.mark.asyncio
async def test_requirement_update_returns_success(monkeypatch):
    req = DummyRequirement("req-1", 0)
    session = FakeSession(result=req)
    result = await repository_module.requirement_update(session, "req-1", {"title": "新标题"})
    assert result == StandardBusinessEnum.SUCCESS.value[0]


@pytest.mark.asyncio
async def test_requirement_update_raises_when_not_found():
    session = FakeSession(result=None)
    with pytest.raises(DivExcep, match="需求不存在"):
        await repository_module.requirement_update(session, "req-1", {"title": "新标题"})


@pytest.mark.asyncio
async def test_requirement_delete_returns_success():
    req = DummyRequirement("req-1", 0)
    session = FakeSession(result=req)
    result = await repository_module.requirement_delete(session, "req-1")
    assert result == StandardBusinessEnum.SUCCESS.value[0]
    assert req.status == 5
