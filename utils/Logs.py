import logging
import threading

from typing import Optional

from tools.Files import create_dir

class ExceptionLog:
    __INSTANCE: Optional['ExceptionLog'] = None
    __LOCK: threading.Lock = threading.Lock()

    @staticmethod
    def get_instance() -> 'ExceptionLog':
        if ExceptionLog.__INSTANCE: return ExceptionLog.__INSTANCE
        else:
            with ExceptionLog.__LOCK:
                if not ExceptionLog.__INSTANCE: ExceptionLog.__INSTANCE = ExceptionLog()
            return ExceptionLog.__INSTANCE

    def __init__(self) -> None:
        if getattr(self, '_initialized', False): return
        else:
            self._initialized: bool = True
            self._logger: logging.Logger = logging.getLogger('ExceptionLog')
            if self._logger.handlers: return
            self._logger.setLevel(logging.DEBUG)

            self._err_log: str | None = create_dir("logs/err")
            self._info_log: str | None = create_dir("logs/info")

            if not self._err_log or not self._info_log: raise Exception("日志目录创建失败")

            # 定义生产环境加载的依赖
            try:
                from rich.logging import RichHandler # type: ignore

                # 添加 RichHandler - 用于终端美化输出
                rich_handler: RichHandler = RichHandler(
                    show_time=True,
                    show_path=False,
                    markup=True,
                    rich_tracebacks=True, # 使用 rich 格式化异常追踪
                    tracebacks_show_locals=True # 在异常追踪中显示局部变量
                )
                rich_handler.setLevel(logging.ERROR)
                self._logger.addHandler(rich_handler)
            except ImportError: pass
            # 创建处理器a
            self._err_file_name: str = f"{self._err_log}/err.log"
            err_handler: logging.FileHandler = logging.FileHandler(
                self._err_file_name,
                encoding='utf-8-sig',
                mode='a' # 追加写入,文件存在则在文件末尾添加内容
            )

            err_handler.setLevel(logging.ERROR)
            err_handler_fmt: logging.Formatter = logging.Formatter(
                "%(asctime)s:%(pathname)s:%(name)s:%(levelname)s:%(message)s"
            )
            err_handler.setFormatter(err_handler_fmt)
            # 为记录器添加处理器
            self._logger.addHandler(err_handler)

            # 创建处理器b
            self._info_file_name: str = f"{self._info_log}/run.log"
            info_handler: logging.FileHandler = logging.FileHandler(
                self._info_file_name,
                encoding="utf-8-sig",
                mode='w' # 重写模式
            )
            info_handler.setLevel(logging.INFO)
            info_handler_fmt: logging.Formatter = logging.Formatter(
                "%(asctime)s:%(levelname)s:%(message)s"
            )
            info_handler.setFormatter(info_handler_fmt)
            self._logger.addHandler(info_handler)

    def info(self, logmsgformat: str, *args) -> None: self._logger.info(logmsgformat, *args)
    def error(self, logmsgformat: str, *args) -> None: self._logger.error(logmsgformat, *args)
