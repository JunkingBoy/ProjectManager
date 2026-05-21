from . import BaseModel, UTCTime

from typing import cast
from copy import deepcopy
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text

from templates.StandardDBTemplate import TbQaTaskTemplate


class QaTask(BaseModel):
    __tablename__ = 'qa_tasks_pool'

    id: Column[int] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="测试任务池表自增ID,自增主键"
    )
    task_id: str = cast(str, Column(
        String(128),
        unique=True,
        index=True,
        nullable=False,
        comment="任务ID,任务唯一标识"
    ))
    requirement_id: str = cast(str, Column(
        String(128),
        index=True,
        nullable=False,
        comment="关联需求ID"
    ))
    point_id: str = cast(str, Column(
        String(128),
        index=True,
        nullable=True,
        comment="关联功能点ID"
    ))
    title: str = cast(str, Column(
        String(128),
        nullable=False,
        comment="任务标题"
    ))
    description: str = cast(str, Column(
        Text,
        nullable=True,
        comment="任务描述"
    ))
    status: int = cast(int, Column(
        Integer,
        default=1,
        nullable=False,
        comment="任务状态,1.待开始2.进行中3.已完成4.已废弃"
    ))
    creator: str = cast(str, Column(
        String(32),
        nullable=True,
        comment="任务创建者"
    ))
    owner: str = cast(str, Column(
        String(32),
        nullable=True,
        comment="任务负责人"
    ))
    developer: str = cast(str, Column(
        String(32),
        nullable=True,
        comment="关联开发人员"
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
        data: TbQaTaskTemplate
    ) -> None:
        self.task_id = data.task_id
        self.requirement_id = data.requirement_id
        self.point_id = data.point_id
        self.title = data.title
        self.description = data.description
        self.status = data.status
        self.creator = data.creator
        self.owner = data.owner
        self.developer = data.developer

    @property
    def info(self) -> dict:
        return deepcopy(self.__dict__)
