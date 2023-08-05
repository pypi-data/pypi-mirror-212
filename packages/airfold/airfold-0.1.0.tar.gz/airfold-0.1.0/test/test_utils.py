from typing import Tuple, Any, List

from airfold.utils import matches_schema


def test_schema_match() -> None:
    schema: List[Tuple[int, str, str, int, Any, int]] = [
        (0, "id", "text", 1, None, 1),
        (1, "name", "text", 0, None, 0),
        (2, "sql", "text", 0, None, 0),
    ]

    table: List[Tuple[int, str, str, int, Any, int]] = [
        (0, "id", "text", 1, None, 1),
        (1, "name", "text", 0, None, 0),
        (2, "sql", "text", 0, None, 0),
    ]
    assert matches_schema(table, schema)

    table = [
        (0, "id", "TEXT", 1, None, 1),
        (1, "name", "TEXT", 0, None, 0),
        (2, "sql", "TEXT", 0, None, 0),
    ]
    assert matches_schema(table, schema)

    table = [
        (0, "Id", "TEXT", 1, None, 1),
        (1, "Name", "TEXT", 0, None, 0),
        (2, "Sql", "TEXT", 0, None, 0),
    ]
    assert matches_schema(table, schema)

    table = []
    assert not matches_schema(table, schema)

    table = [
        (0, "id", "TEXT", 1, None, 1),
    ]
    assert not matches_schema(table, schema)

    table = [
        (0, "id", "TEXT", 1, None, 1),
        (1, "name", "TEXT", 0, None, 0),
        (2, "data", "TEXT", 0, None, 0),
    ]
    assert not matches_schema(table, schema)

    table = [
        (0, "id", "TEXT", 1, None, 0),
        (1, "name", "TEXT", 0, None, 0),
        (2, "sql", "TEXT", 0, None, 0),
    ]
    assert not matches_schema(table, schema)

    table = [
        (0, "id", "text", 1, None, 1),
        (1, "name", "text", 0, "default", 0),
        (2, "sql", "text", 0, None, 0),
    ]
    assert not matches_schema(table, schema)
