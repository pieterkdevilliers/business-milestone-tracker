from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Quarter(Base):
    __tablename__ = "quarters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quarter_number: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    label: Mapped[str] = mapped_column(String(200), nullable=False)
    theme: Mapped[str] = mapped_column(String(200), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    months: Mapped[list["Month"]] = relationship(
        "Month", back_populates="quarter", order_by="Month.sort_order"
    )
    metrics: Mapped[list["QuarterMetric"]] = relationship(
        "QuarterMetric", back_populates="quarter", order_by="QuarterMetric.sort_order"
    )
    note: Mapped[Optional["QuarterNote"]] = relationship(
        "QuarterNote", back_populates="quarter", uselist=False
    )


class Month(Base):
    __tablename__ = "months"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quarter_id: Mapped[int] = mapped_column(Integer, ForeignKey("quarters.id"), nullable=False)
    month_name: Mapped[str] = mapped_column(String(50), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    theme: Mapped[str] = mapped_column(String(200), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)

    quarter: Mapped["Quarter"] = relationship("Quarter", back_populates="months")
    milestones: Mapped[list["Milestone"]] = relationship(
        "Milestone", back_populates="month", order_by="Milestone.sort_order"
    )
    metrics: Mapped[list["MonthMetric"]] = relationship(
        "MonthMetric", back_populates="month", order_by="MonthMetric.sort_order"
    )
    note: Mapped[Optional["MonthNote"]] = relationship(
        "MonthNote", back_populates="month", uselist=False
    )


class Milestone(Base):
    __tablename__ = "milestones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    month_id: Mapped[int] = mapped_column(Integer, ForeignKey("months.id"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)

    month: Mapped["Month"] = relationship("Month", back_populates="milestones")


class MonthMetric(Base):
    __tablename__ = "month_metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    month_id: Mapped[int] = mapped_column(Integer, ForeignKey("months.id"), nullable=False)
    label: Mapped[str] = mapped_column(String(200), nullable=False)
    target: Mapped[str] = mapped_column(String(200), nullable=False)
    actual: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)

    month: Mapped["Month"] = relationship("Month", back_populates="metrics")


class MonthNote(Base):
    __tablename__ = "month_notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    month_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("months.id"), nullable=False, unique=True
    )
    content: Mapped[str] = mapped_column(Text, default="", nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    month: Mapped["Month"] = relationship("Month", back_populates="note")


class QuarterMetric(Base):
    __tablename__ = "quarter_metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quarter_id: Mapped[int] = mapped_column(Integer, ForeignKey("quarters.id"), nullable=False)
    label: Mapped[str] = mapped_column(String(200), nullable=False)
    target: Mapped[str] = mapped_column(String(200), nullable=False)
    actual: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)

    quarter: Mapped["Quarter"] = relationship("Quarter", back_populates="metrics")


class QuarterNote(Base):
    __tablename__ = "quarter_notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quarter_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("quarters.id"), nullable=False, unique=True
    )
    content: Mapped[str] = mapped_column(Text, default="", nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    quarter: Mapped["Quarter"] = relationship("Quarter", back_populates="note")


class MasterMilestone(Base):
    __tablename__ = "master_milestones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    target_date: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    actual_date: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    colour_group: Mapped[str] = mapped_column(String(20), nullable=False)
