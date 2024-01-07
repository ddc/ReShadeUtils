# -*- coding: utf-8 -*-
import pytest
from sqlalchemy.orm import Session
from src.database.db import Database

database = Database(None, ":memory:")
database_engine = database.get_db_engine()


@pytest.fixture(scope="session")
def db_session_fixture():
    with Session(database_engine) as session:
        yield session
