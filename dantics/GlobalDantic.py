from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from fastapi.exceptions import RequestValidationError, ResponseValidationError

from utils.Logs import ExceptionLog
from utils.Excptions import DivExcep
from enums.StandardBusEnum import StandardBusinessEnum
from enums.StandardErrEnum import StandardGlobalErrEnum
from templates.StandardResTemplate import StandardResponse

class CoreModel(BaseModel):
    @classmethod
    async def Global_Model_Error_Catch(
        cls,
        r: Request,
        e: RequestValidationError | ResponseValidationError | ValidationError
    ) -> JSONResponse:
        l: ExceptionLog = ExceptionLog.get_instance()
        res_errors: list = []
        log_errors: list = []
        for error in e.errors():
            res_errors.append({
                "param": error["loc"][0] if isinstance(e, ValidationError) else error["loc"][1],
                "msg": StandardGlobalErrEnum.get_msg_by_type(error["type"]) if StandardGlobalErrEnum.get_msg_by_type(error["type"]) else error["msg"],
            })
            log_errors.append({
                "typ": error["type"], # 全局错误类型
                "loc": error["loc"], # 请求包含的参数以及位置
                "msg": error["msg"],
                "input": error["input"], # 实际参数输入
                "path": r.url.path,
                "ctx": error["ctx"] if "ctx" in error else None
            })
        l.info(f"请求失败,完整响应结构体为 {log_errors}")
        return JSONResponse(
            status_code=200,
            content=StandardResponse(
                code=StandardBusinessEnum.FAIL.value[0],
                msg=StandardBusinessEnum.FAIL.value[1],
                data=res_errors,
                path=r.url.path
            ).info
        )

    @classmethod
    async def Global_Bussiness_Error_Catch(
        cls,
        r: Request,
        e: DivExcep
    ) -> JSONResponse: return JSONResponse(
        status_code=200,
        content=StandardResponse(
            code=e.code,
            msg=e.msg,
            data=None,
            path=r.url.path
        ).info
    )
