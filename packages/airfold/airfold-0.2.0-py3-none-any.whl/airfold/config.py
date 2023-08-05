import os
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

from airfold.log import log
from airfold.utils import model_from_env


class Runtime(BaseModel):
    type: str
    settings: dict = Field(default_factory=dict)


class Storage(BaseModel):
    type: str
    settings: dict = Field(default_factory=dict)


class Profile(BaseModel):
    runtime: Runtime
    storage: Storage


def find_configs() -> Path | None:
    log.info("Searching for config file")
    path: Path = Path.cwd()
    while True:
        config_path: Path = path / ".airfold"
        if config_path.exists():
            log.info(f"Found config file: {config_path}")
            return config_path
        if path == Path.home():
            log.info("Config file not found")
            return None
        path = path.parent


def parse_profiles(data: dict) -> dict[str, Profile]:
    return {name: Profile(**profile) for name, profile in data.items()}


def profiles_from_path(path: Path) -> dict[str, Profile]:
    log.info("Loading profiles")
    profiles_path: Path = path / "profiles.yaml"
    if not profiles_path.exists() or not profiles_path.is_file() or not path.is_dir():
        log.info("No profiles found")
        return {}

    _profiles: dict = yaml.safe_load(open(profiles_path))

    return parse_profiles(_profiles)


def profile_from_env() -> Profile | None:
    log.warning("Loading profile from env does not support nested settings!")
    return model_from_env(Profile)


def load_profile(profile: str = "") -> Profile:
    log.info("Loading profiles")
    prof: Profile | None = profile_from_env()
    log.info(f"Profile from env: {prof}")

    if not prof:
        log.info("No profile from env, loading from config")
        configs: Path | None = find_configs()
        if not configs:
            raise ValueError("No config dir found")

        profiles: dict[str, Profile] = profiles_from_path(configs)
        log.info(f"Profiles: {profiles}")

        if not profiles:
            raise ValueError("No profiles found")

        profile = profile or os.getenv("AIRFOLD_PROFILE", list(profiles.keys())[0])
        prof = profiles[profile]

        log.info(f"Using profile: {profile}")
        log.info(f"Profile: {profiles[profile]}")
    return prof
