from fastapi.requests import Request
from fastapi import APIRouter, Depends

from fastapi.responses import JSONResponse

from depends.Auth import authentication
from depends.Auth import password_verify
from dantics.UserDantic import UserLogin, UserModify
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardResTemplate import StandardResponse
from service.UserCenter import user_register, user_login, user_modify, user_list

user: APIRouter = APIRouter(
    prefix="/user",
    tags=["user"],
)

@user.post("/register")
async def register(
    r: Request,
    success_data: tuple = Depends(password_verify)
) -> JSONResponse:
    if success_data[0] != StandardBusinessEnum.SUCCESS.value[0]:
        ret_res: StandardResponse = StandardResponse(
        code=success_data[0],
        msg=success_data[1],
        data=None,
        path=None
    )
    else:
        reg_res: tuple = await user_register(r, success_data[1])
        ret_res: StandardResponse = StandardResponse(
            code=reg_res[0],
            msg=reg_res[1],
            data=None,
            path=None
        )
    return JSONResponse(
        status_code=200,
        content=ret_res.info
    )

@user.post("/login")
async def login(
    r: Request,
    data: UserLogin
) -> JSONResponse:
    log_res: tuple = await user_login(r, data)
    if log_res[0] == StandardBusinessEnum.SUCCESS.value[0]:
        ret_res: StandardResponse = StandardResponse(
            code=log_res[0],
            msg=log_res[1],
            data=log_res[2],
            path=None
        )
    else:
        ret_res: StandardResponse = StandardResponse(
            code=log_res[0],
            msg=log_res[1],
            data=None,
            path=None
        )
    return JSONResponse(
        status_code=200,
        content=ret_res.info
    )

@user.put("/mod")
async def modify(
    r: Request,
    data: UserModify,
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
        mod_res: tuple = await user_modify(r, data, success_auth[1])
        ret_res: StandardResponse = StandardResponse(
            code=mod_res[0],
            msg=mod_res[1],
            data=None,
            path=None
        )
    return JSONResponse(
        status_code=200,
        content=ret_res.info
    )

@user.get("/list")
async def info(
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
        list_res: tuple = await user_list(r)
        if list_res[0] == StandardBusinessEnum.SUCCESS.value[0]:
            ret_res: StandardResponse = StandardResponse(
                code=list_res[0],
                msg=list_res[1],
                data=list_res[2],
                path=None
            )
        else:
            ret_res: StandardResponse = StandardResponse(
                code=list_res[0],
                msg=list_res[1],
                data=None,
                path=None
            )
    return JSONResponse(
        status_code=200,
        content=ret_res.info
    )
