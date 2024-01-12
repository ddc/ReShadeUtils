# -*- coding: utf-8 -*-
from src.database.db_exceptions import (
    DBAddException,
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
        except Exception as e:
            self.session.rollback()
            raise DBAddException(self.log, e)
        else:
            self.session.commit()

    def execute(self, stmt):
        try:
            self.session.execute(stmt)
        except Exception as e:
            self.session.rollback()
            raise DBExecuteException(self.log, e)
        else:
            self.session.commit()

    def fetchall(self, stmt):
        cursor = None
        try:
            cursor = self.session.execute(stmt)
        except Exception as e:
            self.session.rollback()
            raise DBFetchAllException(self.log, e)
        else:
            self.session.commit()
            return cursor.mappings().all()
        finally:
            cursor.close() if cursor is not None else None

    def fetchone(self, stmt):
        cursor = None
        try:
            cursor = self.session.execute(stmt)
        except Exception as e:
            self.session.rollback()
            raise DBFetchAllException(self.log, e)
        else:
            self.session.commit()
            return cursor.mappings().first()
        finally:
            cursor.close() if cursor is not None else None

    def fetch_value(self, stmt):
        cursor = None
        try:
            cursor = self.session.execute(stmt)
        except Exception as e:
            self.session.rollback()
            raise DBFetchValueException(self.log, e)
        else:
            self.session.commit()
            return cursor.first()[0]
        finally:
            cursor.close() if cursor is not None else None
