from fastapi.requests import Request
from fastapi import APIRouter, Depends, File, UploadFile

from fastapi.responses import JSONResponse

from depends.Auth import authentication
from dantics.ReqDantic import RequirementAdd
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardResTemplate import StandardResponse
from service.RequirementCenter import requirement_file_upload

requirement = APIRouter(
    prefix="/requirement",
    tags=["requirement"],
)

@requirement.post("/add")
async def add_req_one(
    r: Request,
    data: RequirementAdd,
    success_auth: tuple = Depends(authentication)
) -> JSONResponse: ...

@requirement.post("/upload")
async def upload_req_file(
    r: Request,
    file: UploadFile = File(...),
    success_auth: tuple = Depends(authentication)
) -> JSONResponse:
    if success_auth[0] != StandardBusinessEnum.SUCCESS.value[0]:
        ret_res: StandardResponse = StandardResponse(
            code=success_auth[0], msg=success_auth[1], data=None, path=None
        )
    else:
        upload_res: tuple = await requirement_file_upload(r, file)
        ret_res = StandardResponse(
            code=upload_res[0], msg=upload_res[1],
            data=upload_res[2] if len(upload_res) > 2 else None, path=None
        )
    return JSONResponse(status_code=200, content=ret_res.info)
