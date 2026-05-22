import traceback

from pathlib import Path
from typing import Optional
from fastapi import Request
from datetime import datetime

from utils.Encry import decrypt
from tools.Re import generate_uid
from dantics.ReqDantic import RequirementAdd
from utils.Pool import StandardSQLiteDBConnectPool
from templates.StandardDBTemplate import TbRequirementsTemplate
from repository.RequirementRepository import requirement_create
from enums.StandardBusEnum import StandardBusinessEnum, StandardReqSourceEnum, StandardReqStatusEnum, StandardReqPriorityEnum

async def requirement_add(
    r: Request,
    model: RequirementAdd
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
        async with db_pool.get_session() as session:
            req_template: TbRequirementsTemplate = TbRequirementsTemplate(
                req_id=generate_uid(),
                number=model.number,
                title=model.title,
                desc=model.desc,
                source=StandardReqSourceEnum(model.source),
                status=StandardReqStatusEnum(model.status),
                priority=StandardReqPriorityEnum(model.priority),
                system=await decrypt(model.system),
                project=await decrypt(model.project),
                project_type=await decrypt(model.project_type),
                person=await decrypt(model.person),
                relevant=await decrypt(model.relevant),
                related_doc=await decrypt(model.related_doc),
                total=model.total,
                dev_total=model.dev_total,
                dev_price=model.dev_price,
                test_total=model.test_total,
                test_price=model.test_price,
                business_test_total=model.business_test_total,
                business_test_price=model.business_test_price,
                release_time=datetime.fromtimestamp(float(model.release_time))
            )
            res: StandardBusinessEnum = await requirement_create(session, req_template)
            return (res.value[0], "需求创建成功")