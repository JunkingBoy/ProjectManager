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
    SELF = 0    # 自行创建
    THIRD = 1   # 第三方接入

    @classmethod
    def info(cls) -> dict: return {
            cls.SELF.value: "手动创建",
            cls.THIRD.value: "第三方接入"
        }

class StandardReqStatusEnum(Enum):
    '''
    需求状态机枚举
    '''
    STARTG = 0
    TEST = 1
    BUSINESSTEST = 2
    RELEASE = 3
    RELEASED = 4

    @classmethod
    def info(cls) -> dict: return {
            cls.STARTG.value: "进行中",
            cls.TEST.value: "综合测试",
            cls.BUSINESSTEST.value: "业务测试",
            cls.RELEASE.value: "待发布",
            cls.RELEASED.value: "已发布"
        }

class StandardReqPriorityEnum(Enum):
    LOW = 0
    MIDDLE = 1
    HIGHT = 2

    @classmethod
    def info(cls) -> dict: return {
            cls.LOW.value: "低",
            cls.MIDDLE.value: "中",
            cls.HIGHT.value: "高"
        }

class StandardDevTasksStatusEnum(Enum):
    '''
    研发任务池状态机枚举
    '''
    WAIT = 0
    PROGRESS = 1
    FINISH = 2
    BUG = 3
    CLOSE = 4

class StandardTaskTerminalEnum(Enum):
    '''
    终端枚举
    '''
    BACK = 0
    ANDROID = 1
    IOS = 2
    MINI = 3
    H5 = 4

    @classmethod
    def info(cls) -> dict: return {
        cls.BACK.value: "后台",
        cls.ANDROID.value: "安卓",
        cls.IOS.value: "IOS",
        cls.MINI.value: "小程序",
        cls.H5.value: "H5"
    }

class StandardBugStatusEnum(Enum):
    UNFIX = 0
    FIX = 1
    NONBUG = 2
    CLOSE = 3

class StandardUserRoleEnum(Enum):
    '''
    用户角色枚举
    '''
    PM = 0
    DEVELOPER = 1
    ANDROID = 2
    IOS = 3
    MINI = 4
    H5 = 5
    QA = 6

    @classmethod
    def info(cls) -> dict: return {
            cls.PM.value: "项目经理",
            cls.DEVELOPER.value: "后台开发",
            cls.ANDROID.value: "安卓开发",
            cls.IOS.value: "IOS开发",
            cls.MINI.value: "小程序开发",
            cls.H5.value: "H5开发",
            cls.QA.value: "测试",
        }
