from enum import Enum


class RequirementStatusEnum(Enum):
    """需求状态枚举"""
    PENDING = (0, "待领取")
    DESIGNING = (1, "设计中")
    DEVELOPING = (2, "开发中")
    TESTING = (3, "测试中")
    ONLINE = (4, "已上线")
    DISCARDED = (5, "废弃")

    @classmethod
    def get_msg_by_code(cls, code: int) -> str:
        for item in cls:
            if item.value[0] == code:
                return item.value[1]
        return "未知状态"


class FeatureStatusEnum(Enum):
    """功能点状态枚举"""
    PLANNING = (1, "规划中")
    LOCKED = (2, "已锁定")
    DEVELOPING = (3, "开发中")
    COMPLETED = (4, "开发完毕")

    @classmethod
    def get_msg_by_code(cls, code: int) -> str:
        for item in cls:
            if item.value[0] == code:
                return item.value[1]
        return "未知状态"


class DevTaskStatusEnum(Enum):
    """研发任务状态枚举"""
    PENDING = (1, "待开始")
    IN_PROGRESS = (2, "进行中")
    COMPLETED = (3, "已完成")
    DISCARDED = (4, "已废弃")

    @classmethod
    def get_msg_by_code(cls, code: int) -> str:
        for item in cls:
            if item.value[0] == code:
                return item.value[1]
        return "未知状态"


class QaTaskStatusEnum(Enum):
    """测试任务状态枚举"""
    PENDING = (1, "待开始")
    IN_PROGRESS = (2, "进行中")
    COMPLETED = (3, "已完成")
    DISCARDED = (4, "已废弃")

    @classmethod
    def get_msg_by_code(cls, code: int) -> str:
        for item in cls:
            if item.value[0] == code:
                return item.value[1]
        return "未知状态"


class BugStatusEnum(Enum):
    """Bug 状态枚举"""
    UNFIXED = (0, "未修复")
    FIXED = (1, "已修复")
    NOT_BUG = (2, "研发确认非Bug")
    CLOSED = (3, "已关闭")

    @classmethod
    def get_msg_by_code(cls, code: int) -> str:
        for item in cls:
            if item.value[0] == code:
                return item.value[1]
        return "未知状态"


class RequirementSourceEnum(Enum):
    """需求来源枚举"""
    MANUAL = (0, "手动创建")
    THIRD_PARTY = (1, "第三方接入")

    @classmethod
    def get_msg_by_code(cls, code: int) -> str:
        for item in cls:
            if item.value[0] == code:
                return item.value[1]
        return "未知来源"


class PriorityEnum(Enum):
    """优先级枚举"""
    HIGH = (1, "高")
    MEDIUM = (2, "中")
    LOW = (3, "低")

    @classmethod
    def get_msg_by_code(cls, code: int) -> str:
        for item in cls:
            if item.value[0] == code:
                return item.value[1]
        return "未知优先级"
