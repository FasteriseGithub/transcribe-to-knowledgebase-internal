from pydantic import BaseModel
from datetime import date
from enum import Enum

from pydantic_core.core_schema import date_schema

class MeetingTypeEnum(str, Enum):
    marketing = "MARKETING"
    general = "GEN"
    development = "DEV"

class MetaData(BaseModel):
    date: date
    meeting_type: MeetingTypeEnum
    summary: bool
