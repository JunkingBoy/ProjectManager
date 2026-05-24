from datetime import datetime
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
from templates.StandardRepositoryTemplate import StandardRequirementsInfoTemplate, StandardRequirementsDetailTemplate, StandardRequirementsModifyTemplate, StandardRequirementsTasksInfoTemplate

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
    decrypted_related_doc_id: str | None = None,
    decrypted_requirement_id: str | None = None
) -> StandardBusinessEnum:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        conditions: list = [
            or_(
                Requirements.person == decrypted_uid,    # type: ignore
                Requirements.relevant == decrypted_uid   # type: ignore
            )
        ]
        if decrypted_related_doc_id is not None:
            conditions.append(Requirements.related_doc == decrypted_related_doc_id)  # type: ignore
        if decrypted_requirement_id is not None:
            conditions.append(Requirements.requirement_id == decrypted_requirement_id)  # type: ignore
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
                status=req.status,
                priority=req.priority,
                system=req.system,
                person=person_map.get(req.person, req.person or ""),
                related_doc=req.related_doc or "",
                release_time=int(req.release_time.timestamp()) if req.release_time else 0,
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

async def requirement_task_list_info(
    session: AsyncSession,
    decrypted_uid: str
) -> list:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        stmt: Select = select(Requirements).where(
            Requirements.relevant == decrypted_uid,  # type: ignore
            Requirements.status != StandardReqStatusEnum.RELEASED.value # type: ignore
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
            StandardRequirementsTasksInfoTemplate(
                req_id=req.requirement_id,
                number=req.number,
                title=req.title,
                person=person_map.get(req.person, req.person or ""),
                related_doc=req.related_doc or "",
                release_time=int(req.release_time.timestamp()) if req.release_time else 0,
            ) for req in req_list
        ]
        return result
    except SQLAlchemyError as sql_e:
        e.error(f"需求任务列表查询异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求任务列表查询异常"
        )
    except Exception as err:
        e.error(f"需求任务列表查询失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求任务列表查询失败"
        )

async def requirement_mod(
    session: AsyncSession,
    data: StandardRequirementsModifyTemplate
) -> StandardBusinessEnum:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        stmt: Select = select(Requirements).where(
            and_(
                Requirements.requirement_id == data.decrypt_req_id,  # type: ignore
                or_(
                    Requirements.person == data.decrypt_uid,    # type: ignore
                    Requirements.relevant == data.decrypt_uid   # type: ignore
                )
            )
        )
        sql_res: Result = await session.execute(stmt)
        req = sql_res.scalar_one_or_none()
        if not req: return StandardBusinessEnum.FAIL
        req.relevant = data.decrypt_relevant
        req.priority = data.priority
        req.remark = data.remark
        req.release_time = data.release_time
        req.u_time = datetime.now()
        await session.commit()
        e.info(f"需求修改成功: {data.decrypt_req_id}")
        return StandardBusinessEnum.SUCCESS
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"需求修改数据库异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求修改数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"需求修改失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求修改失败"
        )

async def requirement_detail_info(
    session: AsyncSession,
    decrypted_requirement_id: str
) -> StandardRequirementsDetailTemplate | None:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        stmt: Select = select(Requirements).where(
            Requirements.requirement_id == decrypted_requirement_id  # type: ignore
        )
        sql_res: Result = await session.execute(stmt)
        req = sql_res.scalar_one_or_none()
        if not req: return None
        # 查询 relevant 对应的用户名
        relevant_name: str = req.relevant or ""
        if req.relevant:
            user_stmt: Select = select(User.username).where(User.uid == req.relevant)  # type: ignore
            user_res: Result = await session.execute(user_stmt)
            user_row = user_res.scalar_one_or_none()
            if user_row: relevant_name = user_row
        return StandardRequirementsDetailTemplate(
            req_id=req.requirement_id,
            number=req.number,
            relevant=relevant_name,
            status=req.status,
            priority=req.priority,
            system=req.system,
            desc=req.description or "",
            release_time=int(req.release_time.timestamp()) if req.release_time else 0,
            related_doc=req.related_doc or "",
            remark=req.remark or "",
        )
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

async def requirement_status_to_test(
    session: AsyncSession,
    decrypted_req_id: str
) -> StandardBusinessEnum:
    """将需求状态变更为 TEST(1)，如果当前状态已经是 TEST 则跳过"""
    if not decrypted_req_id: return StandardBusinessEnum.FAIL
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        stmt: Select = select(Requirements).where(
            Requirements.requirement_id == decrypted_req_id  # type: ignore
        )
        sql_res: Result = await session.execute(stmt)
        req = sql_res.scalar_one_or_none()
        if not req: return StandardBusinessEnum.FAIL
        if req.status == StandardReqStatusEnum.TEST.value: return StandardBusinessEnum.SUCCESS
        req.status = StandardReqStatusEnum.TEST.value
        req.u_time = datetime.now()
        await session.commit()
        e.info(f"需求状态变更为TEST成功: {decrypted_req_id}")
        return StandardBusinessEnum.SUCCESS
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"需求状态变更数据库异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求状态变更数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"需求状态变更失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求状态变更失败"
        )

async def requirement_file_relationship_mod(
    session: AsyncSession,
    decrypted_requirement_id: str,
    decrypted_related_doc_id: str | None,
) -> StandardBusinessEnum:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        stmt: Select = select(Requirements).where(
            Requirements.requirement_id == decrypted_requirement_id  # type: ignore
        )
        sql_res: Result = await session.execute(stmt)
        req = sql_res.scalar_one_or_none()
        if not req: return StandardBusinessEnum.FAIL
        req.related_doc = decrypted_related_doc_id
        req.u_time = datetime.now()
        await session.commit()
        e.info(f"需求关联文档修改成功: {decrypted_requirement_id}")
        return StandardBusinessEnum.SUCCESS
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"需求关联文档修改数据库异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求关联文档修改数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"需求关联文档修改失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求关联文档修改失败"
        )

async def requirement_status_to_release(
    session: AsyncSession,
    decrypted_req_id: str
) -> StandardBusinessEnum:
    """将需求状态变更为 RELEASE(3)，如果当前状态已经是 RELEASE 则跳过"""
    if not decrypted_req_id: return StandardBusinessEnum.FAIL
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        stmt: Select = select(Requirements).where(
            Requirements.requirement_id == decrypted_req_id  # type: ignore
        )
        sql_res: Result = await session.execute(stmt)
        req = sql_res.scalar_one_or_none()
        if not req: return StandardBusinessEnum.FAIL
        if req.status == StandardReqStatusEnum.RELEASE.value:
            return StandardBusinessEnum.SUCCESS
        req.status = StandardReqStatusEnum.RELEASE.value
        req.u_time = datetime.now()
        await session.commit()
        e.info(f"需求状态变更为RELEASE成功: {decrypted_req_id}")
        return StandardBusinessEnum.SUCCESS
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"需求状态变更数据库异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求状态变更数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"需求状态变更失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求状态变更失败"
        )

async def requirement_person_by_id(
    session: AsyncSession,
    decrypted_req_id: str
) -> str | None:
    """查询需求的person字段"""
    if not decrypted_req_id: return None
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        stmt: Select = select(Requirements.person).where(  # type: ignore
            Requirements.requirement_id == decrypted_req_id  # type: ignore
        )
        sql_res: Result = await session.execute(stmt)
        return sql_res.scalar_one_or_none()
    except SQLAlchemyError as sql_e:
        e.error(f"需求处理人查询异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求处理人查询异常"
        )
    except Exception as err:
        e.error(f"需求处理人查询失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="需求处理人查询失败"
        )
