from pathlib import Path
from typing import Optional
from datetime import datetime
from fastapi import Request

from tools.Re import generate_uid
from utils.Encry import decrypt, encrypt
from utils.Pool import StandardSQLiteDBConnectPool
from repository.UserRepository import user_repeat_normal
from dantics.TasksDantic import TasksAdd, TaskStatusChange, TaskTransferOwner, TaskDescModify, TaskRemarkModify, TaskDelete
from repository.TaskRepository import tasks_create, task_list, tasks_status_change, tasks_transfer_owner, tasks_desc_modify, tasks_remark_modify, tasks_delete
from repository.BugRepository import bug_distinct_task_ids, bug_count_by_task_id
from models.TbWork import TasksPool

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

async def task_about_requirement_list(
    r: Request,
    encrypted_requirement_id: str
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
        async with db_pool.get_session() as session:
            _decrypted_requirement_id: str = await decrypt(encrypted_requirement_id)
            raw_data: list = await task_list(session, {"requirement_id": _decrypted_requirement_id})
            result: list = []
            for item in raw_data:
                d: dict = item.info
                d["task_id"] = await encrypt(item.task_id) if item.task_id else ""
                d["req_id"] = await encrypt(item.req_id) if item.req_id else ""
                result.append(d)
            return (StandardBusinessEnum.SUCCESS.value[0], "查询成功", result)

async def task_about_user_by_status_list(
    r: Request,
    status: int,
    decrypted_uid: str
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
        async with db_pool.get_session() as session:
            raw_data: list = await task_list(session, {"owner": decrypted_uid, "status": status}, order_by_column=TasksPool.end_time.desc())  # type: ignore
            result: list = []
            for item in raw_data:
                d: dict = item.info
                d["task_id"] = await encrypt(item.task_id) if item.task_id else ""
                d["req_id"] = await encrypt(item.req_id) if item.req_id else ""
                result.append(d)
            return (StandardBusinessEnum.SUCCESS.value[0], "查询成功", result)

async def task_status_change(
    r: Request,
    decrypted_uid: str,
    model: TaskStatusChange
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        _decrypted_task_id: str = await decrypt(model.task_id)
        db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
        async with db_pool.get_session() as session:
            _is_normal: bool = await user_repeat_normal(session, decrypted_uid)
            if not _is_normal: return (StandardBusinessEnum.FAIL.value[0], "用户状态异常")
            if model.status == StandardDevTasksStatusEnum.CLOSE.value:
                bug_count: int = await bug_count_by_task_id(session, _decrypted_task_id)
                if bug_count > 0: return (StandardBusinessEnum.FAIL.value[0], "该任务下还有关联Bug未处理，无法关闭")
            _res: StandardBusinessEnum = await tasks_status_change(session, decrypted_uid, _decrypted_task_id, model.status)
            if _res != StandardBusinessEnum.SUCCESS: return (StandardBusinessEnum.FAIL.value[0], "任务不存在或无权限修改")
            return (StandardBusinessEnum.SUCCESS.value[0], "任务状态修改成功")

async def task_transfer_owner(
    r: Request,
    decrypted_uid: str,
    model: TaskTransferOwner
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        _decrypted_task_id: str = await decrypt(model.task_id)
        _decrypted_owner_id: str = await decrypt(model.transfer_uid)
        db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
        async with db_pool.get_session() as session:
            _is_normal: bool = await user_repeat_normal(session, decrypted_uid)
            if not _is_normal: return (StandardBusinessEnum.FAIL.value[0], "用户状态异常")
            _res: StandardBusinessEnum = await tasks_transfer_owner(session, decrypted_uid, _decrypted_task_id, _decrypted_owner_id)
            if _res != StandardBusinessEnum.SUCCESS: return (StandardBusinessEnum.FAIL.value[0], "任务不存在或无权限转移")
            return (StandardBusinessEnum.SUCCESS.value[0], "任务负责人转移成功")

async def task_desc_modify(
    r: Request,
    decrypted_uid: str,
    model: TaskDescModify
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        _decrypted_task_id: str = await decrypt(model.task_id)
        db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
        async with db_pool.get_session() as session:
            _is_normal: bool = await user_repeat_normal(session, decrypted_uid)
            if not _is_normal: return (StandardBusinessEnum.FAIL.value[0], "用户状态异常")
            _res: StandardBusinessEnum = await tasks_desc_modify(session, decrypted_uid, _decrypted_task_id, model.desc)
            if _res != StandardBusinessEnum.SUCCESS: return (StandardBusinessEnum.FAIL.value[0], "任务不存在或无权修改描述")
            return (StandardBusinessEnum.SUCCESS.value[0], "任务描述修改成功")

async def task_remark_modify(
    r: Request,
    decrypted_uid: str,
    model: TaskRemarkModify
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        _decrypted_task_id: str = await decrypt(model.task_id)
        db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
        async with db_pool.get_session() as session:
            _is_normal: bool = await user_repeat_normal(session, decrypted_uid)
            if not _is_normal: return (StandardBusinessEnum.FAIL.value[0], "用户状态异常")
            _res: StandardBusinessEnum = await tasks_remark_modify(session, _decrypted_task_id, model.remark)
            if _res != StandardBusinessEnum.SUCCESS: return (StandardBusinessEnum.FAIL.value[0], "任务不存在")
            return (StandardBusinessEnum.SUCCESS.value[0], "任务备注修改成功")

async def task_delete(
    r: Request,
    decrypted_uid: str,
    data: TaskDelete
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        _decrypted_task_id: str = await decrypt(data.task_id)
        db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
        async with db_pool.get_session() as session:
            _is_normal: bool = await user_repeat_normal(session, decrypted_uid)
            if not _is_normal: return (StandardBusinessEnum.FAIL.value[0], "用户状态异常")
            _res: StandardBusinessEnum = await tasks_delete(session, decrypted_uid, _decrypted_task_id)
            if _res != StandardBusinessEnum.SUCCESS: return (StandardBusinessEnum.FAIL.value[0], "任务不存在或无权限删除")
            return (StandardBusinessEnum.SUCCESS.value[0], "任务删除成功")

async def task_bug_list(
    r: Request,
    decrypted_uid: str,
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
        async with db_pool.get_session() as session:
            # 查当前用户负责的全部任务
            tasks: list = await task_list(session, {"owner": decrypted_uid})
            if not tasks: return (StandardBusinessEnum.SUCCESS.value[0], "查询成功", [])
            # 批量查哪些 task_id 有 Bug
            task_ids: list = [t.task_id for t in tasks if t.task_id]
            bug_task_ids: set = await bug_distinct_task_ids(session, task_ids)
            # 只返回有 Bug 的任务
            result: list = []
            for item in tasks:
                if item.task_id not in bug_task_ids: continue
                d: dict = item.info
                d["task_id"] = await encrypt(item.task_id) if item.task_id else ""
                d["req_id"] = await encrypt(item.req_id) if item.req_id else ""
                result.append(d)
            return (StandardBusinessEnum.SUCCESS.value[0], "查询成功", result)
