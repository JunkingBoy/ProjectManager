from typing import Optional
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from enums.StandardBusEnum import StandardBusinessEnum
from dantics.BugDantic import BugCreate, BugUpdate
from service.BugCenter import (
    bug_list_service,
    bug_detail_service,
    bug_create_service,
    bug_update_service,
    bug_delete_service,
    bug_transfer_service,
)
from templates.StandardResTemplate import StandardResponse

bug: APIRouter = APIRouter(
    prefix="/bug",
    tags=["bug"],
)


@bug.get("/list")
async def list_bugs(
    r: Request,
    requirement_id: Optional[str] = None,
    status: Optional[int] = None,
) -> JSONResponse:
    bugs = await bug_list_service(r, requirement_id, status)
    data = [b.info for b in bugs]
    ret_res: StandardResponse = StandardResponse(
        code=StandardBusinessEnum.SUCCESS.value[0],
        msg="获取成功",
        data=data,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@bug.get("/{bug_id}")
async def get_bug(
    bug_id: str,
    r: Request,
) -> JSONResponse:
    b = await bug_detail_service(r, bug_id)
    ret_res: StandardResponse = StandardResponse(
        code=StandardBusinessEnum.SUCCESS.value[0],
        msg="获取成功",
        data=b.info,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@bug.post("")
async def create_bug(
    data: BugCreate,
    r: Request,
) -> JSONResponse:
    res: tuple = await bug_create_service(r, data.info)
    ret_res: StandardResponse = StandardResponse(
        code=res[0],
        msg=res[1],
        data=None,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@bug.put("/{bug_id}")
async def update_bug(
    bug_id: str,
    data: BugUpdate,
    r: Request,
) -> JSONResponse:
    res: tuple = await bug_update_service(r, bug_id, data.info)
    ret_res: StandardResponse = StandardResponse(
        code=res[0],
        msg=res[1],
        data=None,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@bug.delete("/{bug_id}")
async def delete_bug(
    bug_id: str,
    r: Request,
) -> JSONResponse:
    res: tuple = await bug_delete_service(r, bug_id)
    ret_res: StandardResponse = StandardResponse(
        code=res[0],
        msg=res[1],
        data=None,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@bug.post("/{bug_id}/transfer")
async def transfer_bug(
    bug_id: str,
    r: Request,
    owner: str,
) -> JSONResponse:
    res: tuple = await bug_transfer_service(r, bug_id, owner)
    ret_res: StandardResponse = StandardResponse(
        code=res[0],
        msg=res[1],
        data=None,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)
