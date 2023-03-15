"""add new column

Revision ID: 30149b754784
Revises: 9073ccc6f168
Create Date: 2023-03-14 21:33:53.930110

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30149b754784'
down_revision = '9073ccc6f168'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", column_name="content")
    pass
