from jose import jwt, JWTError, ExpiredSignatureError

from tools.Files import get_env_val
from utils.Logs import ExceptionLog
from utils.Excptions import DivExcep
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardSysTemplate import StandardTokenInfoTemplate

async def create_access_token(data: StandardTokenInfoTemplate) -> str:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        _secret_key: str = get_env_val("jwt_secret", "dev")
        token_str: str = jwt.encode(
            data.info,
            _secret_key
        )
        return token_str
    except Exception as err:
        e.error(f"创建token失败: {str(err)}")
        raise DivExcep(
            code=StandardBusinessEnum.ERROR.value[0],
            msg="创建token失败"
        )

async def verify_access_token(token: str) -> tuple:
    e: ExceptionLog = ExceptionLog.get_instance()
    _secret_key: str = get_env_val("jwt_secret", "dev")
    try:
        decode_data: dict = jwt.decode(
            token,
            _secret_key
        )
        if not decode_data: return StandardBusinessEnum.UNKNOWN.value[0], StandardBusinessEnum.UNKNOWN.value[1]
        return StandardBusinessEnum.SUCCESS.value[0], decode_data
    except ExpiredSignatureError:
        return StandardBusinessEnum.EXPIRED.value[0], StandardBusinessEnum.EXPIRED.value[1]
    except JWTError:
        return StandardBusinessEnum.INVALID.value[0], StandardBusinessEnum.INVALID.value[1]
    except Exception as err:
        e.error(f"验证token失败: {str(err)}")
        raise DivExcep(
            code=StandardBusinessEnum.ERROR.value[0],
            msg="验证token失败"
        )
