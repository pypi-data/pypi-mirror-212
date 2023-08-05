import os
from typing import Any
from uuid import uuid4

from pydantic import BaseModel

from airfold.log import log


def uuid() -> str:
    return "af" + uuid4().hex


def format_quote(s: str) -> str:
    return " ".join(s.split()).strip().replace("'", '"')


def config_from_env(prefix: str) -> dict[str, str]:
    return {k.lower().replace(f"{prefix.lower()}_", ""): v for k, v in os.environ.items() if k.startswith(prefix)}


def model_hierarchy(model) -> dict[str, Any]:
    def _model_hierarchy(model: BaseModel) -> dict[str, Any]:
        fields: dict[str, Any] = {}
        for field in model.__fields__.values():
            if issubclass(field.type_, BaseModel):
                fields[field.name] = _model_hierarchy(field.type_)
            else:
                fields[field.name] = field.type_
        return fields

    return _model_hierarchy(model)


def dict_from_env(schema: dict, prefix: str = "AIRFOLD") -> dict:
    _prefix: str = f"{prefix}_" if prefix else ""

    def _dict_from_env(schema: dict, prefix: str = "") -> dict:
        result: dict = {}
        for key, value in schema.items():
            if isinstance(value, dict):
                result[key] = _dict_from_env(value, prefix + key + "_")
            else:
                env_key: str = f"{prefix}{key}".upper()
                if env_key in os.environ:
                    result[key] = os.environ[env_key]
                if value == dict:
                    result[key] = config_from_env(env_key)
        return result

    return _dict_from_env(schema, _prefix)


def model_from_env(model) -> Any:
    schema: dict = model_hierarchy(model)
    data: dict = dict_from_env(schema)

    try:
        return model(**data)
    except Exception:
        log.warning(f"Failed to load model {model} from env vars")
        return None


class ICase(object):
    def __init__(self, s: Any):
        # use `s.lower()` if exists, or return `s` itself
        self.__s = getattr(s, "lower", lambda: s)()

    def __hash__(self):
        return hash(self.__s)

    def __eq__(self, other: Any):
        other = getattr(other, "__s", lambda: getattr(other, "lower", lambda: other)())()
        return self.__s == other


def matches_schema(table: list[tuple[int, str, str, int, Any, int]], schema: list[tuple[int, str, str, int, Any, int]]):
    if len(table) != len(schema):
        return False
    return all([all([ICase(c[0]) == ICase(c[1]) for c in zip(i[0], i[1])]) for i in zip(schema, table)])


class classproperty(property):
    def __get__(self, obj, t):
        return self.fget(obj)
