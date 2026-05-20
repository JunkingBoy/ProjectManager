from . import BaseModel, UTCTime

from typing import cast
from copy import deepcopy
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text

from templates.StandardDBTemplate import TbPointTemplate

class Point(BaseModel):
    __tablename__ = 'feature_point'

    id: Column[int] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="功能点表自增ID,自增主键"
    )
    point_id: str = cast(str, Column(
        String(128),
        unique=True,
        index=True,
        nullable=False,
        comment="功能点ID,功能点唯一标识"
    ))
    requirement_id: str = cast(str, Column(
        String(128),
        unique=False,
        index=True,
        nullable=False, # 不允许为空
        comment="关联需求ID"
    ))
    title: str = cast(str, Column(
        String(128),
        unique=False,
        index=True,
        nullable=False,
        comment="功能点标题"
    ))
    description: str = cast(str, Column(
        Text,
        unique=False,
        index=False,
        nullable=True,
        comment="功能点描述"
    ))
    status: int = cast(int, Column(
        Integer,
        unique=False,
        index=True,
        nullable=False,
        comment="功能点状态,1.规划中2.已锁定3.开发中4.开发完毕5.暂停中6.废弃"
    ))
    creator: str = cast(str, Column(
        String(32),
        unique=False,
        index=True,
        nullable=True,
        comment="功能点创建者"
    ))
    developer: str = cast(str, Column(
        Text,
        unique=False,
        index=False,
        nullable=True,
        comment="功能点关联开发人员"
    ))
    qa: str = cast(str, Column(
        Text,
        unique=False,
        index=False,
        nullable=False,
        comment="功能点关联测试人员"
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
        data: TbPointTemplate
    ) -> None:
        self.point_id: str = data.point_id
        self.requirement_id: str = data.requirement_id
        self.title: str = data.title
        self.description: str = data.desc
        self.status: int = data.status.value
        self.creator: str = data.creator
        self.developer: str = data.developer
        self.qa: str = data.qa

    @property
    def info(self) -> dict: return deepcopy(self.__dict__)
