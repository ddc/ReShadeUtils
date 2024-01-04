# -*- coding: utf-8 -*-
from sqlalchemy import event
from src import constants, messages
from sqlalchemy.engine import create_engine


class Database:
    def __init__(self):
        self.file = constants.SQLITE3_PATH
        self.batch_size = 100
        #self.engine = self.create_engine()

    # def create_engine(self):
    #     try:
    #         engine = create_engine(f"sqlite:///{self.file}", echo=False).\
    #             execution_options(stream_results=False,
    #                               isolation_level="AUTOCOMMIT")
    #
    #         @event.listens_for(engine, "before_cursor_execute")
    #         def receive_before_cursor_execute(conn,
    #                                           cursor,
    #                                           statement,
    #                                           params,
    #                                           context,
    #                                           executemany):
    #             cursor.arraysize = self.batch_size
    #         return engine
    #     except Exception as err:
    #         print(f"[{str(type(err))}]:[{str(err)}]:"
    #               f"{messages.error_db_connection}")
    #         return None

    # def execute(self, query):
    #     with contextlib.closing(self.engine.connect()) as connection:
    #         try:
    #             connection.execute(query)
    #             return True
    #         except Exception as e:
    #             self.log.error(utils.get_exception(e))
    #     return False
    #
    # def select(self, query):
    #     final_data = None
    #     if self.engine is not None:
    #         with contextlib.closing(self.engine.connect()) as connection:
    #             try:
    #                 if query is not None:
    #                     final_data = {}
    #                     rows = connection.execute(query)
    #                     column_names = list(map(lambda x: x[0],
    #                                             rows.cursor.description)
    #                                         )
    #                     for line_number, data in enumerate(rows):
    #                         final_data[line_number] = {}
    #                         for column_number, value in enumerate(data):
    #                             final_data[line_number][
    #                                 column_names[column_number]
    #                             ] = value
    #                     if len(final_data) == 0:
    #                         final_data = None
    #             except Exception as e:
    #                 self.log.warning(f"[{utils.get_exception(e)}]")
    #                 final_data = None
    #     return final_data
