#! /usr/bin/env python3
#|*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# * Python            : 3.6
#|*****************************************************
# # -*- coding: utf-8 -*-

from src.utils import utils, constants
from src.databases.sqlite3.connection import Sqlite3
from src.databases.postgres.connection import PostgreSQL
################################################################################
################################################################################
################################################################################ 
class Databases():
    def __init__(self, log):
        self.log = log
        self.database_in_use = utils.get_file_settings(constants.db_settings_filename, "Configs", "DatabaseInUse")
################################################################################
################################################################################
################################################################################
    def check_database_connection(self):
        if self.database_in_use == "sqlite":
            sqlite3 = Sqlite3(self.log)
            return sqlite3.create_connection()
        elif self.database_in_use == "postgres":
            postgreSQL = PostgreSQL(self.log)
            return postgreSQL.create_connection()  
################################################################################
################################################################################
################################################################################
    def execute(self, sql):
        if self.database_in_use == "sqlite":
            sqlite3 = Sqlite3(self.log)
            sqlite3.executescript(sql)
        elif self.database_in_use == "postgres":
            postgreSQL = PostgreSQL(self.log)
            postgreSQL.execute(sql)
################################################################################
################################################################################
################################################################################
    def select(self, sql):
        if self.database_in_use == "sqlite":
            sqlite3 = Sqlite3(self.log)
            return sqlite3.select(sql)
        elif self.database_in_use == "postgres":
            postgreSQL = PostgreSQL(self.log)
            return postgreSQL.select(sql)
################################################################################
################################################################################
################################################################################
    def set_primary_key_type(self):
        if self.database_in_use == "sqlite":
            return "INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE"
        elif self.database_in_use == "postgres":
            return "BIGSERIAL NOT NULL PRIMARY KEY UNIQUE"
################################################################################
################################################################################
################################################################################
