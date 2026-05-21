from . import BaseModel, UTCTime

from typing import cast
from copy import deepcopy
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text

from templates.StandardDBTemplate import TbTaskLogTemplate


class TaskLog(BaseModel):
    __tablename__ = 'tasks_log'

    id: Column[int] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="任务日志表自增ID,自增主键"
    )
    task_id: str = cast(str, Column(
        String(128),
        index=True,
        nullable=False,
        comment="关联任务ID,任务唯一标识"
    ))
    description: str = cast(str, Column(
        Text,
        nullable=True,
        comment="任务描述"
    ))
    creator: str = cast(str, Column(
        String(32),
        nullable=True,
        comment="记录创建者"
    ))
    c_time: Column[datetime] = Column(
        DateTime(timezone=False),
        default=lambda: datetime.now(tz=UTCTime),
        nullable=False,
        comment="创建时间,默认为数据插入时间,时区为UTC"
    )

    def __init__(
        self,
        data: TbTaskLogTemplate
    ) -> None:
        self.task_id = data.task_id
        self.description = data.description
        self.creator = data.creator

    @property
    def info(self) -> dict:
        return deepcopy(self.__dict__)
