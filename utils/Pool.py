from contextlib import asynccontextmanager
from typing import TypeVar, Generic, AsyncIterator
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from utils.Logs import ExceptionLog
from utils.Excptions import DivExcep
from duck.IStandardAda import IStandardAdapter
from enums.StandardBusEnum import StandardBusinessEnum

T = TypeVar('T', bound=IStandardAdapter)
class StandardSQLiteDBConnectPool(Generic[T]):
    '''
    使用sqlalchemy自带的QueuePool作为数据库连接池
    '''
    def __init__(
        self,
        adapter: T,
        e: ExceptionLog = ExceptionLog.get_instance()
    ) -> None:
        self._e: ExceptionLog = e
        self._ada: T = adapter
        # 创建异步引擎,用于数据库连接池池化
        self._engine: AsyncEngine = create_async_engine(
            self._ada.conn_info,
            connect_args={
                "check_same_thread": False, # 允许在不同线程中使用同一个连接 (FastAPI/多线程必需)
                "uri": True       # 启用 URI 模式，以便支持查询参数
            },
            echo=True,            # 开发时为True
            pool_size=5,          # 连接池大小
            max_overflow=10,      # 最大溢出连接数
            pool_recycle=3600,    # 每隔一小时自动回收连接 (防止长时间空闲导致的问题)
            pool_pre_ping=True,   # 每次使用连接前先测试是否存活 (防断连神器)
        )
        # 异步会话工厂,用于获取Session
        self._async_session: async_sessionmaker = async_sessionmaker(
            bind=self._engine,                  # 绑定引擎
            class_=AsyncSession,                # 使用异步会话
            expire_on_commit=False              # 提交后对象不会过期，方便后续读取数据
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        """
        异步上下文管理器，用于获取数据库会话。
        FastAPI 会自动管理这个生成器的生命周期。
        """
        async with self._async_session() as session:
            try: yield session
            except Exception as e:
                await session.rollback()
                self._e.error(f"数据库事务异常并回滚: {str(e)}")
                raise DivExcep(
                    code=StandardBusinessEnum.INNERERROR.value[0],
                    msg=StandardBusinessEnum.INNERERROR.value[1]
                )

    async def get_engine(self) -> AsyncEngine: return self._engine
