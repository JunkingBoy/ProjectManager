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

class StandardReqSourceEnum(Enum):
    '''
    需求来源枚举
    '''
    SELF = 1    # 自行创建
    THIRD = 2   # 第三方接入

class StandardReqStatusEnum(Enum):
    '''
    需求状态机枚举
    '''
    WAIT = 1
    DESIGN = 2
    DEVELOP = 3
    TEST = 4
    ONLINE = 5
    CANCEL = 6

class StandardPointStatusEnum(Enum):
    '''
    功能点状态机枚举
    '''
    PLAN = 1
    LOCK = 2
    DEVELOP = 3
    TEST = 4
    REPAIR = 5
    FINISH = 6

class StandardDevTasksStatusEnum(Enum):
    '''
    研发任务池状态机枚举
    '''
    DESIGN = 1
    DEVELOP = 2
    FINISH = 3
    TEST = 4
    CANCEL = 5

class StandardQaTasksPoolStatusEnum(Enum):
    DESIGN = 1
    IMPLEMENT = 2
    REPAIR = 3
    PASS = 4
    CANCEL = 5

class StandardBugStatusEnum(Enum):
    UNFIX = 0
    FIX = 1
    NONBUG = 2
    CLOSE = 3
