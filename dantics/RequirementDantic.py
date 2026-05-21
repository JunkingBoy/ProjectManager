from typing import Annotated, Optional
from pydantic import Field

from dantics.GlobalDantic import CoreModel


class RequirementCreate(CoreModel):
    number: Annotated[str, Field(..., min_length=1, max_length=128, description="需求编号")]
    title: Annotated[str, Field(..., min_length=1, max_length=128, description="需求标题")]
    description: Annotated[Optional[str], Field(default=None, max_length=2000, description="需求描述")]
    source: Annotated[int, Field(default=0, ge=0, le=1, description="需求来源,0:手动创建,1:第三方接入")]
    person: Annotated[Optional[str], Field(default=None, max_length=32, description="需求处理人")]
    relevant: Annotated[Optional[str], Field(default=None, description="需求负责技术经理(JSON数组)")]
    total: Annotated[Optional[str], Field(default=None, max_length=128, description="需求总工时")]
    develop: Annotated[Optional[str], Field(default=None, max_length=128, description="需求开发工时")]
    test: Annotated[Optional[str], Field(default=None, max_length=128, description="需求测试工时")]
    priority: Annotated[Optional[int], Field(default=2, ge=1, le=3, description="优先级,1:高,2:中,3:低")]
    iteration: Annotated[Optional[str], Field(default=None, max_length=128, description="发布迭代")]
    project: Annotated[Optional[str], Field(default=None, max_length=128, description="所属项目")]
    scheme: Annotated[Optional[str], Field(default=None, description="需求方案")]

    @property
    def info(self) -> dict:
        return self.__dict__.copy()


class RequirementUpdate(CoreModel):
    title: Annotated[Optional[str], Field(default=None, min_length=1, max_length=128, description="需求标题")]
    description: Annotated[Optional[str], Field(default=None, max_length=2000, description="需求描述")]
    status: Annotated[Optional[int], Field(default=None, ge=0, le=5, description="需求状态")]
    person: Annotated[Optional[str], Field(default=None, max_length=32, description="需求处理人")]
    relevant: Annotated[Optional[str], Field(default=None, description="需求负责技术经理")]
    total: Annotated[Optional[str], Field(default=None, max_length=128, description="需求总工时")]
    develop: Annotated[Optional[str], Field(default=None, max_length=128, description="需求开发工时")]
    test: Annotated[Optional[str], Field(default=None, max_length=128, description="需求测试工时")]
    priority: Annotated[Optional[int], Field(default=None, ge=1, le=3, description="优先级")]
    iteration: Annotated[Optional[str], Field(default=None, max_length=128, description="发布迭代")]
    project: Annotated[Optional[str], Field(default=None, max_length=128, description="所属项目")]
    scheme: Annotated[Optional[str], Field(default=None, description="需求方案")]

    @property
    def info(self) -> dict:
        return self.__dict__.copy()


class RequirementListQuery(CoreModel):
    status: Annotated[Optional[int], Field(default=None, ge=0, le=5, description="需求状态筛选")]
    project: Annotated[Optional[str], Field(default=None, max_length=128, description="所属项目筛选")]
    person: Annotated[Optional[str], Field(default=None, max_length=32, description="处理人筛选")]
    keyword: Annotated[Optional[str], Field(default=None, max_length=128, description="标题/编号关键词")]

    @property
    def info(self) -> dict:
        return self.__dict__.copy()


class RequirementClaim(CoreModel):
    person: Annotated[str, Field(..., min_length=1, max_length=32, description="领取人")]

    @property
    def info(self) -> dict:
        return self.__dict__.copy()


class RequirementBind(CoreModel):
    person: Annotated[str, Field(..., min_length=1, max_length=32, description="绑定处理人")]
    relevant: Annotated[Optional[str], Field(default=None, description="负责技术经理(JSON数组)")]

    @property
    def info(self) -> dict:
        return self.__dict__.copy()
