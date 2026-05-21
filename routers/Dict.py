from fastapi.requests import Request
from fastapi import APIRouter, Depends

from fastapi.responses import JSONResponse

from depends.Auth import authentication
from dantics.DictDantic import NoSqlCheck, NoSqlAdd
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardResTemplate import StandardResponse
from service.NoSqlCenter import get_nosql_type_list, get_nosql_type_values, add_nosql_value_by_type, del_nosql_value_by_type

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
    else:
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

@dict.get("/get/{nosql}")
async def get_one(
    r: Request,
    nosql: str,
    success_auth: tuple = Depends(authentication)
) -> JSONResponse:
    if success_auth[0] != StandardBusinessEnum.SUCCESS.value[0]:
        ret_res: StandardResponse = StandardResponse(
            code=success_auth[0],
            msg=success_auth[1],
            data=None,
            path=None
        )
    else:
        NoSqlCheck(nosql=nosql)
        service_res: tuple = await get_nosql_type_values(r, nosql)
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

@dict.post("/add")
async def add_one(
    r: Request,
    data: NoSqlAdd,
    success_auth: tuple = Depends(authentication)
) -> JSONResponse:
    if success_auth[0] != StandardBusinessEnum.SUCCESS.value[0]:
        ret_res: StandardResponse = StandardResponse(
            code=success_auth[0],
            msg=success_auth[1],
            data=None,
            path=None
        )
    else:
        service_res: tuple = await add_nosql_value_by_type(r, data)
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

@dict.delete("/del/{nosql}")
async def del_one(
    r: Request,
    nosql: str,
    key: str,
    success_auth: tuple = Depends(authentication)
) -> JSONResponse:
    if success_auth[0] != StandardBusinessEnum.SUCCESS.value[0]:
        ret_res: StandardResponse = StandardResponse(
            code=success_auth[0],
            msg=success_auth[1],
            data=None,
            path=None
        )
    else:
        NoSqlCheck(nosql=nosql)
        service_res: tuple = await del_nosql_value_by_type(r, nosql, key)
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

