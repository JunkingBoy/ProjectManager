from dataclasses import dataclass
from typing import Optional


@dataclass
class StandardUserRepositoryTemplate:
    uid: str | None
    phone: str | None
    email: str | None
    password: str | None

    @property
    def info(self) -> dict:
        return self.__dict__.copy()


@dataclass
class StandardRequirementRepositoryTemplate:
    requirement_id: Optional[str]
    number: Optional[str]
    title: Optional[str]
    person: Optional[str]
    status: Optional[int]

    @property
    def info(self) -> dict:
        return self.__dict__.copy()


@dataclass
class StandardTaskPoolRepositoryTemplate:
    task_id: Optional[str]
    requirement_id: Optional[str]
    point_id: Optional[str]
    status: Optional[int]
    owner: Optional[str]

    @property
    def info(self) -> dict:
        return self.__dict__.copy()


@dataclass
class StandardDevelopTaskRepositoryTemplate:
    task_id: Optional[str]
    requirement_id: Optional[str]
    point_id: Optional[str]
    status: Optional[int]
    owner: Optional[str]

    @property
    def info(self) -> dict:
        return self.__dict__.copy()


@dataclass
class StandardQaTaskRepositoryTemplate:
    task_id: Optional[str]
    requirement_id: Optional[str]
    point_id: Optional[str]
    status: Optional[int]
    owner: Optional[str]
    developer: Optional[str]

    @property
    def info(self) -> dict:
        return self.__dict__.copy()


@dataclass
class StandardBugRepositoryTemplate:
    bug_id: Optional[str]
    requirement_id: Optional[str]
    task_id: Optional[str]
    status: Optional[int]
    owner: Optional[str]
    developer: Optional[str]

    @property
    def info(self) -> dict:
        return self.__dict__.copy()
