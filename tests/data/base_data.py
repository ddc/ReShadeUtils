# -*- coding: utf-8 -*-
import os
import random
import tempfile
from datetime import datetime
from ddcDatabases import DBSqlite
from faker import Faker
from src.constants.variables import ALL_APIS, ALL_ARCHITECTURES, ALL_DLL_NAMES


database_engine = DBSqlite(":memory:").engine()


class Object:
    def __init__(self):
        self._created = datetime.now().isoformat()


def set_randoms():
    _faker = Faker(locale="en_US")
    return {
        "id": _faker.random_int(min=1, max=9999999),
        "name": _faker.uuid4(),
        "now": _faker.date_time_ad(),
    }


def get_fake_config_data():
    rand = set_randoms()
    return {
        "id": rand["id"],
        "program_version": "1.0",
        "reshade_version": "1.2.3",
        "use_dark_theme": False,
        "check_program_updates": True,
        "show_info_messages": True,
        "check_reshade_updates": True,
        "create_screenshots_folder": True,
        "updated_at": rand["now"],
        "created_at": rand["now"],
    }


def get_fake_game_data():
    _random = random.SystemRandom()
    rand = set_randoms()
    return {
        "id": rand["id"],
        "name": rand["name"],
        "architecture": _random.choice(ALL_ARCHITECTURES),
        "api": _random.choice(ALL_APIS),
        "dll": _random.choice(ALL_DLL_NAMES),
        "path": os.path.join(tempfile.gettempdir(), rand["name"]),
        "updated_at": rand["now"],
        "created_at": rand["now"],
    }
