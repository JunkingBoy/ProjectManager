from typing import Protocol, runtime_checkable

@runtime_checkable
class IStandardTable(Protocol):
    @property
    def info(self) -> dict: ...