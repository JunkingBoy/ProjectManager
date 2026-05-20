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
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardDBTemplate import TbUserTemplate
from dantics.UserDantic import UserRegister, UserLogin, UserToken
from templates.StandardSysTemplate import StandardTokenInfoTemplate
from tools.Re import is_valid_email, is_valid_phone, is_valid_password
from templates.StandardRepositoryTemplate import StandardUserRepositoryTemplate
from repository.UserRepository import user_alive, user_create, email_repeat_check, user_repeat_normal

async def user_check(
    r: Request,
    model: UserToken
) -> tuple:
    db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        user_repeat_res: bool = await user_repeat_normal(session, model.uid)
        if not user_repeat_res: return StandardBusinessEnum.FAIL.value[0], "用户已注销"
        else: return StandardBusinessEnum.SUCCESS.value[0], await decrypt(model.uid)

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
                    uid=await encrypt(alive_res[1]),
                    exp=int((datetime.now(tz=UTCTime) + timedelta(minutes=240)).timestamp())
                )
                auth: str = await create_access_token(token_inner_info)
                return (StandardBusinessEnum.SUCCESS.value[0], "登录成功", {"token": auth})