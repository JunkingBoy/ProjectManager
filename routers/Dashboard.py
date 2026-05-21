from typing import Optional
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from enums.StandardBusEnum import StandardBusinessEnum
from service.DashboardCenter import (
    yield_dashboard_service,
    employee_dashboard_service,
)
from templates.StandardResTemplate import StandardResponse

dashboard: APIRouter = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
)


@dashboard.get("/yield")
async def get_yield_dashboard(
    r: Request,
    year: Optional[int] = None,
    system: Optional[str] = None,
    project_type: Optional[str] = None,
) -> JSONResponse:
    data = await yield_dashboard_service(r, year, system, project_type)
    ret_res: StandardResponse = StandardResponse(
        code=StandardBusinessEnum.SUCCESS.value[0],
        msg="获取成功",
        data=data,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)


@dashboard.get("/employee")
async def get_employee_dashboard(
    r: Request,
    year: Optional[int] = None,
    month: Optional[int] = None,
) -> JSONResponse:
    data = await employee_dashboard_service(r, year, month)
    ret_res: StandardResponse = StandardResponse(
        code=StandardBusinessEnum.SUCCESS.value[0],
        msg="获取成功",
        data=data,
        path=None,
    )
    return JSONResponse(status_code=200, content=ret_res.info)
