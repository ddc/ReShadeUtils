# -*- coding: utf-8 -*-
import os
from tempfile import TemporaryDirectory
from unittest.mock import patch
import pytest
from ddcUtils import FileUtils
from src.tools import program_utils


class TestProgramUtils:
    @classmethod
    def setup_class(cls):
        """setup_class"""
        pass

    @classmethod
    def teardown_class(cls):
        """teardown_class"""
        pass

    #@pytest.mark.skip("skiping due to rate limit")
    def test_download_alembic_dir(self, log):
        local_dir_path = "src.constants.variables.ALEMBIC_MIGRATIONS_DIR"
        with patch(local_dir_path, "./alembic_dir") as mock_alembic_dir:
            result = program_utils.download_alembic_dir(log)
            assert result is True
            assert os.path.isdir(mock_alembic_dir) == True
            FileUtils.remove(mock_alembic_dir)
            assert os.path.exists(mock_alembic_dir) == False

    @patch("src.database.dal.config_dal.ConfigDal.get_configs")
    def test_show_info_messages(self, rs_config, db_session, log):
        rs_config.return_value = [{"show_info_messages": True}]
        result = program_utils.show_info_messages(db_session, log)
        assert result is True

        rs_config.return_value = [{"show_info_messages": False}]
        result = program_utils.show_info_messages(db_session, log)
        assert result is False

    @patch("src.database.dal.config_dal.ConfigDal.get_configs")
    @patch("src.tools.program_utils.get_program_remote_version")
    def test_check_program_updates(self, program_remote_version_mock, get_configs_mocks, db_session, log):
        local_version = "src.constants.variables.VERSION"

        # check no new version available
        with patch(local_version, (1, 0, 0)):
            remote_version = (1, 0, 0)
            program_remote_version_mock.return_value = remote_version
            get_configs_mocks.return_value = ({"check_program_updates": True},)
            result = program_utils.check_program_updates(log, db_session)
            assert result is None

        # check new version available
        with patch(local_version, (1, 0, 0)):
            remote_version = (2, 1, 0)
            program_remote_version_mock.return_value = remote_version
            get_configs_mocks.return_value = ({"check_program_updates": True},)
            result = program_utils.check_program_updates(log, db_session)
            assert result == ".".join(str(x) for x in remote_version)

        # check if update is disabled
        with patch(local_version, (1, 0, 0)):
            remote_version = (2, 1, 0)
            program_remote_version_mock.return_value = remote_version
            get_configs_mocks.return_value = ({"check_program_updates": False},)
            result = program_utils.check_program_updates(log, db_session)
            assert result is None

    def test_get_program_remote_version(self, log):
        result = program_utils.get_program_remote_version(log)
        assert isinstance(result, tuple) is True

    @patch("src.tools.program_utils.show_info_messages")
    def test_download_new_program_version(self, show_info_messages, db_session, log):
        with TemporaryDirectory() as tmp_dir:
            show_info_messages.return_value = False
            local_path = os.path.join(tmp_dir, "ReshadeTest.exe")
            new_version = "5.0.1"
            result = program_utils.download_new_program_version(log, db_session, local_path, new_version)
            assert result is True
            assert os.path.isfile(local_path) == True
            FileUtils.remove(local_path)
            assert os.path.exists(local_path) == False

    @patch("ddcUtils.ConfFileUtils.get_value")
    @patch("src.database.dal.config_dal.ConfigDal.get_configs")
    def test_get_screenshot_path(self, rs_config, reshade_config_screenshot_path, db_session, log):
        with TemporaryDirectory() as tmp_dir:
            reshade_screenshot_dir = "src.constants.variables.RESHADE_SCREENSHOT_DIR"
            game_dir = os.path.join(tmp_dir, "test_game_dir")
            game_name = "test_game_name"
            with patch(reshade_screenshot_dir, os.path.join(tmp_dir, "screenshots")) as mock_screenshot_dir:
                # test create dir
                rs_config.return_value = [{"create_screenshots_folder": True}]
                result = program_utils.get_screenshot_path(log, db_session, game_dir, game_name)
                assert result == f"{mock_screenshot_dir}/{game_name}"

                # test existing dir
                rs_config.return_value = [{"create_screenshots_folder": False}]
                reshade_config_screenshot_path.return_value = None
                result = program_utils.get_screenshot_path(log, db_session, game_dir, game_name)
                assert result == f"{mock_screenshot_dir}/{game_name}"

                # delete dirs
                assert os.path.isdir(mock_screenshot_dir) == True
                FileUtils.remove(mock_screenshot_dir)
                assert os.path.exists(mock_screenshot_dir) == False
