# -*- coding: utf-8 -*-
from unittest.mock import patch
from src.tools import program_utils
from tests.data.base_data import qtbutton, qtlabel, Object


class TestProgramUtils:
    @patch("src.tools.program_utils.get_program_remote_version")
    def test_check_program_updates(self, program_remote_version_mock, qtbutton, qtlabel):
        obj = Object()
        obj.qtobj = Object()
        obj.qtobj.update_button = qtbutton
        obj.qtobj.updateAvail_label = qtlabel

        version_file = "src.constants.variables.VERSION"

        # check no new version available
        with patch(version_file, (1, 0, 0)):
            program_remote_version_mock.return_value = (1, 0, 0)
            obj.check_program_updates = True
            result = program_utils.check_program_updates(obj)
            assert result is False

        # check new version available
        with patch(version_file, (1, 0, 0)):
            program_remote_version_mock.return_value = (2, 1, 0)
            obj.check_program_updates = True
            result = program_utils.check_program_updates(obj)
            assert result is True

        # check for updates is disabled
        with patch(version_file, (1, 0, 0)):
            program_remote_version_mock.return_value = (2, 1, 0)
            obj.check_program_updates = False
            result = program_utils.check_program_updates(obj)
            assert result is None
