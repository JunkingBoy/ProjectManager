import types

from typing import Protocol, runtime_checkable, Any

@runtime_checkable
class IStandardAdapter(Protocol):
    '''
    标准适配器协议,所有要接入系统的适配器都必须满足这个协议
    '''
    @property
    def conn_info(self) -> Any: ... # 数据库的连接参数字典
    def test_conn(self) -> str: ... # 测试连接的SQL语句
    def creator(self) -> types.ModuleType: ... # 数据库的驱动模块
