import re
import uuid
import secrets

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
