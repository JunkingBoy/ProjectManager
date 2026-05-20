from . import BaseModel, UTCTime

from typing import cast
from copy import deepcopy
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text

from templates.StandardDBTemplate import TbRequirementsTemplate

class Requirements(BaseModel):
    __tablename__ = 'requirements'

    id: Column[int] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="需求表自增ID,自增主键"
    )
    requirement_id: str = cast(str, Column(
        String(128),
        unique=True, # 字段唯一
        index=True,
        nullable=False, # 不允许为空
        comment="需求ID,需求唯一标识"
    ))
    number: str = cast(str, Column(
        String(128),
        unique=False,   # 允许重复需求
        index=True,
        nullable=False, # 不允许为空
        comment="需求编号"
    ))
    title: str = cast(str, Column(
        String(128),
        unique=False,
        index=True,
        nullable=False,
        comment="需求标题"
    ))
    description: str = cast(str, Column(
        Text,
        unique=False,
        index=False,
        nullable=True,
        comment="需求描述"
    ))
    source: int = cast(int, Column(
        Integer,
        unique=False,
        index=True,
        nullable=False,
        comment="需求来源,0:手动创建,1:第三方接入"
    ))
    status: int = cast(int, Column(
        Integer,
        unique=False,
        index=True,
        nullable=False,
        comment="需求状态,0.待领取1.设计中2.开发中3.测试中4.已上线5.废弃"
    ))
    person: str = cast(str, Column(
        String(32),
        unique=False,
        index=True,
        nullable=True,
        comment="需求处理人"
    ))
    relevant: str = cast(str, Column(
        Text,
        unique=False,
        index=False,
        nullable=True,
        comment="需求负责技术经理"
    ))
    total: str = cast(str, Column(
        String(128),
        unique=False,
        index=True,
        nullable=True,
        comment="需求总工时"
    ))
    develop_total: str = cast(str, Column(
        String(128),
        unique=False,
        index=True,
        nullable=True,
        comment="需求开发工时"
    ))
    test_total: str = cast(str, Column(
        String(128),
        unique=False,
        index=True,
        nullable=True,
        comment="需求测试工时"
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
        nullable=False,
        comment="更新时间,初始默认为数据插入时间,时区为UTC"
    )

    def __init__(
        self,
        data: TbRequirementsTemplate # 修改模型字段
    ) -> None:
        self.number: str = data.number
        self.title: str = data.title
        self.description: str = data.desc
        self.source: int = data.source.value
        self.status: int = data.status.value
        self.person: str = data.person
        self.relevant: str = data.relevant

    @property
    def info(self) -> dict: return deepcopy(self.__dict__)
