from . import BaseModel, UTCTime

from typing import cast
from copy import deepcopy
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text

from templates.StandardDBTemplate import TbDevelopTasksPoolTmplate

class TasksPool(BaseModel):
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
        unique=False,
        index=True,
        nullable=False, # 不允许为空
        comment="关联需求ID"
    ))
    terminal: int = cast(int, Column(
        Integer,
        unique=False,
        index=True,
        nullable=True, # 考虑任务终端表
        comment="任务终端,0后台1安卓2IOS3鸿蒙4小程序5H5"
    ))
    title: str = cast(str, Column(
        String(128),
        unique=False,
        index=True,
        nullable=False,
        comment="任务标题"
    ))
    description: str = cast(str, Column(
        Text,
        unique=False,
        index=False,
        nullable=True,
        comment="任务描述"
    ))
    develop_total: str = cast(str, Column(
        String(128),
        unique=False,
        index=True,
        nullable=True,
        comment="需求开发工时"
    ))
    status: int = cast(int, Column(
        Integer,
        unique=False,
        index=True,
        nullable=False,
        comment="任务状态,0.待处理1.进行中2.已完成3.待修复4.已关闭"
    ))
    creator: str = cast(str, Column(
        String(32),
        unique=False,
        index=True,
        nullable=True,
        comment="任务创建者"
    ))
    owner: str = cast(str, Column(
        String(32),
        unique=False,
        index=True,
        nullable=True,
        comment="任务负责人"
    ))
    remark: str = cast(str, Column(
        Text,
        unique=False,
        index=False,
        nullable=True,
        comment="任务备注"
    ))
    end_time: datetime = cast(datetime, Column(
        DateTime(timezone=False),
        default=None,
        nullable=True,
        comment="任务计划结束时间"
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
        data: TbDevelopTasksPoolTmplate
    ) -> None:
        self.task_id: str = data.task_id
        self.requirement_id: str = data.req_id
        self.terminal: int = data.terminal.value
        self.title: str = data.title
        self.description: str = data.desc
        self.develop_total: str = data.dev_total
        self.status: int = data.status.value
        self.creator: str = data.creator
        self.owner: str = data.owner
        self.remark: str = data.remark
        self.end_time: datetime = data.end_time


class TasksLog(BaseModel):
    __tablename__ = 'tasks_log'

    id: Column[int] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="任务日志表自增ID,自增主键"
    )
    task_id: str = cast(str, Column(
        String(128),
        unique=False,
        index=True,
        nullable=False,
        comment="关联任务ID,任务唯一标识"
    ))
    description: str = cast(str, Column(
        Text,
        unique=False,
        index=False,
        nullable=True,
        comment="任务描述"
    ))
    creator: str = cast(str, Column(
        String(32),
        unique=False,
        index=True,
        nullable=True,
        comment="记录创建者"
    ))
    c_time: Column[datetime] = Column(
        DateTime(timezone=False),
        default=lambda: datetime.now(tz=UTCTime),
        nullable=False,
        comment="创建时间,默认为数据插入时间,时区为UTC"
    )
