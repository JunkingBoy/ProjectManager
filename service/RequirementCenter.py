import traceback

from pathlib import Path
from typing import Optional
from datetime import datetime
from fastapi import Request, UploadFile

from tools.Re import generate_uid
from utils.Encry import decrypt, encrypt
from utils.Pool import StandardSQLiteDBConnectPool
from repository.UserRepository import user_repeat_normal
from templates.StandardDBTemplate import TbRequirementsTemplate
from repository.RequirementRepository import requirement_create
from tools.Files import create_dir, calc_file_hash, search_download_file, del_path_or_file
from repository.RequirementRepository import confirm_user_doc_relation, requirement_list_info
from dantics.ReqDantic import RequirementAdd, RequirementFileUpload, RequirementFileDownload
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

async def requirement_file_upload(
    r: Request,
    file: UploadFile
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        RequirementFileUpload(file=file)
        content: bytes = await file.read()
        file_hash: str = calc_file_hash(content)
        date_dir: str = create_dir('downloads', need_date=True)
        today: str = Path(date_dir).name
        ext: str = Path(file.filename or "").suffix
        new_filename: str = f"{today}{file_hash}{ext}"
        dst_path: str = f"{date_dir}/{new_filename}"
        with open(dst_path, "wb") as f: f.write(content)
        await file.seek(0)
        file_tag: str = await encrypt(f"{today}{file_hash}")
        return (StandardBusinessEnum.SUCCESS.value[0], "文件上传成功", {"tag": file_tag})

async def requirement_file_download(
    r: Request,
    encrypted_uid: str,
    model: RequirementFileDownload
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
        async with db_pool.get_session() as session:
            _tmp_uid: str = await decrypt(encrypted_uid)
            _is_normal: bool = await user_repeat_normal(session, _tmp_uid)
            if not _is_normal: return (StandardBusinessEnum.FAIL.value[0], "用户状态异常")
            _tmp_requirement_id: str = await decrypt(model.requirement_id)
            _tmp_related_doc_id: str = await decrypt(model.related_doc_id)
            _is_exist: StandardBusinessEnum = await confirm_user_doc_relation(
                session,
                _tmp_uid,
                _tmp_related_doc_id,
                _tmp_requirement_id
            )
            if _is_exist != StandardBusinessEnum.SUCCESS: return (StandardBusinessEnum.FAIL.value[0], "您所下载的文件和您的关系不正确")
            _file_path: str = search_download_file("downloads", _tmp_related_doc_id)
            if not _file_path: return (StandardBusinessEnum.FAIL.value[0], "未找到文件")
            return (StandardBusinessEnum.SUCCESS.value[0], "文件下载成功", _file_path)

async def requirement_file_delete(
    r: Request,
    encrypted_uid: str,
    encrypted_related_doc_id: str
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
        async with db_pool.get_session() as session:
            _tmp_uid: str = await decrypt(encrypted_uid)
            _is_normal: bool = await user_repeat_normal(session, _tmp_uid)
            if not _is_normal: return (StandardBusinessEnum.FAIL.value[0], "用户状态异常")
            _tmp_related_doc_id: str = await decrypt(encrypted_related_doc_id)
            _is_exist: StandardBusinessEnum = await confirm_user_doc_relation(
                session,
                _tmp_uid,
                _tmp_related_doc_id
            )
            if _is_exist != StandardBusinessEnum.SUCCESS: return (StandardBusinessEnum.FAIL.value[0], "您要删除的文件和您的关系不正确")
            _file_path: str = search_download_file("downloads", _tmp_related_doc_id)
            if not _file_path: return (StandardBusinessEnum.FAIL.value[0], "未找到文件")
            del_path_or_file(_file_path, only_file=True)
            return (StandardBusinessEnum.SUCCESS.value[0], "文件删除成功")

async def requirement_list(
    r: Request
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
        async with db_pool.get_session() as session:
            raw_data: list = await requirement_list_info(session)
            result: list = []
            for item in raw_data:
                d: dict = item.info
                d["req_id"] = await encrypt(item.req_id)
                result.append(d)
            return (StandardBusinessEnum.SUCCESS.value[0], "查询成功", result)

async def req_source_list(
    r: Request
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else: return (StandardBusinessEnum.SUCCESS.value[0], "操作成功", StandardReqSourceEnum.info())

async def req_status_list(
    r: Request
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else: return (StandardBusinessEnum.SUCCESS.value[0], "操作成功", StandardReqStatusEnum.info())

async def req_priority_list(
    r: Request
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else: return (StandardBusinessEnum.SUCCESS.value[0], "操作成功", StandardReqPriorityEnum.info())
