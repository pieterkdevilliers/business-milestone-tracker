from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MilestoneSchema(BaseModel):
    id: int
    month_id: int
    text: str
    completed: bool
    sort_order: int

    model_config = {"from_attributes": True}


class MonthMetricSchema(BaseModel):
    id: int
    month_id: int
    label: str
    target: str
    actual: Optional[str] = None
    sort_order: int

    model_config = {"from_attributes": True}


class MonthNoteSchema(BaseModel):
    id: int
    month_id: int
    content: str
    updated_at: datetime

    model_config = {"from_attributes": True}


class MonthDetail(BaseModel):
    id: int
    quarter_id: int
    month_name: str
    year: int
    theme: str
    sort_order: int
    milestones: list[MilestoneSchema]
    metrics: list[MonthMetricSchema]
    note: Optional[MonthNoteSchema] = None

    model_config = {"from_attributes": True}


class QuarterMetricSchema(BaseModel):
    id: int
    quarter_id: int
    label: str
    target: str
    actual: Optional[str] = None
    sort_order: int

    model_config = {"from_attributes": True}


class QuarterNoteSchema(BaseModel):
    id: int
    quarter_id: int
    content: str
    updated_at: datetime

    model_config = {"from_attributes": True}


class QuarterDetail(BaseModel):
    id: int
    quarter_number: int
    label: str
    theme: str
    year: int
    months: list[MonthDetail]
    metrics: list[QuarterMetricSchema]
    note: Optional[QuarterNoteSchema] = None

    model_config = {"from_attributes": True}


class MasterMilestoneSchema(BaseModel):
    id: int
    target_date: str
    text: str
    completed: bool
    actual_date: Optional[str] = None
    notes: Optional[str] = None
    sort_order: int
    colour_group: str

    model_config = {"from_attributes": True}


# Request bodies

class MilestoneCreate(BaseModel):
    month_id: int
    text: str


class MilestoneUpdate(BaseModel):
    completed: Optional[bool] = None
    text: Optional[str] = None


class MetricUpdate(BaseModel):
    actual: Optional[str] = None


class NoteUpdate(BaseModel):
    content: str


class MasterMilestoneUpdate(BaseModel):
    completed: Optional[bool] = None
    actual_date: Optional[str] = None
    notes: Optional[str] = None
