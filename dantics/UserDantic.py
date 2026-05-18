from typing import Annotated
from pydantic_core import core_schema
from pydantic import Field, field_validator

from dantics.GlobalDantic import CoreModel

class UserRegister(CoreModel):
    phone: Annotated[str, Field(
        ...,
        min_length=36,
        max_length=60,
        description="手机号加密值"
    )]
    email: Annotated[str, Field(
        ...,
        min_length=5,
        max_length=64,
        description="邮箱加密值"
    )]
    password: Annotated[str, Field(
        ...,
        min_length=36,
        max_length=60,
        description="用户密码加密值"
    )]
    password_confirm: Annotated[str, Field(
        ...,
        min_length=36,
        max_length=60,
        description="用户确认密码加密值"
    )]

    @property
    def info(self) -> dict: return self.__dict__.copy()

    @field_validator("password_confirm")
    def vertry_password_match(cls, v: str, values: core_schema.ValidationInfo) -> str:
        if "password" in values.data and v != values.data["password"]: raise ValueError("两次输入密码不一致")
        else: return v

class UserLogin(CoreModel):
    phone: Annotated[str, Field(
        ...,
        min_length=36,
        max_length=60,
        description="手机号加密值"
    )]
    password: Annotated[str, Field(
        ...,
        min_length=36,
        max_length=60,
        description="用户密码加密值"
    )]

    @property
    def info(self) -> dict: return self.__dict__.copy()
