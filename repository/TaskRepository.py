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
from models.TbRequirements import Requirements
from templates.StandardDBTemplate import TbDevelopTasksPoolTmplate
from enums.StandardBusEnum import StandardBusinessEnum, StandardReqStatusEnum
from templates.StandardRepositoryTemplate import StandardRequirementsInfoTemplate, StandardRequirementsDetailTemplate, StandardRequirementsModifyTemplate, StandardRequirementsTasksInfoTemplate

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
