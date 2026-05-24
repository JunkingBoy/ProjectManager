from typing import Annotated
from pydantic import Field, field_validator, ConfigDict

from dantics.GlobalDantic import CoreModel
from enums.StandardBusEnum import StandardBugStatusEnum

class BugQuery(CoreModel):
    model_config = ConfigDict(from_attributes=True, extra='forbid')

    req_id: str | None = None
    task_id: str | None = None
    status: int | None = None
    creator: str | None = None
    owner: str | None = None
    developer: str | None = None
    filter_self_created: bool = False
    filter_self_assigned: bool = False

class BugAdd(CoreModel):
    model_config = ConfigDict(from_attributes=True)

    req_id: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=256,
        description="关联需求ID加密值"
    )]
    task_id: Annotated[str, Field(
        "",
        max_length=256,
        description="关联任务ID加密值"
    )]
    title: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=128,
        description="Bug标题"
    )]
    desc: Annotated[str, Field(
        "",
        max_length=1024,
        description="Bug描述"
    )]
    expected_res: Annotated[str, Field(
        "",
        max_length=1024,
        description="预期结果"
    )]
    status: Annotated[int, Field(
        ...,
        description="Bug状态,0.未修复1.已修复2.研发确认非Bug3.已关闭"
    )]
    owner: Annotated[str, Field(
        "",
        max_length=256,
        description="测试负责人ID加密值"
    )]
    developer: Annotated[str, Field(
        "",
        max_length=256,
        description="关联开发ID加密值"
    )]

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: int) -> int:
        valid_values: set = {item.value for item in StandardBugStatusEnum}
        if v not in valid_values: raise ValueError('非法Bug状态')
        return v

class BugFilterQuery(CoreModel):
    model_config = ConfigDict(from_attributes=True, extra='forbid')

    req_id: str | None = None
    task_id: str | None = None
    status: int | None = None

class BugDetail(CoreModel):
    model_config = ConfigDict(from_attributes=True)

    bug_id: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=256,
        description="BugID加密值"
    )]

class BugModify(CoreModel):
    model_config = ConfigDict(from_attributes=True)

    bug_id: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=256,
        description="BugID加密值"
    )]
    title: Annotated[str, Field(
        "",
        max_length=128,
        description="Bug标题"
    )]
    desc: Annotated[str, Field(
        "",
        max_length=1024,
        description="Bug描述"
    )]
    expected_res: Annotated[str, Field(
        "",
        max_length=1024,
        description="预期结果"
    )]
    owner: Annotated[str, Field(
        "",
        max_length=256,
        description="测试负责人ID加密值"
    )]
    developer: Annotated[str, Field(
        "",
        max_length=256,
        description="关联开发ID加密值"
    )]


class BugStatusChange(CoreModel):
    model_config = ConfigDict(from_attributes=True)

    bug_id: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=256,
        description="BugID加密值"
    )]
    status: Annotated[int, Field(
        ...,
        description="Bug状态,0.未修复1.已修复2.研发确认非Bug3.已关闭"
    )]

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: int) -> int:
        valid_values: set = {item.value for item in StandardBugStatusEnum}
        if v not in valid_values: raise ValueError('非法Bug状态')
        return v
