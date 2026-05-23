from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from depends.Auth import authentication
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardResTemplate import StandardResponse
from dantics.BugDantic import BugAdd, BugQuery
from service.BugCenter import bug_add, bug_list

bug: APIRouter = APIRouter(
    prefix="/bug",
    tags=["bug"],
)

@bug.post("/add")
async def add_bug(
    r: Request,
    data: BugAdd,
    success_auth: tuple = Depends(authentication)
) -> JSONResponse:
    if success_auth[0] != StandardBusinessEnum.SUCCESS.value[0]:
        return JSONResponse(status_code=200, content=StandardResponse(
            code=success_auth[0], msg=success_auth[1], data=None, path=None
        ).info)
    else:
        add_res: tuple = await bug_add(r, data, success_auth[1])
        return JSONResponse(status_code=200, content=StandardResponse(
            code=add_res[0], msg=add_res[1], data=None, path=None
        ).info)


@bug.get("/list")
async def get_bug_list(
    r: Request,
    data: BugQuery = Depends(),
    success_auth: tuple = Depends(authentication)
) -> JSONResponse:
    if success_auth[0] != StandardBusinessEnum.SUCCESS.value[0]:
        return JSONResponse(status_code=200, content=StandardResponse(
            code=success_auth[0], msg=success_auth[1], data=None, path=None
        ).info)
    res: tuple = await bug_list(r, success_auth[1], data)
    return JSONResponse(status_code=200, content=StandardResponse(
        code=res[0], msg=res[1], data=res[2] if len(res) > 2 else None, path=None
    ).info)
