from typing import Optional, List
from fastapi import Request

from models.TbTaskPool import TaskPool
from utils.Logs import ExceptionLog
from utils.Excptions import DivExcep
from enums.StandardBusEnum import StandardBusinessEnum
from tools.Re import generate_uid
from templates.StandardDBTemplate import TbTaskPoolTemplate
from repository.TaskPoolRepository import (
    task_pool_list,
    task_pool_get,
    task_pool_create,
    task_pool_update,
    task_pool_delete,
)


async def task_pool_list_service(
    r: Request,
    requirement_id: Optional[str] = None,
    status: Optional[int] = None,
) -> List[TaskPool]:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        return await task_pool_list(session, requirement_id, status)


async def task_pool_detail_service(
    r: Request,
    task_id: str
) -> TaskPool:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        task: TaskPool = await task_pool_get(session, task_id)
        if not task:
            raise DivExcep(
                code=StandardBusinessEnum.UNKNOWN.value[0],
                msg="功能点不存在"
            )
        return task


async def task_pool_create_service(
    r: Request,
    data: dict
) -> tuple:
    db_pool = r.app.state.db_pool
    template: TbTaskPoolTemplate = TbTaskPoolTemplate(
        task_id=generate_uid(),
        requirement_id=data.get("requirement_id", ""),
        terminal=data.get("terminal"),
        description=data.get("description"),
        develop_total=data.get("develop_total"),
        status=1,
        creator=data.get("creator"),
        owner=data.get("owner"),
        remark=data.get("remark"),
    )
    async with db_pool.get_session() as session:
        code: int = await task_pool_create(session, template)
        return (code, "功能点创建成功")


async def task_pool_update_service(
    r: Request,
    task_id: str,
    data: dict
) -> tuple:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        code: int = await task_pool_update(session, task_id, data)
        return (code, "功能点更新成功")


async def task_pool_delete_service(
    r: Request,
    task_id: str
) -> tuple:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        code: int = await task_pool_delete(session, task_id)
        return (code, "功能点删除成功")


async def task_pool_lock_service(
    r: Request,
    task_id: str
) -> tuple:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        task: TaskPool = await task_pool_get(session, task_id)
        if not task:
            raise DivExcep(
                code=StandardBusinessEnum.UNKNOWN.value[0],
                msg="功能点不存在"
            )
        code: int = await task_pool_update(session, task_id, {"status": 2})
        return (code, "功能点锁定成功")
