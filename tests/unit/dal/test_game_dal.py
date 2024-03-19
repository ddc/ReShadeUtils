# -*- coding: utf-8 -*-
import pytest
import sqlalchemy as sa
from src.database.dal.games_dal import GamesDal
from src.database.models.games_model import Games
from tests.data.base_data import get_fake_game_data, database_engine


@pytest.fixture
def fake_data(db_session):
    # init
    fdata = get_fake_game_data()
    yield fdata
    # teardown
    db_session.execute(sa.delete(Games))


class TestGamesDal:
    @classmethod
    def setup_class(cls):
        Games.__table__.create(database_engine)

    @classmethod
    def teardown_class(cls):
        Games.__table__.drop(database_engine)

    @pytest.fixture(autouse=True)
    def test_insert_game(self, db_session, fake_data):
        games_dal = GamesDal(db_session, None)
        game_id = fake_data["id"]
        db_session.add(Games(**fake_data))
        results = games_dal.get_game_by_id(game_id)
        assert results is not None

    def test_get_all_games(self, db_session, fake_data):
        games_dal = GamesDal(db_session, None)
        db_session.add(Games(**get_fake_game_data()))
        db_session.add(Games(**get_fake_game_data()))
        results = games_dal.get_all_games()
        assert len(results) == 3

    def test_get_game_by_path(self, db_session, fake_data):
        games_dal = GamesDal(db_session, None)
        results = games_dal.get_game_by_path(fake_data["path"])
        assert results is not None
        assert results.path == fake_data["path"]

    def test_get_game_by_name(self, db_session, fake_data):
        games_dal = GamesDal(db_session, None)
        results = games_dal.get_game_by_name(fake_data["name"])
        assert results is not None
        assert results.name == fake_data["name"]

    def test_update_game(self, db_session, fake_data):
        games_dal = GamesDal(db_session, None)
        game_id = fake_data["id"]
        fake_update_data = get_fake_game_data()
        fake_update_data["id"] = fake_data["id"]
        games_dal.update_game(fake_update_data)
        results = games_dal.get_game_by_id(game_id)
        assert results is not None
        assert results.name == fake_update_data["name"]
        assert results.api == fake_update_data["api"]
        assert results.dll == fake_update_data["dll"]

    def test_update_game_path(self, db_session, fake_data):
        games_dal = GamesDal(db_session, None)
        game_id = fake_data["id"]
        new_path = "/tmp/new_path"
        games_dal.update_game_path(game_id, new_path)
        results = games_dal.get_game_by_path(new_path)
        assert results is not None
        assert results.path == new_path

    def test_update_game_architecture(self, db_session, fake_data):
        games_dal = GamesDal(db_session, None)
        game_id = fake_data["id"]
        new_architecture = "64bits"
        games_dal.update_game_architecture(game_id, new_architecture)
        results = games_dal.get_game_by_id(game_id)
        assert results is not None
        assert results.architecture == new_architecture

    def test_update_game_api(self, db_session, fake_data):
        games_dal = GamesDal(db_session, None)
        game_id = fake_data["id"]
        new_api = "OpenGL"
        games_dal.update_game_api(game_id, new_api)
        results = games_dal.get_game_by_id(game_id)
        assert results is not None
        assert results.api == new_api

    def test_delete_game(self, db_session, fake_data):
        games_dal = GamesDal(db_session, None)
        game_id = fake_data["id"]
        games_dal.delete_game(game_id)
        results = games_dal.get_game_by_id(game_id)
        assert results is None
