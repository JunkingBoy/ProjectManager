import importlib
import sys
import types

import pytest


class FakeField:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class FakeValidationInfo:
    def __init__(self, data):
        self.data = data


def fake_field_validator(field_name):
    def decorator(func):
        return classmethod(func)
    return decorator


def load_user_dantic_module():
    sys.modules.pop("dantics.UserDantic", None)

    pydantic_module = types.ModuleType("pydantic")
    pydantic_module.Field = FakeField
    pydantic_module.field_validator = fake_field_validator

    pydantic_core_module = types.ModuleType("pydantic_core")
    pydantic_core_module.core_schema = types.SimpleNamespace(ValidationInfo=FakeValidationInfo)

    global_dantic_module = types.ModuleType("dantics.GlobalDantic")
    global_dantic_module.CoreModel = object

    sys.modules["pydantic"] = pydantic_module
    sys.modules["pydantic_core"] = pydantic_core_module
    sys.modules["dantics.GlobalDantic"] = global_dantic_module

    return importlib.import_module("dantics.UserDantic")


user_dantic_module = load_user_dantic_module()


def build_user_register(password="b" * 36, password_confirm="b" * 36):
    model = user_dantic_module.UserRegister()
    model.phone = "a" * 36
    model.email = "user@example.com"
    model.password = password
    model.password_confirm = password_confirm
    return model


def build_user_login(password="b" * 36):
    model = user_dantic_module.UserLogin()
    model.phone = "a" * 36
    model.password = password
    return model


def test_user_register_info_returns_copy():
    model = build_user_register()

    info = model.info
    info["phone"] = "changed"

    assert model.phone == "a" * 36
    assert info["phone"] == "changed"


def test_user_login_info_returns_copy():
    model = build_user_login()

    info = model.info
    info["phone"] = "changed"

    assert model.phone == "a" * 36
    assert info["phone"] == "changed"


def test_user_register_validator_allows_matching_password_confirm():
    result = user_dantic_module.UserRegister.vertry_password_match("same", FakeValidationInfo({"password": "same"}))

    assert result == "same"


def test_user_register_validator_rejects_mismatched_password_confirm():
    with pytest.raises(ValueError, match="两次输入密码不一致"):
        user_dantic_module.UserRegister.vertry_password_match("different", FakeValidationInfo({"password": "same"}))


def test_user_login_has_expected_fields_only():
    assert hasattr(user_dantic_module.UserLogin, "info")
    assert not hasattr(user_dantic_module.UserLogin, "vertry_password")
