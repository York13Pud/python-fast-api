"""create posts table

Revision ID: 785b3ca90a20
Revises: 
Create Date: 2022-06-17 12:11:37.725054

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '785b3ca90a20'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", 
                    sa.Column("id", 
                              sa.Integer, 
                              nullable = False, 
                              primary_key = True),
                    sa.Column("title", 
                              sa.String, 
                              nullable = False))


def downgrade() -> None:
    op.drop_table("posts")
