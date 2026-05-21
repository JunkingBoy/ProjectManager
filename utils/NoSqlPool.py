from typing import Generic, TypeVar

from utils.Logs import ExceptionLog
from duck.INoSqlAda import INoSQLAdapter

T = TypeVar("T", bound=INoSQLAdapter)
class StandardNoSQLPool(Generic[T]):
    """
    通用 NoSQL 连接池 (泛型版本)
    类似 StandardSQLiteDBConnectPool[T]，通过鸭子协议支持多种 NoSQL 后端:
      - JSONNoSQLAdapter → JSON 文件
      - RedisNoSQLAdapter → Redis (后续扩展)
    """
    def __init__(
        self,
        adapter: T,
        e: ExceptionLog = ExceptionLog.get_instance()
    ) -> None:
        self._e: ExceptionLog = e
        self._ada: T = adapter
        self._ada.init()

    @property
    def adapter(self) -> T: return self._ada
