from typing import Optional
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from enums.StandardBusEnum import StandardBusinessEnum
from dantics.QaTaskDantic import QaTaskCreate, QaTaskUpdate
from service.QaTaskCenter import (
    qa_task_list_service,
    qa_task_detail_service,
    qa_task_create_service,
    qa_task_update_service,
    qa_task_delete_service,
    qa_task_transfer_service,
)
from templates.StandardResTemplate import StandardResponse

qa_task: APIRouter = APIRouter(
    prefix="/qa-task",
    tags=["qa-task"],
)


@qa_task.get("/list")
async def list_qa_tasks(
    r: Request,
    requirement_id: Optional[str] = None,
    status: Optional[int] = None,
) -> JSONResponse:
    tasks = await qa_task_list_service(r, requirement_id, status)
    data = [task.info for task in tasks]
    ret_res: StandardResponse = StandardResponse(
        code=StandardBusinessEnum.SUCCESS.value[0],
        msg="获取成功",
        data=data,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@qa_task.get("/{task_id}")
async def get_qa_task(
    task_id: str,
    r: Request,
) -> JSONResponse:
    task = await qa_task_detail_service(r, task_id)
    ret_res: StandardResponse = StandardResponse(
        code=StandardBusinessEnum.SUCCESS.value[0],
        msg="获取成功",
        data=task.info,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@qa_task.post("")
async def create_qa_task(
    data: QaTaskCreate,
    r: Request,
) -> JSONResponse:
    res: tuple = await qa_task_create_service(r, data.info)
    ret_res: StandardResponse = StandardResponse(
        code=res[0],
        msg=res[1],
        data=None,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@qa_task.put("/{task_id}")
async def update_qa_task(
    task_id: str,
    data: QaTaskUpdate,
    r: Request,
) -> JSONResponse:
    res: tuple = await qa_task_update_service(r, task_id, data.info)
    ret_res: StandardResponse = StandardResponse(
        code=res[0],
        msg=res[1],
        data=None,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@qa_task.delete("/{task_id}")
async def delete_qa_task(
    task_id: str,
    r: Request,
) -> JSONResponse:
    res: tuple = await qa_task_delete_service(r, task_id)
    ret_res: StandardResponse = StandardResponse(
        code=res[0],
        msg=res[1],
        data=None,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@qa_task.post("/{task_id}/transfer")
async def transfer_qa_task(
    task_id: str,
    r: Request,
    owner: str,
) -> JSONResponse:
    res: tuple = await qa_task_transfer_service(r, task_id, owner)
    ret_res: StandardResponse = StandardResponse(
        code=res[0],
        msg=res[1],
        data=None,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)
