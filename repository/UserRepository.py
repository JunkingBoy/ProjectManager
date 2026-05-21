from typing import List
from sqlalchemy.sql import Select
from sqlalchemy import select, and_
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models.TbUser import User
from utils.Encry import decrypt
from utils.Logs import ExceptionLog
from utils.Excptions import DivExcep
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardDBTemplate import TbUserTemplate
from templates.StandardRepositoryTemplate import StandardUserRepositoryTemplate

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

async def user_alive(
    session: AsyncSession,
    encrypted_data: StandardUserRepositoryTemplate
) -> tuple:
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
        if not user_info: return StandardBusinessEnum.UNREGISTERED.value[0], StandardBusinessEnum.UNREGISTERED.value[1]
        else:
            # 密码校验
            if await decrypt(user_info.password) != encrypted_data.password: return StandardBusinessEnum.PWDERROR.value[0], StandardBusinessEnum.PWDERROR.value[1]
            return StandardBusinessEnum.SUCCESS.value[0], user_info.uid
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
) -> int:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        # 创建User对象
        new_user: User = User(user=user_tmplate)
        session.add(new_user)
        await session.commit()
        # 刷新数据库
        await session.refresh(new_user)
        e.info(f"用户创建成功{new_user.info}")
        return StandardBusinessEnum.SUCCESS.value[0]
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


async def user_list(
    session: AsyncSession
) -> List[User]:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        user_sql: Select = select(User).where(
            and_(
                User.active == 0,  # type: ignore
                User.deleted == 0  # type: ignore
            )
        )
        sql_res: Result = await session.execute(user_sql)
        return list(sql_res.scalars().all())
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


async def user_get_by_uids(
    session: AsyncSession,
    uids: List[str]
) -> List[User]:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        user_sql: Select = select(User).where(
            and_(
                User.uid.in_(uids),  # type: ignore
                User.active == 0,    # type: ignore
                User.deleted == 0    # type: ignore
            )
        )
        sql_res: Result = await session.execute(user_sql)
        return list(sql_res.scalars().all())
    except SQLAlchemyError as sql_e:
        e.error(f"用户批量查询异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="用户批量查询异常"
        )
    except Exception as err:
        e.error(f"用户批量查询失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="用户批量查询失败"
        )
