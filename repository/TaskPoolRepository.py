from typing import List, Optional
from sqlalchemy.sql import Select
from sqlalchemy import select, and_, desc
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models.TbTaskPool import TaskPool
from utils.Logs import ExceptionLog
from utils.Excptions import DivExcep
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardDBTemplate import TbTaskPoolTemplate


async def task_pool_list(
    session: AsyncSession,
    requirement_id: Optional[str] = None,
    status: Optional[int] = None,
) -> List[TaskPool]:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        sql: Select = select(TaskPool)
        conditions = []
        if requirement_id:
            conditions.append(TaskPool.requirement_id == requirement_id)
        if status is not None:
            conditions.append(TaskPool.status == status)
        if conditions:
            sql = sql.where(and_(*conditions))
        sql = sql.order_by(desc(TaskPool.c_time))
        sql_res: Result = await session.execute(sql)
        return list(sql_res.scalars().all())
    except SQLAlchemyError as sql_e:
        e.error(f"功能点列表查询异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="功能点列表查询异常"
        )
    except Exception as err:
        e.error(f"功能点列表查询失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="功能点列表查询失败"
        )


async def task_pool_get(
    session: AsyncSession,
    task_id: str
) -> Optional[TaskPool]:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        sql: Select = select(TaskPool).where(TaskPool.task_id == task_id)
        sql_res: Result = await session.execute(sql)
        return sql_res.scalar_one_or_none()
    except SQLAlchemyError as sql_e:
        e.error(f"功能点详情查询异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="功能点详情查询异常"
        )
    except Exception as err:
        e.error(f"功能点详情查询失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="功能点详情查询失败"
        )


async def task_pool_create(
    session: AsyncSession,
    template: TbTaskPoolTemplate
) -> int:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        new_task: TaskPool = TaskPool(data=template)
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)
        e.info(f"功能点创建成功{new_task.info}")
        return StandardBusinessEnum.SUCCESS.value[0]
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"功能点创建数据库异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="功能点创建数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"功能点创建失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="功能点创建失败"
        )


async def task_pool_update(
    session: AsyncSession,
    task_id: str,
    updates: dict
) -> int:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        sql: Select = select(TaskPool).where(TaskPool.task_id == task_id)
        sql_res: Result = await session.execute(sql)
        task: TaskPool = sql_res.scalar_one_or_none()
        if not task:
            raise DivExcep(
                code=StandardBusinessEnum.UNKNOWN.value[0],
                msg="功能点不存在"
            )
        for key, value in updates.items():
            if hasattr(task, key) and value is not None:
                setattr(task, key, value)
        await session.commit()
        await session.refresh(task)
        e.info(f"功能点更新成功{task_id}")
        return StandardBusinessEnum.SUCCESS.value[0]
    except DivExcep:
        raise
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"功能点更新数据库异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="功能点更新数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"功能点更新失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="功能点更新失败"
        )


async def task_pool_delete(
    session: AsyncSession,
    task_id: str
) -> int:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        sql: Select = select(TaskPool).where(TaskPool.task_id == task_id)
        sql_res: Result = await session.execute(sql)
        task: TaskPool = sql_res.scalar_one_or_none()
        if not task:
            raise DivExcep(
                code=StandardBusinessEnum.UNKNOWN.value[0],
                msg="功能点不存在"
            )
        await session.delete(task)
        await session.commit()
        e.info(f"功能点删除成功{task_id}")
        return StandardBusinessEnum.SUCCESS.value[0]
    except DivExcep:
        raise
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"功能点删除数据库异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="功能点删除数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"功能点删除失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="功能点删除失败"
        )
