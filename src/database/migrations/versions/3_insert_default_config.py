"""insert_default_config

Revision ID: 3
Revises: 2
Create Date: 2024-01-04 19:45:48.493481

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from src.database.models.config_model import Config


# revision identifiers, used by Alembic.
revision: str = '3'
down_revision: Union[str, None] = '2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.insert(Config))


def downgrade() -> None:
    op.execute(sa.delete(Config))
