# -*- coding: utf-8 -*-
from unittest.mock import patch
from src.tools import program_utils
from tests.data.base_data import Object


class TestProgramUtils:
    @patch("src.database.dal.config_dal.ConfigDal.get_configs")
    @patch("src.tools.program_utils.get_program_remote_version")
    def test_check_program_updates(self, program_remote_version_mock, get_configs_mocks, db_session, qpushbutton, qlabel, log):
        obj = Object()
        obj.qtobj = Object()
        obj.qtobj.update_button = qpushbutton
        obj.qtobj.update_avail_label = qlabel

        local_version = "src.constants.variables.VERSION"

        # check no new version available
        with patch(local_version, (1, 0, 0)):
            remote_version = (1, 0, 0)
            program_remote_version_mock.return_value = remote_version
            get_configs_mocks.return_value = ({"check_program_updates": True},)
            result = program_utils.check_program_updates(log, db_session)
            assert result is None

        # check for updates is disabled
        with patch(local_version, (1, 0, 0)):
            remote_version = (2, 1, 0)
            program_remote_version_mock.return_value = remote_version
            get_configs_mocks.return_value = ({"check_program_updates": False},)
            result = program_utils.check_program_updates(log, db_session)
            assert result is None

        # check new version available
        with patch(local_version, (1, 0, 0)):
            remote_version = (2, 1, 0)
            program_remote_version_mock.return_value = remote_version
            get_configs_mocks.return_value = ({"check_program_updates": True},)
            result = program_utils.check_program_updates(log, db_session)
            assert result == ".".join(str(x) for x in remote_version)
