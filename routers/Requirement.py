from pathlib import Path
from fastapi.requests import Request
from fastapi import APIRouter, Depends, File, UploadFile

from fastapi.responses import JSONResponse, FileResponse

from depends.Auth import authentication
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardResTemplate import StandardResponse
from dantics.ReqDantic import RequirementAdd, RequirementFileDownload, RequirementDetail, RequirementModify
from service.RequirementCenter import (
    requirement_file_upload,
    requirement_file_download,
    requirement_file_delete,
    requirement_file_modify,
    requirement_add,
    requirement_list,
    requirement_detail,
    requirement_modify,
    req_source_list,
    req_status_list,
    req_priority_list,
)

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

@requirement.delete("/del")
async def delete_req_file(
    r: Request,
    data: RequirementFileDownload = Depends(),
    success_auth: tuple = Depends(authentication)
) -> JSONResponse:
    if success_auth[0] != StandardBusinessEnum.SUCCESS.value[0]:
        return JSONResponse(status_code=200, content=StandardResponse(
            code=success_auth[0], msg=success_auth[1], data=None, path=None
        ).info)
    else:
        del_res: tuple = await requirement_file_delete(
            r,
            success_auth[1],
            data.requirement_id,
            data.related_doc_id
        )
        return JSONResponse(status_code=200, content=StandardResponse(
            code=del_res[0], msg=del_res[1], data=None, path=None
        ).info)

@requirement.post("/add")
async def add_req_one(
    r: Request,
    data: RequirementAdd,
    success_auth: tuple = Depends(authentication)
) -> JSONResponse:
    if success_auth[0] != StandardBusinessEnum.SUCCESS.value[0]:
        return JSONResponse(status_code=200, content=StandardResponse(
            code=success_auth[0], msg=success_auth[1], data=None, path=None
        ).info)
    else:
        add_res: tuple = await requirement_add(r, data)
        return JSONResponse(status_code=200, content=StandardResponse(
            code=add_res[0], msg=add_res[1], data=None, path=None
        ).info)

@requirement.post("/related")
async def add_req_related(
    r: Request,
    data: RequirementFileDownload,
    success_auth: tuple = Depends(authentication)
) -> JSONResponse:
    if success_auth[0] != StandardBusinessEnum.SUCCESS.value[0]:
        return JSONResponse(status_code=200, content=StandardResponse(
            code=success_auth[0], msg=success_auth[1], data=None, path=None
        ).info)
    else:
        mod_res: tuple = await requirement_file_modify(r, success_auth[1], data)
        return JSONResponse(status_code=200, content=StandardResponse(
            code=mod_res[0], msg=mod_res[1], data=None, path=None
        ).info)

@requirement.get("/source")
async def get_source_list(
    r: Request,
) -> JSONResponse:
    res: tuple = await req_source_list(r)
    return JSONResponse(status_code=200, content=StandardResponse(
        code=res[0], msg=res[1], data=res[2] if len(res) > 2 else None, path=None
    ).info)

@requirement.get("/status")
async def get_status_list(
    r: Request,
) -> JSONResponse:
    res: tuple = await req_status_list(r)
    return JSONResponse(status_code=200, content=StandardResponse(
        code=res[0], msg=res[1], data=res[2] if len(res) > 2 else None, path=None
    ).info)

@requirement.get("/priority")
async def get_priority_list(
    r: Request,
) -> JSONResponse:
    res: tuple = await req_priority_list(r)
    return JSONResponse(status_code=200, content=StandardResponse(
        code=res[0], msg=res[1], data=res[2] if len(res) > 2 else None, path=None
    ).info)

@requirement.get("/list")
async def get_requirement_list(
    r: Request,
    success_auth: tuple = Depends(authentication)
) -> JSONResponse:
    if success_auth[0] != StandardBusinessEnum.SUCCESS.value[0]:
        return JSONResponse(status_code=200, content=StandardResponse(
            code=success_auth[0], msg=success_auth[1], data=None, path=None
        ).info)
    res: tuple = await requirement_list(r)
    return JSONResponse(status_code=200, content=StandardResponse(
        code=res[0], msg=res[1], data=res[2] if len(res) > 2 else None, path=None
    ).info)

@requirement.get("/detail")
async def get_requirement_detail(
    r: Request,
    data: RequirementDetail = Depends(),
    success_auth: tuple = Depends(authentication)
) -> JSONResponse:
    if success_auth[0] != StandardBusinessEnum.SUCCESS.value[0]:
        return JSONResponse(status_code=200, content=StandardResponse(
            code=success_auth[0], msg=success_auth[1], data=None, path=None
        ).info)
    res: tuple = await requirement_detail(r, data.requirement_id)
    return JSONResponse(status_code=200, content=StandardResponse(
        code=res[0], msg=res[1], data=res[2] if len(res) > 2 else None, path=None
    ).info)

@requirement.put("/modify")
async def modify_requirement(
    r: Request,
    data: RequirementModify,
    success_auth: tuple = Depends(authentication)
) -> JSONResponse:
    if success_auth[0] != StandardBusinessEnum.SUCCESS.value[0]:
        return JSONResponse(status_code=200, content=StandardResponse(
            code=success_auth[0], msg=success_auth[1], data=None, path=None
        ).info)
    else:
        mod_res: tuple = await requirement_modify(r, success_auth[1], data)
        return JSONResponse(status_code=200, content=StandardResponse(
            code=mod_res[0], msg=mod_res[1], data=None, path=None
        ).info)
