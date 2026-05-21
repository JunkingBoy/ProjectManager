from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncEngine
from fastapi.exceptions import RequestValidationError

from routers.User import user
from routers.Requirement import requirement
from routers.TaskPool import task_pool
from routers.DevelopTask import develop_task
from routers.QaTask import qa_task
from routers.Bug import bug
from routers.Dashboard import dashboard
from routers.TaskPool import task_pool
from routers.DevelopTask import develop_task
from routers.QaTask import qa_task
from routers.Bug import bug
from routers.Dashboard import dashboard

from utils.Logs import ExceptionLog
from utils.Excptions import DivExcep
from models import BaseModel, TbUser
from adapters.Sqlite import SQLiteAdapter
from dantics.GlobalDantic import CoreModel
from utils.Pool import StandardSQLiteDBConnectPool
from templates.StandardSysTemplate import StandardSqliteConnTemplate

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
    try:
        app.include_router(user)
        app.include_router(requirement)
        app.include_router(task_pool)
        app.include_router(develop_task)
        app.include_router(qa_task)
        app.include_router(bug)
        app.include_router(dashboard)
        app.include_router(task_pool)
        app.include_router(develop_task)
        app.include_router(qa_task)
        app.include_router(bug)
        app.include_router(dashboard)
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