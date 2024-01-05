"""create_config_table

Revision ID: 1
Revises:
Create Date: 2024-01-04 18:53:37.512091

"""
import constants
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('config',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('program_version', sa.String(), server_default=constants.VERSION, nullable=True),
    sa.Column('reshade_version', sa.String(), nullable=True),
    sa.Column('use_dark_theme', sa.Boolean(), server_default='0', nullable=False),
    sa.Column('check_program_updates', sa.Boolean(), server_default='1', nullable=False),
    sa.Column('show_info_messages', sa.Boolean(), server_default='1', nullable=False),
    sa.Column('check_reshade_updates', sa.Boolean(), server_default='1', nullable=False),
    sa.Column('update_shaders', sa.Boolean(), server_default='1', nullable=False),
    sa.Column('create_screenshots_folder', sa.Boolean(), server_default='1', nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('config')
    # ### end Alembic commands ###
