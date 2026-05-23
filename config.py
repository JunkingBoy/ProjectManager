from fastapi import FastAPI
from fastapi import Request
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncEngine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from routers.Key import key
from routers.User import user
from routers.Dict import dict
from routers.Task import task
from routers.Requirement import requirement
from routers.Bug import bug

from tools.Files import create_dir
from utils.Logs import ExceptionLog
from utils.Excptions import DivExcep
from adapters.NoSql import NoSQLAdapter
from adapters.Sqlite import SQLiteAdapter
from dantics.GlobalDantic import CoreModel
from utils.NoSqlPool import StandardNoSQLPool
from utils.Pool import StandardSQLiteDBConnectPool
from models import BaseModel, TbUser, TbRequirements, TbBug, TbWork
from templates.StandardSysTemplate import StandardSqliteConnTemplate, StandardNoSqlConnTemplate

# 提供初始化用的建表方法
async def create_all_tables() -> StandardSQLiteDBConnectPool:
    e: ExceptionLog = ExceptionLog.get_instance()
    # 创建数据库连接池和初始化表
    sqlite_info: StandardSqliteConnTemplate = StandardSqliteConnTemplate()
    sqlite: SQLiteAdapter = SQLiteAdapter(sqlite_info)
    db_pool: StandardSQLiteDBConnectPool = StandardSQLiteDBConnectPool(sqlite)
    try:
        _engine: AsyncEngine = await db_pool.get_engine()
        e.info(f"数据库连接url: {_engine.url} 开始创建数据库表...")
        async with _engine.begin() as conn: await conn.run_sync(BaseModel.metadata.create_all)
        e.info(f"数据库表创建成功！")
        return db_pool
    except Exception as err:
        e.error(f"数据库表创建失败: {str(err)}")
        raise

# 初始化Nosql存储
async def init_nosql_storage() -> StandardNoSQLPool:
    nosql_info: StandardNoSqlConnTemplate = StandardNoSqlConnTemplate()
    nosql_ada: NoSQLAdapter = NoSQLAdapter(nosql_info)
    nosql_pool: StandardNoSQLPool = StandardNoSQLPool(nosql_ada)
    return nosql_pool

# 定义fastapi推荐的生命周期管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    e: ExceptionLog = ExceptionLog()
    routers: list = [user, key, dict, requirement, task, bug]
    for router in routers: app.include_router(router)
    try:
        # 创建数据库连接池和初始化表
        db_pool: StandardSQLiteDBConnectPool = await create_all_tables()
        # 挂载到 FastAPI 实例上，方便全局访问
        app.state.db_pool = db_pool
        # 初始化 NoSQL 存储并挂载
        nosql_pool: StandardNoSQLPool = await init_nosql_storage()
        app.state.nosql_pool = nosql_pool
        # 创建下载文件存储目录
        create_dir('downloads')
        yield
    except Exception as exc:
        e.error(str(exc))
        raise exc

def create_app() -> FastAPI:
    app: FastAPI = FastAPI(
        title="Project Manager Server Py",
        description="A Backend Server for Project Manager",
        version="1.0.0",
        lifespan=lifespan
    )
    app.add_middleware(
          CORSMiddleware,
          allow_origins=["*"],  # 或指定具体域名
          allow_credentials=True,
          allow_methods=["*"],
          allow_headers=["*"],
      )
    return app

'''
定义FastAPI的全局配置
'''
ProjectServer: FastAPI = create_app()

# 请求模型异常全局处理
@ProjectServer.exception_handler(RequestValidationError)
async def validation_exception_handler(r: Request, e: RequestValidationError) -> JSONResponse: return await CoreModel.Global_Model_Error_Catch(r, e)

# 解析异常全局处理
@ProjectServer.exception_handler(DivExcep)
async def div_exception_handler(r: Request, e: DivExcep) -> JSONResponse: return await CoreModel.Global_Bussiness_Error_Catch(r, e)

# Pydantic异常全局处理
@ProjectServer.exception_handler(ValidationError)
async def pydantic_exception_handler(r: Request, e: ValidationError) -> JSONResponse: return await CoreModel.Global_Model_Error_Catch(r, e)