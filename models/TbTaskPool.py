from . import BaseModel, UTCTime

from typing import cast
from copy import deepcopy
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text

from templates.StandardDBTemplate import TbTaskPoolTemplate


class TaskPool(BaseModel):
    __tablename__ = 'tasks_pool'

    id: Column[int] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="任务池表自增ID,自增主键"
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
    terminal: str = cast(str, Column(
        String(128),
        nullable=True,
        comment="任务关联开发终端"
    ))
    description: str = cast(str, Column(
        Text,
        nullable=True,
        comment="任务描述"
    ))
    develop_total: str = cast(str, Column(
        String(128),
        nullable=True,
        comment="需求开发工时"
    ))
    status: int = cast(int, Column(
        Integer,
        default=1,
        nullable=False,
        comment="任务状态,1.规划中2.已锁定3.开发中4.开发完毕"
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
    remark: str = cast(str, Column(
        Text,
        nullable=True,
        comment="任务备注"
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
        data: TbTaskPoolTemplate
    ) -> None:
        self.task_id = data.task_id
        self.requirement_id = data.requirement_id
        self.terminal = data.terminal
        self.description = data.description
        self.develop_total = data.develop_total
        self.status = data.status
        self.creator = data.creator
        self.owner = data.owner
        self.remark = data.remark

    @property
    def info(self) -> dict:
        return deepcopy(self.__dict__)
