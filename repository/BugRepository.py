from datetime import datetime
from sqlalchemy.sql import Select
from sqlalchemy.engine import Result
from sqlalchemy import select, and_, or_, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models.TbUser import User
from models.TbBug import TbBugsPool
from utils.Logs import ExceptionLog
from utils.Excptions import DivExcep
from templates.StandardDBTemplate import TbBugsPoolTemplate
from templates.StandardRepositoryTemplate import StandardBugListInfoTemplate
from enums.StandardBusEnum import StandardBusinessEnum, StandardBugStatusEnum

async def bug_create(
    session: AsyncSession,
    data: TbBugsPoolTemplate
) -> StandardBusinessEnum:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        new_bug: TbBugsPool = TbBugsPool(data=data)
        session.add(new_bug)
        await session.commit()
        e.info(f"Bug创建成功: {data.bug_id}")
        return StandardBusinessEnum.SUCCESS
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"Bug创建数据库异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="Bug创建数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"Bug创建失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="Bug创建失败"
        )

async def bug_list(
    session: AsyncSession,
    decrypted_uid: str | None,
    decrypted_req_id: str | None,
    decrypted_owner: str | None,
    status: int | None,
    filter_self_created: bool = False,
    filter_self_assigned: bool = False,
    decrypted_task_id: str | None = None,
) -> list:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        conditions: list = []
        if filter_self_created:
            conditions.append(TbBugsPool.creator == decrypted_uid)  # type: ignore
        elif filter_self_assigned:
            conditions.append(TbBugsPool.owner == decrypted_uid)  # type: ignore
        elif decrypted_uid is not None:
            conditions.append(
                or_(TbBugsPool.creator == decrypted_uid, TbBugsPool.owner == decrypted_uid)  # type: ignore
            )
        if decrypted_req_id is not None:
            conditions.append(TbBugsPool.requirement_id == decrypted_req_id)  # type: ignore
        if decrypted_owner is not None:
            conditions.append(TbBugsPool.owner == decrypted_owner)  # type: ignore
        if status is not None:
            conditions.append(TbBugsPool.status == status)  # type: ignore
        if decrypted_task_id is not None:
            conditions.append(TbBugsPool.task_id == decrypted_task_id)  # type: ignore
        stmt: Select = select(TbBugsPool)
        if conditions: stmt = stmt.where(and_(*conditions))
        sql_res: Result = await session.execute(stmt)
        bug_list = sql_res.scalars().all()
        uid_set: set = set()
        for bug in bug_list:
            if bug.creator: uid_set.add(bug.creator)
            if bug.owner: uid_set.add(bug.owner)
            if bug.developer: uid_set.add(bug.developer)
        if not uid_set: user_map = {}
        else:
            user_stmt: Select = select(User.uid, User.username).where(  # type: ignore
                User.uid.in_(uid_set)  # type: ignore
            )
            user_res: Result = await session.execute(user_stmt)
            user_map: dict = {row.uid: row.username for row in user_res}
        result: list = [
            StandardBugListInfoTemplate(
                bug_id=bug.bug_id,
                req_id=bug.requirement_id,
                task_id=bug.task_id or "",
                title=bug.title,
                desc=bug.description or "",
                expected_res=bug.expected_res or "",
                status=bug.status,
                creator=user_map.get(bug.creator, bug.creator or ""),
                owner=user_map.get(bug.owner, bug.owner or ""),
                developer=user_map.get(bug.developer, bug.developer or ""),
                c_time=int(bug.c_time.timestamp()) if bug.c_time else 0,
                u_time=int(bug.u_time.timestamp()) if bug.u_time else 0,
            ) for bug in bug_list
        ]
        return result
    except SQLAlchemyError as sql_e:
        e.error(f"Bug列表查询异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="Bug列表查询异常"
        )
    except Exception as err:
        e.error(f"Bug列表查询失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="Bug列表查询失败"
        )

async def bug_detail(
    session: AsyncSession,
    decrypted_bug_id: str
) -> TbBugsPool | None:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        stmt: Select = select(TbBugsPool).where(
            TbBugsPool.bug_id == decrypted_bug_id  # type: ignore
        )
        sql_res: Result = await session.execute(stmt)
        return sql_res.scalar_one_or_none()
    except SQLAlchemyError as sql_e:
        e.error(f"Bug详情查询异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="Bug详情查询异常"
        )
    except Exception as err:
        e.error(f"Bug详情查询失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="Bug详情查询失败"
        )

async def bug_count_by_req_id(
    session: AsyncSession,
    decrypted_req_id: str,
    status: int | None = None,
    have_task: bool | None = None
) -> int:
    """查询需求下 Bug 总数，支持按 status 和 have_task 过滤"""
    if not decrypted_req_id: return 0
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        conditions: list = [TbBugsPool.requirement_id == decrypted_req_id]  # type: ignore
        if status is not None:
            conditions.append(TbBugsPool.status == status)  # type: ignore
        if have_task is True:
            conditions.append(TbBugsPool.task_id.isnot(None))  # type: ignore
        elif have_task is False:
            conditions.append(TbBugsPool.task_id.is_(None))  # type: ignore
        stmt: Select = select(func.count(TbBugsPool.bug_id)).where(  # type: ignore
            and_(*conditions)
        )
        sql_res: Result = await session.execute(stmt)
        return sql_res.scalar() or 0
    except SQLAlchemyError as sql_e:
        e.error(f"需求Bug数量查询异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求Bug数量查询异常"
        )
    except Exception as err:
        e.error(f"需求Bug数量查询失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求Bug数量查询失败"
        )


async def bug_count_grouped_by_req_id(
    session: AsyncSession,
    decrypted_req_id: str,
    have_task: bool | None = None
) -> dict:
    """查询需求下按 status 分组的 Bug 计数，返回 {total, unfix, fix, nonbug, close}"""
    if not decrypted_req_id: return {"total": 0, "unfix": 0, "fix": 0, "nonbug": 0, "close": 0}
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        conditions: list = [TbBugsPool.requirement_id == decrypted_req_id]  # type: ignore
        if have_task is True:
            conditions.append(TbBugsPool.task_id.isnot(None))  # type: ignore
        elif have_task is False:
            conditions.append(TbBugsPool.task_id.is_(None))  # type: ignore
        stmt: Select = select(
            func.count(TbBugsPool.bug_id), # type: ignore
            func.sum(case((TbBugsPool.status == StandardBugStatusEnum.UNFIX.value, 1), else_=0)), # type: ignore
            func.sum(case((TbBugsPool.status == StandardBugStatusEnum.FIX.value, 1), else_=0)), # type: ignore
            func.sum(case((TbBugsPool.status == StandardBugStatusEnum.NONBUG.value, 1), else_=0)), # type: ignore
            func.sum(case((TbBugsPool.status == StandardBugStatusEnum.CLOSE.value, 1), else_=0)), # type: ignore
        ).where(and_(*conditions))
        sql_res: Result = await session.execute(stmt)
        row = sql_res.one()
        return {
            "total": row[0] or 0,
            "unfix": row[1] or 0,
            "fix": row[2] or 0,
            "nonbug": row[3] or 0,
            "close": row[4] or 0,
        }
    except SQLAlchemyError as sql_e:
        e.error(f"需求Bug分组统计查询异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求Bug分组统计查询异常"
        )
    except Exception as err:
        e.error(f"需求Bug分组统计查询失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求Bug分组统计查询失败"
        )


async def bug_count_by_task_id(
    session: AsyncSession,
    decrypted_task_id: str
) -> int:
    """查询指定任务下关联的 Bug 数量"""
    if not decrypted_task_id: return 0
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        stmt: Select = select(func.count(TbBugsPool.bug_id)).where(  # type: ignore
            TbBugsPool.task_id == decrypted_task_id  # type: ignore
        )
        sql_res: Result = await session.execute(stmt)
        return sql_res.scalar() or 0
    except SQLAlchemyError as sql_e:
        e.error(f"Bug数量查询异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="Bug数量查询异常"
        )
    except Exception as err:
        e.error(f"Bug数量查询失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="Bug数量查询失败"
        )

async def bug_modify(
    session: AsyncSession,
    decrypted_bug_id: str,
    decrypted_uid: str,
    title: str = "",
    desc: str = "",
    expected_res: str = "",
    owner: str = "",
    developer: str = "",
) -> StandardBusinessEnum:
    """修改 Bug 信息，校验 creator 或 owner"""
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        stmt: Select = select(TbBugsPool).where(
            TbBugsPool.bug_id == decrypted_bug_id  # type: ignore
        )
        sql_res: Result = await session.execute(stmt)
        bug = sql_res.scalar_one_or_none()
        if not bug: return StandardBusinessEnum.FAIL
        if bug.creator != decrypted_uid and bug.owner != decrypted_uid:
            return StandardBusinessEnum.FAIL
        if title: bug.title = title
        if desc: bug.description = desc
        if expected_res: bug.expected_res = expected_res
        if owner: bug.owner = owner
        if developer: bug.developer = developer
        bug.u_time = datetime.now()
        await session.commit()
        e.info(f"Bug信息修改成功: {decrypted_bug_id}")
        return StandardBusinessEnum.SUCCESS
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"Bug修改数据库异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="Bug修改数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"Bug修改失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="Bug修改失败"
        )

async def bug_status_change(
    session: AsyncSession,
    decrypted_bug_id: str,
    decrypted_uid: str,
    new_status: int
) -> tuple[StandardBusinessEnum, str]:
    """变更Bug状态，校验owner，返回(结果, task_id)"""
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        stmt: Select = select(TbBugsPool).where(
            TbBugsPool.bug_id == decrypted_bug_id  # type: ignore
        )
        sql_res: Result = await session.execute(stmt)
        bug = sql_res.scalar_one_or_none()
        if not bug: return (StandardBusinessEnum.FAIL, "")
        if bug.owner != decrypted_uid: return (StandardBusinessEnum.FAIL, "")
        task_id: str = bug.task_id or ""
        bug.status = new_status
        bug.u_time = datetime.now()
        await session.commit()
        e.info(f"Bug状态修改成功: {decrypted_bug_id}")
        return (StandardBusinessEnum.SUCCESS, task_id)
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"Bug状态修改数据库异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="Bug状态修改数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"Bug状态修改失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="Bug状态修改失败"
        )

async def bug_open_count_by_task_id(
    session: AsyncSession,
    decrypted_task_id: str
) -> int:
    """查询指定任务下状态为 UNFIX(0) 的 Bug 数量"""
    if not decrypted_task_id: return 0
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        stmt: Select = select(func.count(TbBugsPool.bug_id)).where(  # type: ignore
            and_(
                TbBugsPool.task_id == decrypted_task_id,  # type: ignore
                TbBugsPool.status == StandardBugStatusEnum.UNFIX.value  # type: ignore
            )
        )
        sql_res: Result = await session.execute(stmt)
        return sql_res.scalar() or 0
    except SQLAlchemyError as sql_e:
        e.error(f"Bug开放数量查询异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="Bug开放数量查询异常"
        )
    except Exception as err:
        e.error(f"Bug开放数量查询失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="Bug开放数量查询失败"
        )

async def bug_distinct_task_ids(
    session: AsyncSession,
    task_ids: list,
    status: int | None = None
) -> set:
    """批量查询哪些 task_id 存在关联的 Bug，可选按 status 过滤，返回有 Bug 的 task_id 集合"""
    if not task_ids: return set()
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        conditions: list = [TbBugsPool.task_id.in_(task_ids)]  # type: ignore
        if status is not None:
            conditions.append(TbBugsPool.status == status)  # type: ignore
        stmt: Select = select(TbBugsPool.task_id).distinct().where(  # type: ignore
            and_(*conditions)
        )
        sql_res: Result = await session.execute(stmt)
        return {row[0] for row in sql_res}
    except SQLAlchemyError as sql_e:
        e.error(f"Bug任务ID查询异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="Bug任务ID查询异常"
        )
    except Exception as err:
        e.error(f"Bug任务ID查询失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="Bug任务ID查询失败"
        )
