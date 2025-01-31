"""Full Models6

Revision ID: 8df5a24d7d2a
Revises: 5983c865748a
Create Date: 2024-07-17 22:07:01.838399

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8df5a24d7d2a'
down_revision: Union[str, None] = '5983c865748a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comment', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DATE(),
               existing_nullable=True)
    op.alter_column('comment', 'update_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DATE(),
               existing_nullable=True)
    op.alter_column('post', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DATE(),
               existing_nullable=True)
    op.alter_column('post', 'update_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DATE(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('post', 'update_at',
               existing_type=sa.DATE(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)
    op.alter_column('post', 'created_at',
               existing_type=sa.DATE(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)
    op.alter_column('comment', 'update_at',
               existing_type=sa.DATE(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)
    op.alter_column('comment', 'created_at',
               existing_type=sa.DATE(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)
    # ### end Alembic commands ###
