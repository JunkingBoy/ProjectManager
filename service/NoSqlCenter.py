from fastapi import Request

from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardSysTemplate import StandardNoSqlConnTemplate
from utils.Logs import ExceptionLog

async def get_nosql_type_list(
    r: Request
) -> tuple:
    e: ExceptionLog = ExceptionLog.get_instance()
    try:
        template: StandardNoSqlConnTemplate = StandardNoSqlConnTemplate()
        type_list: list = [
            template.SYS_NOSQL_NAME.replace(".json", ""),
            template.PROJECT_NOSQL_NAME.replace(".json", ""),
            template.PROJECT_TYPE_NOSQL_NAME.replace(".json", ""),
        ]
        e.info(f"NoSQL 类型列表获取成功: {type_list}")
        return (StandardBusinessEnum.SUCCESS.value[0], StandardBusinessEnum.SUCCESS.value[1], type_list)
    except Exception as err:
        e.error(f"NoSQL 类型列表获取失败: {str(err)}")
        return (StandardBusinessEnum.FAIL.value[0], StandardBusinessEnum.FAIL.value[1], None)
