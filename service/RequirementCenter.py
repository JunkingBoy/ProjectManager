from typing import Optional, List
from fastapi import Request

from models.TbRequirement import Requirement
from utils.Logs import ExceptionLog
from utils.Excptions import DivExcep
from enums.StandardBusEnum import StandardBusinessEnum
from tools.Re import generate_uid
from templates.StandardDBTemplate import TbRequirementTemplate
from repository.RequirementRepository import (
    requirement_list,
    requirement_get,
    requirement_create,
    requirement_update,
    requirement_delete,
)


async def requirement_list_service(
    r: Request,
    status: Optional[int] = None,
    project: Optional[str] = None,
    person: Optional[str] = None,
    keyword: Optional[str] = None
) -> List[Requirement]:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        return await requirement_list(session, status, project, person, keyword)


async def requirement_detail_service(
    r: Request,
    requirement_id: str
) -> Requirement:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        req: Requirement = await requirement_get(session, requirement_id)
        if not req:
            raise DivExcep(
                code=StandardBusinessEnum.UNKNOWN.value[0],
                msg="需求不存在"
            )
        return req


async def requirement_create_service(
    r: Request,
    data: dict
) -> tuple:
    e: ExceptionLog = ExceptionLog.get_instance()
    db_pool = r.app.state.db_pool
    template: TbRequirementTemplate = TbRequirementTemplate(
        requirement_id=generate_uid(),
        number=data.get("number", ""),
        title=data.get("title", ""),
        description=data.get("description"),
        source=data.get("source", 0),
        status=0,
        person=data.get("person"),
        relevant=data.get("relevant"),
        total=data.get("total"),
        develop=data.get("develop"),
        test=data.get("test"),
        priority=data.get("priority", 2),
        iteration=data.get("iteration"),
        project=data.get("project"),
        scheme=data.get("scheme"),
    )
    async with db_pool.get_session() as session:
        code: int = await requirement_create(session, template)
        return (code, "需求创建成功")


async def requirement_update_service(
    r: Request,
    requirement_id: str,
    data: dict
) -> tuple:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        code: int = await requirement_update(session, requirement_id, data)
        return (code, "需求更新成功")


async def requirement_claim_service(
    r: Request,
    requirement_id: str,
    person: str
) -> tuple:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        req: Requirement = await requirement_get(session, requirement_id)
        if not req:
            raise DivExcep(
                code=StandardBusinessEnum.UNKNOWN.value[0],
                msg="需求不存在"
            )
        if req.status != 0:
            raise DivExcep(
                code=StandardBusinessEnum.FAIL.value[0],
                msg="当前需求不可领取"
            )
        code: int = await requirement_update(
            session, requirement_id,
            {"status": 1, "person": person}
        )
        return (code, "需求领取成功")


async def requirement_bind_service(
    r: Request,
    requirement_id: str,
    person: str,
    relevant: Optional[str]
) -> tuple:
    db_pool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        req: Requirement = await requirement_get(session, requirement_id)
        if not req:
            raise DivExcep(
                code=StandardBusinessEnum.UNKNOWN.value[0],
                msg="需求不存在"
            )
        updates = {"person": person}
        if relevant is not None:
            updates["relevant"] = relevant
        code: int = await requirement_update(session, requirement_id, updates)
        return (code, "需求绑定成功")
