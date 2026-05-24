from sqlalchemy.sql import Select
from sqlalchemy.engine import Result
from sqlalchemy import select, and_, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models.TbUser import User
from models.TbBug import TbBugsPool
from utils.Logs import ExceptionLog
from utils.Excptions import DivExcep
from templates.StandardDBTemplate import TbBugsPoolTemplate
from templates.StandardRepositoryTemplate import StandardBugListInfoTemplate
from enums.StandardBusEnum import StandardBusinessEnum

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

async def bug_distinct_task_ids(
    session: AsyncSession,
    task_ids: list
) -> set:
    """批量查询哪些 task_id 存在关联的 Bug，返回有 Bug 的 task_id 集合"""
    if not task_ids: return set()
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        stmt: Select = select(TbBugsPool.task_id).distinct().where(  # type: ignore
            TbBugsPool.task_id.in_(task_ids)  # type: ignore
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
