from fastapi import APIRouter
from fastapi.requests import Request

from fastapi.responses import JSONResponse

from service.KeyCenter import get_aes_key
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardResTemplate import StandardResponse

key: APIRouter = APIRouter(
    prefix="/key",
    tags=["key"],
)

@key.get("/key")
async def get_key(
    r: Request
) -> JSONResponse:
    key_res: tuple = await get_aes_key(r)
    if key_res[0] == StandardBusinessEnum.SUCCESS.value[0]:
        ret_res: StandardResponse = StandardResponse(
            code=key_res[0],
            msg=key_res[1],
            data=key_res[2],
            path=None
        )
    else:
        ret_res: StandardResponse = StandardResponse(
            code=key_res[0],
            msg=key_res[1],
            data=None,
            path=None
        )
    return JSONResponse(
        status_code=200,
        content=ret_res.info
    )
