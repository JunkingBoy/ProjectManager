from copy import deepcopy
from datetime import datetime
from dataclasses import dataclass

from enums.StandardBusEnum import (StandardReqSourceEnum,
StandardReqStatusEnum,
StandardPointStatusEnum,
StandardDevTasksStatusEnum,
StandardQaTasksPoolStatusEnum,
StandardBugStatusEnum,
StandardReqPriorityEnum)

'''
所有表的操作模型
'''
@dataclass
class TbUserTemplate:
    uid: str
    username: str
    phone: str
    email: str
    password: str

    @property
    def info(self) -> dict: return self.__dict__.copy()

@dataclass
class TbRequirementsTemplate:
    req_id: str
    number: str
    title: str
    desc: str
    source: StandardReqSourceEnum     # 需求来源
    status: StandardReqStatusEnum     # 需求状态
    priority: StandardReqPriorityEnum # 需求优先级,枚举值
    system: str                       # 所属系统,为StandardNoSqlConnTemplate中的system下的值
    project: str                      # 所属项目,为StandardNoSqlConnTemplate中的project下的值
    project_type: str                 # 所属项目类型,为StandardNoSqlConnTemplate中的project_type下的值
    person: str                       # 为空则业务层传空字符串
    relevant: str
    related_doc: str                  # 需求关联文档,为空则业务层传空字符
    total: str                        # 需求总工时浮点数转为字符串存
    dev_total: str                    # 需求开发工时浮点数转为字符串存
    dev_price: str                    # 需求开发单价
    test_total: str                   # 需求测试工时浮点数转为字符串存
    test_price: str
    business_test_total: str
    business_test_price: str
    release_time: datetime            # 计划发布时间     

    @property
    def info(self) -> dict: return deepcopy(self.__dict__)

@dataclass
class TbPointTemplate:
    point_id: str
    requirement_id: str
    title: str
    desc: str
    status: StandardPointStatusEnum
    creator: str
    developer: str
    qa: str

    @property
    def info(self) -> dict: return deepcopy(self.__dict__)

@dataclass
class TbDevelopTasksPoolTmplate:
    task_id: str
    req_id: str
    point_id: str
    title: str
    desc: str
    status: StandardDevTasksStatusEnum
    creator: str
    owner: str

    @property
    def info(self) -> dict: return deepcopy(self.__dict__)

@dataclass
class TbQaTasksPoolTemplate:
    task_id: str
    req_id: str
    point_id: str
    title: str
    desc: str
    status: StandardQaTasksPoolStatusEnum
    creator: str
    owner: str
    developer: str

    @property
    def info(self) -> dict: return deepcopy(self.__dict__)

@dataclass
class TbBugsPoolTemplate:
    bug_id: str
    req_id: str
    point_id: str
    test_task_id: str
    title: str
    desc: str
    status: StandardBugStatusEnum
    creator: str
    owner: str
    developer: str

    @property
    def info(self) -> dict: return deepcopy(self.__dict__)
