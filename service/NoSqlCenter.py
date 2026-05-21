import asyncio
import traceback

from pathlib import Path
from typing import Optional
from fastapi import Request

from utils.Logs import ExceptionLog
from repository.NosqlRepository import sync_read
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardSysTemplate import StandardNoSqlConnTemplate

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
            e.info(f"NoSQL 数据查询成功: nosql={nosql}")
            return (StandardBusinessEnum.SUCCESS.value[0], "数据查询成功", result)
        except Exception as err:
            e.error(f"NoSQL 数据查询失败: {str(err)}\n{traceback.format_exc()}")
            return (StandardBusinessEnum.FAIL.value[0], "数据查询失败", None)