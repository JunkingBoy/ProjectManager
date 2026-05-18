from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncEngine
from fastapi.exceptions import RequestValidationError

from routers.Key import key
from routers.User import user

from utils.Logs import ExceptionLog
from utils.Excptions import DivExcep
from adapters.Sqlite import SQLiteAdapter
from dantics.GlobalDantic import CoreModel
from utils.Pool import StandardSQLiteDBConnectPool
from templates.StandardSysTemplate import StandardSqliteConnTemplate
from models import BaseModel, TbUser, TbRequirements, TbPiont,TbBug, TbWork

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

# 定义fastapi推荐的生命周期管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    e: ExceptionLog = ExceptionLog()
    routers: list = [user, key]
    for router in routers: app.include_router(router)
    try:
        # 创建数据库连接池和初始化表
        db_pool: StandardSQLiteDBConnectPool = await create_all_tables()
        # 挂载到 FastAPI 实例上，方便全局访问
        app.state.db_pool = db_pool
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