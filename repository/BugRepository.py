from typing import List, Optional
from sqlalchemy.sql import Select
from sqlalchemy import select, and_, desc
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models.TbBug import BugPool
from utils.Logs import ExceptionLog
from utils.Excptions import DivExcep
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardDBTemplate import TbBugTemplate


async def bug_list(
    session: AsyncSession,
    requirement_id: Optional[str] = None,
    status: Optional[int] = None,
) -> List[BugPool]:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        sql: Select = select(BugPool)
        conditions = []
        if requirement_id:
            conditions.append(BugPool.requirement_id == requirement_id)
        if status is not None:
            conditions.append(BugPool.status == status)
        if conditions:
            sql = sql.where(and_(*conditions))
        sql = sql.order_by(desc(BugPool.c_time))
        sql_res: Result = await session.execute(sql)
        return list(sql_res.scalars().all())
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


async def bug_get(
    session: AsyncSession,
    bug_id: str
) -> Optional[BugPool]:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        sql: Select = select(BugPool).where(BugPool.bug_id == bug_id)
        sql_res: Result = await session.execute(sql)
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


async def bug_create(
    session: AsyncSession,
    template: TbBugTemplate
) -> int:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        new_bug: BugPool = BugPool(data=template)
        session.add(new_bug)
        await session.commit()
        await session.refresh(new_bug)
        e.info(f"Bug创建成功{new_bug.info}")
        return StandardBusinessEnum.SUCCESS.value[0]
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


async def bug_update(
    session: AsyncSession,
    bug_id: str,
    updates: dict
) -> int:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        sql: Select = select(BugPool).where(BugPool.bug_id == bug_id)
        sql_res: Result = await session.execute(sql)
        bug: BugPool = sql_res.scalar_one_or_none()
        if not bug:
            raise DivExcep(
                code=StandardBusinessEnum.UNKNOWN.value[0],
                msg="Bug不存在"
            )
        for key, value in updates.items():
            if hasattr(bug, key) and value is not None:
                setattr(bug, key, value)
        await session.commit()
        await session.refresh(bug)
        e.info(f"Bug更新成功{bug_id}")
        return StandardBusinessEnum.SUCCESS.value[0]
    except DivExcep:
        raise
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"Bug更新数据库异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="Bug更新数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"Bug更新失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="Bug更新失败"
        )


async def bug_delete(
    session: AsyncSession,
    bug_id: str
) -> int:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        sql: Select = select(BugPool).where(BugPool.bug_id == bug_id)
        sql_res: Result = await session.execute(sql)
        bug: BugPool = sql_res.scalar_one_or_none()
        if not bug:
            raise DivExcep(
                code=StandardBusinessEnum.UNKNOWN.value[0],
                msg="Bug不存在"
            )
        await session.delete(bug)
        await session.commit()
        e.info(f"Bug删除成功{bug_id}")
        return StandardBusinessEnum.SUCCESS.value[0]
    except DivExcep:
        raise
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"Bug删除数据库异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="Bug删除数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"Bug删除失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="Bug删除失败"
        )
