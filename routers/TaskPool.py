from typing import Optional
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from enums.StandardBusEnum import StandardBusinessEnum
from dantics.TaskPoolDantic import TaskPoolCreate, TaskPoolUpdate
from service.TaskPoolCenter import (
    task_pool_list_service,
    task_pool_detail_service,
    task_pool_create_service,
    task_pool_update_service,
    task_pool_delete_service,
    task_pool_lock_service,
)
from templates.StandardResTemplate import StandardResponse


task_pool: APIRouter = APIRouter(
    prefix="/feature",
    tags=["feature"],
)


@task_pool.get("/list")
async def list_task_pools(
    r: Request,
    requirement_id: Optional[str] = None,
    status: Optional[int] = None,
) -> JSONResponse:
    data = await task_pool_list_service(r, requirement_id, status)
    ret_res: StandardResponse = StandardResponse(
        code=StandardBusinessEnum.SUCCESS.value[0],
        msg="获取成功",
        data=data,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@task_pool.get("/{task_id}")
async def get_task_pool(
    task_id: str,
    r: Request,
) -> JSONResponse:
    task = await task_pool_detail_service(r, task_id)
    ret_res: StandardResponse = StandardResponse(
        code=StandardBusinessEnum.SUCCESS.value[0],
        msg="获取成功",
        data=task.info,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@task_pool.post("")
async def create_task_pool(
    data: TaskPoolCreate,
    r: Request,
) -> JSONResponse:
    res: tuple = await task_pool_create_service(r, data.info)
    ret_res: StandardResponse = StandardResponse(
        code=res[0],
        msg=res[1],
        data=None,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@task_pool.put("/{task_id}")
async def update_task_pool(
    task_id: str,
    data: TaskPoolUpdate,
    r: Request,
) -> JSONResponse:
    res: tuple = await task_pool_update_service(r, task_id, data.info)
    ret_res: StandardResponse = StandardResponse(
        code=res[0],
        msg=res[1],
        data=None,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@task_pool.delete("/{task_id}")
async def delete_task_pool(
    task_id: str,
    r: Request,
) -> JSONResponse:
    res: tuple = await task_pool_delete_service(r, task_id)
    ret_res: StandardResponse = StandardResponse(
        code=res[0],
        msg=res[1],
        data=None,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@task_pool.post("/{task_id}/lock")
async def lock_task_pool(
    task_id: str,
    r: Request,
) -> JSONResponse:
    res: tuple = await task_pool_lock_service(r, task_id)
    ret_res: StandardResponse = StandardResponse(
        code=res[0],
        msg=res[1],
        data=None,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)
