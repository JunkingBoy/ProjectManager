from sqlalchemy.sql import Select
from sqlalchemy.engine import Result
from sqlalchemy import select, and_, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models.TbUser import User
from utils.Logs import ExceptionLog
from utils.Excptions import DivExcep
from models.TbRequirements import Requirements
from templates.StandardDBTemplate import TbRequirementsTemplate
from enums.StandardBusEnum import StandardBusinessEnum, StandardReqStatusEnum
from templates.StandardRepositoryTemplate import StandardRequirementsInfoTemplate

async def requirement_create(
    session: AsyncSession,
    req_template: TbRequirementsTemplate
) -> StandardBusinessEnum:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        new_req: Requirements = Requirements(data=req_template)
        session.add(new_req)
        await session.commit()
        await session.refresh(new_req)
        e.info(f"需求创建成功{new_req.info}")
        return StandardBusinessEnum.SUCCESS
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

async def confirm_user_doc_relation(
    session: AsyncSession,
    decrypted_uid: str,
    decrypted_related_doc_id: str,
    decrypted_requirement_id: str | None = None
) -> StandardBusinessEnum:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        conditions: list = [
            Requirements.related_doc == decrypted_related_doc_id,  # type: ignore
        ]
        if not decrypted_requirement_id: conditions.append(Requirements.person == decrypted_uid)  # type: ignore
        else:
            conditions.append(
                and_(
                    Requirements.requirement_id == decrypted_requirement_id, # type: ignore
                    or_(
                        Requirements.person == decrypted_uid,   # type: ignore
                        Requirements.relevant == decrypted_uid  # type: ignore
                    )
                )
            )
        stmt: Select = select(Requirements).where(and_(*conditions))
        sql_res: Result = await session.execute(stmt)
        data = sql_res.scalar_one_or_none()
        if data: return StandardBusinessEnum.SUCCESS
        else: return StandardBusinessEnum.FAIL
    except SQLAlchemyError as sql_e:
        e.error(f"用户文档关系确认数据库异常{sql_e}", )
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="用户文档关系确认数据库异常"
        )
    except Exception as err:
        e.error(f"用户文档关系确认失败{err}", )
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="用户文档关系确认失败"
        )

async def requirement_list_info(
    session: AsyncSession
) -> list:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        stmt: Select = select(Requirements).where(
            Requirements.status != StandardReqStatusEnum.RELEASED.value  # type: ignore
        )
        sql_res: Result = await session.execute(stmt)
        req_list = sql_res.scalars().all()
        # 收集所有 person ID 并批量查询用户名
        person_ids: set = {req.person for req in req_list if req.person}
        if not person_ids: person_map = {}
        else:
            user_stmt: Select = select(User.uid, User.username).where( # type: ignore
                User.uid.in_(person_ids)  # type: ignore
            )
            user_res: Result = await session.execute(user_stmt)
            person_map: dict = {row.uid: row.username for row in user_res}
        result: list = [
            StandardRequirementsInfoTemplate(
                req_id=req.requirement_id,
                number=req.number,
                title=req.title,
                desc=req.description,
                status=req.status,
                priority=req.priority,
                system=req.system,
                person=person_map.get(req.person, req.person or ""),
                related_doc=req.related_doc or "",
                req_dev_tasks_count=0,
                req_dev_tasks_done_count=0,
                req_bug_count=0,
                req_bug_done_count=0,
                req_business_bug_done_count=0,
            ) for req in req_list
        ]
        return result
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
