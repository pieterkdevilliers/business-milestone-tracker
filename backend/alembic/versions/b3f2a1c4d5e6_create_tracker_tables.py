"""create tracker tables

Revision ID: b3f2a1c4d5e6
Revises: 220cd69694ba
Create Date: 2026-04-17 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "b3f2a1c4d5e6"
down_revision: Union[str, Sequence[str], None] = "220cd69694ba"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "quarters",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("quarter_number", sa.Integer(), nullable=False),
        sa.Column("label", sa.String(200), nullable=False),
        sa.Column("theme", sa.String(200), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("quarter_number"),
    )
    op.create_table(
        "months",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("quarter_id", sa.Integer(), nullable=False),
        sa.Column("month_name", sa.String(50), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("theme", sa.String(200), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["quarter_id"], ["quarters.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("sort_order"),
    )
    op.create_table(
        "milestones",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("month_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["month_id"], ["months.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "month_metrics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("month_id", sa.Integer(), nullable=False),
        sa.Column("label", sa.String(200), nullable=False),
        sa.Column("target", sa.String(200), nullable=False),
        sa.Column("actual", sa.String(200), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["month_id"], ["months.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "month_notes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("month_id", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False, server_default=""),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["month_id"], ["months.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("month_id"),
    )
    op.create_table(
        "quarter_metrics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("quarter_id", sa.Integer(), nullable=False),
        sa.Column("label", sa.String(200), nullable=False),
        sa.Column("target", sa.String(200), nullable=False),
        sa.Column("actual", sa.String(200), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["quarter_id"], ["quarters.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "quarter_notes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("quarter_id", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False, server_default=""),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["quarter_id"], ["quarters.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("quarter_id"),
    )
    op.create_table(
        "master_milestones",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("target_date", sa.String(50), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False, server_default="0"),
        sa.Column("actual_date", sa.String(50), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.Column("colour_group", sa.String(20), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("master_milestones")
    op.drop_table("quarter_notes")
    op.drop_table("quarter_metrics")
    op.drop_table("month_notes")
    op.drop_table("month_metrics")
    op.drop_table("milestones")
    op.drop_table("months")
    op.drop_table("quarters")
