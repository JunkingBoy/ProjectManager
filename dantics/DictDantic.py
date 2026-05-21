from typing import Annotated
from pydantic import Field, field_validator, ConfigDict

from dantics.GlobalDantic import CoreModel
from templates.StandardSysTemplate import StandardNoSqlConnTemplate

class NoSqlCheck(CoreModel):
    model_config = ConfigDict(from_attributes=True)

    nosql: Annotated[str, Field(
        ...,
        min_length=1,
        max_length=128,
        description="NoSql名称"
    )]

    @field_validator("nosql")
    def vertry_nosql_match(cls, v: str) -> str:
        template: StandardNoSqlConnTemplate = StandardNoSqlConnTemplate()
        valid_names: list = [
            template.SYS_NOSQL_NAME.replace(".json", ""),
            template.PROJECT_NOSQL_NAME.replace(".json", ""),
            template.PROJECT_TYPE_NOSQL_NAME.replace(".json", ""),
        ]
        if v not in valid_names: raise ValueError("无该类型数据")
        return v
