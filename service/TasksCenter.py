from pathlib import Path
from typing import Optional
from datetime import datetime
from fastapi import Request

from tools.Re import generate_uid
from utils.Encry import decrypt, encrypt
from utils.Pool import StandardSQLiteDBConnectPool
from repository.UserRepository import user_repeat_normal
from repository.RequirementRepository import requirement_create

from templates.StandardRepositoryTemplate import StandardRequirementsTasksInfoTemplate
from enums.StandardBusEnum import StandardBusinessEnum, StandardTaskTerminalEnum, StandardDevTasksStatusEnum

async def task_terminal_list(
    r: Request
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else: return (StandardBusinessEnum.SUCCESS.value[0], "操作成功", StandardTaskTerminalEnum.info())

async def task_status_list(
    r: Request,
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else: return (StandardBusinessEnum.SUCCESS.value[0], "操作成功", StandardDevTasksStatusEnum.info())
