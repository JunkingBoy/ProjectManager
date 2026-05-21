from fastapi.requests import Request
from fastapi import APIRouter, Depends

from fastapi.responses import JSONResponse

from depends.Auth import authentication
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardResTemplate import StandardResponse
from service.NoSqlCenter import get_nosql_type_list

dict: APIRouter = APIRouter(
    prefix="/dict",
    tags=["dict"],
)

@dict.get("/get/all")
async def get_all(
    r: Request,
    success_auth: tuple = Depends(authentication)
) -> JSONResponse:
    if success_auth[0] != StandardBusinessEnum.SUCCESS.value[0]:
        ret_res: StandardResponse = StandardResponse(
            code=success_auth[0],
            msg=success_auth[1],
            data=None,
            path=None
        )
    service_res: tuple = await get_nosql_type_list(r)
    if service_res[0] == StandardBusinessEnum.SUCCESS.value[0]:
        ret_res: StandardResponse = StandardResponse(
            code=service_res[0],
            msg=service_res[1],
            data=service_res[2],
            path=None
        )
    else:
        ret_res: StandardResponse = StandardResponse(
            code=service_res[0],
            msg=service_res[1],
            data=None,
            path=None
        )
    return JSONResponse(
        status_code=200,
        content=ret_res.info
    )
