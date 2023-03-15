"""add last columns 2

Revision ID: 92b4defa4e57
Revises: 9dc73a21fc3e
Create Date: 2023-03-14 22:42:36.272730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92b4defa4e57'
down_revision = '9dc73a21fc3e'
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
