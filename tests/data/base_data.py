# -*- coding: utf-8 -*-
import random
import tempfile
from datetime import datetime
from ddcUtils.databases import DBSqlite
from faker import Faker
from src.constants.variables import ALL_APIS, ALL_ARCHITECTURES


database_engine = DBSqlite(":memory:").engine()


class Object:
    def __init__(self):
        self._created = datetime.now().isoformat()


def get_randoms():
    Faker.seed(0)
    _faker = Faker(locale="en_US")
    _random = random.SystemRandom()
    _now_mock = _faker.date_time_ad()
    return _faker, _random, _now_mock


def get_fake_config_data():
    _faker, _random, _now_mock = get_randoms()
    return {
        "id": _random.randint(1000000, 9999999),
        "program_version": "1.0",
        "reshade_version": "1.2.3",
        "use_dark_theme": False,
        "check_program_updates": True,
        "show_info_messages": True,
        "check_reshade_updates": True,
        "create_screenshots_folder": True,
        "updated_at": _now_mock,
        "created_at": _now_mock,
    }


def get_fake_game_data():
    _faker, _random, _now_mock = get_randoms()
    return {
        "id": _random.randint(1000000, 9999999),
        "name": _faker.pystr(),
        "architecture": _random.choice(ALL_ARCHITECTURES),
        "api": _random.choice(ALL_APIS),
        "path": tempfile.gettempdir(),
        "updated_at": _now_mock,
        "created_at": _now_mock,
    }
