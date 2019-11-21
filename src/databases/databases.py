#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# * Python            : 3.6
# |*****************************************************
# # -*- coding: utf-8 -*-

from src.databases.sqlite3.connection import Sqlite3
from src.databases.postgres.connection import PostgreSQL


class Databases:
    def __init__(self, main):
        self.main = main
        self.log = main.log
        self.database_in_use = main.settings["DatabaseInUse"]

    ################################################################################
    def check_database_connection(self):
        if self.database_in_use == "sqlite":
            sqlite3 = Sqlite3(self.main)
            return sqlite3.create_connection()
        elif self.database_in_use == "postgres":
            postgreSQL = PostgreSQL(self.main)
            return postgreSQL.create_connection()

    ################################################################################
    def execute(self, sql):
        if self.database_in_use == "sqlite":
            sqlite3 = Sqlite3(self.main)
            sqlite3.executescript(sql)
        elif self.database_in_use == "postgres":
            postgreSQL = PostgreSQL(self.main)
            postgreSQL.execute(sql)

    ################################################################################
    def select(self, sql):
        if self.database_in_use == "sqlite":
            sqlite3 = Sqlite3(self.main)
            return sqlite3.select(sql)
        elif self.database_in_use == "postgres":
            postgreSQL = PostgreSQL(self.main)
            return postgreSQL.select(sql)

    ################################################################################
    def set_primary_key_type(self):
        if self.database_in_use == "sqlite":
            return "INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE"
        elif self.database_in_use == "postgres":
            return "BIGSERIAL NOT NULL PRIMARY KEY UNIQUE"
