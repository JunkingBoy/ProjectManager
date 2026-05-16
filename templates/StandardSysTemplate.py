from copy import deepcopy
from dataclasses import dataclass

from tools.Files import create_dir
from enums.StandardErrEnum import StandardSysErrEnum

'''
系统中所有非转换模板存放处
'''
@dataclass
class StandardLogDataTemplate:
    code: int | StandardSysErrEnum
    msg: str

    @property
    def info(self) -> dict: return deepcopy(self.__dict__)

    def __post_init__(self) -> None:
        if isinstance(self.code, StandardSysErrEnum):
            self.msg: str = str(self.code.value[1])
            self.code = int(self.code.value[0])

@dataclass
class StandardSqliteConnTemplate:
    DB_PATH: str = create_dir("db")
    DB_NAME: str = "pm.db"

    @property
    def info(self) -> dict: return deepcopy(self.__dict__)

@dataclass
class StandardTokenInfoTemplate:
    uid: str
    exp: int # token颁发时的时间戳

    @property
    def info(self) -> dict: return self.__dict__.copy()
