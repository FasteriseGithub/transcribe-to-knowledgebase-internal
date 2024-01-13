from pydantic import BaseModel
from datetime import date
from enum import Enum

class MeetingTypeEnum(str, Enum):
    marketing = "Marketing"
    general = "General"
    development = "Development"
    outreach = "Outreach"
    discovery = "Discovery"

class MetaData(BaseModel):
    date: date
    meeting_type: MeetingTypeEnum
    summary: bool
