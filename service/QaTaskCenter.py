from typing import Optional, List
from fastapi import Request

from models.TbQaTask import QaTask
from utils.Logs import ExceptionLog
from utils.Excptions import DivExcep
from enums.StandardBusEnum import StandardBusinessEnum
from tools.Re import generate_uid
from templates.StandardDBTemplate import TbQaTaskTemplate
from repository.QaTaskRepository import (
    qa_task_list,
    qa_task_get,
    qa_task_create,
    qa_task_update,
    qa_task_delete,
)


async def qa_task_list_service(
    r: Request,
    requirement_id: Optional[str] = None,
    status: Optional[int] = None,
) -> List[QaTask]:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        return await qa_task_list(session, requirement_id, status)


async def qa_task_detail_service(
    r: Request,
    task_id: str
) -> QaTask:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        task: QaTask = await qa_task_get(session, task_id)
        if not task:
            raise DivExcep(
                code=StandardBusinessEnum.UNKNOWN.value[0],
                msg="测试任务不存在"
            )
        return task


async def qa_task_create_service(
    r: Request,
    data: dict
) -> tuple:
    db_pool = r.app.state.db_pool
    template: TbQaTaskTemplate = TbQaTaskTemplate(
        task_id=generate_uid(),
        requirement_id=data.get("requirement_id", ""),
        point_id=data.get("point_id"),
        title=data.get("title", ""),
        description=data.get("description"),
        status=1,
        creator=data.get("creator"),
        owner=data.get("owner"),
        developer=data.get("developer"),
    )
    async with db_pool.get_session() as session:
        code: int = await qa_task_create(session, template)
        return (code, "测试任务创建成功")


async def qa_task_update_service(
    r: Request,
    task_id: str,
    data: dict
) -> tuple:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        code: int = await qa_task_update(session, task_id, data)
        return (code, "测试任务更新成功")


async def qa_task_delete_service(
    r: Request,
    task_id: str
) -> tuple:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        code: int = await qa_task_delete(session, task_id)
        return (code, "测试任务删除成功")


async def qa_task_transfer_service(
    r: Request,
    task_id: str,
    owner: str
) -> tuple:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        task: QaTask = await qa_task_get(session, task_id)
        if not task:
            raise DivExcep(
                code=StandardBusinessEnum.UNKNOWN.value[0],
                msg="测试任务不存在"
            )
        code: int = await qa_task_update(session, task_id, {"owner": owner})
        return (code, "测试任务转派成功")
