from pathlib import Path
from typing import Optional
from datetime import datetime
from fastapi import Request

from tools.Re import generate_uid
from dantics.TasksDantic import TasksAdd
from utils.Encry import decrypt, encrypt
from utils.Pool import StandardSQLiteDBConnectPool
from repository.UserRepository import user_repeat_normal
from repository.TaskRepository import tasks_create
from repository.RequirementRepository import requirement_create

from templates.StandardDBTemplate import TbDevelopTasksPoolTmplate
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

async def task_add(
    r: Request,
    data: list[TasksAdd],
    decrypted_uid: str,
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
        async with db_pool.get_session() as session:
            _is_normal: bool = await user_repeat_normal(session, decrypted_uid)
            if not _is_normal: return (StandardBusinessEnum.FAIL.value[0], "用户状态异常")
            tasks_list: list = []
            for item in data:
                tasks_list.append(TbDevelopTasksPoolTmplate(
                    task_id=generate_uid(),
                    req_id=await decrypt(item.req_id),
                    terminal=StandardTaskTerminalEnum(item.terminal),
                    title=item.title,
                    desc=item.desc,
                    dev_total=item.dev_total,
                    status=StandardDevTasksStatusEnum(item.status),
                    creator=decrypted_uid,
                    owner=await decrypt(item.owner),
                    remark=item.remark,
                    end_time=datetime.fromtimestamp(float(item.end_time))
                ))
            _res: StandardBusinessEnum = await tasks_create(session, tasks_list)
            if _res != StandardBusinessEnum.SUCCESS: return (StandardBusinessEnum.FAIL.value[0], "任务创建失败")
            return (StandardBusinessEnum.SUCCESS.value[0], "任务创建成功")

