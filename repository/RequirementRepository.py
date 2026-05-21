from typing import List, Optional
from sqlalchemy.sql import Select
from sqlalchemy import select, and_, or_, desc
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models.TbRequirement import Requirement
from utils.Logs import ExceptionLog
from utils.Excptions import DivExcep
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardDBTemplate import TbRequirementTemplate


async def requirement_list(
    session: AsyncSession,
    status: Optional[int] = None,
    project: Optional[str] = None,
    person: Optional[str] = None,
    keyword: Optional[str] = None
) -> List[Requirement]:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        sql: Select = select(Requirement)
        conditions = []
        if status is not None:
            conditions.append(Requirement.status == status)
        if project:
            conditions.append(Requirement.project == project)
        if person:
            conditions.append(Requirement.person == person)
        if keyword:
            conditions.append(
                or_(
                    Requirement.title.ilike(f"%{keyword}%"),
                    Requirement.number.ilike(f"%{keyword}%")
                )
            )
        if conditions:
            sql = sql.where(and_(*conditions))
        sql = sql.order_by(desc(Requirement.c_time))
        sql_res: Result = await session.execute(sql)
        return list(sql_res.scalars().all())
    except SQLAlchemyError as sql_e:
        e.error(f"需求列表查询异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求列表查询异常"
        )
    except Exception as err:
        e.error(f"需求列表查询失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求列表查询失败"
        )


async def requirement_get(
    session: AsyncSession,
    requirement_id: str
) -> Optional[Requirement]:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        sql: Select = select(Requirement).where(Requirement.requirement_id == requirement_id)
        sql_res: Result = await session.execute(sql)
        return sql_res.scalar_one_or_none()
    except SQLAlchemyError as sql_e:
        e.error(f"需求详情查询异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求详情查询异常"
        )
    except Exception as err:
        e.error(f"需求详情查询失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求详情查询失败"
        )


async def requirement_create(
    session: AsyncSession,
    template: TbRequirementTemplate
) -> int:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        new_req: Requirement = Requirement(data=template)
        session.add(new_req)
        await session.commit()
        await session.refresh(new_req)
        e.info(f"需求创建成功{new_req.info}")
        return StandardBusinessEnum.SUCCESS.value[0]
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"需求创建数据库异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求创建数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"需求创建失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求创建失败"
        )


async def requirement_update(
    session: AsyncSession,
    requirement_id: str,
    updates: dict
) -> int:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        sql: Select = select(Requirement).where(Requirement.requirement_id == requirement_id)
        sql_res: Result = await session.execute(sql)
        req: Requirement = sql_res.scalar_one_or_none()
        if not req:
            raise DivExcep(
                code=StandardBusinessEnum.UNKNOWN.value[0],
                msg="需求不存在"
            )
        for key, value in updates.items():
            if hasattr(req, key) and value is not None:
                setattr(req, key, value)
        await session.commit()
        await session.refresh(req)
        e.info(f"需求更新成功{requirement_id}")
        return StandardBusinessEnum.SUCCESS.value[0]
    except DivExcep:
        raise
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"需求更新数据库异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求更新数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"需求更新失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求更新失败"
        )


async def requirement_delete(
    session: AsyncSession,
    requirement_id: str
) -> int:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        sql: Select = select(Requirement).where(Requirement.requirement_id == requirement_id)
        sql_res: Result = await session.execute(sql)
        req: Requirement = sql_res.scalar_one_or_none()
        if not req:
            raise DivExcep(
                code=StandardBusinessEnum.UNKNOWN.value[0],
                msg="需求不存在"
            )
        req.status = 5  # 废弃
        await session.commit()
        e.info(f"需求废弃成功{requirement_id}")
        return StandardBusinessEnum.SUCCESS.value[0]
    except DivExcep:
        raise
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"需求废弃数据库异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求废弃数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"需求废弃失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求废弃失败"
        )
