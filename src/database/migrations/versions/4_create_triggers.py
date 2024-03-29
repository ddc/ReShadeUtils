"""create_config_trigger

Revision ID: 4
Revises: 3
Create Date: 2024-01-04 18:56:58.984108

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '4'
down_revision: Union[str, None] = '3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        """
            CREATE TRIGGER [update_timestamp_games_tr]
                AFTER UPDATE
                ON games
                FOR EACH ROW
                WHEN OLD.updated_at < CURRENT_TIMESTAMP
            BEGIN
                UPDATE games SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
            END;
        """
    )
    op.execute(
        """
            CREATE TRIGGER [update_timestamp_config_tr]
                AFTER UPDATE ON config
                FOR EACH ROW
                WHEN OLD.updated_at < CURRENT_TIMESTAMP
            BEGIN
                UPDATE config SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
            END;
        """
    )
    op.execute("""
        CREATE TRIGGER [before_insert_config_table]
                BEFORE INSERT ON config
                BEGIN
                    SELECT CASE
                        WHEN (SELECT COUNT(*) FROM config)IS 1 THEN
                        RAISE(ABORT, 'CANNOT INSERT INTO CONFIG TABLE ANYMORE')
                    END;
                END;    
    """)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('DROP TRIGGER IF EXISTS update_timestamp_games_tr')
    op.execute('DROP TRIGGER IF EXISTS before_insert_config_table')
    op.execute('DROP TRIGGER IF EXISTS update_timestamp_config_tr')
    # ### end Alembic commands ###
