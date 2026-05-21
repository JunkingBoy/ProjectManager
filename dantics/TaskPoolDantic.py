from typing import Annotated, Optional
from pydantic import Field

from dantics.GlobalDantic import CoreModel


class TaskPoolCreate(CoreModel):
    requirement_id: Annotated[str, Field(..., min_length=1, max_length=128, description="关联需求ID")]
    terminal: Annotated[Optional[str], Field(default=None, max_length=128, description="任务关联开发终端")]
    description: Annotated[Optional[str], Field(default=None, max_length=2000, description="任务描述")]
    develop_total: Annotated[Optional[str], Field(default=None, max_length=128, description="需求开发工时")]
    creator: Annotated[Optional[str], Field(default=None, max_length=32, description="任务创建者")]
    owner: Annotated[Optional[str], Field(default=None, max_length=32, description="任务负责人")]
    remark: Annotated[Optional[str], Field(default=None, description="任务备注")]

    @property
    def info(self) -> dict:
        return self.__dict__.copy()


class TaskPoolUpdate(CoreModel):
    terminal: Annotated[Optional[str], Field(default=None, max_length=128, description="任务关联开发终端")]
    description: Annotated[Optional[str], Field(default=None, max_length=2000, description="任务描述")]
    develop_total: Annotated[Optional[str], Field(default=None, max_length=128, description="需求开发工时")]
    status: Annotated[Optional[int], Field(default=None, ge=1, le=4, description="任务状态")]
    owner: Annotated[Optional[str], Field(default=None, max_length=32, description="任务负责人")]
    remark: Annotated[Optional[str], Field(default=None, description="任务备注")]

    @property
    def info(self) -> dict:
        return self.__dict__.copy()
