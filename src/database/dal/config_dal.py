# -*- coding: utf-8 -*-
import sqlalchemy as sa
from ddcDatabases import DBUtils
from ddcDatabases.exceptions import DBFetchAllException
from src.database.models.config_model import Config


class ConfigDal:
    def __init__(self, db_session, log):
        self.log = log
        self.columns = [x for x in Config.__table__.columns]
        self.db_utils = DBUtils(db_session)

    def update_dark_theme(self, status: bool, config_id=1):
        stmt = sa.update(Config).where(Config.id == config_id).values(use_dark_theme=status)
        self.db_utils.execute(stmt)

    def update_check_program_updates(self, status: bool, config_id=1):
        stmt = sa.update(Config).where(Config.id == config_id).values(check_program_updates=status)
        self.db_utils.execute(stmt)

    def update_show_info_messages(self, status: bool, config_id=1):
        stmt = sa.update(Config).where(Config.id == config_id).values(show_info_messages=status)
        self.db_utils.execute(stmt)

    def update_check_reshade_updates(self, status: bool, config_id=1):
        stmt = sa.update(Config).where(Config.id == config_id).values(check_reshade_updates=status)
        self.db_utils.execute(stmt)

    def update_create_screenshots_folder(self, status: bool, config_id=1):
        stmt = sa.update(Config).where(Config.id == config_id).values(create_screenshots_folder=status)
        self.db_utils.execute(stmt)

    def update_reshade_version(self, reshade_version: str, config_id=1):
        stmt = sa.update(Config).where(Config.id == config_id).values(reshade_version=reshade_version)
        self.db_utils.execute(stmt)

    def update_program_version(self, program_version: str, config_id=1):
        stmt = sa.update(Config).where(Config.id == config_id).values(program_version=program_version)
        self.db_utils.execute(stmt)

    def get_configs(self, config_id=1):
        try:
            stmt = sa.select(*self.columns).where(Config.id == config_id)
            results = self.db_utils.fetchall(stmt)
            return results
        except DBFetchAllException:
            return None
