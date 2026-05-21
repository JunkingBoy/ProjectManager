from pathlib import Path

from tools.Files import create_file
from templates.StandardSysTemplate import StandardNoSqlConnTemplate


class NoSQLAdapter:
    """
    JSON 文件版 NoSQL 适配器 (实现 INoSQLAdapter 协议)
    """
    def __init__(
        self,
        data: StandardNoSqlConnTemplate
    ) -> None:
        self._param: StandardNoSqlConnTemplate = data

    def init(self) -> None:
        for file_name in [
            self._param.SYS_NOSQL_NAME,
            self._param.PROJECT_NOSQL_NAME,
            self._param.PROJECT_TYPE_NOSQL_NAME,
        ]:
            create_file(self._param.NOSQL_PATH, file_name.replace(".json", ""), ".json")

    @property
    def sys_file_path(self) -> str: return (Path(self._param.NOSQL_PATH) / self._param.SYS_NOSQL_NAME).as_posix()

    @property
    def project_file_path(self) -> str: return (Path(self._param.NOSQL_PATH) / self._param.PROJECT_NOSQL_NAME).as_posix()

    @property
    def project_type_file_path(self) -> str: return (Path(self._param.NOSQL_PATH) / self._param.PROJECT_TYPE_NOSQL_NAME).as_posix()
