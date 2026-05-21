from fastapi import APIRouter
from fastapi.requests import Request

from fastapi.responses import JSONResponse

from enums.StandardBusEnum import StandardBusinessEnum
from dantics.UserDantic import UserRegister, UserLogin
from service.UserCenter import user_register, user_login, user_list_service, user_relevant_service
from templates.StandardResTemplate import StandardResponse

user: APIRouter = APIRouter(
    prefix="/user",
    tags=["user"],
)

@user.post("/register")
async def register(
    data: UserRegister,
    r: Request
) -> JSONResponse:
    reg_res: tuple = await user_register(r, data)
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


@user.get("/list")
async def get_user_list(
    r: Request
) -> JSONResponse:
    data = await user_list_service(r)
    ret_res: StandardResponse = StandardResponse(
        code=StandardBusinessEnum.SUCCESS.value[0],
        msg="获取成功",
        data=data,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@user.get("/relevant/{requirement_id}")
async def get_relevant_users(
    requirement_id: str,
    r: Request
) -> JSONResponse:
    data = await user_relevant_service(r, requirement_id)
    ret_res: StandardResponse = StandardResponse(
        code=StandardBusinessEnum.SUCCESS.value[0],
        msg="获取成功",
        data=data,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)

@user.post("/login")
async def login(
    data: UserLogin,
    r: Request
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