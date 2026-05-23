from . import BaseModel, CST

from typing import cast
from copy import deepcopy
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text

from templates.StandardDBTemplate import TbUserTemplate

class User(BaseModel):
    __tablename__ = 'user'

    id: Column[int] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="用户表自增ID,自增主键"
    )
    uid: str = cast(str, Column(
        String(32),
        unique=True, # 字段唯一
        index=True,
        nullable=False, # 不允许为空
        comment="用户ID,唯一标识"
    ))
    username: str = cast(str, Column(
        String(13),
        unique=False,
        index=True,
        nullable=False,
        comment="用户名,注册默认生成,可更改"
    ))
    phone: str = cast(str, Column(
        String(128),
        unique=False, # 手机号允许重复,业务逻辑判断是否已经注册
        index=True,
        nullable=False,
        comment="手机号加密值,注册默认插入,可更改"
    ))
    email: str = cast(str, Column(
        String(128),
        unique=True, # 邮箱不允许重复
        index=False,
        nullable=False,
        comment="邮箱,注册默认插入,可更改"
    ))
    password: str = cast(str, Column(
        String(256),
        unique=False,
        index=False,
        nullable=False,
        comment="密码加密值"
    ))
    role: str = cast(str, Column(
        Text,
        unique=False,
        index=True,
        nullable=True,
        comment="用户角色列表,JSON数组字符串,如[0,1,5] 0:项目经理1:后台开发2:安卓开发3:IOS开发4:小程序5:H56:测试"
    ))
    active: int = cast(int, Column(
        Integer,
        default=0,
        unique=False,
        index=False,
        nullable=False,
        comment="用户状态,0:正常,1:禁用"
    ))
    deleted: int = cast(int, Column(
        Integer,
        default=0,
        unique=False,
        index=True,
        nullable=False,
        comment="用户删除状态,0:正常,1:删除"
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
        user: TbUserTemplate
    ) -> None:
        self.uid: str = user.uid
        self.phone: str = user.phone
        self.email: str = user.email
        self.username: str = user.username
        self.password: str = user.password
        self.role: str = user.role

    @property
    def info(self) -> dict: return deepcopy(self.__dict__)
