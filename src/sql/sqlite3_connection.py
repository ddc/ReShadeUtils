#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# # -*- coding: utf-8 -*-

import sqlite3
from src import constants


class Sqlite3:
    def __init__(self, main):
        self.log = main.log
        self.db_file = constants.SQLITE3_FILENAME


    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_file)
        except Exception as e:
            conn = None
            msg = "sqlite3: Cannot Create Database Connection."
            self.log.error(f"{msg}{str(e)}")
            self.log.exception("sqlite", exc_info=e)
            raise sqlite3.OperationalError(e)
        return conn


    def executescript(self, sql):
        result = None
        conn = self.create_connection()
        if conn is not None:
            try:
                c = conn.cursor()
                sql = f"""PRAGMA foreign_keys = ON;
                      BEGIN TRANSACTION;
                      {sql}
                      COMMIT TRANSACTION;\n"""
                c.executescript(sql)
                c.close()
                conn.commit()
            except Exception as e:
                self.log.exception("sqlite", exc_info=e)
                self.log.error(f"sql:({sql})")
                raise sqlite3.OperationalError(e)

            if conn is not None:
                conn.close()
        return result


    def select(self, sql):
        final_data = None
        conn = self.create_connection()
        if conn is not None:
            try:
                if sql is not None and len(sql) > 0:
                    final_data = {}
                    c = conn.cursor()
                    c.execute(sql)
                    rows = c.fetchall()
                    column_names = list(map(lambda x: x[0], c.description))
                    c.close()
                    for lineNumber, data in enumerate(rows):
                        final_data[lineNumber] = {}
                        for columnNumber, value in enumerate(data):
                            final_data[lineNumber][column_names[columnNumber]] = value
                    if len(final_data) == 0:
                        final_data = None
            except Exception as e:
                self.log.exception("sqlite", exc_info=e)
                self.log.error(f"sql:({sql})")

            if conn is not None:
                conn.close()
        return final_data
