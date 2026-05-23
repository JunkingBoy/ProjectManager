from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models.TbBug import TbBugsPool
from utils.Logs import ExceptionLog
from utils.Excptions import DivExcep
from templates.StandardDBTemplate import TbBugsPoolTemplate
from enums.StandardBusEnum import StandardBusinessEnum

async def bug_create(
    session: AsyncSession,
    data: TbBugsPoolTemplate
) -> StandardBusinessEnum:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        new_bug: TbBugsPool = TbBugsPool(data=data)
        session.add(new_bug)
        await session.commit()
        e.info(f"Bug创建成功: {data.bug_id}")
        return StandardBusinessEnum.SUCCESS
    except SQLAlchemyError as sql_e:
        await session.rollback()
        e.error(f"Bug创建数据库异常{sql_e}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="Bug创建数据库异常"
        )
    except Exception as err:
        await session.rollback()
        e.error(f"Bug创建失败{err}")
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="Bug创建失败"
        )
