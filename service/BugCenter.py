from typing import Optional
from fastapi import Request

from tools.Re import generate_uid
from utils.Encry import decrypt, encrypt
from utils.Pool import StandardSQLiteDBConnectPool
from repository.BugRepository import bug_create, bug_list as bug_list_repo
from templates.StandardDBTemplate import TbBugsPoolTemplate
from enums.StandardBusEnum import StandardBusinessEnum, StandardBugStatusEnum
from dantics.BugDantic import BugAdd, BugQuery

async def bug_add(
    r: Request,
    data: BugAdd,
    decrypted_uid: str,
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
        async with db_pool.get_session() as session:
            bug_template: TbBugsPoolTemplate = TbBugsPoolTemplate(
                bug_id=generate_uid(),
                req_id=await decrypt(data.req_id),
                task_id=await decrypt(data.task_id) if data.task_id else "",
                title=data.title,
                desc=data.desc,
                expected_res=data.expected_res,
                status=StandardBugStatusEnum(data.status),
                creator=decrypted_uid,
                owner=await decrypt(data.owner) if data.owner else "",
                developer=await decrypt(data.developer) if data.developer else "",
            )
            _res: StandardBusinessEnum = await bug_create(session, bug_template)
            if _res != StandardBusinessEnum.SUCCESS: return (StandardBusinessEnum.FAIL.value[0], "Bug创建失败")
            return (StandardBusinessEnum.SUCCESS.value[0], "Bug创建成功")

async def bug_list(
    r: Request,
    decrypted_uid: str,
    data: BugQuery
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
        async with db_pool.get_session() as session:
            _req_id: str | None = await decrypt(data.req_id) if data.req_id else None
            _owner: str | None = await decrypt(data.owner) if data.owner else None
            raw_data: list = await bug_list_repo(
                session,
                decrypted_uid,
                _req_id,
                _owner,
                data.status,
                data.filter_self_created,
                data.filter_self_assigned,
            )
            result: list = []
            for item in raw_data:
                d: dict = item.info
                d["bug_id"] = await encrypt(item.bug_id) if item.bug_id else ""
                d["req_id"] = await encrypt(item.req_id) if item.req_id else ""
                d["task_id"] = await encrypt(item.task_id) if item.task_id else ""
                result.append(d)
            return (StandardBusinessEnum.SUCCESS.value[0], "查询成功", result)
