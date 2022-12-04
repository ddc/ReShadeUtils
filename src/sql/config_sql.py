# |*****************************************************
# * Copyright         : Copyright (C) 2022
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# -*- coding: utf-8 -*-
from src.sql.tables import Configs


class ConfigSql:
    def __init__(self, main):
        self.main = main
        self.log = main.log
        self.table = Configs.__table__
        self.database = main.database

    def get_configs(self):
        sql = self.table.select().where(self.table.columns.id == 1)
        return self.database.select(sql)

    def get_program_version(self):
        from sqlalchemy.sql import select
        sql = select(self.table.columns.program_version).where(
            self.table.columns.id == 1
        )
        return self.database.select(sql)

    def set_default_configs(self):
        sql = self.table.insert()
        return self.database.execute(sql)

    def update_dark_theme(self, status):
        sql = self.table.update().\
            values(use_dark_theme=status).\
            where(self.table.columns.id == 1)
        return self.database.execute(sql)

    def update_shaders(self, status):
        sql = self.table.update().\
            values(update_shaders=status).\
            where(self.table.columns.id == 1)
        return self.database.execute(sql)

    def update_check_program_updates(self, status):
        sql = self.table.update().\
            values(check_program_updates=status).\
            where(self.table.columns.id == 1)
        return self.database.execute(sql)

    def update_show_info_messages(self, status):
        sql = self.table.update().\
            values(show_info_messages=status).\
            where(self.table.columns.id == 1)
        return self.database.execute(sql)

    def update_check_resahde_updates(self, status):
        sql = self.table.update().\
            values(check_reshade_updates=status).\
            where(self.table.columns.id == 1)
        return self.database.execute(sql)

    def update_create_screenshots_folder(self, status):
        sql = self.table.update().\
            values(create_screenshots_folder=status).\
            where(self.table.columns.id == 1)
        return self.database.execute(sql)

    def update_reshade_version(self, reshade_version):
        sql = self.table.update().\
            values(reshade_version=reshade_version).\
            where(self.table.columns.id == 1)
        return self.database.execute(sql)

    def update_program_version(self, program_version):
        sql = self.table.update().\
            values(program_version=program_version).\
            where(self.table.columns.id == 1)
        return self.database.execute(sql)
