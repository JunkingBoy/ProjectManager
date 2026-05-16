import importlib
import sys
import types

from templates.StandardDBTemplate import TbUserTemplate


class FakeColumn:
    def __init__(self, column_type, **kwargs):
        self.column_type = column_type
        self.kwargs = kwargs

    def __class_getitem__(cls, _item):
        return cls


class FakeInteger:
    pass


class FakeString:
    def __init__(self, length):
        self.length = length


class FakeDateTime:
    def __init__(self, timezone=False):
        self.timezone = timezone


def load_user_module():
    for name in ["models.TbUser", "models"]:
        sys.modules.pop(name, None)

    pytz_module = types.ModuleType("pytz")

    class FakeTimezone:
        def __init__(self, zone):
            self.zone = zone

    pytz_module.timezone = lambda zone: FakeTimezone(zone)

    declarative_module = types.ModuleType("sqlalchemy.ext.declarative")
    declarative_module.declarative_base = lambda: type("FakeBase", (), {"metadata": object()})

    sqlalchemy_module = types.ModuleType("sqlalchemy")
    sqlalchemy_module.Column = FakeColumn
    sqlalchemy_module.Integer = FakeInteger
    sqlalchemy_module.String = FakeString
    sqlalchemy_module.DateTime = FakeDateTime

    sys.modules["pytz"] = pytz_module
    sys.modules["sqlalchemy.ext.declarative"] = declarative_module
    sys.modules["sqlalchemy"] = sqlalchemy_module

    return importlib.import_module("models.TbUser")


def build_user_template():
    return TbUserTemplate(
        uid="u-1",
        username="tester",
        phone="13800000000",
        password="secret",
    )


def test_user_init_assigns_template_fields():
    user_module = load_user_module()
    user = user_module.User(build_user_template())

    assert user.uid == "u-1"
    assert user.username == "tester"
    assert user.phone == "13800000000"
    assert user.password == "secret"


def test_user_info_returns_deep_copy():
    user_module = load_user_module()
    user = user_module.User(build_user_template())

    info = user.info
    info["username"] = "changed"

    assert user.username == "tester"
    assert info["username"] == "changed"


def test_user_table_name_is_user():
    user_module = load_user_module()

    assert user_module.User.__tablename__ == "user"


def test_user_declares_expected_columns():
    user_module = load_user_module()

    assert isinstance(user_module.User.id, FakeColumn)
    assert isinstance(user_module.User.uid, FakeColumn)
    assert isinstance(user_module.User.username, FakeColumn)
    assert isinstance(user_module.User.phone, FakeColumn)
    assert isinstance(user_module.User.password, FakeColumn)
    assert isinstance(user_module.User.active, FakeColumn)
    assert isinstance(user_module.User.deleted, FakeColumn)
    assert isinstance(user_module.User.c_time, FakeColumn)
    assert isinstance(user_module.User.u_time, FakeColumn)
