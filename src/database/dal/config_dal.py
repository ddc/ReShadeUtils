# -*- coding: utf-8 -*-
import sqlalchemy as sa
from src.database.models.config_model import Config
from src.database.db_utils import DBUtils


class ConfigDal:
    def __init__(self, db_session, log):
        self.log = log
        self.columns = [x for x in Config.__table__.columns]
        self.db_utils = DBUtils(db_session, log)

    def get_configs(self):
        stmt = sa.select(*self.columns).where(Config.id == 1)
        results = self.db_utils.fetchall(stmt)
        return results

    def get_program_version(self):
        stmt = sa.select(Config.program_version).where(Config.id == 1)
        program_version = self.db_utils.fetch_value(stmt)
        return program_version

    def update_dark_theme(self, status):
        stmt = sa.update(Config).where(Config.id == 1).values(use_dark_theme=status)
        self.db_utils.execute(stmt)

    def update_shaders(self, status):
        stmt = sa.update(Config).where(Config.id == 1).values(update_shaders=status)
        self.db_utils.execute(stmt)

    def update_check_program_updates(self, status):
        stmt = sa.update(Config).where(Config.id == 1).values(check_program_updates=status)
        self.db_utils.execute(stmt)

    def update_show_info_messages(self, status):
        stmt = sa.update(Config).where(Config.id == 1).values(show_info_messages=status)
        self.db_utils.execute(stmt)

    def update_check_resahde_updates(self, status):
        stmt = sa.update(Config).where(Config.id == 1).values(check_reshade_updates=status)
        self.db_utils.execute(stmt)

    def update_create_screenshots_folder(self, status):
        stmt = sa.update(Config).where(Config.id == 1).values(create_screenshots_folder=status)
        self.db_utils.execute(stmt)

    def update_reshade_version(self, reshade_version):
        stmt = sa.update(Config).where(Config.id == 1).values(reshade_version=reshade_version)
        self.db_utils.execute(stmt)

    def update_program_version(self, program_version):
        stmt = sa.update(Config).where(Config.id == 1).values(program_version=program_version)
        self.db_utils.execute(stmt)
