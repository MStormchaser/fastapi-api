"""add new user table

Revision ID: 4f37787953d5
Revises: a858e8204881
Create Date: 2023-03-14 22:02:50.369590

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f37787953d5'
down_revision = 'a858e8204881'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
                sa.Column("id", sa.Integer(), nullable=False),
                sa.Column("email", sa.String(), nullable=False),
                sa.Column("password", sa.String(), nullable=False),
                sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                            server_default=sa.text("now()"), nullable=False),
                sa.PrimaryKeyConstraint("id"),
                sa.UniqueConstraint("email"))
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
