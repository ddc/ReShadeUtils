#! /usr/bin/env python3
# |*****************************************************
# * Copyright         : Copyright (C) 2019
# * Author            : ddc
# * License           : GPL v3
# |*****************************************************
# # -*- coding: utf-8 -*-

import contextlib
from src import constants
from sqlalchemy.engine import create_engine
from sqlalchemy import event


class DatabaseClass:
    def __init__(self, main):
        self.log = main.log
        self.db_file = constants.SQLITE3_FILENAME
        self.batch_size = 100
        self.db_engine = main.db_engine


    def create_engine(self):
        try:
            engine = create_engine(f"sqlite:///{self.db_file}",
                                   echo=False
                                   ).execution_options(stream_results=False,
                                                       isolation_level="AUTOCOMMIT")

            @event.listens_for(engine, "before_cursor_execute")
            def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
                cursor.arraysize = self.batch_size

            return engine
        except Exception as err:
            self.log.error(f"[{str(type(err))}]:[{str(err)}]:Cannot Create Database Connection")
            return None


    def execute(self, query):
        with contextlib.closing(self.db_engine.connect()) as connection:
            try:
                # sql = f"""PRAGMA foreign_keys = OFF;
                #       BEGIN TRANSACTION;
                #       {query}
                #       COMMIT TRANSACTION;\n"""
                # connection.execute(sql)
                connection.execute(query)
                return True
            except Exception as e:
                self.log.error(str(e))

        return False


    def select(self, query):
        if self.db_engine is not None:
            with contextlib.closing(self.db_engine.connect()) as connection:
                try:
                    if query is not None:
                        final_data = {}
                        rows = connection.execute(query)
                        column_names = list(map(lambda x: x[0], rows.cursor.description))
                        for lineNumber, data in enumerate(rows):
                            final_data[lineNumber] = {}
                            for columnNumber, value in enumerate(data):
                                final_data[lineNumber][column_names[columnNumber]] = value
                        if len(final_data) == 0:
                            final_data = None
                except Exception as e:
                    self.log.exception("sqlite", exc_info=e)
                    self.log.error(f"sql:({query})")
                    final_data = None

        return final_data
