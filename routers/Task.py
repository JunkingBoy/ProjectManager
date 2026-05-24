from fastapi.requests import Request
from fastapi import APIRouter, Depends

from fastapi.responses import JSONResponse

from depends.Auth import authentication
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardResTemplate import StandardResponse
from dantics.TasksDantic import TasksAdd, RequirementTask, TaskStatusChange, TaskTransferOwner, TaskStatus, TaskDescModify, TaskRemarkModify, TaskDelete
from service.TasksCenter import (
    task_terminal_list,
    task_status_list,
    task_add,
    task_about_requirement_list,
    task_about_user_by_status_list,
    task_status_change,
    task_transfer_owner,
    task_desc_modify,
    task_remark_modify,
    task_delete,
    task_bug_list,
    task_statistics,
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

@task.get("/requirement")
async def get_task_about_requirement(
    r: Request,
    data: RequirementTask = Depends(),
    success_auth: tuple = Depends(authentication)
) -> JSONResponse:
    if success_auth[0] != StandardBusinessEnum.SUCCESS.value[0]:
        return JSONResponse(status_code=200, content=StandardResponse(
            code=success_auth[0], msg=success_auth[1], data=None, path=None
        ).info)
    else:
        res: tuple = await task_about_requirement_list(r, data.req_id)
        return JSONResponse(status_code=200, content=StandardResponse(
            code=res[0], msg=res[1], data=res[2] if len(res) > 2 else None, path=None
        ).info)

@task.get("/user/status")
async def get_user_status_tasks(
    r: Request,
    data: TaskStatus = Depends(),
    success_auth: tuple = Depends(authentication)
) -> JSONResponse:
    if success_auth[0] != StandardBusinessEnum.SUCCESS.value[0]:
        return JSONResponse(status_code=200, content=StandardResponse(
            code=success_auth[0], msg=success_auth[1], data=None, path=None
        ).info)
    res: tuple = await task_about_user_by_status_list(r, data.status, success_auth[1])
    return JSONResponse(status_code=200, content=StandardResponse(
        code=res[0], msg=res[1], data=res[2] if len(res) > 2 else None, path=None
    ).info)

@task.put("/status")
async def change_task_status(
    r: Request,
    data: TaskStatusChange,
    success_auth: tuple = Depends(authentication)
) -> JSONResponse:
    if success_auth[0] != StandardBusinessEnum.SUCCESS.value[0]:
        return JSONResponse(status_code=200, content=StandardResponse(
            code=success_auth[0], msg=success_auth[1], data=None, path=None
        ).info)
    else:
        change_res: tuple = await task_status_change(r, success_auth[1], data)
        return JSONResponse(status_code=200, content=StandardResponse(
            code=change_res[0], msg=change_res[1], data=None, path=None
        ).info)

@task.put("/transfer")
async def transfer_task_owner(
    r: Request,
    data: TaskTransferOwner,
    success_auth: tuple = Depends(authentication)
) -> JSONResponse:
    if success_auth[0] != StandardBusinessEnum.SUCCESS.value[0]:
        return JSONResponse(status_code=200, content=StandardResponse(
            code=success_auth[0], msg=success_auth[1], data=None, path=None
        ).info)
    else:
        transfer_res: tuple = await task_transfer_owner(r, success_auth[1], data)
        return JSONResponse(status_code=200, content=StandardResponse(
            code=transfer_res[0], msg=transfer_res[1], data=None, path=None
        ).info)

@task.put("/modify/desc")
async def modify_task_desc(
    r: Request,
    data: TaskDescModify,
    success_auth: tuple = Depends(authentication)
) -> JSONResponse:
    if success_auth[0] != StandardBusinessEnum.SUCCESS.value[0]:
        return JSONResponse(status_code=200, content=StandardResponse(
            code=success_auth[0], msg=success_auth[1], data=None, path=None
        ).info)
    else:
        mod_res: tuple = await task_desc_modify(r, success_auth[1], data)
        return JSONResponse(status_code=200, content=StandardResponse(
            code=mod_res[0], msg=mod_res[1], data=None, path=None
        ).info)

@task.put("/modify/remark")
async def modify_task_remark(
    r: Request,
    data: TaskRemarkModify,
    success_auth: tuple = Depends(authentication)
) -> JSONResponse:
    if success_auth[0] != StandardBusinessEnum.SUCCESS.value[0]:
        return JSONResponse(status_code=200, content=StandardResponse(
            code=success_auth[0], msg=success_auth[1], data=None, path=None
        ).info)
    else:
        mod_res: tuple = await task_remark_modify(r, success_auth[1], data)
        return JSONResponse(status_code=200, content=StandardResponse(
            code=mod_res[0], msg=mod_res[1], data=None, path=None
        ).info)

@task.delete("/del")
async def delete_task(
    r: Request,
    data: TaskDelete = Depends(),
    success_auth: tuple = Depends(authentication)
) -> JSONResponse:
    if success_auth[0] != StandardBusinessEnum.SUCCESS.value[0]:
        return JSONResponse(status_code=200, content=StandardResponse(
            code=success_auth[0], msg=success_auth[1], data=None, path=None
        ).info)
    else:
        del_res: tuple = await task_delete(r, success_auth[1], data)
        return JSONResponse(status_code=200, content=StandardResponse(
            code=del_res[0], msg=del_res[1], data=None, path=None
        ).info)

@task.get("/bug")
async def get_task_bug_list(
    r: Request,
    success_auth: tuple = Depends(authentication)
) -> JSONResponse:
    if success_auth[0] != StandardBusinessEnum.SUCCESS.value[0]:
        return JSONResponse(status_code=200, content=StandardResponse(
            code=success_auth[0], msg=success_auth[1], data=None, path=None
        ).info)
    res: tuple = await task_bug_list(r, success_auth[1])
    return JSONResponse(status_code=200, content=StandardResponse(
        code=res[0], msg=res[1], data=res[2] if len(res) > 2 else None, path=None
    ).info)

@task.get("/statistics")
async def get_task_statistics(
    r: Request,
    data: RequirementTask = Depends(),
    success_auth: tuple = Depends(authentication)
) -> JSONResponse:
    if success_auth[0] != StandardBusinessEnum.SUCCESS.value[0]:
        return JSONResponse(status_code=200, content=StandardResponse(
            code=success_auth[0], msg=success_auth[1], data=None, path=None
        ).info)
    res: tuple = await task_statistics(r, success_auth[1], data)
    return JSONResponse(status_code=200, content=StandardResponse(
        code=res[0], msg=res[1], data=res[2] if len(res) > 2 else None, path=None
    ).info)
