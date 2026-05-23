from fastapi.requests import Request
from fastapi import APIRouter, Depends

from fastapi.responses import JSONResponse

from depends.Auth import authentication
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardResTemplate import StandardResponse
from service.TasksCenter import (
    terminal_list
)

task: APIRouter = APIRouter(
    prefix="/task",
    tags=["task"],
)

@task.get("/terminal")
async def get_terminal_list(
    r: Request,
) -> JSONResponse:
    res: tuple = await terminal_list(r)
    return JSONResponse(status_code=200, content=StandardResponse(
        code=res[0], msg=res[1], data=res[2] if len(res) > 2 else None, path=None
    ).info)
