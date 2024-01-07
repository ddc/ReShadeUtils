# -*- coding: utf-8 -*-
from sqlalchemy import event
from src.constants import variables, messages
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session


class Database:
    def __init__(self, log, db_path=None):
        self.log = log
        self.file = db_path if db_path else variables.DATABASE_PATH
        self.batch_size = 100

    def get_db_engine(self):
        try:
            engine = create_engine(f"sqlite:///{self.file}", echo=True if variables.DEBUG else False).\
                execution_options(stream_results=True if variables.DEBUG else False,
                                  isolation_level="AUTOCOMMIT")

            @event.listens_for(engine, "before_cursor_execute")
            def receive_before_cursor_execute(conn,
                                              cursor,
                                              statement,
                                              params,
                                              context,
                                              executemany):
                cursor.arraysize = self.batch_size
            return engine
        except Exception as err:
            self.log.error(f"[{str(type(err))}]:[{str(err)}]:{messages.error_db_connection}")
            return None

    @staticmethod
    def get_db_session(engine):
        session = Session(bind=engine)
        return session
