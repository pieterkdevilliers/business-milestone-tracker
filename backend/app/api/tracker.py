from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.tracker import (
    MasterMilestoneSchema,
    MasterMilestoneUpdate,
    MetricUpdate,
    MilestoneCreate,
    MilestoneSchema,
    MilestoneUpdate,
    MonthDetail,
    MonthMetricSchema,
    MonthNoteSchema,
    NoteUpdate,
    QuarterDetail,
    QuarterMetricSchema,
    QuarterNoteSchema,
)
from app.services import tracker as service

router = APIRouter(prefix="/tracker", tags=["tracker"])


@router.get("/months", response_model=list[MonthDetail])
async def list_months(db: AsyncSession = Depends(get_db)):
    return await service.get_all_months(db)


@router.get("/months/{month_id}", response_model=MonthDetail)
async def get_month(month_id: int, db: AsyncSession = Depends(get_db)):
    month = await service.get_month_by_id(db, month_id)
    if not month:
        raise HTTPException(status_code=404, detail="Month not found")
    return month


@router.post("/milestones", response_model=MilestoneSchema, status_code=201)
async def create_milestone(
    body: MilestoneCreate,
    db: AsyncSession = Depends(get_db),
):
    return await service.create_milestone(db, body.month_id, body.text)


@router.patch("/milestones/{milestone_id}", response_model=MilestoneSchema)
async def update_milestone(
    milestone_id: int,
    body: MilestoneUpdate,
    db: AsyncSession = Depends(get_db),
):
    milestone = await service.update_milestone(db, milestone_id, body.completed, body.text)
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    return milestone


@router.delete("/milestones/{milestone_id}", status_code=204)
async def delete_milestone(
    milestone_id: int,
    db: AsyncSession = Depends(get_db),
):
    deleted = await service.delete_milestone(db, milestone_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Milestone not found")


@router.patch("/month-metrics/{metric_id}", response_model=MonthMetricSchema)
async def update_month_metric(
    metric_id: int,
    body: MetricUpdate,
    db: AsyncSession = Depends(get_db),
):
    metric = await service.update_month_metric(db, metric_id, body.actual)
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    return metric


@router.patch("/month-notes/{month_id}", response_model=MonthNoteSchema)
async def update_month_note(
    month_id: int,
    body: NoteUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await service.upsert_month_note(db, month_id, body.content)


@router.get("/quarters", response_model=list[QuarterDetail])
async def list_quarters(db: AsyncSession = Depends(get_db)):
    return await service.get_all_quarters(db)


@router.patch("/quarter-metrics/{metric_id}", response_model=QuarterMetricSchema)
async def update_quarter_metric(
    metric_id: int,
    body: MetricUpdate,
    db: AsyncSession = Depends(get_db),
):
    metric = await service.update_quarter_metric(db, metric_id, body.actual)
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    return metric


@router.patch("/quarter-notes/{quarter_id}", response_model=QuarterNoteSchema)
async def update_quarter_note(
    quarter_id: int,
    body: NoteUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await service.upsert_quarter_note(db, quarter_id, body.content)


@router.get("/master-milestones", response_model=list[MasterMilestoneSchema])
async def list_master_milestones(db: AsyncSession = Depends(get_db)):
    return await service.get_all_master_milestones(db)


@router.patch(
    "/master-milestones/{milestone_id}", response_model=MasterMilestoneSchema
)
async def update_master_milestone(
    milestone_id: int,
    body: MasterMilestoneUpdate,
    db: AsyncSession = Depends(get_db),
):
    milestone = await service.update_master_milestone(
        db, milestone_id, body.completed, body.actual_date, body.notes
    )
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    return milestone
