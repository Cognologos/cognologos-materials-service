from typing import Any

from pydantic import Field, field_validator

from .abc import BaseModel


class PingSchema(BaseModel):
    id: str = Field(validation_alias="_id")
    ok: bool = True

    @field_validator("id", mode="before")
    @classmethod
    def validate_objectid(cls, v: Any):
        return str(v)
