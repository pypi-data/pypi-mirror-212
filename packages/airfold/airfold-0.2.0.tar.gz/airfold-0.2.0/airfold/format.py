AIRFOLD_CORE = "core.airfold.co"
DEFAULT_VERSION = f"{AIRFOLD_CORE}/v1"

SUPPORTED_TYPES = ["Pipe", "TableSource", "KafkaSource"]
SUPPORTED_VERSIONS = [f"{AIRFOLD_CORE}/v1"]

SOURCE_TYPES = ["TableSource", "KafkaSource"]


class FormatError(Exception):
    pass


def normalize_version(data: dict) -> str:
    ver: str | None = data.get("version")
    if ver is None or ver == "":
        ver = DEFAULT_VERSION
    assert ver
    res = ver.split("/", 1)
    if len(res) == 1:
        res.insert(0, AIRFOLD_CORE)
    elif len(res) > 2:
        raise FormatError(f"Error parsing version: {ver}")
    norm_ver = "/".join(res)
    if norm_ver not in SUPPORTED_VERSIONS:
        raise FormatError(f"Unknown or not supported version: {norm_ver}")
    return norm_ver


def normalize_type(data: dict) -> str:
    data_type: str | None = data.get("type")
    if data_type is None or data_type == "":
        if "topic" in data:
            data_type = "KafkaSource"
        elif "cols" in data or "sql" in data:
            data_type = "TableSource"
        elif "nodes" in data:
            data_type = "Pipe"
        else:
            raise FormatError("Type is not set, and failed to guess it")
    assert data_type
    if data_type not in SUPPORTED_TYPES:
        raise FormatError(f"Unknown or not supported type definition: {data_type}")
    return data_type


def normalize_format(data: dict) -> dict:
    data["version"] = normalize_version(data)
    data["type"] = normalize_type(data)
    return data


def is_source(data: dict) -> bool:
    return data["type"] in SOURCE_TYPES
