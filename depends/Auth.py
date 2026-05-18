from fastapi import Request

from utils.Excptions import DivExcep
from utils.JWT import verify_access_token
from enums.StandardBusEnum import StandardBusinessEnum

async def authentication(r: Request) -> tuple:
    _headers: str | None = r.headers.get("Authorization")
    if not _headers: raise DivExcep(StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    if not _headers.startswith("Bearer "): raise DivExcep(StandardBusinessEnum.FAIL.value[0], "Token 格式错误")
    _token: str = _headers[len("Bearer "):]
    _verify_res: tuple = await verify_access_token(_token)
    if StandardBusinessEnum.SUCCESS.value[0] != _verify_res[0]: return _verify_res[0], _verify_res[1]
    return _verify_res
