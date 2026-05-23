from fastapi.requests import Request
from fastapi import APIRouter, Depends

from fastapi.responses import JSONResponse

from depends.Auth import authentication
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardResTemplate import StandardResponse
from dantics.TasksDantic import TasksAdd
from service.TasksCenter import (
    task_terminal_list,
    task_status_list,
    task_add
)

task: APIRouter = APIRouter(
    prefix="/task",
    tags=["task"],
)

@task.get("/terminal")
async def get_terminal_list(
    r: Request,
) -> JSONResponse:
    res: tuple = await task_terminal_list(r)
    return JSONResponse(status_code=200, content=StandardResponse(
        code=res[0], msg=res[1], data=res[2] if len(res) > 2 else None, path=None
    ).info)

@task.get("/status")
async def get_task_status_list(
    r: Request,
) -> JSONResponse:
    res: tuple = await task_status_list(r)
    return JSONResponse(status_code=200, content=StandardResponse(
        code=res[0], msg=res[1], data=res[2] if len(res) > 2 else None, path=None
    ).info)

@task.post("/add")
async def add_task(
    r: Request,
    data: list[TasksAdd],
    success_auth: tuple = Depends(authentication)
) -> JSONResponse:
    if success_auth[0] != StandardBusinessEnum.SUCCESS.value[0]:
        return JSONResponse(status_code=200, content=StandardResponse(
            code=success_auth[0], msg=success_auth[1], data=None, path=None
        ).info)
    else:
        add_res: tuple = await task_add(r, data, success_auth[1])
        return JSONResponse(status_code=200, content=StandardResponse(
            code=add_res[0], msg=add_res[1], data=None, path=None
        ).info)
