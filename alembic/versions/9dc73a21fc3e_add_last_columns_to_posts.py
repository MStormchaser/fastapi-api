"""add last columns to posts

Revision ID: 9dc73a21fc3e
Revises: bf99173f2b80
Create Date: 2023-03-14 22:35:09.009480

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9dc73a21fc3e'
down_revision = 'bf99173f2b80'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published",
                                     sa.Boolean(), nullable=False, server_default="TRUE"))
    op.add_column("posts", sa.Column("created_at", 
                                     sa.TIMESTAMP(timezone=True), nullable=False, 
                                     server_default=sa.text("NOW()")))
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
