import asyncio
import traceback

from pathlib import Path
from typing import Optional
from fastapi import Request
from datetime import datetime

from tools.Re import generate_uid
from utils.Logs import ExceptionLog
from dantics.DictDantic import NoSqlAdd
from utils.Encry import encrypt, decrypt
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardNoSqlTemplate import NoSqlDataTemplate
from templates.StandardSysTemplate import StandardNoSqlConnTemplate
from repository.NosqlRepository import sync_create, sync_read, sync_delete

async def get_nosql_type_list(
    r: Request
) -> tuple:
    e: ExceptionLog = ExceptionLog.get_instance()
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        try:
            template: StandardNoSqlConnTemplate = StandardNoSqlConnTemplate()
            type_list: list = [
                template.SYS_NOSQL_NAME.replace(".json", ""),
                template.PROJECT_NOSQL_NAME.replace(".json", ""),
                template.PROJECT_TYPE_NOSQL_NAME.replace(".json", ""),
            ]
            e.info(f"NoSQL 类型列表获取成功: {type_list}")
            return (StandardBusinessEnum.SUCCESS.value[0], StandardBusinessEnum.SUCCESS.value[1], type_list)
        except Exception as err:
            e.error(f"NoSQL 类型列表获取失败: {str(err)}")
            return (StandardBusinessEnum.FAIL.value[0], StandardBusinessEnum.FAIL.value[1], None)

async def get_nosql_type_values(
    r: Request,
    nosql: str
) -> tuple:
    e: ExceptionLog = ExceptionLog.get_instance()
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        try:
            template: StandardNoSqlConnTemplate = StandardNoSqlConnTemplate()
            file_map: dict = {
                "system": template.SYS_NOSQL_NAME,
                "project": template.PROJECT_NOSQL_NAME,
                "project_type": template.PROJECT_TYPE_NOSQL_NAME,
            }
            file_path: str = (Path(template.NOSQL_PATH) / file_map[nosql]).as_posix()
            loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
            result: str | dict = await loop.run_in_executor(None, sync_read, file_path)
            if isinstance(result, dict):
                encrypted_result: dict = {}
                for k, v in result.items():
                    encrypted_key: str = await encrypt(k)
                    encrypted_result[encrypted_key] = v
                result = encrypted_result
            e.info(f"NoSQL 数据查询成功: nosql={nosql}")
            return (StandardBusinessEnum.SUCCESS.value[0], "数据查询成功", result)
        except Exception as err:
            e.error(f"NoSQL 数据查询失败: {str(err)}\n{traceback.format_exc()}")
            return (StandardBusinessEnum.FAIL.value[0], "数据查询失败", None)

async def add_nosql_value_by_type(
    r: Request,
    model: NoSqlAdd
) -> tuple:
    e: ExceptionLog = ExceptionLog.get_instance()
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        try:
            template: StandardNoSqlConnTemplate = StandardNoSqlConnTemplate()
            file_map: dict = {
                "system": template.SYS_NOSQL_NAME,
                "project": template.PROJECT_NOSQL_NAME,
                "project_type": template.PROJECT_TYPE_NOSQL_NAME,
            }
            file_path: str = (Path(template.NOSQL_PATH) / file_map[model.nosql]).as_posix()
            loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
            # 组装写入数据: 时间戳 + uid后6位
            _key: str = f"{datetime.now().strftime('%Y%m%d%H%M%S')}{generate_uid()[-6:]}"
            _data: NoSqlDataTemplate = NoSqlDataTemplate(key=_key, value=model.value)
            await loop.run_in_executor(None, sync_create, file_path, _data)
            e.info(f"NoSQL 数据写入成功: nosql={model.nosql}, key={_key}")
            return (StandardBusinessEnum.SUCCESS.value[0], "创建成功")
        except Exception as err:
            e.error(f"NoSQL 数据写入失败: {str(err)}\n{traceback.format_exc()}")
            return (StandardBusinessEnum.FAIL.value[0], "创建失败")

async def del_nosql_value_by_type(
    r: Request,
    nosql: str,
    key: str
) -> tuple:
    e: ExceptionLog = ExceptionLog.get_instance()
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        try:
            # 修复 URL query 中 + → 空格 与丢失的 base64 填充
            _fixed_key: str = key.replace(" ", "+")
            _fixed_key += "=" * (-len(_fixed_key) % 4)
            _decrypted_key: str = await decrypt(_fixed_key)
            template: StandardNoSqlConnTemplate = StandardNoSqlConnTemplate()
            file_map: dict = {
                "system": template.SYS_NOSQL_NAME,
                "project": template.PROJECT_NOSQL_NAME,
                "project_type": template.PROJECT_TYPE_NOSQL_NAME,
            }
            file_path: str = (Path(template.NOSQL_PATH) / file_map[nosql]).as_posix()
            loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
            await loop.run_in_executor(None, sync_delete, file_path, _decrypted_key)
            e.info(f"NoSQL 数据删除成功: nosql={nosql}, key={_decrypted_key}")
            return (StandardBusinessEnum.SUCCESS.value[0], "删除成功")
        except Exception as err:
            e.error(f"NoSQL 数据删除失败: {str(err)}\n{traceback.format_exc()}")
            return (StandardBusinessEnum.FAIL.value[0], "删除失败")
