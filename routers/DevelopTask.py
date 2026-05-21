from typing import Optional
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from enums.StandardBusEnum import StandardBusinessEnum
from dantics.DevelopTaskDantic import DevelopTaskCreate, DevelopTaskUpdate
from service.DevelopTaskCenter import (
    develop_task_list_service,
    develop_task_detail_service,
    develop_task_create_service,
    develop_task_update_service,
    develop_task_delete_service,
    develop_task_transfer_service,
)
from templates.StandardResTemplate import StandardResponse

develop_task: APIRouter = APIRouter(
    prefix="/dev-task",
    tags=["dev-task"],
)


@develop_task.get("/list")
async def list_develop_tasks(
    r: Request,
    requirement_id: Optional[str] = None,
    status: Optional[int] = None,
) -> JSONResponse:
    tasks = await develop_task_list_service(r, requirement_id, status)
    data = [task.info for task in tasks]
    ret_res: StandardResponse = StandardResponse(
        code=StandardBusinessEnum.SUCCESS.value[0],
        msg="获取成功",
        data=data,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@develop_task.get("/{task_id}")
async def get_develop_task(
    task_id: str,
    r: Request,
) -> JSONResponse:
    task = await develop_task_detail_service(r, task_id)
    ret_res: StandardResponse = StandardResponse(
        code=StandardBusinessEnum.SUCCESS.value[0],
        msg="获取成功",
        data=task.info,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@develop_task.post("")
async def create_develop_task(
    data: DevelopTaskCreate,
    r: Request,
) -> JSONResponse:
    res: tuple = await develop_task_create_service(r, data.info)
    ret_res: StandardResponse = StandardResponse(
        code=res[0],
        msg=res[1],
        data=None,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@develop_task.put("/{task_id}")
async def update_develop_task(
    task_id: str,
    data: DevelopTaskUpdate,
    r: Request,
) -> JSONResponse:
    res: tuple = await develop_task_update_service(r, task_id, data.info)
    ret_res: StandardResponse = StandardResponse(
        code=res[0],
        msg=res[1],
        data=None,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@develop_task.delete("/{task_id}")
async def delete_develop_task(
    task_id: str,
    r: Request,
) -> JSONResponse:
    res: tuple = await develop_task_delete_service(r, task_id)
    ret_res: StandardResponse = StandardResponse(
        code=res[0],
        msg=res[1],
        data=None,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@develop_task.post("/{task_id}/transfer")
async def transfer_develop_task(
    task_id: str,
    r: Request,
    owner: str,
) -> JSONResponse:
    res: tuple = await develop_task_transfer_service(r, task_id, owner)
    ret_res: StandardResponse = StandardResponse(
        code=res[0],
        msg=res[1],
        data=None,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)
