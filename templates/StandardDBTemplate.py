from dataclasses import dataclass

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
