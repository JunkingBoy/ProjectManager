from . import BaseModel, UTCTime

from typing import cast
from copy import deepcopy
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON

from templates.StandardDBTemplate import TbReqFeatureLogTemplate


class ReqFeatureLog(BaseModel):
    __tablename__ = 'requirement_feature_logs'

    id: Column[int] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="审计日志表自增ID,自增主键"
    )
    req_id: int = cast(int, Column(
        Integer,
        index=True,
        nullable=False,
        comment="需求ID"
    ))
    feature_id: int = cast(int, Column(
        Integer,
        index=True,
        default=0,
        nullable=True,
        comment="功能点ID"
    ))
    biz_type: str = cast(str, Column(
        String(32),
        index=True,
        nullable=False,
        comment="业务类型: REQUIREMENT-需求变更, FEATURE-功能点变更"
    ))
    operator_id: int = cast(int, Column(
        Integer,
        nullable=False,
        comment="操作人ID"
    ))
    created_at: Column[datetime] = Column(
        DateTime(timezone=False),
        default=lambda: datetime.now(tz=UTCTime),
        nullable=False,
        comment="操作时间"
    )
    changed_fields: dict = cast(dict, Column(
        JSON,
        nullable=True,
        comment="被修改的字段名列表"
    ))
    before_snapshot: dict = cast(dict, Column(
        JSON,
        nullable=True,
        comment="修改前的全量数据快照"
    ))
    after_snapshot: dict = cast(dict, Column(
        JSON,
        nullable=True,
        comment="修改后的全量数据快照"
    ))

    def __init__(
        self,
        data: TbReqFeatureLogTemplate
    ) -> None:
        self.req_id = data.req_id
        self.feature_id = data.feature_id
        self.biz_type = data.biz_type
        self.operator_id = data.operator_id
        self.changed_fields = data.changed_fields
        self.before_snapshot = data.before_snapshot
        self.after_snapshot = data.after_snapshot

    @property
    def info(self) -> dict:
        return deepcopy(self.__dict__)
