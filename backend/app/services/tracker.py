from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.tracker import (
    MasterMilestone,
    Milestone,
    Month,
    MonthMetric,
    MonthNote,
    Quarter,
    QuarterMetric,
    QuarterNote,
)


async def get_all_months(db: AsyncSession) -> list[Month]:
    result = await db.execute(
        select(Month)
        .options(
            selectinload(Month.milestones),
            selectinload(Month.metrics),
            selectinload(Month.note),
        )
        .order_by(Month.sort_order)
    )
    return list(result.scalars().all())


async def get_month_by_id(db: AsyncSession, month_id: int) -> Optional[Month]:
    result = await db.execute(
        select(Month)
        .options(
            selectinload(Month.milestones),
            selectinload(Month.metrics),
            selectinload(Month.note),
        )
        .where(Month.id == month_id)
    )
    return result.scalar_one_or_none()


async def toggle_milestone(
    db: AsyncSession, milestone_id: int, completed: bool
) -> Optional[Milestone]:
    result = await db.execute(
        select(Milestone).where(Milestone.id == milestone_id)
    )
    milestone = result.scalar_one_or_none()
    if milestone:
        milestone.completed = completed
        await db.commit()
        await db.refresh(milestone)
    return milestone


async def update_milestone(
    db: AsyncSession,
    milestone_id: int,
    completed: Optional[bool],
    text: Optional[str],
) -> Optional[Milestone]:
    result = await db.execute(
        select(Milestone).where(Milestone.id == milestone_id)
    )
    milestone = result.scalar_one_or_none()
    if milestone:
        if completed is not None:
            milestone.completed = completed
        if text is not None:
            milestone.text = text
        await db.commit()
        await db.refresh(milestone)
    return milestone


async def create_milestone(db: AsyncSession, month_id: int, text: str) -> Milestone:
    result = await db.execute(
        select(Milestone)
        .where(Milestone.month_id == month_id)
        .order_by(Milestone.sort_order.desc())
    )
    last = result.scalars().first()
    next_order = (last.sort_order + 1) if last else 1
    milestone = Milestone(
        month_id=month_id, text=text, completed=False, sort_order=next_order
    )
    db.add(milestone)
    await db.commit()
    await db.refresh(milestone)
    return milestone


async def delete_milestone(db: AsyncSession, milestone_id: int) -> bool:
    result = await db.execute(
        select(Milestone).where(Milestone.id == milestone_id)
    )
    milestone = result.scalar_one_or_none()
    if not milestone:
        return False
    await db.delete(milestone)
    await db.commit()
    return True


async def update_month_metric(
    db: AsyncSession, metric_id: int, actual: Optional[str]
) -> Optional[MonthMetric]:
    result = await db.execute(
        select(MonthMetric).where(MonthMetric.id == metric_id)
    )
    metric = result.scalar_one_or_none()
    if metric:
        metric.actual = actual
        await db.commit()
        await db.refresh(metric)
    return metric


async def upsert_month_note(
    db: AsyncSession, month_id: int, content: str
) -> MonthNote:
    result = await db.execute(
        select(MonthNote).where(MonthNote.month_id == month_id)
    )
    note = result.scalar_one_or_none()
    if note:
        note.content = content
        note.updated_at = datetime.utcnow()
    else:
        note = MonthNote(
            month_id=month_id, content=content, updated_at=datetime.utcnow()
        )
        db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


async def get_all_quarters(db: AsyncSession) -> list[Quarter]:
    result = await db.execute(
        select(Quarter)
        .options(
            selectinload(Quarter.months)
            .selectinload(Month.milestones),
            selectinload(Quarter.months)
            .selectinload(Month.metrics),
            selectinload(Quarter.months)
            .selectinload(Month.note),
            selectinload(Quarter.metrics),
            selectinload(Quarter.note),
        )
        .order_by(Quarter.quarter_number)
    )
    return list(result.scalars().all())


async def update_quarter_metric(
    db: AsyncSession, metric_id: int, actual: Optional[str]
) -> Optional[QuarterMetric]:
    result = await db.execute(
        select(QuarterMetric).where(QuarterMetric.id == metric_id)
    )
    metric = result.scalar_one_or_none()
    if metric:
        metric.actual = actual
        await db.commit()
        await db.refresh(metric)
    return metric


async def upsert_quarter_note(
    db: AsyncSession, quarter_id: int, content: str
) -> QuarterNote:
    result = await db.execute(
        select(QuarterNote).where(QuarterNote.quarter_id == quarter_id)
    )
    note = result.scalar_one_or_none()
    if note:
        note.content = content
        note.updated_at = datetime.utcnow()
    else:
        note = QuarterNote(
            quarter_id=quarter_id, content=content, updated_at=datetime.utcnow()
        )
        db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


async def get_all_master_milestones(db: AsyncSession) -> list[MasterMilestone]:
    result = await db.execute(
        select(MasterMilestone).order_by(MasterMilestone.sort_order)
    )
    return list(result.scalars().all())


async def update_master_milestone(
    db: AsyncSession,
    milestone_id: int,
    completed: Optional[bool],
    actual_date: Optional[str],
    notes: Optional[str],
) -> Optional[MasterMilestone]:
    result = await db.execute(
        select(MasterMilestone).where(MasterMilestone.id == milestone_id)
    )
    milestone = result.scalar_one_or_none()
    if milestone:
        if completed is not None:
            milestone.completed = completed
        if actual_date is not None:
            milestone.actual_date = actual_date
        if notes is not None:
            milestone.notes = notes
        await db.commit()
        await db.refresh(milestone)
    return milestone
