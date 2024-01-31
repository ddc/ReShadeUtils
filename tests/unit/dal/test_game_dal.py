# -*- coding: utf-8 -*-
import pytest
import sqlalchemy as sa
from sqlalchemy.orm import Session
from src.database.dal.games_dal import GamesDal
from src.database.models.games_model import Games
from tests.data import base_data


database_engine = base_data.get_database_engine()


@pytest.fixture(name="db_session")
def get_db_session():
    with Session(database_engine) as session:
        yield session


@pytest.fixture
def fake_data(db_session):
    # init
    fdata = base_data.get_fake_game_data()
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
        assert len(results) == 1

    def test_get_all_games(self, db_session, fake_data):
        games_dal = GamesDal(db_session, None)
        second_fdata = base_data.get_fake_game_data()
        db_session.add(Games(**second_fdata))
        results = games_dal.get_all_games()
        assert len(results) == 2

    def test_get_game_by_path(self, db_session, fake_data):
        games_dal = GamesDal(db_session, None)
        results = games_dal.get_game_by_path(fake_data["path"])
        assert len(results) == 1
        assert results[0].path == fake_data["path"]

    def test_get_game_by_name(self, db_session, fake_data):
        games_dal = GamesDal(db_session, None)
        results = games_dal.get_game_by_name(fake_data["name"])
        assert len(results) == 1
        assert results[0].name == fake_data["name"]

    def test_update_game(self, db_session, fake_data):
        games_dal = GamesDal(db_session, None)
        game_id = fake_data["id"]
        fdata = {
            "id": game_id,
            "name": "new name",
            "architecture": "new architecture",
            "api": "new api"
        }
        games_dal.update_game(fdata)
        results = games_dal.get_game_by_id(game_id)
        assert results[0].name == fdata["name"]
        assert results[0].architecture == fdata["architecture"]
        assert results[0].api == fdata["api"]

    def test_update_game_path(self, db_session, fake_data):
        games_dal = GamesDal(db_session, None)
        game_id = fake_data["id"]
        new_path = "/tmp/new_path"
        games_dal.update_game_path(game_id, new_path)
        results = games_dal.get_game_by_path(new_path)
        assert len(results) == 1
        assert results[0].path == new_path

    def test_update_game_architecture(self, db_session, fake_data):
        games_dal = GamesDal(db_session, None)
        game_id = fake_data["id"]
        new_architecture = "128bits"
        games_dal.update_game_architecture(game_id, new_architecture)
        results = games_dal.get_game_by_id(game_id)
        assert len(results) == 1
        assert results[0].architecture == new_architecture

    def test_update_game_api(self, db_session, fake_data):
        games_dal = GamesDal(db_session, None)
        game_id = fake_data["id"]
        new_api = "Vulkan"
        games_dal.update_game_api(game_id, new_api)
        results = games_dal.get_game_by_id(game_id)
        assert len(results) == 1
        assert results[0].api == new_api

    def test_delete_game(self, db_session, fake_data):
        games_dal = GamesDal(db_session, None)
        game_id = fake_data["id"]
        games_dal.delete_game(game_id)
        results = games_dal.get_game_by_id(game_id)
        assert len(results) == 0
