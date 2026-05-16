from typing import Any
from copy import deepcopy
from dataclasses import dataclass

@dataclass
class StandardResponse:
    code: int # 系统内部响应code
    msg: str  # 系统内部响应msg
    data: Any # 系统内部响应data可为None
    path: str | None # 请求路径

    @property
    def info(self) -> dict: return {k: deepcopy(v) for k, v in self.__dict__.items() if v is not None}
