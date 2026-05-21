from typing import Optional, List
from fastapi import Request

from models.TbBug import BugPool
from utils.Logs import ExceptionLog
from utils.Excptions import DivExcep
from enums.StandardBusEnum import StandardBusinessEnum
from tools.Re import generate_uid
from templates.StandardDBTemplate import TbBugTemplate
from repository.BugRepository import (
    bug_list,
    bug_get,
    bug_create,
    bug_update,
    bug_delete,
)


async def bug_list_service(
    r: Request,
    requirement_id: Optional[str] = None,
    status: Optional[int] = None,
) -> List[BugPool]:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        return await bug_list(session, requirement_id, status)


async def bug_detail_service(
    r: Request,
    bug_id: str
) -> BugPool:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        bug: BugPool = await bug_get(session, bug_id)
        if not bug:
            raise DivExcep(
                code=StandardBusinessEnum.UNKNOWN.value[0],
                msg="Bug不存在"
            )
        return bug


async def bug_create_service(
    r: Request,
    data: dict
) -> tuple:
    db_pool = r.app.state.db_pool
    template: TbBugTemplate = TbBugTemplate(
        bug_id=generate_uid(),
        requirement_id=data.get("requirement_id", ""),
        task_id=data.get("task_id"),
        title=data.get("title", ""),
        description=data.get("description"),
        expected_res=data.get("expected_res"),
        status=0,
        creator=data.get("creator"),
        owner=data.get("owner"),
        developer=data.get("developer"),
    )
    async with db_pool.get_session() as session:
        code: int = await bug_create(session, template)
        return (code, "Bug创建成功")


async def bug_update_service(
    r: Request,
    bug_id: str,
    data: dict
) -> tuple:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        code: int = await bug_update(session, bug_id, data)
        return (code, "Bug更新成功")


async def bug_delete_service(
    r: Request,
    bug_id: str
) -> tuple:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        code: int = await bug_delete(session, bug_id)
        return (code, "Bug删除成功")


async def bug_transfer_service(
    r: Request,
    bug_id: str,
    owner: str
) -> tuple:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        bug: BugPool = await bug_get(session, bug_id)
        if not bug:
            raise DivExcep(
                code=StandardBusinessEnum.UNKNOWN.value[0],
                msg="Bug不存在"
            )
        code: int = await bug_update(session, bug_id, {"owner": owner})
        return (code, "Bug转派成功")
