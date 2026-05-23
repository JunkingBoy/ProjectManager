from datetime import datetime
from dataclasses import dataclass

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
    status: int
    priority: int
    system: str
    person: str
    related_doc: str
    release_time: int
    req_dev_tasks_count: int # 需求关联开发任务总数
    req_dev_tasks_done_count: int # 需求关联开发任务完成数
    req_bug_count: int # 需求关联bug总数
    req_bug_done_count: int # 需求关联bug完成数
    req_business_bug_done_count: int # 需求关联业务bug完成数

    @property
    def info(self) -> dict: return self.__dict__.copy()

@dataclass
class StandardRequirementsTasksInfoTemplate:
    req_id: str
    number: str # 需求编号
    title: str
    person: str
    related_doc: str
    release_time: int

    @property
    def info(self) -> dict: return self.__dict__.copy()

@dataclass
class StandardRequirementsDetailTemplate:
    req_id: str
    number: str # 需求编号  
    relevant: str # 需求技术负责人
    status: int
    priority: int
    system: str
    desc: str
    release_time: int
    related_doc: str
    remark: str

    @property
    def info(self) -> dict: return self.__dict__.copy()

@dataclass
class StandardRequirementsModifyTemplate:
    decrypt_uid: str
    decrypt_req_id: str
    decrypt_relevant: str
    priority: int
    remark: str
    release_time: datetime

    @property
    def info(self) -> dict: return self.__dict__.copy()

@dataclass
class StandardTasksListInfoTemplate:
    task_id: str | None
    req_id: str | None
    terminal: int
    title: str
    desc: str
    dev_total: str
    status: int
    creator: str
    owner: str
    remark: str
    end_time: int
    update_time: int

    @property
    def info(self) -> dict: return self.__dict__.copy()


@dataclass
class StandardBugListInfoTemplate:
    bug_id: str
    req_id: str
    task_id: str
    title: str
    desc: str
    expected_res: str
    status: int
    creator: str
    owner: str
    developer: str
    c_time: int
    u_time: int

    @property
    def info(self) -> dict: return self.__dict__.copy()
