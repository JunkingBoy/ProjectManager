import re
import uuid
import string
import secrets

from datetime import datetime, date

def generate_aes_params() -> bytes: return secrets.token_bytes(16) # 返回16字节的初始化向量
def generate_uid() -> str: return uuid.uuid4().hex

def is_valid_password(s: str) -> bool:
    # 字母 + 数字 + 特殊字符 + 至少6位
    pattern: str = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]+$"
    return bool(re.match(pattern, s)) # match只会校验开头部分

def is_valid_phone(s: str) -> bool:
    pattern: str = r"^1[3-9]\d{9}$"
    return bool(re.match(pattern, s))

def is_valid_email(s: str) -> bool:
    # 匹配规则：字母数字及常见符号 + @ + 域名 + . + 至少2位的顶级域名
    pattern: str = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, s))

def is_valid_username(s: str) -> bool:
    # 匹配规则：字母、数字、字母+数字
    pattern: str = r"^[\u4e00-\u9fa5a-zA-Z0-9]+$"
    return bool(re.match(pattern, s))

def ts_to_datetime_or_zero(ts: float) -> datetime | int:
    """时间戳转datetime, 日期<今天返回0, 否则返回datetime"""
    dt: datetime = datetime.fromtimestamp(ts)
    return 0 if dt.date() < date.today() else dt

def filling_random_chars(index: int, s: str) -> str:
    if not s: return ""
    else:
        all_chars: str = string.ascii_letters + string.digits + string.punctuation
        # 随机数,6位
        random_part: str = ''.join(secrets.choice(all_chars) for _ in range(6))
        # 微妙,6位
        micro_second_str: str = datetime.now().strftime("%f")
        # UUID,4位
        uuid_feature: str = uuid.uuid4().hex[-4:]
        final_random_str: str = random_part + micro_second_str + uuid_feature
        return s[:index] + final_random_str + s[index:]
