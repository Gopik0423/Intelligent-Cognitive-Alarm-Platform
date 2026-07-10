"""create challenges table

Revision ID: 0001_create_challenges
Revises:
Create Date: 2026-07-06 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


revision = "0001_create_challenges"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "challenges",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("type", sa.String(length=50), nullable=False, index=True),
        sa.Column("difficulty", sa.String(length=20), nullable=False, index=True),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("answer", sa.Text(), nullable=False),
        sa.Column("options", sa.JSON(), nullable=True),
        sa.Column("hint", sa.Text(), nullable=True),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("time_limit", sa.Integer(), nullable=False),
        sa.Column("points", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "type IN ('Math Problems', 'Logic Puzzles', 'Memory Challenges', 'Word Games', 'Pattern Recognition', 'Riddles', 'Quick Quizzes')",
            name="ck_challenges_type",
        ),
        sa.CheckConstraint(
            "difficulty IN ('Beginner', 'Easy', 'Medium', 'Hard', 'Expert')",
            name="ck_challenges_difficulty",
        ),
    )


def downgrade() -> None:
    op.drop_table("challenges")
