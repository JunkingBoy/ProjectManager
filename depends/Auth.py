from fastapi import Request

from utils.Encry import decrypt
from utils.Excptions import DivExcep
from service.UserCenter import user_check
from utils.JWT import verify_access_token
from enums.StandardBusEnum import StandardBusinessEnum
from dantics.UserDantic import UserToken, UserRegister

async def password_verify(model: UserRegister) -> tuple:
    if await decrypt(model.password) != await decrypt(model.password_confirm): return StandardBusinessEnum.FAIL.value[0], "两次输入密码不一致"
    return StandardBusinessEnum.SUCCESS.value[0], model

async def authentication(r: Request) -> tuple:
    _headers: str | None = r.headers.get("Authorization")
    if not _headers: raise DivExcep(StandardBusinessEnum.FAIL.value[0], "请求头缺少参数")
    if not _headers.startswith("Bearer "): raise DivExcep(StandardBusinessEnum.FAIL.value[0], "Token 格式错误")
    _token: str = _headers[len("Bearer "):]
    _verify_res: tuple = await verify_access_token(_token)
    if StandardBusinessEnum.SUCCESS.value[0] != _verify_res[0]: return _verify_res[0], _verify_res[1]
    else:
        _tmp_token_info: UserToken = UserToken(**_verify_res[1])
        if await user_check(r, _tmp_token_info) != StandardBusinessEnum.SUCCESS: return StandardBusinessEnum.FAIL.value[0], "用户已注销"
        return StandardBusinessEnum.SUCCESS.value[0], await decrypt(_tmp_token_info.uid)
