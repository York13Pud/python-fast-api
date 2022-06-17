"""add content to posts table

Revision ID: 4097c81ae64b
Revises: 1df955918de1
Create Date: 2022-06-17 14:54:40.603229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4097c81ae64b'
down_revision = '785b3ca90a20'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable = False))


def downgrade() -> None:
    op.drop_column("posts", "content")
