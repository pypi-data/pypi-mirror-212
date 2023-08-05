import os

import yaml

from airfold.config import Profile, parse_profiles, profile_from_env
from airfold.log import log
from airfold.runtime.type import RUNTIME
from airfold.storage.type import STORAGE


def test_profiles() -> None:
    raw_profiles: str = """
    local:
        runtime:
            type: clickhouse
            settings:
                host: localhost
                interface: http
                port: 8123
                username: admin
                password: admin
                settings:
                    max_memory_usage: 2048

        storage:
            type: sqlite
            settings:
                database: state.db

    prod:
        runtime:
            type: clickhouse
            settings:
                host: localhost
                interface: http
                port: 8123
                username: admin
                password: admin
                settings:
                    max_memory_usage: 2048

        storage:
            type: clickhouse
            settings:
                host: prod.ch.company.com
                interface: https
                port: 8443
                username: admin
                password: admin
                settings:
                    max_memory_usage: 2048
    """

    _profiles: dict = yaml.safe_load(raw_profiles)

    log.info(f"Loaded raw profiles: {_profiles}")

    profiles: list[tuple[str, Profile]] = list(parse_profiles(_profiles).items())

    log.info(f"Parsed profiles: {profiles}")

    assert len(profiles) == 2
    assert profiles[0][0] == "local"
    assert profiles[0][1].runtime.type == "clickhouse"
    assert profiles[0][1].runtime.settings == {
        "host": "localhost",
        "interface": "http",
        "port": 8123,
        "username": "admin",
        "password": "admin",
        "settings": {"max_memory_usage": 2048},
    }
    assert profiles[0][1].storage.type == "sqlite"
    assert profiles[0][1].storage.settings == {"database": "state.db"}

    assert profiles[1][0] == "prod"
    assert profiles[1][1].runtime.type == "clickhouse"
    assert profiles[1][1].runtime.settings == {
        "host": "localhost",
        "interface": "http",
        "port": 8123,
        "username": "admin",
        "password": "admin",
        "settings": {"max_memory_usage": 2048},
    }
    assert profiles[1][1].storage.type == "clickhouse"
    assert profiles[1][1].storage.settings == {
        "host": "prod.ch.company.com",
        "interface": "https",
        "port": 8443,
        "username": "admin",
        "password": "admin",
        "settings": {"max_memory_usage": 2048},
    }


def test_storage_runtime(wait_for_clickhouse) -> None:
    _profiles = """
    local:
        runtime:
            type: clickhouse
            settings:
                host: localhost

        storage:
            type: sqlite
            settings:
                database: test.db
    """

    profiles: dict[str, Profile] = parse_profiles(yaml.safe_load(_profiles))

    assert len(profiles) > 0

    profile: Profile = list(profiles.values())[0]

    storage = STORAGE[profile.storage.type](**profile.storage.settings)
    runtime = RUNTIME[profile.runtime.type](**profile.runtime.settings)

    if os.path.exists(profile.storage.settings["database"]):
        os.remove(profile.storage.settings["database"])

    assert storage
    assert runtime


def test_profile_from_env(wait_for_clickhouse, monkeypatch) -> None:
    monkeypatch.setenv("AIRFOLD_RUNTIME_TYPE", "clickhouse")
    monkeypatch.setenv("AIRFOLD_RUNTIME_SETTINGS_HOST", "localhost")
    monkeypatch.setenv("AIRFOLD_RUNTIME_SETTINGS_DATABASE", "default")
    monkeypatch.setenv("AIRFOLD_STORAGE_TYPE", "sqlite")
    monkeypatch.setenv("AIRFOLD_STORAGE_SETTINGS_DATABASE", "test.db")

    profile: Profile | None = profile_from_env()

    log.info(profile)

    assert profile

    runtime = RUNTIME[profile.runtime.type](**profile.runtime.settings)
    storage = STORAGE[profile.storage.type](**profile.storage.settings)

    if os.path.exists(profile.storage.settings["database"]):
        os.remove(profile.storage.settings["database"])

    assert storage
    assert runtime
