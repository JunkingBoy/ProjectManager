from . import BaseModel, UTCTime

from typing import cast
from copy import deepcopy
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text

from templates.StandardDBTemplate import TbDevelopTasksPoolTmplate, TbQaTasksPoolTemplate

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
    terminal: str = cast(str, Column(
        String(128),
        unique=False,
        index=True,
        nullable=True, # 功能点ID可以为空
        comment="任务关联开发终端,0后台1安卓2IOS3鸿蒙4小程序5H5"
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
        comment="任务状态,1.设计中2.开发中3.开发完毕4.测试中5.废弃"
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

class DevelopTasksPool(BaseModel):
    __tablename__ = 'develop_tasks_pool'

    id: Column[int] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="研发任务池表自增ID,自增主键"
    )
    task_id: str = cast(str, Column(
        String(128),
        unique=True,
        index=True,
        nullable=False,
        comment="研发任务ID,研发任务唯一标识"
    ))
    requirement_id: str = cast(str, Column(
        String(128),
        unique=False,
        index=True,
        nullable=False, # 不允许为空
        comment="关联需求ID"
    ))
    point_id: str = cast(str, Column(
        String(128),
        unique=False,
        index=True,
        nullable=True, # 功能点ID可以为空
        comment="关联功能点ID,功能点唯一标识"
    ))
    title: str = cast(str, Column(
        String(128),
        unique=False,
        index=True,
        nullable=False,
        comment="研发任务标题"
    ))
    description: str = cast(str, Column(
        Text,
        unique=False,
        index=False,
        nullable=True,
        comment="研发任务描述"
    ))
    status: int = cast(int, Column(
        Integer,
        unique=False,
        index=True,
        nullable=False,
        comment="研发任务状态,1.设计中2.开发中3.开发完毕4.测试中5.废弃"
    ))
    creator: str = cast(str, Column(
        String(32),
        unique=False,
        index=True,
        nullable=True,
        comment="研发任务创建者"
    ))
    owner: str = cast(str, Column(
        String(32),
        unique=False,
        index=True,
        nullable=True,
        comment="研发任务负责人"
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
        self.point_id: str = data.point_id
        self.title: str = data.title
        self.description: str = data.desc
        self.status: int = data.status.value
        self.creator: str = data.creator
        self.owner: str = data.owner
    
    @property
    def info(self) -> dict: return deepcopy(self.__dict__)

class QaTasksPool(BaseModel):
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
        comment="测试任务ID,研发任务唯一标识"
    ))
    requirement_id: str = cast(str, Column(
        String(128),
        unique=False,
        index=True,
        nullable=False, # 不允许为空
        comment="关联需求ID"
    ))
    point_id: str = cast(str, Column(
        String(128),
        unique=False,
        index=True,
        nullable=True, # 功能点ID可以为空
        comment="关联功能点ID,功能点唯一标识"
    ))
    title: str = cast(str, Column(
        String(128),
        unique=False,
        index=True,
        nullable=False,
        comment="测试任务标题"
    ))
    description: str = cast(str, Column(
        Text,
        unique=False,
        index=False,
        nullable=True,
        comment="测试任务描述"
    ))
    status: int = cast(int, Column(
        Integer,
        unique=False,
        index=True,
        nullable=False,
        comment="测试任务状态,1.设计中2.执行中3.Bug修复中4.测试通过5.无需测试"
    ))
    creator: str = cast(str, Column(
        String(32),
        unique=False,
        index=True,
        nullable=True,
        comment="测试任务创建者"
    ))
    owner: str = cast(str, Column(
        String(32),
        unique=False,
        index=True,
        nullable=True,
        comment="测试任务负责人"
    ))
    developer: str = cast(str, Column(
        String(32),
        unique=False,
        index=True,
        nullable=True,
        comment="测试任务关联开发"
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
        data: TbQaTasksPoolTemplate
    ) -> None:
        self.task_id: str = data.task_id
        self.requirement_id: str = data.req_id
        self.point_id: str = data.point_id
        self.title: str = data.title
        self.description: str = data.desc
        self.status: int = data.status.value
        self.creator: str = data.creator
        self.owner: str = data.owner
        self.developer: str = data.developer

    @property
    def info(self) -> dict: return deepcopy(self.__dict__)
