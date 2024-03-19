# -*- coding: utf-8 -*-
from unittest.mock import patch
import pytest
import sqlalchemy as sa
from src.database.dal.games_dal import GamesDal
from src.database.models.config_model import Config
from src.database.models.games_model import Games
from src.tools import reshade_utils
from tests.data.base_data import database_engine, get_fake_game_data


@pytest.fixture
def fake_data(db_session):
    # init
    fdata = get_fake_game_data()
    yield fdata
    # teardown
    db_session.execute(sa.delete(Games))


class TestReshadeUtils:
    @classmethod
    def setup_class(cls):
        Config.__table__.create(database_engine)
        Games.__table__.create(database_engine)

    @classmethod
    def teardown_class(cls):
        Config.__table__.drop(database_engine)
        Games.__table__.drop(database_engine)

    @pytest.fixture(autouse=True)
    def insert_game(self, db_session, fake_data):
        games_dal = GamesDal(db_session, None)
        game_id = fake_data["id"]
        db_session.add(Games(**fake_data))
        results = games_dal.get_game_by_id(game_id)
        assert results is not None

    @pytest.skip(reason="github actions lack the support for PyQt6")
    @patch("src.database.dal.config_dal.ConfigDal.get_configs")
    @patch("src.tools.reshade_utils.unzip_reshade")
    @patch("src.tools.reshade_utils.download_reshade")
    @patch("src.tools.reshade_utils.get_remote_reshade_version")
    def test_check_and_download_new_reshade_version(self, remote_reshade_version_mock, download_reshade_mock, unzip_reshade_mock, get_configs_mocks, qtobj, fake_data, db_session, log):
        remote_reshade_version_mock.return_value = (9, 9, 999)
        download_reshade_mock.return_value = True
        unzip_reshade_mock.return_value = True
        get_configs_mocks.return_value = ({"check_program_updates": True, "show_info_messages": False},)

        db_reshade_version = (1, 0, 0)
        new_reshade_version = reshade_utils.check_and_download_new_reshade_version(db_session, log, qtobj, db_reshade_version)
        assert new_reshade_version == ".".join(str(x) for x in remote_reshade_version_mock.return_value)
