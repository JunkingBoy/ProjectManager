from copy import deepcopy
from dataclasses import dataclass

from enums.StandardBusEnum import StandardReqSourceEnum, StandardReqStatusEnum, StandardPointStatusEnum

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
    number: str
    title: str
    desc: str
    source: StandardReqSourceEnum     # 需求来源
    status: StandardReqStatusEnum     # 需求状态
    person: str     # 为空则业务层传空字符串
    relevant: str

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
