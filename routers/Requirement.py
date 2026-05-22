from pathlib import Path
from fastapi.requests import Request
from fastapi import APIRouter, Depends, File, UploadFile

from fastapi.responses import JSONResponse, FileResponse

from depends.Auth import authentication
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardResTemplate import StandardResponse
from dantics.ReqDantic import RequirementAdd, RequirementFileDownload
from service.RequirementCenter import requirement_file_upload, requirement_file_download

requirement = APIRouter(
    prefix="/requirement",
    tags=["requirement"],
)

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

@requirement.get("/download", response_model=None)
async def download_req_file(
    r: Request,
    data: RequirementFileDownload = Depends(),
    success_auth: tuple = Depends(authentication)
) -> JSONResponse | FileResponse:
    if success_auth[0] != StandardBusinessEnum.SUCCESS.value[0]:
        return JSONResponse(status_code=200, content=StandardResponse(
            code=success_auth[0], msg=success_auth[1], data=None, path=None
        ).info)
    else:
        down_res: tuple = await requirement_file_download(r, success_auth[1], data)
        if down_res[0] != StandardBusinessEnum.SUCCESS.value[0]:
            return JSONResponse(status_code=200, content=StandardResponse(
                code=down_res[0], msg=down_res[1], data=None, path=None
            ).info)
        return FileResponse(
            down_res[2],
            filename=Path(down_res[2]).name,
            media_type="application/octet-stream"
        )

@requirement.post("/add")
async def add_req_one(
    r: Request,
    data: RequirementAdd,
    success_auth: tuple = Depends(authentication)
) -> JSONResponse: ...
