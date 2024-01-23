# -*- coding: utf-8 -*-
import pytest
import sqlalchemy as sa
from sqlalchemy.orm import Session
from src.database.dal.config_dal import ConfigDal
from src.database.models.config_model import Config
from tests.data import base_data


database_engine = base_data.get_database_engine_fixture()


@pytest.fixture(scope="session")
def db_session_fixture():
    with Session(database_engine) as session:
        yield session


@pytest.fixture(name="db_session")
def get_db_session(db_session_fixture):
    return db_session_fixture


@pytest.fixture
def fake_data(db_session):
    # init
    fdata = base_data.get_fake_config_data()
    yield fdata
    # teardown
    db_session.execute(sa.delete(Config))


class TestConfigDal:
    @classmethod
    def setup_class(cls):
        Config.__table__.create(database_engine)

    @classmethod
    def teardown_class(cls):
        Config.__table__.drop(database_engine)

    @pytest.fixture(autouse=True)
    def test_insert_configs(self, db_session, fake_data):
        config_dal = ConfigDal(db_session, None)
        config_id = fake_data["id"]
        db_session.add(Config(**fake_data))
        results = config_dal.get_configs(config_id)
        assert len(results) == 1

    def test_get_config(self, db_session, fake_data):
        config_dal = ConfigDal(db_session, None)
        config_id = fake_data["id"]
        results = config_dal.get_configs(config_id)
        assert len(results) == 1

    def test_update_dark_theme(self, db_session, fake_data):
        config_dal = ConfigDal(db_session, None)
        config_id = fake_data["id"]
        status = (True, False,)
        for st in status:
            config_dal.update_dark_theme(st, config_id)
            results = config_dal.get_configs(config_id)
            assert results[0].use_dark_theme is st

    def test_update_shaders(self, db_session, fake_data):
        config_dal = ConfigDal(db_session, None)
        config_id = fake_data["id"]
        status = (True, False,)
        for st in status:
            config_dal.update_shaders(st, config_id)
            results = config_dal.get_configs(config_id)
            assert results[0].update_shaders is st

    def test_update_check_program_updates(self, db_session, fake_data):
        config_dal = ConfigDal(db_session, None)
        config_id = fake_data["id"]
        status = (True, False,)
        for st in status:
            config_dal.update_check_program_updates(st, config_id)
            results = config_dal.get_configs(config_id)
            assert results[0].check_program_updates is st

    def test_update_show_info_messages(self, db_session, fake_data):
        config_dal = ConfigDal(db_session, None)
        config_id = fake_data["id"]
        status = (True, False,)
        for st in status:
            config_dal.update_show_info_messages(st, config_id)
            results = config_dal.get_configs(config_id)
            assert results[0].show_info_messages is st

    def test_update_check_resahde_updates(self, db_session, fake_data):
        config_dal = ConfigDal(db_session, None)
        config_id = fake_data["id"]
        status = (True, False,)
        for st in status:
            config_dal.update_check_resahde_updates(st, config_id)
            results = config_dal.get_configs(config_id)
            assert results[0].check_reshade_updates is st

    def test_update_create_screenshots_folder(self, db_session, fake_data):
        config_dal = ConfigDal(db_session, None)
        config_id = fake_data["id"]
        status = (True, False,)
        for st in status:
            config_dal.update_create_screenshots_folder(st, config_id)
            results = config_dal.get_configs(config_id)
            assert results[0].create_screenshots_folder is st

    def test_update_reshade_version(self, db_session, fake_data):
        config_dal = ConfigDal(db_session, None)
        config_id = fake_data["id"]
        new_version = "99.99.99"
        config_dal.update_reshade_version(new_version, config_id)
        results = config_dal.get_configs(config_id)
        assert results[0].reshade_version == new_version

    def test_update_program_version(self, db_session, fake_data):
        config_dal = ConfigDal(db_session, None)
        config_id = fake_data["id"]
        new_version = "99.99.99"
        config_dal.update_program_version(new_version, config_id)
        results = config_dal.get_configs(config_id)
        assert results[0].program_version == new_version
