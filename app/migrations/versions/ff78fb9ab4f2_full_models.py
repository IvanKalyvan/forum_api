"""full models

Revision ID: ff78fb9ab4f2
Revises: 683bba71d372
Create Date: 2024-07-16 13:23:51.060601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff78fb9ab4f2'
down_revision: Union[str, None] = '683bba71d372'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
