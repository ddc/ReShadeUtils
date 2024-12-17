# -*- coding: utf-8 -*-
from src.database.dal.games_dal import GamesDal
from src.database.models.games_model import Games
from tests.data.base_data import get_fake_game_data


class TestGamesDal:
    @classmethod
    def setup_class(cls):
        """setup_class"""
        pass

    @classmethod
    def teardown_class(cls):
        """teardown_class"""
        pass

    def test_games_dal(self, db_session, fake_game_data):
        Games.__table__.create(db_session.bind)
        db_session.add(Games(**fake_game_data))
        games_dal = GamesDal(db_session, None)
        game_id = fake_game_data["id"]
        result = games_dal.get_game_by_id(game_id)
        assert result is not None

        # test get_all_games
        results = games_dal.get_all_games()
        assert len(results) == 1

        # test_get_game_by_path
        results = games_dal.get_game_by_path(fake_game_data["path"])
        assert results is not None
        assert results.path == fake_game_data["path"]

        # test_get_game_by_path
        games_dal = GamesDal(db_session, None)
        results = games_dal.get_game_by_path(fake_game_data["path"])
        assert results is not None
        assert results.path == fake_game_data["path"]

        # test_get_game_by_name
        games_dal = GamesDal(db_session, None)
        results = games_dal.get_game_by_name(fake_game_data["name"])
        assert results is not None
        assert results.name == fake_game_data["name"]

        # test_update_game
        games_dal = GamesDal(db_session, None)
        game_id = fake_game_data["id"]
        fake_update_data = get_fake_game_data()
        fake_update_data["id"] = fake_game_data["id"]
        games_dal.update_game(fake_update_data)
        results = games_dal.get_game_by_id(game_id)
        assert results is not None
        assert results.name == fake_update_data["name"]
        assert results.api == fake_update_data["api"]
        assert results.dll == fake_update_data["dll"]

        # test_update_game_path
        games_dal = GamesDal(db_session, None)
        game_id = fake_game_data["id"]
        new_path = "/tmp/new_path"
        games_dal.update_game_path(game_id, new_path)
        results = games_dal.get_game_by_path(new_path)
        assert results is not None
        assert results.path == new_path

        # test_update_game_architecture
        games_dal = GamesDal(db_session, None)
        game_id = fake_game_data["id"]
        new_architecture = "64bits"
        games_dal.update_game_architecture(game_id, new_architecture)
        results = games_dal.get_game_by_id(game_id)
        assert results is not None
        assert results.architecture == new_architecture

        # test_update_game_api
        games_dal = GamesDal(db_session, None)
        game_id = fake_game_data["id"]
        new_api = "OpenGL"
        games_dal.update_game_api(game_id, new_api)
        results = games_dal.get_game_by_id(game_id)
        assert results is not None
        assert results.api == new_api

        # test_delete_game
        games_dal = GamesDal(db_session, None)
        game_id = fake_game_data["id"]
        games_dal.delete_game(game_id)
        results = games_dal.get_game_by_id(game_id)
        assert results is None
