from typing import Annotated
from pydantic import Field, field_validator, ConfigDict

from tools.Re import is_valid_username
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
    role: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=128,
        description="用户角色加密值"
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
    def info(self) -> dict: return self.model_dump()

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
    def info(self) -> dict: return self.model_dump()

class UserToken(CoreModel):
    model_config = ConfigDict(from_attributes=True)

    uid: Annotated[str, Field(
        ...,
        description="用户ID加密值",
    )]
    exp: Annotated[int, Field(
        ...,
        description="Token过期时间戳"
    )]

    @property
    def info(self) -> dict: return self.model_dump()

class UserModify(CoreModel):
    model_config = ConfigDict(from_attributes=True)

    username: Annotated[str, Field(
        ...,
        min_length=2,
        max_length=13,
        description="用户名明文"
    )]
    new_password: Annotated[str | None, Field(
        None,
        min_length=36,
        max_length=60,
        description="用户密码加密值(为空默认不修改密码)"
    )]

    @property
    def info(self) -> dict: return self.model_dump()

    @field_validator("username")
    @classmethod
    def vertry_username_match(cls, v: str) -> str:
        if not is_valid_username(v): raise ValueError("非法用户名")
        else: return v
