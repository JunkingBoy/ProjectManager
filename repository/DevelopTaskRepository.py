from typing import List, Optional
from sqlalchemy.sql import Select
from sqlalchemy import select, and_, desc
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models.TbDevelopTask import DevelopTask
from utils.Logs import ExceptionLog
from utils.Excptions import DivExcep
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardDBTemplate import TbDevelopTaskTemplate


async def develop_task_list(
    session: AsyncSession,
    requirement_id: Optional[str] = None,
    status: Optional[int] = None,
) -> List[DevelopTask]:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        sql: Select = select(DevelopTask)
        conditions = []
        if requirement_id:
            conditions.append(DevelopTask.requirement_id == requirement_id)
        if status is not None:
            conditions.append(DevelopTask.status == status)
        if conditions:
            sql = sql.where(and_(*conditions))
        sql = sql.order_by(desc(DevelopTask.c_time))
        sql_res: Result = await session.execute(sql)
        return list(sql_res.scalars().all())
    except SQLAlchemyError as sql_e:
        e.error(f"研发任务列表查询异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="研发任务列表查询异常"
        )
    except Exception as err:
        e.error(f"研发任务列表查询失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="研发任务列表查询失败"
        )


async def develop_task_get(
    session: AsyncSession,
    task_id: str
) -> Optional[DevelopTask]:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        sql: Select = select(DevelopTask).where(DevelopTask.task_id == task_id)
        sql_res: Result = await session.execute(sql)
        return sql_res.scalar_one_or_none()
    except SQLAlchemyError as sql_e:
        e.error(f"研发任务详情查询异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="研发任务详情查询异常"
        )
    except Exception as err:
        e.error(f"研发任务详情查询失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="研发任务详情查询失败"
        )


async def develop_task_create(
    session: AsyncSession,
    template: TbDevelopTaskTemplate
) -> int:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        new_task: DevelopTask = DevelopTask(data=template)
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)
        e.info(f"研发任务创建成功{new_task.info}")
        return StandardBusinessEnum.SUCCESS.value[0]
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"研发任务创建数据库异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="研发任务创建数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"研发任务创建失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="研发任务创建失败"
        )


async def develop_task_update(
    session: AsyncSession,
    task_id: str,
    updates: dict
) -> int:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        sql: Select = select(DevelopTask).where(DevelopTask.task_id == task_id)
        sql_res: Result = await session.execute(sql)
        task: DevelopTask = sql_res.scalar_one_or_none()
        if not task:
            raise DivExcep(
                code=StandardBusinessEnum.UNKNOWN.value[0],
                msg="研发任务不存在"
            )
        for key, value in updates.items():
            if hasattr(task, key) and value is not None:
                setattr(task, key, value)
        await session.commit()
        await session.refresh(task)
        e.info(f"研发任务更新成功{task_id}")
        return StandardBusinessEnum.SUCCESS.value[0]
    except DivExcep:
        raise
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"研发任务更新数据库异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="研发任务更新数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"研发任务更新失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="研发任务更新失败"
        )


async def develop_task_delete(
    session: AsyncSession,
    task_id: str
) -> int:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        sql: Select = select(DevelopTask).where(DevelopTask.task_id == task_id)
        sql_res: Result = await session.execute(sql)
        task: DevelopTask = sql_res.scalar_one_or_none()
        if not task:
            raise DivExcep(
                code=StandardBusinessEnum.UNKNOWN.value[0],
                msg="研发任务不存在"
            )
        await session.delete(task)
        await session.commit()
        e.info(f"研发任务删除成功{task_id}")
        return StandardBusinessEnum.SUCCESS.value[0]
    except DivExcep:
        raise
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"研发任务删除数据库异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="研发任务删除数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"研发任务删除失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="研发任务删除失败"
        )
