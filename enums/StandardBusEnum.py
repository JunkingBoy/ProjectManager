from enum import Enum

class StandardBusinessEnum(Enum):
    '''
    标准业务响应Code枚举
    '''
    FAIL = (1002, "操作失败")
    ERROR = (1003, "操作异常")
    SUCCESS = (1001, "操作成功")
    LOSS = (1005, "请求参数错误")
    UNKNOWN = (1004, "未找到相关数据")
    INNERERROR = (2001, "服务器内部错误")
    # 用户相关错误代码
    PWDERROR = (4001, "密码错误")
    UNREGISTERED = (4002, "用户未注册")
    # 签名相关错误代码
    INVALID = (3001, "签名验证失败")
    EXPIRED = (3002, "签名已过期")

    @classmethod
    def get_msg_by_code(cls, code: int) -> str:
        for item in cls:
            if item.value[0] == code: return item.value[1]
        return "未知业务状态码"
