from typing import Optional, List
from fastapi import Request

from models.TbDevelopTask import DevelopTask
from utils.Logs import ExceptionLog
from utils.Excptions import DivExcep
from enums.StandardBusEnum import StandardBusinessEnum
from tools.Re import generate_uid
from templates.StandardDBTemplate import TbDevelopTaskTemplate
from repository.DevelopTaskRepository import (
    develop_task_list,
    develop_task_get,
    develop_task_create,
    develop_task_update,
    develop_task_delete,
)


async def develop_task_list_service(
    r: Request,
    requirement_id: Optional[str] = None,
    status: Optional[int] = None,
) -> List[DevelopTask]:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        return await develop_task_list(session, requirement_id, status)


async def develop_task_detail_service(
    r: Request,
    task_id: str
) -> DevelopTask:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        task: DevelopTask = await develop_task_get(session, task_id)
        if not task:
            raise DivExcep(
                code=StandardBusinessEnum.UNKNOWN.value[0],
                msg="研发任务不存在"
            )
        return task


async def develop_task_create_service(
    r: Request,
    data: dict
) -> tuple:
    db_pool = r.app.state.db_pool
    template: TbDevelopTaskTemplate = TbDevelopTaskTemplate(
        task_id=generate_uid(),
        requirement_id=data.get("requirement_id", ""),
        point_id=data.get("point_id"),
        title=data.get("title", ""),
        description=data.get("description"),
        status=1,
        creator=data.get("creator"),
        owner=data.get("owner"),
    )
    async with db_pool.get_session() as session:
        code: int = await develop_task_create(session, template)
        return (code, "研发任务创建成功")


async def develop_task_update_service(
    r: Request,
    task_id: str,
    data: dict
) -> tuple:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        code: int = await develop_task_update(session, task_id, data)
        return (code, "研发任务更新成功")


async def develop_task_delete_service(
    r: Request,
    task_id: str
) -> tuple:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        code: int = await develop_task_delete(session, task_id)
        return (code, "研发任务删除成功")


async def develop_task_transfer_service(
    r: Request,
    task_id: str,
    owner: str
) -> tuple:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        task: DevelopTask = await develop_task_get(session, task_id)
        if not task:
            raise DivExcep(
                code=StandardBusinessEnum.UNKNOWN.value[0],
                msg="研发任务不存在"
            )
        code: int = await develop_task_update(session, task_id, {"owner": owner})
        return (code, "研发任务转派成功")
