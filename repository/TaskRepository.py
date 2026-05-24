from datetime import datetime
from sqlalchemy.sql import Select
from sqlalchemy.engine import Result
from sqlalchemy import select, and_, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models.TbUser import User
from utils.Logs import ExceptionLog
from utils.Excptions import DivExcep
from models.TbWork import TasksPool
from templates.StandardDBTemplate import TbDevelopTasksPoolTmplate
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardRepositoryTemplate import StandardTasksListInfoTemplate

async def tasks_desc_modify(
    session: AsyncSession,
    decrypted_uid: str,
    decrypted_task_id: str,
    new_desc: str
) -> StandardBusinessEnum:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        stmt: Select = select(TasksPool).where(
            TasksPool.task_id == decrypted_task_id  # type: ignore
        )
        sql_res: Result = await session.execute(stmt)
        task = sql_res.scalar_one_or_none()
        if not task: return StandardBusinessEnum.FAIL
        if task.creator != decrypted_uid: return StandardBusinessEnum.FAIL
        task.description = new_desc
        task.u_time = datetime.now()
        await session.commit()
        e.info(f"任务描述修改成功: {decrypted_task_id}")
        return StandardBusinessEnum.SUCCESS
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"任务描述修改数据库异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="任务描述修改数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"任务描述修改失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="任务描述修改失败"
        )

async def tasks_remark_modify(
    session: AsyncSession,
    decrypted_task_id: str,
    new_remark: str
) -> StandardBusinessEnum:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        stmt: Select = select(TasksPool).where(
            TasksPool.task_id == decrypted_task_id  # type: ignore
        )
        sql_res: Result = await session.execute(stmt)
        task = sql_res.scalar_one_or_none()
        if not task: return StandardBusinessEnum.FAIL
        task.remark = new_remark
        task.u_time = datetime.now()
        await session.commit()
        e.info(f"任务备注修改成功: {decrypted_task_id}")
        return StandardBusinessEnum.SUCCESS
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"任务备注修改数据库异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="任务备注修改数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"任务备注修改失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="任务备注修改失败"
        )

async def tasks_create(
    session: AsyncSession,
    data: list[TbDevelopTasksPoolTmplate]
) -> StandardBusinessEnum:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        for item in data:
            new_task: TasksPool = TasksPool(data=item)
            session.add(new_task)
        await session.commit()
        e.info(f"任务创建成功,共 {len(data)} 条")
        return StandardBusinessEnum.SUCCESS
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"任务创建数据库异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="任务创建数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"任务创建失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="任务创建失败"
        )

async def task_list(
    session: AsyncSession,
    filters: dict,
    order_by_column=None
) -> list:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        stmt: Select = select(TasksPool)
        conditions: list = []
        for field, value in filters.items():
            if value is not None:
                conditions.append(getattr(TasksPool, field) == value)  # type: ignore
        if conditions:
            stmt = stmt.where(and_(*conditions))
        if order_by_column is not None:
            stmt = stmt.order_by(order_by_column)
        sql_res: Result = await session.execute(stmt)
        task_list = sql_res.scalars().all()
        uid_set: set = set()
        for task in task_list:
            if task.creator: uid_set.add(task.creator)
            if task.owner: uid_set.add(task.owner)
        if not uid_set: user_map = {}
        else:
            user_stmt: Select = select(User.uid, User.username).where(  # type: ignore
                User.uid.in_(uid_set)  # type: ignore
            )
            user_res: Result = await session.execute(user_stmt)
            user_map: dict = {row.uid: row.username for row in user_res}
        result: list = [
            StandardTasksListInfoTemplate(
                task_id=task.task_id,
                req_id=task.requirement_id,
                terminal=task.terminal,
                title=task.title,
                desc=task.description or "",
                dev_total=task.develop_total or "",
                status=task.status,
                creator=user_map.get(task.creator, task.creator or ""),
                owner=user_map.get(task.owner, task.owner or ""),
                remark=task.remark or "",
                end_time=int(task.end_time.timestamp()) if task.end_time else 0,
                update_time=int(task.u_time.timestamp()) if task.u_time else 0
            ) for task in task_list
        ]
        return result
    except SQLAlchemyError as sql_e:
        e.error(f"任务列表查询异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="任务列表查询异常"
        )
    except Exception as err:
        e.error(f"任务列表查询失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="任务列表查询失败"
        )

async def tasks_status_change(
    session: AsyncSession,
    decrypted_uid: str,
    decrypted_task_id: str,
    status: int
) -> StandardBusinessEnum:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        stmt: Select = select(TasksPool).where(
            and_(
                TasksPool.task_id == decrypted_task_id,  # type: ignore
                TasksPool.owner == decrypted_uid  # type: ignore
            )
        )
        sql_res: Result = await session.execute(stmt)
        task = sql_res.scalar_one_or_none()
        if not task: return StandardBusinessEnum.FAIL
        task.status = status
        task.u_time = datetime.now()
        await session.commit()
        e.info(f"任务状态修改成功: {decrypted_task_id}")
        return StandardBusinessEnum.SUCCESS
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"任务状态修改数据库异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="任务状态修改数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"任务状态修改失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="任务状态修改失败"
        )

async def tasks_transfer_owner(
    session: AsyncSession,
    decrypted_uid: str,
    decrypted_task_id: str,
    decrypted_owner_id: str
) -> StandardBusinessEnum:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        stmt: Select = select(TasksPool).where(
            and_(
                TasksPool.task_id == decrypted_task_id,  # type: ignore
                or_(
                    TasksPool.creator == decrypted_uid,  # type: ignore
                    TasksPool.owner == decrypted_uid  # type: ignore
                )
            )
        )
        sql_res: Result = await session.execute(stmt)
        task = sql_res.scalar_one_or_none()
        if not task: return StandardBusinessEnum.FAIL
        task.owner = decrypted_owner_id
        task.u_time = datetime.now()
        await session.commit()
        e.info(f"任务负责人转移成功: {decrypted_task_id}")
        return StandardBusinessEnum.SUCCESS
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"任务负责人转移数据库异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="任务负责人转移数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"任务负责人转移失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="任务负责人转移失败"
        )
