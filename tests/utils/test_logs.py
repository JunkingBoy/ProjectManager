import builtins
import logging
import sys
import types

import pytest

import utils.Logs as logs_module
from utils.Logs import ExceptionLog


class DummyRichHandler(logging.Handler):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs


def reset_exception_log_state():
    ExceptionLog._ExceptionLog__INSTANCE = None # type: ignore
    logger = logging.getLogger("ExceptionLog")
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()
    logger.setLevel(logging.NOTSET)


def setup_function():
    reset_exception_log_state()


def teardown_function():
    reset_exception_log_state()


def test_get_instance_returns_singleton(monkeypatch):
    calls = []

    def fake_create_dir(path):
        calls.append(path)
        return f"/tmp/{path}"

    monkeypatch.setattr(logs_module, "create_dir", fake_create_dir)

    first = ExceptionLog.get_instance()
    second = ExceptionLog.get_instance()

    assert first is second
    assert calls == ["logs/err", "logs/info"]


def test_exception_log_uses_rich_handler_when_available(monkeypatch):
    monkeypatch.setattr(logs_module, "create_dir", lambda path: f"/tmp/{path}")
    rich_module = types.ModuleType("rich.logging")
    rich_module.RichHandler = DummyRichHandler # type: ignore
    monkeypatch.setitem(sys.modules, "rich.logging", rich_module)

    instance = ExceptionLog()

    handlers = instance._logger.handlers
    assert len(handlers) == 1
    assert isinstance(handlers[0], DummyRichHandler)
    assert handlers[0].level == logging.ERROR


def test_exception_log_falls_back_to_file_handlers_when_rich_is_missing(monkeypatch, tmp_path):
    def fake_create_dir(path):
        target = tmp_path.joinpath(path.replace("/", "_"))
        target.mkdir(parents=True, exist_ok=True)
        return target.as_posix()

    monkeypatch.setattr(logs_module, "create_dir", fake_create_dir)
    monkeypatch.delitem(sys.modules, "rich.logging", raising=False)

    original_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "rich.logging":
            raise ImportError("rich not installed")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    instance = ExceptionLog()

    handlers = instance._logger.handlers
    assert len(handlers) == 2
    assert all(isinstance(handler, logging.FileHandler) for handler in handlers)
    assert sorted(handler.level for handler in handlers) == [logging.INFO, logging.ERROR]


def test_exception_log_raises_when_log_directory_creation_fails(monkeypatch):
    monkeypatch.setattr(logs_module, "create_dir", lambda path: None)

    with pytest.raises(Exception, match="日志目录创建失败"):
        ExceptionLog()


def test_exception_log_skips_reinitialization_when_logger_already_has_handlers(monkeypatch):
    monkeypatch.setattr(logs_module, "create_dir", lambda path: f"/tmp/{path}")
    logger = logging.getLogger("ExceptionLog")
    existing_handler = logging.StreamHandler()
    logger.addHandler(existing_handler)

    instance = ExceptionLog()

    assert instance._logger is logger
    assert logger.handlers == [existing_handler]
