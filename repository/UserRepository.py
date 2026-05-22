from typing import Sequence
from sqlalchemy.sql import Select, Update
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, and_, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.TbUser import User
from utils.Encry import decrypt
from utils.Logs import ExceptionLog
from utils.Excptions import DivExcep
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardDBTemplate import TbUserTemplate
from templates.StandardRepositoryTemplate import StandardUserRepositoryTemplate, StandardUserModRepositoryTemplate

async def email_repeat_check(
    session: AsyncSession,
    encrypted_email: str
) -> bool:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        user_sql: Select = select(User).where(
            and_(
                User.email == encrypted_email, # type: ignore
                User.active == 0,                  # type: ignore
                User.deleted == 0                  # type: ignore
            )
        )
        sql_res: Result = await session.execute(user_sql)
        user_info = sql_res.scalar_one_or_none()
        if user_info: return True
        else: return False
    except SQLAlchemyError as sql_e:
        e.error(f"邮箱数据查询异常{sql_e}", )
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="邮箱数据查询异常"
        )
    except Exception as err:
        e.error(f"邮箱数据查询失败{err}", )
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="邮箱数据查询失败"
        )

async def user_repeat_normal(
    session: AsyncSession,
    decrypted_uid: str
) -> bool:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        user_sql: Select = select(User).where(
            and_(
                User.uid == decrypted_uid, # type: ignore
                User.active == 0,                  # type: ignore
                User.deleted == 0                  # type: ignore
            )
        )
        sql_res: Result = await session.execute(user_sql)
        user_info = sql_res.scalar_one_or_none()
        if user_info: return True
        else: return False
    except SQLAlchemyError as sql_e:
        e.error(f"用户确认异常{sql_e}", )
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="用户确认异常"
        )
    except Exception as err:
        e.error(f"用户确认失败{err}", )
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="用户确认失败"
        )

async def user_uid(
    session: AsyncSession,
    encrypted_data: StandardUserRepositoryTemplate
) -> str:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        user_sql: Select = select(User).where(
            and_(
                User.phone == encrypted_data.phone, # type: ignore
                User.active == 0,                  # type: ignore
                User.deleted == 0                  # type: ignore
            )
        )
        sql_res: Result = await session.execute(user_sql)
        user_info = sql_res.scalar_one_or_none()
        return user_info.uid # type: ignore
    except SQLAlchemyError as sql_e:
        e.error(f"用户ID查询异常{sql_e}", )
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="用户ID查询异常"
        )
    except Exception as err:
        e.error(f"用户ID查询失败{err}", )
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="用户ID查询失败"
        )

async def user_alive(
    session: AsyncSession,
    encrypted_data: StandardUserRepositoryTemplate
) -> StandardBusinessEnum:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        user_sql: Select = select(User).where(
            and_(
                User.phone == encrypted_data.phone, # type: ignore
                User.active == 0,                  # type: ignore
                User.deleted == 0                  # type: ignore
            )
        )
        sql_res: Result = await session.execute(user_sql)
        user_info = sql_res.scalar_one_or_none()
        if not user_info: return StandardBusinessEnum.UNREGISTERED
        else:
            # 密码校验
            if await decrypt(user_info.password) != encrypted_data.password: return StandardBusinessEnum.PWDERROR
            return StandardBusinessEnum.SUCCESS
    except SQLAlchemyError as sql_e:
        e.error(f"用户数据查询异常{sql_e}", )
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="用户数据查询异常"
        )
    except Exception as err:
        e.error(f"用户数据查询失败{err}", )
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="用户数据查询失败"
        )

async def user_create(
    session: AsyncSession,
    user_tmplate: TbUserTemplate
) -> StandardBusinessEnum:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        # 创建User对象
        new_user: User = User(user=user_tmplate)
        session.add(new_user)
        await session.commit()
        # 刷新数据库
        await session.refresh(new_user)
        e.info(f"用户创建成功{new_user.info}")
        return StandardBusinessEnum.SUCCESS
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"用户创建数据库异常{sql_e}", )
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="用户创建数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"用户创建失败{err}", )
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="用户创建失败"
        )

async def user_update(
    session: AsyncSession,
    user_mod_template: StandardUserModRepositoryTemplate
) -> StandardBusinessEnum:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        # uid是解密值
        update_data: dict = {"username": user_mod_template.username}
        if user_mod_template.password is not None: update_data["password"] = user_mod_template.password
        stmt: Update = update(User).where(
            User.uid == user_mod_template.uid # type: ignore
        ).values(**update_data).execution_options(synchronize_session="fetch")
        res_rows: Result = await session.execute(stmt)
        if res_rows.rowcount != 1: return StandardBusinessEnum.FAIL # type: ignore
        await session.commit()
        return StandardBusinessEnum.SUCCESS
    except SQLAlchemyError as sql_e:
        e.error(f"用户数据修改异常{sql_e}", )
        await session.rollback()
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="用户数据修改异常"
        )
    except Exception as err:
        e.error(f"用户数据修改失败{err}", )
        await session.rollback()
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="用户数据修改失败"
        )

async def user_all(
    session: AsyncSession
) -> list:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        user_sql: Select = select(User).where(
            and_(
                User.active == 0,   # type: ignore
                User.deleted == 0,  # type: ignore
            )
        )
        sql_res: Result = await session.execute(user_sql)
        user_list: Sequence = sql_res.scalars().all()
        result: list = [{"uid": user.uid, "username": user.username} for user in user_list]
        return result
    except SQLAlchemyError as sql_e:
        e.error(f"用户列表查询异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="用户列表查询异常"
        )
    except Exception as err:
        e.error(f"用户列表查询失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="用户列表查询失败"
        )

async def user_info(
    session: AsyncSession,
    decrypted_uid: str
) -> tuple:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        user_sql: Select = select(User).where(
            and_(
                User.uid == decrypted_uid,  # type: ignore
                User.active == 0,           # type: ignore
                User.deleted == 0           # type: ignore
            )
        )
        sql_res: Result = await session.execute(user_sql)
        user_info = sql_res.scalar_one_or_none()
        if not user_info: return (StandardBusinessEnum.FAIL, None)
        return (StandardBusinessEnum.SUCCESS, user_info.username)
    except SQLAlchemyError as sql_e:
        e.error(f"用户信息查询异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="用户信息查询异常"
        )
    except Exception as err:
        e.error(f"用户信息查询失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="用户信息查询失败"
        )
