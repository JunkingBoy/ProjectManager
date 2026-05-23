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
        comment="需求状态,0.进行中1.综合测试2.业务测试3.待发布4.已发布"
    ))
    priority: int = cast(int, Column(
        Integer,
        unique=False,
        index=True,
        nullable=False,
        comment="需求优先级,0.高1.中2.低"
    ))
    system: str = cast(str, Column(
        String(32),
        unique=False,
        index=True,
        nullable=False,
        comment="需求所属系统:nosql值"
    ))
    project: str = cast(str, Column(
        String(32),
        unique=False,
        index=True,
        nullable=False,
        comment="需求所属项目:nosql值"
    ))
    project_type: str = cast(str, Column(
        String(32),
        unique=False,
        index=True,
        nullable=False,
        comment="需求所属项目类型:nosql值"
    ))
    person: str = cast(str, Column(
        String(32),
        unique=False,
        index=True,
        nullable=True,
        comment="需求处理人"
    ))
    relevant: str = cast(str, Column(
        String(32),
        unique=False,
        index=False,
        nullable=True,
        comment="需求负责技术经理"
    ))
    related_doc: str = cast(str, Column(
        String(256),
        unique=False,
        index=False,
        nullable=True,
        comment="需求关联文档,只记录文档唯一标识"
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
    develop_price: str = cast(str, Column(
        String(128),
        unique=False,
        index=True,
        nullable=True,
        comment="需求开发单价"
    ))
    test_total: str = cast(str, Column(
        String(128),
        unique=False,
        index=True,
        nullable=True,
        comment="需求测试工时"
    ))
    test_price: str = cast(str, Column(
        String(128),
        unique=False,
        index=True,
        nullable=True,
        comment="需求测试单价"
    ))
    business_test_total: str = cast(str, Column(
        String(128),
        unique=False,
        index=True,
        nullable=True,
        comment="需求业务测试工时"
    ))
    business_test_price: str = cast(str, Column(
        String(128),
        unique=False,
        index=True,
        nullable=True,
        comment="需求业务测试单价"
    ))
    release_time: datetime = cast(datetime, Column(
        DateTime(timezone=False),
        default=None,
        nullable=True,
        comment="需求计划发布时间"
    ))
    remark: str = cast(str, Column(
        Text,
        unique=False,
        index=False,
        nullable=True,
        comment="需求备注"
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
        self.requirement_id: str = data.req_id
        self.number: str = data.number
        self.title: str = data.title
        self.description: str = data.desc
        self.source: int = data.source.value
        self.status: int = data.status.value
        self.priority: int = data.priority.value
        self.system: str = data.system
        self.project: str = data.project
        self.project_type: str = data.project_type
        self.person: str = data.person
        self.relevant: str = data.relevant
        self.related_doc: str = data.related_doc
        self.total: str = data.total
        self.develop_total: str = data.dev_total
        self.develop_price: str = data.dev_price
        self.test_total: str = data.test_total
        self.test_price: str = data.test_price
        self.business_test_total: str = data.business_test_total
        self.business_test_price: str = data.business_test_price
        self.release_time = data.release_time
        self.remark: str = data.remark

    @property
    def info(self) -> dict: return deepcopy(self.__dict__)
