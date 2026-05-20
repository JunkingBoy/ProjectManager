from typing import Annotated
from pydantic_core import core_schema
from pydantic import Field, field_validator, ConfigDict

from dantics.GlobalDantic import CoreModel

class UserRegister(CoreModel):
    model_config = ConfigDict(from_attributes=True)

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

class UserToken(CoreModel):
    model_config = ConfigDict(from_attributes=True)

    uid: Annotated[str, Field(
        ...,
        description="用户ID加密值",
    )]
    exp: Annotated[str, Field(
        ...,
        description="用户过期时间戳"
    )]
