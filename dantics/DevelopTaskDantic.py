from typing import Annotated, Optional
from pydantic import Field

from dantics.GlobalDantic import CoreModel


class DevelopTaskCreate(CoreModel):
    requirement_id: Annotated[str, Field(..., min_length=1, max_length=128, description="关联需求ID")]
    point_id: Annotated[Optional[str], Field(default=None, max_length=128, description="关联功能点ID")]
    title: Annotated[str, Field(..., min_length=1, max_length=128, description="任务标题")]
    description: Annotated[Optional[str], Field(default=None, max_length=2000, description="任务描述")]
    creator: Annotated[Optional[str], Field(default=None, max_length=32, description="任务创建者")]
    owner: Annotated[Optional[str], Field(default=None, max_length=32, description="任务负责人")]

    @property
    def info(self) -> dict:
        return self.__dict__.copy()


class DevelopTaskUpdate(CoreModel):
    point_id: Annotated[Optional[str], Field(default=None, max_length=128, description="关联功能点ID")]
    title: Annotated[Optional[str], Field(default=None, min_length=1, max_length=128, description="任务标题")]
    description: Annotated[Optional[str], Field(default=None, max_length=2000, description="任务描述")]
    status: Annotated[Optional[int], Field(default=None, ge=1, le=4, description="任务状态")]
    owner: Annotated[Optional[str], Field(default=None, max_length=32, description="任务负责人")]

    @property
    def info(self) -> dict:
        return self.__dict__.copy()
