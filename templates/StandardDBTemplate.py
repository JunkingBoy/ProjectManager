from dataclasses import dataclass
from typing import Optional

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
    def info(self) -> dict:
        return self.__dict__.copy()


@dataclass
class TbRequirementTemplate:
    requirement_id: str
    number: str
    title: str
    description: Optional[str]
    source: int
    status: int
    person: Optional[str]
    relevant: Optional[str]
    total: Optional[str]
    develop: Optional[str]
    test: Optional[str]
    priority: Optional[int]
    iteration: Optional[str]
    project: Optional[str]
    scheme: Optional[str]

    @property
    def info(self) -> dict:
        return self.__dict__.copy()


@dataclass
class TbTaskPoolTemplate:
    task_id: str
    requirement_id: str
    terminal: Optional[str]
    description: Optional[str]
    develop_total: Optional[str]
    status: int
    creator: Optional[str]
    owner: Optional[str]
    remark: Optional[str]

    @property
    def info(self) -> dict:
        return self.__dict__.copy()


@dataclass
class TbDevelopTaskTemplate:
    task_id: str
    requirement_id: str
    point_id: Optional[str]
    title: str
    description: Optional[str]
    status: int
    creator: Optional[str]
    owner: Optional[str]

    @property
    def info(self) -> dict:
        return self.__dict__.copy()


@dataclass
class TbQaTaskTemplate:
    task_id: str
    requirement_id: str
    point_id: Optional[str]
    title: str
    description: Optional[str]
    status: int
    creator: Optional[str]
    owner: Optional[str]
    developer: Optional[str]

    @property
    def info(self) -> dict:
        return self.__dict__.copy()


@dataclass
class TbBugTemplate:
    bug_id: str
    requirement_id: str
    task_id: Optional[str]
    title: str
    description: Optional[str]
    expected_res: Optional[str]
    status: int
    creator: Optional[str]
    owner: Optional[str]
    developer: Optional[str]

    @property
    def info(self) -> dict:
        return self.__dict__.copy()


@dataclass
class TbTaskLogTemplate:
    task_id: str
    description: Optional[str]
    creator: Optional[str]

    @property
    def info(self) -> dict:
        return self.__dict__.copy()


@dataclass
class TbReqFeatureLogTemplate:
    req_id: int
    feature_id: int
    biz_type: str
    operator_id: int
    changed_fields: Optional[dict]
    before_snapshot: Optional[dict]
    after_snapshot: Optional[dict]

    @property
    def info(self) -> dict:
        return self.__dict__.copy()
