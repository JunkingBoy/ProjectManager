from typing import Optional
from fastapi import Request
from datetime import datetime, timedelta

from models import UTCTime
from tools.Re import generate_uid
from tools.Files import get_env_val
from utils.Excptions import DivExcep
from utils.Encry import decrypt, encrypt
from utils.JWT import create_access_token
from utils.Pool import StandardSQLiteDBConnectPool
from dantics.UserDantic import UserRegister, UserLogin
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardDBTemplate import TbUserTemplate
from templates.StandardSysTemplate import StandardTokenInfoTemplate
from tools.Re import is_valid_email, is_valid_phone, is_valid_password
from templates.StandardRepositoryTemplate import StandardUserRepositoryTemplate
from repository.UserRepository import user_alive, user_create, email_repeat_check, user_list, user_get_by_uids

async def user_register(
    r: Request,
    model: UserRegister
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        # 拿到全局挂载的连接池
        db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
        # 提取内容解密
        decrypted_phone: str = await decrypt(model.phone)
        decrypted_email: str = await decrypt(model.email)
        decrypted_password: str = await decrypt(model.password)
        if not is_valid_phone(decrypted_phone): raise DivExcep(StandardBusinessEnum.FAIL.value[0], "手机号格式错误")
        if not is_valid_email(decrypted_email): raise DivExcep(StandardBusinessEnum.FAIL.value[0], "邮箱格式错误")
        if not is_valid_password(decrypted_password): raise DivExcep(StandardBusinessEnum.FAIL.value[0], "密码格式错误")
        # 获取系统向量
        tmp_vector: str = get_env_val("iv", "dev")
        encrypted_data: StandardUserRepositoryTemplate = StandardUserRepositoryTemplate(
            uid=None,
            phone=await encrypt(decrypted_phone, tmp_vector),
            password=decrypted_password,
            email=decrypted_email
        )
        # 拿到连接池的session
        async with db_pool.get_session() as session:
            email_repeat_res: bool = await email_repeat_check(
                session,
                await encrypt(decrypted_email, tmp_vector)
            )
            if email_repeat_res: return (StandardBusinessEnum.FAIL.value[0], "邮箱已存在")
            alive_res: tuple = await user_alive(session, encrypted_data)
            if StandardBusinessEnum.UNREGISTERED.value[0] != alive_res[0]: return (StandardBusinessEnum.FAIL.value[0], "用户已存在")
            # 加密用户数据
            tmp_uid: str = generate_uid()
            tmp_username: str = f"用户{decrypted_phone}"
            tmp_password: str = await encrypt(decrypted_password)
            tmp_email: str = await encrypt(decrypted_email, tmp_vector)
            tmp_encrypted_phone: str = await encrypt(decrypted_phone, tmp_vector)
            user_tmplate: TbUserTemplate = TbUserTemplate(
                uid=tmp_uid,
                username=tmp_username,
                phone=tmp_encrypted_phone,
                password=tmp_password,
                email=tmp_email
            )
            # 创建用户
            create_res_code: int = await user_create(session, user_tmplate)
            return (create_res_code, "用户注册成功")

async def user_login(
    r: Request,
    model: UserLogin
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        # 拿到全局挂载的连接池
        db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
        decrypted_phone: str = await decrypt(model.phone)
        decrypted_password: str = await decrypt(model.password)
        if not is_valid_phone(decrypted_phone): raise DivExcep(StandardBusinessEnum.FAIL.value[0], "手机号格式错误")
        if not is_valid_password(decrypted_password): raise DivExcep(StandardBusinessEnum.FAIL.value[0], "密码格式错误")
        # 获取系统向量
        tmp_vector: str = get_env_val("iv", "dev")
        encrypted_data: StandardUserRepositoryTemplate = StandardUserRepositoryTemplate(
            uid=None,
            phone=await encrypt(decrypted_phone, tmp_vector),
            password=decrypted_password,
            email=None
        )
        # 拿到连接池的session
        async with db_pool.get_session() as session:
            alive_res: tuple = await user_alive(session, encrypted_data)
            if StandardBusinessEnum.UNREGISTERED.value[0] == alive_res[0]: return (StandardBusinessEnum.UNREGISTERED.value[0], "用户未注册")
            elif StandardBusinessEnum.PWDERROR.value[0] == alive_res[0]: return (StandardBusinessEnum.PWDERROR.value[0], "密码错误")
            else:
                # 发布签名
                token_inner_info: StandardTokenInfoTemplate = StandardTokenInfoTemplate(
                    uid=alive_res[1],
                    exp=int((datetime.now(tz=UTCTime) + timedelta(minutes=240)).timestamp() * 1000)
                )
                auth: str = await create_access_token(token_inner_info)
                return (StandardBusinessEnum.SUCCESS.value[0], "登录成功", {"token": auth})


async def user_list_service(
    r: Request
) -> list:
    db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        users = await user_list(session)
        return [u.info for u in users]


async def user_relevant_service(
    r: Request,
    requirement_id: str
) -> list:
    from repository.RequirementRepository import requirement_get
    db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        req = await requirement_get(session, requirement_id)
        if not req:
            raise DivExcep(
                code=StandardBusinessEnum.UNKNOWN.value[0],
                msg="需求不存在"
            )
        uids = []
        if req.person:
            uids.append(req.person)
        if req.relevant:
            import json
            try:
                relevant_uids = json.loads(req.relevant)
                if isinstance(relevant_uids, list):
                    uids.extend(relevant_uids)
            except (json.JSONDecodeError, TypeError):
                pass
        if not uids:
            return []
        users = await user_get_by_uids(session, list(set(uids)))
        return [u.info for u in users]