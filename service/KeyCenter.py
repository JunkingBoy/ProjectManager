import base64
import secrets

from fastapi import Request

from tools.Files import get_env_val
from tools.Re import filling_random_chars
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardResTemplate import StandardKeyResStruct

async def get_aes_key(
    r: Request
) -> tuple:
    tmp_key: str = get_env_val("aes", "dev")
    random_index: int = secrets.SystemRandom().randrange(0, len(tmp_key) + 1)
    # 16位固定长度随机填充值
    tmp_filling_str: str = filling_random_chars(random_index, tmp_key)
    if not tmp_filling_str: return (StandardBusinessEnum.FAIL.value[0], "环境变量配置错误")
    else:
        res_filling_str: str = base64.b64encode(tmp_filling_str.encode('utf-8')).decode("utf-8")
        res_struct: StandardKeyResStruct = StandardKeyResStruct(
            index=random_index,
            key=res_filling_str,
        )
        return (StandardBusinessEnum.SUCCESS.value[0], "操作成功", res_struct.info)
