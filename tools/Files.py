import os
import json
import fcntl
import msvcrt
import platform
import tempfile

from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from typing import Any, Optional, IO

'''
文件操作相关的工具方法统一存放
'''
def get_env_val(
    env_key: str,
    env_name: Optional[str] = None
) -> str:
    from utils.Logs import ExceptionLog
    e: ExceptionLog = ExceptionLog.get_instance()
    if not env_key: temp_val: str = ""
    else: temp_val: str = env_key.upper()
    if env_name: dotenv_path: str = f".env.{env_name.lower()}"
    else: dotenv_path: str = ".env"
    # 加载指定的 .env 文件(不覆盖已存在的系统环境变量)
    load_dotenv(dotenv_path=dotenv_path, override=False)
    try: return os.getenv(temp_val, "")
    except Exception:
        e.info(f"获取环境变量{temp_val}失败!")
        return ""

def create_dir(
    dir_name: str,
    need_date: bool = False
) -> str:
    '''
    创建指定名称目录,返回目录名称
    '''
    if not dir_name: raise ValueError('参数[dir_name]不能为空')
    try:
        cur_dir: Path = Path.cwd()
        # 当前目录下创建子文件夹
        dir_path: Path = cur_dir.joinpath(dir_name)
        if not need_date:
            dir_path.mkdir(parents=True, exist_ok=True)
            return dir_path.as_posix()
        else:
            today: str = datetime.now().strftime('%Y%m%d')
            tar_path: Path = dir_path.joinpath(today)
            if not tar_path.exists(): tar_path.mkdir(parents=True, exist_ok=True)
            return tar_path.as_posix()
    except Exception: raise Exception('创建目录失败')

def create_file(
    op_path: str,
    op_file_name: str,
    op_end_with: str,
    is_second: bool = False
) -> str:
    '''
    在指定路径下创建指定名称文件,返回文件名称
    '''
    if not op_path or not op_file_name or not op_end_with: raise ValueError('参数[op_path, op_file_name, op_end_with]不能为空')
    if not Path(op_path).exists() or not Path(op_path).is_dir(): raise ValueError('参数[op_path]指定的目录不存在或不是一个目录')
    try:
        if not is_second: tar_file: Path = Path(op_path).joinpath(f"{op_file_name}{op_end_with}")
        else:
            now: str = datetime.now().strftime("%H%M%S")
            tar_file: Path = Path(op_path).joinpath(f"{op_file_name}{now}{op_end_with}")
        if not tar_file.exists(): tar_file.touch()
        return tar_file.as_posix()
    except Exception: raise Exception('创建文件失败')

if platform.system() == "Windows":
    def _lock(f: IO[Any]) -> None: msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)
    def _unlock(f: IO[Any]) -> None: msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
else:
    def _lock(f: IO[Any]) -> None: fcntl.flock(f.fileno(), fcntl.LOCK_EX) # type: ignore
    def _unlock(f: IO[Any]) -> None: fcntl.flock(f.fileno(), fcntl.LOCK_UN) # type: ignore

class FileLock:
    def __init__(self, file: IO[Any]) -> None: self._file: IO[Any] = file
    def __enter__(self) -> None: _lock(self._file)
    def __exit__(self, *args: Any) -> None: _unlock(self._file)

def atomic_write(file_path: str, content: dict) -> None:
    """将 dict 以 JSON 格式原子写入文件"""
    file: Path = Path(file_path)
    fd, tmp_path = tempfile.mkstemp(dir=file.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f: json.dump(content, f, ensure_ascii=False, indent=4)
        os.replace(tmp_path, file_path)
    except Exception:
        try: os.unlink(tmp_path)
        except OSError: pass
        raise
