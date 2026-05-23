from typing import Any
from datetime import timezone, timedelta
from sqlalchemy.ext.declarative import declarative_base

# orm基类,所有orm模型都需要继承这个基类
BaseModel: Any = declarative_base()
# 设置建表时候的默认时区时间（中国时区 UTC+8）
CST: Any = timezone(timedelta(hours=8))
