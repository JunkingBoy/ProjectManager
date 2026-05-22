from pathlib import Path
from typing import Annotated
from fastapi import UploadFile
from pydantic import Field, field_validator, ConfigDict

from dantics.GlobalDantic import CoreModel
from tools.Re import ts_to_datetime_or_zero

class RequirementAdd(CoreModel):
    model_config = ConfigDict(from_attributes=True)

    number: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=128,
        description="需求编号"
    )]
    title: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=128,
        description="需求标题"
    )]
    desc: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=256,
        description="需求描述"
    )]
    source: Annotated[int, Field(
        ...,
        description="需求来源,默认传0"
    )]
    status: Annotated[int, Field(
        ...,
        description="需求状态"
    )]
    priority: Annotated[int, Field(
        ...,
        description="需求优先级"
    )]
    system: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=128,
        description="需求所属系统加密值"
    )]
    project: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=128,
        description="需求所属项目加密值"
    )]
    project_type: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=128,
        description="需求所属项目类型加密值"
    )]
    person: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=128,
        description="需求所属人员ID加密值"
    )]
    relevant: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=128,
        description="需求技术负责人ID加密值"
    )]
    related_doc: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=128,
        description="需求关联文档ID加密值"
    )]
    total: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=4,
        description="需求总工时,传浮点字符串"
    )]
    dev_total: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=4,
        description="需求开发总工时,传浮点字符串"
    )]
    dev_price: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=6,
        description="需求开发单价,传浮点字符串"
    )]
    test_total: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=4,
        description="需求测试总工时,传浮点字符串"
    )]
    test_price: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=6,
        description="需求测试单价,传浮点字符串"
    )]
    business_test_total: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=4,
        description="需求业务测试总工时,传浮点字符串"
    )]
    business_test_price: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=6,
        description="需求业务测试单价,传浮点字符串"
    )]
    release_time: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=128,
        description="需求发布时间,格式为秒级时间戳"
    )]

    @field_validator('source')
    @classmethod
    def validate_source(cls, v: int) -> int:
        if v not in (0, 1): raise ValueError('非法创建渠道')
        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: int) -> int:
        if v not in range(5): raise ValueError('非法状态')
        return v

    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v: int) -> int:
        if v not in range(3): raise ValueError('非法优先级')
        return v

    @field_validator('total', 'dev_total', 'test_total', 'business_test_total',
                     'dev_price', 'test_price', 'business_test_price')
    @classmethod
    def validate_float_str(cls, v: str) -> str:
        try: float(v)
        except ValueError: raise ValueError(f'"{v}" 为非法浮点字符串')
        return v

    @field_validator('release_time')
    @classmethod
    def validate_release_time(cls, v: str) -> str:
        try: ts: float = float(v)
        except ValueError: raise ValueError(f'"{v}" 为无效时间戳')
        if ts_to_datetime_or_zero(ts) == 0: raise ValueError('非法时间')
        return v

class RequirementFileUpload(CoreModel):
    file: UploadFile

    @field_validator('file')
    @classmethod
    def validate_file_type(cls, v: UploadFile) -> UploadFile:
        if Path(v.filename or "").suffix.lower() not in {'.docx', '.pdf'}: raise ValueError('不支持的文件类型')
        return v

class RequirementFileDownload(CoreModel):
    model_config = ConfigDict(from_attributes=True)

    requirement_id: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=256,
        description="需求ID加密值"
    )]
    related_doc_id: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=256,
        description="需求关联文档tag加密值"
    )]

class RequirementFileDelete(CoreModel):
    model_config = ConfigDict(from_attributes=True)

    related_doc_id: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=256,
        description="需求关联文档tag加密值"
    )]

class RequirementDetail(CoreModel):
    model_config = ConfigDict(from_attributes=True)

    requirement_id: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=256,
        description="需求ID加密值"
    )]
