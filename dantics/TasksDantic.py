from typing import Annotated
from pydantic import Field, field_validator, ConfigDict

from dantics.GlobalDantic import CoreModel
from enums.StandardBusEnum import StandardTaskTerminalEnum, StandardDevTasksStatusEnum

class TasksAdd(CoreModel):
    model_config = ConfigDict(from_attributes=True)

    req_id: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=256,
        description="关联需求ID加密值"
    )]
    terminal: Annotated[int, Field(
        ...,
        description="终端类型,0:后台1:安卓2:iOS3:小程序4:H5"
    )]
    title: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=128,
        description="任务标题"
    )]
    desc: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=256,
        description="任务描述"
    )]
    dev_total: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=4,
        description="开发工时,浮点字符串"
    )]
    status: Annotated[int, Field(
        ...,
        description="任务状态,0.待处理1.进行中2.已完成3.待修复4.已关闭"
    )]
    owner: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=256,
        description="负责人ID加密值"
    )]
    remark: Annotated[str, Field(
        "",
        max_length=256,
        description="任务备注"
    )]
    end_time: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=128,
        description="计划结束时间,秒级时间戳"
    )]

    @field_validator('terminal')
    @classmethod
    def validate_terminal(cls, v: int) -> int:
        valid_values: set = {item.value for item in StandardTaskTerminalEnum}
        if v not in valid_values: raise ValueError('非法终端类型')
        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: int) -> int:
        valid_values: set = {item.value for item in StandardDevTasksStatusEnum}
        if v not in valid_values: raise ValueError('非法任务状态')
        return v

    @field_validator('dev_total')
    @classmethod
    def validate_float_str(cls, v: str) -> str:
        try: float(v)
        except ValueError: raise ValueError(f'"{v}" 为非法浮点字符串')
        return v

class RequirementTask(CoreModel):
    model_config = ConfigDict(from_attributes=True)

    req_id: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=256,
        description="需求ID加密值"
    )]

class TaskStatusChange(CoreModel):
    model_config = ConfigDict(from_attributes=True)

    task_id: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=256,
        description="任务ID加密值"
    )]
    status: Annotated[int, Field(
        ...,
        description="任务状态"
    )]

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: int) -> int:
        valid_values: set = {item.value for item in StandardDevTasksStatusEnum}
        if v not in valid_values: raise ValueError('非法任务状态')
        return v
