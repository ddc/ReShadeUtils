#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# * Python            : 3.6
# |*****************************************************
# # -*- coding: utf-8 -*-

from src.databases.databases import Databases


class ConfigsSql:
    def __init__(self, main):
        self.main = main
        self.log = main.log

    ################################################################################
    def get_configs(self):
        sql = "SELECT * from configs where id = 1;"
        databases = Databases(self.main)
        return databases.select(sql)

    ################################################################################
    def set_default_configs(self, configsObj: object):
        sql = f"""INSERT INTO configs(
            use_dark_theme,
            update_shaders,
            check_program_updates,
            check_reshade_updates,
            create_screenshots_folder
            )VALUES(
            '{configsObj.use_dark_theme}',
            '{configsObj.update_shaders}',
            '{configsObj.check_program_updates}',
            '{configsObj.check_reshade_updates}',
            '{configsObj.create_screenshots_folder}'
            );"""
        databases = Databases(self.main)
        databases.execute(sql)

    #################################################################################
    def update_dark_theme(self, configsObj: object):
        sql = f"""UPDATE configs SET
                use_dark_theme = '{configsObj.status}'
                WHERE id = 1;"""
        databases = Databases(self.main)
        databases.execute(sql)

    #################################################################################
    def update_shaders(self, configsObj: object):
        sql = f"""UPDATE configs SET
                update_shaders = '{configsObj.status}'
                WHERE id = 1;"""
        databases = Databases(self.main)
        databases.execute(sql)

    #################################################################################
    def update_check_program_updates(self, configsObj: object):
        sql = f"""UPDATE configs SET
                check_program_updates = '{configsObj.status}'
                WHERE id = 1;"""
        databases = Databases(self.main)
        databases.execute(sql)

    #################################################################################
    def update_check_resahde_updates(self, configsObj: object):
        sql = f"""UPDATE configs SET
                check_reshade_updates = '{configsObj.status}'
                WHERE id = 1;"""
        databases = Databases(self.main)
        databases.execute(sql)

    #################################################################################
    def update_create_screenshots_folder(self, configsObj: object):
        sql = f"""UPDATE configs SET
                create_screenshots_folder = '{configsObj.status}'
                WHERE id = 1;"""
        databases = Databases(self.main)
        databases.execute(sql)

    #################################################################################
    def update_reshade_version(self, configsObj: object):
        sql = f"""UPDATE configs SET
                reshade_version = '{configsObj.reshade_version}'
                WHERE id = 1;"""
        databases = Databases(self.main)
        databases.execute(sql)

    ################################################################################
    def update_reset_reshade_files(self, configsObj: object):
        sql = f"""UPDATE configs SET
                reset_reshade_files = '{configsObj.status}'
                WHERE id = 1;"""
        databases = Databases(self.main)
        databases.execute(sql)
