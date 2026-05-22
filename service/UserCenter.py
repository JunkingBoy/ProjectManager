import json
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
from templates.StandardDBTemplate import TbUserTemplate
from templates.StandardSysTemplate import StandardTokenInfoTemplate
from tools.Re import is_valid_email, is_valid_phone, is_valid_password
from enums.StandardBusEnum import StandardBusinessEnum, StandardUserRoleEnum
from dantics.UserDantic import UserRegister, UserLogin, UserToken, UserModify
from templates.StandardRepositoryTemplate import StandardUserRepositoryTemplate, StandardUserModRepositoryTemplate
from repository.UserRepository import user_alive, user_create, email_repeat_check, user_repeat_normal, user_update, user_uid, user_all, user_info

async def user_check(
    r: Request,
    model: UserToken
) -> StandardBusinessEnum:
    db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
    async with db_pool.get_session() as session:
        _tmp_decrypted_uid: str = await decrypt(model.uid)
        user_repeat_res: bool = await user_repeat_normal(session, _tmp_decrypted_uid)
        if not user_repeat_res: return StandardBusinessEnum.FAIL
        else: return StandardBusinessEnum.SUCCESS

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
        # 解密并校验角色
        decrypted_role: str = await decrypt(model.role)
        try: role_list: list = json.loads(decrypted_role)
        except json.JSONDecodeError: raise DivExcep(StandardBusinessEnum.FAIL.value[0], "角色数据格式异常")
        if not isinstance(role_list, list) or not role_list: raise DivExcep(StandardBusinessEnum.FAIL.value[0], "角色数据格式错误")
        valid_values: set = {item.value for item in StandardUserRoleEnum}
        for r in role_list:
            if r not in valid_values: raise DivExcep(StandardBusinessEnum.FAIL.value[0], f"非法角色值: {r}")
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
            alive_res: StandardBusinessEnum = await user_alive(session, encrypted_data)
            if StandardBusinessEnum.UNREGISTERED != alive_res: return (StandardBusinessEnum.FAIL.value[0], "用户已存在")
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
                email=tmp_email,
                role=json.dumps(role_list)
            )
            # 创建用户
            create_res_code: StandardBusinessEnum = await user_create(session, user_tmplate)
            return (create_res_code.value[0], "用户注册成功")

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
            alive_res: StandardBusinessEnum = await user_alive(session, encrypted_data)
            if StandardBusinessEnum.UNREGISTERED == alive_res: return (StandardBusinessEnum.UNREGISTERED.value[0], "用户未注册")
            elif StandardBusinessEnum.PWDERROR == alive_res: return (StandardBusinessEnum.PWDERROR.value[0], "密码错误")
            else:
                _uid: str = await user_uid(session, encrypted_data)
                # 发布签名
                token_inner_info: StandardTokenInfoTemplate = StandardTokenInfoTemplate(
                    uid=await encrypt(_uid),
                    exp=int((datetime.now(tz=UTCTime) + timedelta(minutes=240)).timestamp())
                )
                auth: str = await create_access_token(token_inner_info)
                return (StandardBusinessEnum.SUCCESS.value[0], "登录成功", {"token": auth})

async def user_list(
    r: Request
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
        async with db_pool.get_session() as session:
            raw_list: list = await user_all(session)
            result: list = [{"uid": await encrypt(item["uid"]), "username": item["username"]} for item in raw_list]
            return (StandardBusinessEnum.SUCCESS.value[0], "查询成功", result)

async def user_modify(
    r: Request,
    model: UserModify,
    decrypted_uid: str
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        # 拿到全局挂载的连接池
        db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
        _password: str | None = model.new_password
        if _password is not None:
            _password = await decrypt(_password)
            if not is_valid_password(_password): raise DivExcep(StandardBusinessEnum.FAIL.value[0], "密码格式错误")
        # 获取系统向量
        tmp_vector: str = get_env_val("iv", "dev")
        encrypted_data: StandardUserModRepositoryTemplate = StandardUserModRepositoryTemplate(
            uid=decrypted_uid,
            username=model.username,
            password=await encrypt(_password, tmp_vector) if _password is not None else None
        )
        async with db_pool.get_session() as session:
            update_res: StandardBusinessEnum = await user_update(session, encrypted_data)
            if update_res != StandardBusinessEnum.SUCCESS: return update_res.value[0], "用户信息修改失败"
            return StandardBusinessEnum.SUCCESS.value[0], "用户信息修改成功"

async def user_person_info(
    r: Request,
    decrypted_uid: str
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else:
        # 拿到全局挂载的连接池
        db_pool: StandardSQLiteDBConnectPool = r.app.state.db_pool
        async with db_pool.get_session() as session:
            info: tuple = await user_info(session, decrypted_uid)
            if StandardBusinessEnum.FAIL == info[0]: return info[0].value[0], "用户信息获取失败"
            return (StandardBusinessEnum.SUCCESS.value[0], "用户信息获取成功", {"username": info[1]})

async def user_role_list(
    r: Request
) -> tuple:
    u_platform: Optional[str] = r.headers.get("sec-ch-ua-platform")
    if not u_platform: return (StandardBusinessEnum.FAIL.value[0], "请求头校验失败")
    else: return (StandardBusinessEnum.SUCCESS.value[0], "操作成功", StandardUserRoleEnum.info())
