from typing import Any
from datetime import timezone
from sqlalchemy.ext.declarative import declarative_base

# orm基类,所有orm模型都需要继承这个基类
BaseModel: Any = declarative_base()
# 设置建表时候的默认时区时间
UTCTime: Any = timezone.utc

from models.TbUser import User
from models.TbRequirement import Requirement
from models.TbTaskPool import TaskPool
from models.TbDevelopTask import DevelopTask
from models.TbQaTask import QaTask
from models.TbBug import BugPool
from models.TbTaskLog import TaskLog
from models.TbReqFeatureLog import ReqFeatureLog

__all__ = [
    "BaseModel",
    "UTCTime",
    "User",
    "Requirement",
    "TaskPool",
    "DevelopTask",
    "QaTask",
    "BugPool",
    "TaskLog",
    "ReqFeatureLog",
]
