# -*- coding: utf-8 -*-
class DBBaseException(Exception):
    def __init__(self, log, msg):
        log.error(msg)


class DBExecuteException(DBBaseException):
    pass


class DBFetchAllException(DBBaseException):
    pass


class DBFetchValueException(DBBaseException):
    pass
