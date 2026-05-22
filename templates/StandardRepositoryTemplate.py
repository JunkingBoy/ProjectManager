from dataclasses import dataclass

from enums.StandardBusEnum import StandardReqStatusEnum

@dataclass
class StandardUserRepositoryTemplate:
    uid: str | None
    phone: str | None
    email: str | None
    password: str | None

    @property
    def info(self) -> dict: return self.__dict__.copy()

@dataclass
class StandardUserModRepositoryTemplate:
    uid: str | None
    username: str | None
    password: str | None

    @property
    def info(self) -> dict: return self.__dict__.copy()

@dataclass
class StandardRequirementsInfoTemplate:
    req_id: str
    number: str # 需求编号
    title: str
    desc: str
    status: int
    priority: int
    req_dev_tasks_count: int # 需求关联开发任务总数
    req_dev_tasks_done_count: int # 需求关联开发任务完成数
    req_bug_count: int # 需求关联bug总数
    req_bug_done_count: int # 需求关联bug完成数
    req_business_bug_done_count: int # 需求关联业务bug完成数

    @property
    def info(self) -> dict: return self.__dict__.copy()
