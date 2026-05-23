from . import BaseModel, CST

from typing import cast
from copy import deepcopy
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text

from templates.StandardDBTemplate import TbBugsPoolTemplate

class TbBugsPool(BaseModel):
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
        unique=False,
        index=True,
        nullable=False, # 不允许为空
        comment="关联需求ID"
    ))
    task_id: str = cast(str, Column(
        String(128),
        unique=False,
        index=True,
        nullable=True, # 测试任务ID可以为空,为了区分综合测试Bug和业务测试Bug
        comment="关联任务ID,任务唯一标识"
    ))
    title: str = cast(str, Column(
        String(128),
        unique=False,
        index=True,
        nullable=False,
        comment="Bug标题"
    ))
    description: str = cast(str, Column(
        Text,
        unique=False,
        index=False,
        nullable=True,
        comment="Bug描述"
    ))
    expected_res: str = cast(str, Column(
        Text,
        unique=False,
        index=False,
        nullable=True,
        comment="正确情况下预期结果"
    ))
    status: int = cast(int, Column(
        Integer,
        unique=False,
        index=True,
        nullable=False,
        comment="Bug状态,0.未修复1.已修复2.研发确认非Bug3.已关闭"
    ))
    creator: str = cast(str, Column(
        String(32),
        unique=False,
        index=True,
        nullable=True,
        comment="Bug创建者"
    ))
    owner: str = cast(str, Column(
        String(32),
        unique=False,
        index=True,
        nullable=True,
        comment="测试负责人"
    ))
    developer: str = cast(str, Column(
        String(32),
        unique=False,
        index=True,
        nullable=True,
        comment="Bug关联开发"
    ))
    c_time: Column[datetime] = Column(
        DateTime(timezone=False),
        default=lambda: datetime.now(tz=CST),
        nullable=False,
        comment="创建时间,默认为数据插入时间,时区为UTC"
    )
    u_time: Column[datetime] = Column(
        DateTime(timezone=False),
        default=lambda: datetime.now(tz=CST),
        nullable=False,
        comment="更新时间,初始默认为数据插入时间,时区为UTC"
    )

    def __init__(
        self,
        data: TbBugsPoolTemplate
    ) -> None:
        self.bug_id: str = data.bug_id
        self.requirement_id: str = data.req_id
        self.point_id: str = data.point_id
        self.test_task_id: str = data.test_task_id
        self.title: str = data.title
        self.description: str = data.desc
        self.status: int = data.status.value
        self.creator: str = data.creator
        self.owner: str = data.owner
        self.developer: str = data.developer

    @property
    def info(self) -> dict: return deepcopy(self.__dict__)
