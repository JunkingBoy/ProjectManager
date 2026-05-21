from typing import Optional
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse

from enums.StandardBusEnum import StandardBusinessEnum
from dantics.RequirementDantic import (
    RequirementCreate,
    RequirementUpdate,
    RequirementClaim,
    RequirementBind,
)
from service.RequirementCenter import (
    requirement_list_service,
    requirement_detail_service,
    requirement_create_service,
    requirement_update_service,
    requirement_claim_service,
    requirement_bind_service,
)
from templates.StandardResTemplate import StandardResponse
from utils.JWT import verify_access_token
from utils.Excptions import DivExcep


async def jwt_dependency(token: str):
    code, result = await verify_access_token(token)
    if code != StandardBusinessEnum.SUCCESS.value[0]:
        raise DivExcep(code=code, msg=result)
    return result


requirement: APIRouter = APIRouter(
    prefix="/requirement",
    tags=["requirement"],
)


@requirement.get("/list")
async def list_requirements(
    r: Request,
    status: Optional[int] = None,
    project: Optional[str] = None,
    person: Optional[str] = None,
    keyword: Optional[str] = None,
) -> JSONResponse:
    reqs = await requirement_list_service(r, status, project, person, keyword)
    data = [req.info for req in reqs]
    ret_res: StandardResponse = StandardResponse(
        code=StandardBusinessEnum.SUCCESS.value[0],
        msg="获取成功",
        data=data,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@requirement.get("/{requirement_id}")
async def get_requirement(
    requirement_id: str,
    r: Request,
) -> JSONResponse:
    req = await requirement_detail_service(r, requirement_id)
    ret_res: StandardResponse = StandardResponse(
        code=StandardBusinessEnum.SUCCESS.value[0],
        msg="获取成功",
        data=req.info,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@requirement.post("")
async def create_requirement(
    data: RequirementCreate,
    r: Request,
) -> JSONResponse:
    res: tuple = await requirement_create_service(r, data.info)
    ret_res: StandardResponse = StandardResponse(
        code=res[0],
        msg=res[1],
        data=None,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@requirement.put("/{requirement_id}")
async def update_requirement(
    requirement_id: str,
    data: RequirementUpdate,
    r: Request,
) -> JSONResponse:
    res: tuple = await requirement_update_service(r, requirement_id, data.info)
    ret_res: StandardResponse = StandardResponse(
        code=res[0],
        msg=res[1],
        data=None,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@requirement.post("/{requirement_id}/claim")
async def claim_requirement(
    requirement_id: str,
    data: RequirementClaim,
    r: Request,
) -> JSONResponse:
    res: tuple = await requirement_claim_service(r, requirement_id, data.person)
    ret_res: StandardResponse = StandardResponse(
        code=res[0],
        msg=res[1],
        data=None,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@requirement.post("/{requirement_id}/bind")
async def bind_requirement(
    requirement_id: str,
    data: RequirementBind,
    r: Request,
) -> JSONResponse:
    res: tuple = await requirement_bind_service(
        r, requirement_id, data.person, data.relevant
    )
    ret_res: StandardResponse = StandardResponse(
        code=res[0],
        msg=res[1],
        data=None,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)
