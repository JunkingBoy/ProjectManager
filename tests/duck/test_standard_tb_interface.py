from dataclasses import dataclass

from duck.IStandardTb import IStandardTable


@dataclass
class TableLike:
    info: dict


@dataclass
class NotTableLike:
    uid: str


def test_runtime_checkable_protocol_accepts_object_with_info_property():
    table = TableLike(info={"id": 1})

    assert isinstance(table, IStandardTable)


def test_runtime_checkable_protocol_rejects_object_without_info_property():
    table = NotTableLike(uid="user-1")

    assert not isinstance(table, IStandardTable)
