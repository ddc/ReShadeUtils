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

    async def add(self, stmt):
        try:
            self.session.add(stmt)
            await self.session.commit()
        except Exception as e:
            self.log.error(e)
            raise DBExecuteException(self.log, e)

    async def execute(self, stmt):
        try:
            await self.session.execute(stmt)
            await self.session.commit()
        except Exception as e:
            self.log.error(e)
            raise DBExecuteException(self.log, e)

    async def fetchall(self, stmt):
        try:
            cursor = await self.session.execute(stmt)
            return cursor.mappings().all()
        except Exception as e:
            self.log.error(e)
            raise DBFetchAllException(self.log, e)

    async def fetchone(self, stmt):
        try:
            cursor = await self.session.execute(stmt)
            return cursor.mappings().first()
        except Exception as e:
            self.log.error(e)
            raise DBFetchAllException(self.log, e)

    async def fetch_value(self, stmt):
        try:
            cursor = await self.session.execute(stmt)
            return cursor.first()[0]
        except Exception as e:
            self.log.error(e)
            raise DBFetchValueException(self.log, e)
