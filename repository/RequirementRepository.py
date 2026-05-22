from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from utils.Logs import ExceptionLog
from utils.Excptions import DivExcep
from models.TbRequirements import Requirements
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardDBTemplate import TbRequirementsTemplate

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


