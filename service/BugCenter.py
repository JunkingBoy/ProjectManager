from typing import Optional
from fastapi import Request
from tools.Re import generate_uid
from utils.Encry import decrypt, encrypt
from utils.Pool import StandardSQLiteDBConnectPool
from models.TbBug import TbBugsPool
from repository.BugRepository import bug_create, bug_list as bug_list_repo, bug_detail as bug_detail_repo, bug_status_change as bug_status_change_repo, bug_open_count_by_task_id
from repository.UserRepository import user_map_by_uids
from repository.TaskRepository import tasks_force_status_change, task_current_status
from repository.RequirementRepository import requirement_status_to_test
from templates.StandardDBTemplate import TbBugsPoolTemplate
from enums.StandardBusEnum import StandardBusinessEnum, StandardBugStatusEnum, StandardDevTasksStatusEnum
from dantics.BugDantic import BugAdd, BugQuery, BugFilterQuery, BugDetail, BugStatusChange

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
            await requirement_status_to_test(session, bug_template.req_id)
            if bug_template.task_id:
                await tasks_force_status_change(session, bug_template.task_id, StandardDevTasksStatusEnum.BUG.value)
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

async def bug_filter_list(
    r: Request,
    decrypted_uid: str,
    data: BugFilterQuery
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
        async with db_pool.get_session() as session:
            _req_id: str | None = await decrypt(data.req_id) if data.req_id else None
            _task_id: str | None = await decrypt(data.task_id) if data.task_id else None
            raw_data: list = await bug_list_repo(
                session,
                decrypted_uid,
                _req_id,
                None,
                data.status,
                decrypted_task_id=_task_id,
            )
            result: list = []
            for item in raw_data:
                d: dict = item.info
                d["bug_id"] = await encrypt(item.bug_id) if item.bug_id else ""
                d["req_id"] = await encrypt(item.req_id) if item.req_id else ""
                d["task_id"] = await encrypt(item.task_id) if item.task_id else ""
                result.append(d)
            return (StandardBusinessEnum.SUCCESS.value[0], "查询成功", result)

async def bug_detail(
    r: Request,
    decrypted_uid: str,
    data: BugDetail
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        _decrypted_bug_id: str = await decrypt(data.bug_id)
        db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
        async with db_pool.get_session() as session:
            bug: TbBugsPool | None = await bug_detail_repo(session, _decrypted_bug_id)
            if not bug: return (StandardBusinessEnum.FAIL.value[0], "Bug不存在")
            if bug.creator != decrypted_uid and bug.developer != decrypted_uid:
                return (StandardBusinessEnum.FAIL.value[0], "无权查看")
            # 查询用户姓名映射
            uid_set: set = {bug.creator, bug.owner, bug.developer} - {""}
            user_map: dict = await user_map_by_uids(session, uid_set)
            d: dict = {
                "bug_id": await encrypt(bug.bug_id),
                "req_id": await encrypt(bug.requirement_id),
                "task_id": await encrypt(bug.task_id) if bug.task_id else "",
                "title": bug.title,
                "desc": bug.description or "",
                "expected_res": bug.expected_res or "",
                "status": bug.status,
                "creator": user_map.get(bug.creator, bug.creator or ""),
                "owner": user_map.get(bug.owner, bug.owner or ""),
                "developer": user_map.get(bug.developer, bug.developer or ""),
                "c_time": int(bug.c_time.timestamp()),
                "u_time": int(bug.u_time.timestamp()),
            }
            return (StandardBusinessEnum.SUCCESS.value[0], "查询成功", d)

async def bug_status_change(
    r: Request,
    decrypted_uid: str,
    model: BugStatusChange
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        _decrypted_bug_id: str = await decrypt(model.bug_id)
        db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
        async with db_pool.get_session() as session:
            _res, _task_id = await bug_status_change_repo(
                session, _decrypted_bug_id, decrypted_uid, model.status
            )
            if _res != StandardBusinessEnum.SUCCESS:
                return (StandardBusinessEnum.FAIL.value[0], "Bug不存在或无权限修改")
            if _task_id:
                if model.status in (StandardBugStatusEnum.CLOSE.value, StandardBugStatusEnum.FIX.value):
                    open_count: int = await bug_open_count_by_task_id(session, _task_id)
                    if open_count == 0:
                        await tasks_force_status_change(
                            session, _task_id, StandardDevTasksStatusEnum.FINISH.value
                        )
                elif model.status == StandardBugStatusEnum.UNFIX.value:
                    current_status: int | None = await task_current_status(session, _task_id)
                    if current_status is not None and current_status != StandardDevTasksStatusEnum.BUG.value:
                        await tasks_force_status_change(
                            session, _task_id, StandardDevTasksStatusEnum.BUG.value
                        )
            return (StandardBusinessEnum.SUCCESS.value[0], "Bug状态修改成功")
