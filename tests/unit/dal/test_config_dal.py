# -*- coding: utf-8 -*-
from src.database.dal.config_dal import ConfigDal
from src.database.models.config_model import Config


class TestConfigDal:
    @classmethod
    def setup_class(cls):
        """ setup_class """
        pass

    @classmethod
    def teardown_class(cls):
        """ teardown_class """
        pass

    def test_config_dal(self, db_session, fake_config_data):
        Config.__table__.create(db_session.bind)
        db_session.add(Config(**fake_config_data))
        config_dal = ConfigDal(db_session, None)
        config_id = fake_config_data["id"]
        results = config_dal.get_configs(config_id)
        assert len(results) == 1

        # test_get_config
        config_dal = ConfigDal(db_session, None)
        config_id = fake_config_data["id"]
        results = config_dal.get_configs(config_id)
        assert len(results) == 1

        # test_update_dark_theme
        config_dal = ConfigDal(db_session, None)
        config_id = fake_config_data["id"]
        status = (True, False)
        for st in status:
            config_dal.update_dark_theme(st, config_id)
            results = config_dal.get_configs(config_id)
            assert results[0].use_dark_theme is st

        # test_update_check_program_updates
        config_dal = ConfigDal(db_session, None)
        config_id = fake_config_data["id"]
        status = (True, False)
        for st in status:
            config_dal.update_check_program_updates(st, config_id)
            results = config_dal.get_configs(config_id)
            assert results[0].check_program_updates is st

        # test_update_show_info_messages
        config_dal = ConfigDal(db_session, None)
        config_id = fake_config_data["id"]
        status = (True, False)
        for st in status:
            config_dal.update_show_info_messages(st, config_id)
            results = config_dal.get_configs(config_id)
            assert results[0].show_info_messages is st

        # test_update_check_reshade_updates
        config_dal = ConfigDal(db_session, None)
        config_id = fake_config_data["id"]
        status = (True, False)
        for st in status:
            config_dal.update_check_reshade_updates(st, config_id)
            results = config_dal.get_configs(config_id)
            assert results[0].check_reshade_updates is st

        # test_update_create_screenshots_folder
        config_dal = ConfigDal(db_session, None)
        config_id = fake_config_data["id"]
        status = (True, False)
        for st in status:
            config_dal.update_create_screenshots_folder(st, config_id)
            results = config_dal.get_configs(config_id)
            assert results[0].create_screenshots_folder is st

        # test_update_reshade_version
        config_dal = ConfigDal(db_session, None)
        config_id = fake_config_data["id"]
        new_version = "99.99.99"
        config_dal.update_reshade_version(new_version, config_id)
        results = config_dal.get_configs(config_id)
        assert results[0].reshade_version == new_version

        # test_update_program_version
        config_dal = ConfigDal(db_session, None)
        config_id = fake_config_data["id"]
        new_version = "99.99.99"
        config_dal.update_program_version(new_version, config_id)
        results = config_dal.get_configs(config_id)
        assert results[0].program_version == new_version
