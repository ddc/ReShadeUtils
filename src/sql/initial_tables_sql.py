#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# * Python            : 3.6
# |*****************************************************
# # -*- coding: utf-8 -*-

from src.databases.databases import Databases
from src.utils import utilities, constants


class InitialTablesSql:
    def __init__(self, main):
        self.main = main
        self.log = main.log

    ################################################################################
    def create_initial_tables(self):
        databases = Databases(self.main)
        primary_key_type = databases.set_primary_key_type()

        # if changed order of columns, need to change on update_tables_sql.py as well
        sql = f"""
        CREATE TABLE IF NOT EXISTS configs (
            id                              {primary_key_type},
            use_dark_theme                  CHAR(1)  NOT NULL DEFAULT 'Y',
            update_shaders                  CHAR(1)  NOT NULL DEFAULT 'Y',
            check_program_updates           CHAR(1)  NOT NULL DEFAULT 'Y',
            check_reshade_updates           CHAR(1)  NOT NULL DEFAULT 'Y',
            silent_reshade_updates          CHAR(1)  NOT NULL DEFAULT 'Y',
            reset_reshade_files             CHAR(1)  NOT NULL DEFAULT 'N',
            create_screenshots_folder       CHAR(1)  NOT NULL DEFAULT 'Y',
            program_version                 TEXT,
            reshade_version                 TEXT,
            CONSTRAINT  check_use_dark_theme CHECK (use_dark_theme IN ('Y','N')),
            CONSTRAINT  check_update_shaders CHECK (update_shaders IN ('Y','N')),
            CONSTRAINT  check_program_updates CHECK (check_program_updates IN ('Y','N')),
            CONSTRAINT  check_reshade_updates CHECK (check_reshade_updates IN ('Y','N')),
            CONSTRAINT  check_create_screenshots_folder CHECK (create_screenshots_folder IN ('Y','N')),
            CONSTRAINT  check_silent_reshade_updates CHECK (silent_reshade_updates IN ('Y','N')),
            CONSTRAINT  check_reset_reshade_files CHECK (reset_reshade_files IN ('Y','N'))
        );
        
        CREATE TABLE IF NOT EXISTS games (
            id             {primary_key_type},
            name           TEXT     NOT NULL,
            architecture   TEXT     NOT NULL,
            api            TEXT     NOT NULL,
            path           TEXT     NOT NULL
        );

        """
        databases.execute(sql)
