from copy import deepcopy
from dataclasses import dataclass

@dataclass
class NoSqlDataTemplate:
    key: str
    value: str

    @property
    def info(self) -> dict: return deepcopy(self.__dict__)
