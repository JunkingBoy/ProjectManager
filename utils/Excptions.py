from typing import Any
from fastapi import HTTPException

class DivExcep(HTTPException):
    def __init__(self, code: int, msg: str):
        super().__init__(status_code=200, detail=msg) 
        self.code: int = code
        self.msg: Any = msg
