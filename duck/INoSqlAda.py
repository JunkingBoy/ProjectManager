from typing import Protocol, runtime_checkable


@runtime_checkable
class INoSQLAdapter(Protocol):
    """
    NoSQL 适配器协议, 所有要接入系统的 NoSQL 适配器都必须满足这个协议
    """
    def init(self) -> None: ...
