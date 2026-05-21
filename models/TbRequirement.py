from . import BaseModel, UTCTime

from typing import cast
from copy import deepcopy
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text

from templates.StandardDBTemplate import TbRequirementTemplate


class Requirement(BaseModel):
    __tablename__ = 'requirements'

    id: Column[int] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="需求表自增ID,自增主键"
    )
    requirement_id: str = cast(str, Column(
        String(128),
        unique=True,
        index=True,
        nullable=False,
        comment="需求ID,需求唯一标识"
    ))
    number: str = cast(str, Column(
        String(128),
        unique=False,
        index=True,
        nullable=False,
        comment="需求编号"
    ))
    title: str = cast(str, Column(
        String(128),
        nullable=False,
        comment="需求标题"
    ))
    description: str = cast(str, Column(
        Text,
        nullable=True,
        comment="需求描述"
    ))
    source: int = cast(int, Column(
        Integer,
        default=0,
        nullable=False,
        comment="需求来源,0:手动创建,1:第三方接入"
    ))
    status: int = cast(int, Column(
        Integer,
        default=0,
        nullable=False,
        comment="需求状态,0.待领取1.设计中2.开发中3.测试中4.已上线5.废弃"
    ))
    person: str = cast(str, Column(
        String(32),
        nullable=True,
        comment="需求处理人(创建者)"
    ))
    relevant: str = cast(str, Column(
        Text,
        nullable=True,
        comment="需求负责技术经理(JSON数组)"
    ))
    total: str = cast(str, Column(
        String(128),
        nullable=True,
        comment="需求总工时"
    ))
    develop: str = cast(str, Column(
        String(128),
        nullable=True,
        comment="需求开发工时"
    ))
    test: str = cast(str, Column(
        String(128),
        nullable=True,
        comment="需求测试工时"
    ))
    priority: int = cast(int, Column(
        Integer,
        default=2,
        nullable=True,
        comment="优先级,1:高,2:中,3:低"
    ))
    iteration: str = cast(str, Column(
        String(128),
        nullable=True,
        comment="发布迭代"
    ))
    project: str = cast(str, Column(
        String(128),
        nullable=True,
        comment="所属项目"
    ))
    scheme: str = cast(str, Column(
        Text,
        nullable=True,
        comment="需求方案"
    ))
    c_time: Column[datetime] = Column(
        DateTime(timezone=False),
        default=lambda: datetime.now(tz=UTCTime),
        nullable=False,
        comment="创建时间,默认为数据插入时间,时区为UTC"
    )
    u_time: Column[datetime] = Column(
        DateTime(timezone=False),
        default=lambda: datetime.now(tz=UTCTime),
        onupdate=lambda: datetime.now(tz=UTCTime),
        nullable=False,
        comment="更新时间,初始默认为数据插入时间,时区为UTC"
    )

    def __init__(
        self,
        data: TbRequirementTemplate
    ) -> None:
        self.requirement_id = data.requirement_id
        self.number = data.number
        self.title = data.title
        self.description = data.description
        self.source = data.source
        self.status = data.status
        self.person = data.person
        self.relevant = data.relevant
        self.total = data.total
        self.develop = data.develop
        self.test = data.test
        self.priority = data.priority
        self.iteration = data.iteration
        self.project = data.project
        self.scheme = data.scheme

    @property
    def info(self) -> dict:
        return deepcopy(self.__dict__)
