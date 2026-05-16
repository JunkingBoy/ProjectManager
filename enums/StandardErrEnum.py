from enum import Enum

class StandardSysErrEnum(Enum):
    OSFAIL = (5001, "操作系统错误")
    IOFAIL = (5002, "IO错误")
    TYPEFAIL = (5003, "类型错误")
    ATTRIBUTEFAIL = (5004, "属性错误")
    CONNECTFAIL = (5005, "连接错误")
    UNKNOWNFAIL = (5006, "未知错误")

class StandardGlobalErrEnum(Enum):
    '''
    非手动抛出的异常
    '''
    MISSING = ("missing", "缺少必要字段")
    UNAUTH = ("Not authenticated", "认证失败")
    UNSTRING = ("string_type", "需要字符串类型数据")
    STRING_EFFECTIVE = ("string_too_long", "字符串长度过长")
    STRING_EFFECTIVE_SHORT = ("string_too_short", "字符串长度过短")
    JSON_INVALID = ("json_invalid", "无效请求")
    STRING_VALUE_ERROR = ("string_pattern_mismatch", "非法字符串数据")
    GE_THAN = ("greater_than_equal", "日期不能小于1天")
    LE_THAN = ("less_than_equal", "日期不能大于7天")

    @classmethod
    def get_msg_by_type(cls, typ: str) -> str | None:
        for item in cls:
            if item.value[0] == str(typ): return item.value[1]
        return
