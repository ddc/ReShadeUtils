# -*- coding: utf-8 -*-
from src.database.db_exceptions import (
    DBExecuteException,
    DBFetchAllException,
    DBFetchValueException
)


class DBUtils:
    def __init__(self, session, log):
        self.session = session
        self.log = log

    def add(self, stmt):
        try:
            self.session.add(stmt)
            self.session.commit()
        except Exception as e:
            raise DBExecuteException(self.log, e)

    def execute(self, stmt):
        try:
            self.session.execute(stmt)
            self.session.commit()
        except Exception as e:
            raise DBExecuteException(self.log, e)

    def fetchall(self, stmt):
        try:
            cursor = self.session.execute(stmt)
            return cursor.mappings().all()
        except Exception as e:
            raise DBFetchAllException(self.log, e)

    def fetchone(self, stmt):
        try:
            cursor = self.session.execute(stmt)
            return cursor.mappings().first()
        except Exception as e:
            raise DBFetchAllException(self.log, e)

    def fetch_value(self, stmt):
        try:
            cursor = self.session.execute(stmt)
            return cursor.first()[0]
        except Exception as e:
            raise DBFetchValueException(self.log, e)
