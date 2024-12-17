# -*- coding: utf-8 -*-
import os
from tempfile import TemporaryDirectory
from unittest.mock import patch
import pytest
from src.constants import variables
from src.database.dal.games_dal import GamesDal
from src.database.models.config_model import Config
from src.database.models.games_model import Games
from src.tools import reshade_utils


class TestReshadeUtils:
    @classmethod
    def setup_class(cls):
        """setup_class"""
        pass

    @classmethod
    def teardown_class(cls):
        """teardown_class"""
        pass

    def test_get_reshade_dll_log_names(self):
        result = reshade_utils.get_reshade_dll_log_names("OpenGL")
        assert result == ["opengl32.dll", "opengl32.log"]
        result = reshade_utils.get_reshade_dll_log_names("DirectX 9")
        assert result == ["d3d9.dll", "d3d9.log"]
        result = reshade_utils.get_reshade_dll_log_names("DirectX (10,11,12)")
        assert result == ["dxgi.dll", "dxgi.log"]

    def test_check_reshade_config_files(self, log):
        with TemporaryDirectory() as tmp_dir:
            result = reshade_utils.check_reshade_config_files(log=log, check_shaders=False, local_dir=tmp_dir)
            assert result is None

    def test_get_remote_reshade_version(self, log):
        result = reshade_utils.get_remote_reshade_version(log)
        assert isinstance(result, tuple) is True

    @pytest.mark.skip(reason="github actions lack the support for PyQt6")
    @patch("src.database.dal.config_dal.ConfigDal.get_configs")
    @patch("src.tools.reshade_utils.unzip_reshade")
    @patch("src.tools.reshade_utils.download_reshade")
    @patch("src.tools.reshade_utils.get_remote_reshade_version")
    def test_check_and_download_new_reshade_version(
        self,
        remote_reshade_version_mock,
        download_reshade_mock,
        unzip_reshade_mock,
        get_configs_mocks,
        qtobj,
        db_session,
        fake_game_data,
        log,
    ):
        Config.__table__.create(db_session.bind)
        Games.__table__.create(db_session.bind)
        games_dal = GamesDal(db_session, None)
        game_id = fake_game_data["id"]
        db_session.add(Games(**fake_game_data))
        results = games_dal.get_game_by_id(game_id)
        assert results is not None

        remote_reshade_version_mock.return_value = (9, 9, 999)
        download_reshade_mock.return_value = True
        unzip_reshade_mock.return_value = True
        get_configs_mocks.return_value = ({"check_program_updates": True, "show_info_messages": False},)
        db_reshade_version = (1, 0, 0)
        new_reshade_version = reshade_utils.check_and_download_new_reshade_version(
            db_session,
            log,
            qtobj,
            db_reshade_version,
        )
        assert new_reshade_version == ".".join(str(x) for x in remote_reshade_version_mock.return_value)

    def test_download_reshade(self, log):
        with TemporaryDirectory() as tmp_dir:
            remote_reshade_version = "6.0.0"
            local_reshade = f"ReShade_Setup_{remote_reshade_version}.exe"
            local_reshade_path = f"{tmp_dir}/{local_reshade}"
            assert os.path.exists(tmp_dir) is True
            result = reshade_utils.download_reshade(log, remote_reshade_version, tmp_dir)
            assert result is True
            assert os.path.exists(local_reshade_path) is True
            result = reshade_utils.check_game_path_exists(local_reshade_path)
            assert result is True

    def test_download_reshade_ini_file(self):
        with TemporaryDirectory() as tmp_dir:
            assert os.path.exists(tmp_dir) is True
            local_ini_file_path = os.path.join(tmp_dir, variables.RESHADE_INI)
            result = reshade_utils.download_reshade_ini_file(tmp_dir)
            assert result is True
            assert os.path.exists(local_ini_file_path) is True

            # test_apply_reshade_ini_file
            screenshot_path = os.path.join(tmp_dir, "screenshots")
            os.makedirs(screenshot_path, exist_ok=True)
            assert os.path.exists(screenshot_path) is True
            result = reshade_utils.apply_reshade_ini_file(tmp_dir, screenshot_path, local_ini_file_path)
            assert result is True

    def test_download_reshade_preset_file(self):
        with TemporaryDirectory() as tmp_dir:
            assert os.path.exists(tmp_dir) is True
            local_preset_file_path = os.path.join(tmp_dir, variables.RESHADE_PRESET_INI)
            result = reshade_utils.download_reshade_preset_file(tmp_dir)
            assert result is True
            assert os.path.exists(local_preset_file_path) is True

    def test_download_qss_file(self):
        with TemporaryDirectory() as tmp_dir:
            assert os.path.exists(tmp_dir) is True
            local_qss_file_path = os.path.join(tmp_dir, "style.qss")
            result = reshade_utils.download_qss_file(local_qss_file_path)
            assert result is True
            assert os.path.exists(local_qss_file_path) is True

    def test_download_about_html_file(self):
        with TemporaryDirectory() as tmp_dir:
            assert os.path.exists(tmp_dir) is True
            local_html_file_path = os.path.join(tmp_dir, "about.html")
            result = reshade_utils.download_about_html_file(local_html_file_path)
            assert result is True
            assert os.path.exists(local_html_file_path) is True
