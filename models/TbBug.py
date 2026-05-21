from . import BaseModel, UTCTime

from typing import cast
from copy import deepcopy
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text

from templates.StandardDBTemplate import TbBugTemplate


class BugPool(BaseModel):
    __tablename__ = 'bugs_pool'

    id: Column[int] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Bug池表自增ID,自增主键"
    )
    bug_id: str = cast(str, Column(
        String(128),
        unique=True,
        index=True,
        nullable=False,
        comment="BugID,Bug唯一标识"
    ))
    requirement_id: str = cast(str, Column(
        String(128),
        index=True,
        nullable=False,
        comment="关联需求ID"
    ))
    task_id: str = cast(str, Column(
        String(128),
        index=True,
        nullable=True,
        comment="关联任务ID,任务唯一标识"
    ))
    title: str = cast(str, Column(
        String(128),
        nullable=False,
        comment="Bug标题"
    ))
    description: str = cast(str, Column(
        Text,
        nullable=True,
        comment="Bug描述"
    ))
    expected_res: str = cast(str, Column(
        Text,
        nullable=True,
        comment="正确情况下预期结果"
    ))
    status: int = cast(int, Column(
        Integer,
        default=0,
        nullable=False,
        comment="Bug状态,0.未修复1.已修复2.研发确认非Bug3.已关闭"
    ))
    creator: str = cast(str, Column(
        String(32),
        nullable=True,
        comment="Bug创建者"
    ))
    owner: str = cast(str, Column(
        String(32),
        nullable=True,
        comment="测试负责人"
    ))
    developer: str = cast(str, Column(
        String(32),
        nullable=True,
        comment="Bug关联开发"
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
        data: TbBugTemplate
    ) -> None:
        self.bug_id = data.bug_id
        self.requirement_id = data.requirement_id
        self.task_id = data.task_id
        self.title = data.title
        self.description = data.description
        self.expected_res = data.expected_res
        self.status = data.status
        self.creator = data.creator
        self.owner = data.owner
        self.developer = data.developer

    @property
    def info(self) -> dict:
        return deepcopy(self.__dict__)
