import json

from pathlib import Path

from utils.Logs import ExceptionLog
from utils.Excptions import DivExcep
from tools.Files import FileLock, atomic_write
from enums.StandardBusEnum import StandardBusinessEnum
from templates.StandardNoSqlTemplate import NoSqlDataTemplate

def sync_create(
    file_path: str,
    data: NoSqlDataTemplate
) -> StandardBusinessEnum:
    e: ExceptionLog = ExceptionLog.get_instance()
    file: Path = Path(file_path)
    if not file.exists():
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg=f"NoSQL 文件不存在: {file_path}"
        )
    with open(file_path, "r", encoding="utf-8") as f:
        with FileLock(f):
            content: dict = json.load(f) if file.stat().st_size > 0 else {}
            if data.key in content:
                raise DivExcep(
                    code=StandardBusinessEnum.FAIL.value[0],
                    msg=f"key '{data.key}' 已存在"
                )
            content[data.key] = data.value
    try: atomic_write(file_path, content)
    except Exception:
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            # 检测磁盘空间
            msg="NoSQL 写入失败"
        )
    e.info(f"NoSQL 写入成功: key={data.key}, file={file_path}")
    return StandardBusinessEnum.SUCCESS

def sync_delete(
    file_path: str,
    key: str
) -> StandardBusinessEnum:
    e: ExceptionLog = ExceptionLog.get_instance()
    file: Path = Path(file_path)
    if not file.exists():
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg=f"NoSQL 文件不存在: {file_path}"
        )
    with open(file_path, "r", encoding="utf-8") as f:
        with FileLock(f):
            content: dict = json.load(f) if file.stat().st_size > 0 else {}
            if key not in content:
                raise DivExcep(
                    code=StandardBusinessEnum.FAIL.value[0],
                    msg=f"key '{key}' 不存在"
                )
            del content[key]
    try: atomic_write(file_path, content)
    except Exception:
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="NoSQL 删除失败"
        )
    e.info(f"NoSQL 删除成功: key={key}, file={file_path}")
    return StandardBusinessEnum.SUCCESS

def sync_update(
    file_path: str,
    data: NoSqlDataTemplate
) -> StandardBusinessEnum:
    e: ExceptionLog = ExceptionLog.get_instance()
    file: Path = Path(file_path)
    if not file.exists():
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg=f"NoSQL 文件不存在: {file_path}"
        )
    with open(file_path, "r", encoding="utf-8") as f:
        with FileLock(f):
            content: dict = json.load(f) if file.stat().st_size > 0 else {}
            if data.key not in content:
                raise DivExcep(
                    code=StandardBusinessEnum.FAIL.value[0],
                    msg=f"key '{data.key}' 不存在"
                )
            content[data.key] = data.value
    try: atomic_write(file_path, content)
    except Exception:
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg="NoSQL 修改失败"
        )
    e.info(f"NoSQL 修改成功: key={data.key}, file={file_path}")
    return StandardBusinessEnum.SUCCESS

def sync_read(
    file_path: str,
    key: str = ""
) -> str | dict:
    file: Path = Path(file_path)
    if not file.exists():
        raise DivExcep(
            code=StandardBusinessEnum.FAIL.value[0],
            msg=f"NoSQL 文件不存在: {file_path}"
        )
    with open(file_path, "r+", encoding="utf-8") as f:
        with FileLock(f):
            content: dict = json.load(f) if file.stat().st_size > 0 else {}
            if not key: return content
            if key not in content:
                raise DivExcep(
                    code=StandardBusinessEnum.FAIL.value[0],
                    msg=f"key '{key}' 不存在"
                )
            return content[key]
