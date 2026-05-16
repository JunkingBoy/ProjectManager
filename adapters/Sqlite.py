import types
import sqlite3

from typing import Any
from pathlib import Path

from templates.StandardSysTemplate import StandardSqliteConnTemplate

class SQLiteAdapter:
    def __init__(
        self,
        data: StandardSqliteConnTemplate,
    ) -> None:
        self._sqlite_param: StandardSqliteConnTemplate = data

    @property
    def conn_info(self) -> Any:
        # 使用Pathlib安全转为uri
        tmp_db_file_path: Path = Path(self._sqlite_param.DB_PATH) / self._sqlite_param.DB_NAME
        return f"sqlite+aiosqlite:///{tmp_db_file_path}"

    def test_conn(self) -> str: return "SELECT 1"
    def creator(self) -> types.ModuleType: return sqlite3
