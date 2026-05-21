from typing import Annotated, Optional
from pydantic import Field

from dantics.GlobalDantic import CoreModel


class BugCreate(CoreModel):
    requirement_id: Annotated[str, Field(..., min_length=1, max_length=128, description="关联需求ID")]
    task_id: Annotated[Optional[str], Field(default=None, max_length=128, description="关联任务ID")]
    title: Annotated[str, Field(..., min_length=1, max_length=128, description="Bug标题")]
    description: Annotated[Optional[str], Field(default=None, max_length=2000, description="Bug描述")]
    expected_res: Annotated[Optional[str], Field(default=None, description="正确情况下预期结果")]
    creator: Annotated[Optional[str], Field(default=None, max_length=32, description="Bug创建者")]
    owner: Annotated[Optional[str], Field(default=None, max_length=32, description="测试负责人")]
    developer: Annotated[Optional[str], Field(default=None, max_length=32, description="Bug关联开发")]

    @property
    def info(self) -> dict:
        return self.__dict__.copy()


class BugUpdate(CoreModel):
    task_id: Annotated[Optional[str], Field(default=None, max_length=128, description="关联任务ID")]
    title: Annotated[Optional[str], Field(default=None, min_length=1, max_length=128, description="Bug标题")]
    description: Annotated[Optional[str], Field(default=None, max_length=2000, description="Bug描述")]
    expected_res: Annotated[Optional[str], Field(default=None, description="正确情况下预期结果")]
    status: Annotated[Optional[int], Field(default=None, ge=0, le=3, description="Bug状态")]
    owner: Annotated[Optional[str], Field(default=None, max_length=32, description="测试负责人")]
    developer: Annotated[Optional[str], Field(default=None, max_length=32, description="Bug关联开发")]

    @property
    def info(self) -> dict:
        return self.__dict__.copy()
