"""Full Models

Revision ID: c5d406226019
Revises: ff78fb9ab4f2
Create Date: 2024-07-16 13:27:19.772027

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c5d406226019'
down_revision: Union[str, None] = 'ff78fb9ab4f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('content', sa.Text, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('update_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('is_blocked', sa.BOOLEAN(), nullable=True),
    sa.Column('user_id', sa.BIGINT(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('content', sa.Text, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('update_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('is_blocked', sa.BOOLEAN(), nullable=True),
    sa.Column('user_id', sa.BIGINT(), nullable=True),
    sa.Column('post_id', sa.BIGINT(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    op.drop_table('post')
    # ### end Alembic commands ###
