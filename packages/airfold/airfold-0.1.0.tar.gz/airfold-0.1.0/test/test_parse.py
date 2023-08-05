import json

import yaml
from sqlglot import parse_one
from sqlglot.dialects import ClickHouse

from airfold.models import Node, Pipe
from airfold.parse import (
    parse,
    ParsingError,
    SQLParser,
)
from airfold.utils import uuid


def test_check_sequentiality(dialect) -> None:
    parser: SQLParser = SQLParser(dialect)
    nodes: list[Node] = [
        Node(name="node1", sql="SELECT * FROM source1"),
        Node(name="node2", sql="SELECT * FROM node1 WHERE x > 5"),
        Node(name="node3", sql="SELECT * FROM node2 WHERE y > 5"),
    ]

    parser.check_sequentiality(nodes)

    nodes = [
        Node(name="node1", sql="SELECT * FROM source1"),
        Node(name="node2", sql="SELECT * FROM node3 WHERE x > 5"),
        Node(name="node3", sql="SELECT * FROM node1 WHERE y > 5"),
    ]

    try:
        parser.check_sequentiality(nodes)
        raise Exception("Should have failed")
    except ParsingError:
        pass

    nodes = [
        Node(name="node1", sql="SELECT * FROM source1"),
        Node(name="node2", sql="SELECT * FROM node2 WHERE x > 5"),
    ]

    try:
        parser.check_sequentiality(nodes)
        raise Exception("Should have failed")
    except ParsingError:
        pass

    nodes = [
        Node(name="node1", sql="SELECT * FROM source1"),
        Node(name="node2", sql="SELECT * FROM node1 WHERE x > 5"),
        Node(name="node3", sql="SELECT * FROM node2 WHERE y > 5"),
        Node(name="node4", sql="SELECT * FROM node1 WHERE x <= 5", union="node3"),
    ]

    parser.check_sequentiality(nodes)

    nodes = [
        Node(name="node1", sql="SELECT * FROM source1"),
        Node(name="node2", sql="SELECT * FROM node1 WHERE x > 5"),
        Node(name="node3", sql="SELECT * FROM node1 WHERE x <= 5", union="node4"),
        Node(name="node4", sql="SELECT * FROM node2 WHERE y > 5"),
    ]

    try:
        parser.check_sequentiality(nodes)
        raise Exception("Should have failed")
    except ParsingError:
        pass


def test_replace_from(dialect) -> None:
    parser: SQLParser = SQLParser(dialect)
    sql: str = "SELECT * FROM source1"
    mapping: dict[str, str] = {"source1": "source2"}
    assert parser.replace(sql, mapping) == str(parse_one('SELECT * FROM "source2"', read=ClickHouse))

    sql = "SELECT * FROM source1 WHERE x > 5"
    mapping = {"source1": "source2"}
    assert parser.replace(sql, mapping) == str(parse_one('SELECT * FROM "source2" WHERE x > 5', read=ClickHouse))

    sql = "SELECT * FROM source1 WHERE x > 5"
    mapping = {"source1": "source2", "source3": "source4"}
    assert parser.replace(sql, mapping) == str(parse_one('SELECT * FROM "source2" WHERE x > 5', read=ClickHouse))

    sql = "SELECT * FROM source1 WHERE x > 5"
    mapping = {}
    assert parser.replace(sql, mapping) == str(parse_one("SELECT * FROM source1 WHERE x > 5", read=ClickHouse))


def test_parse(dialect) -> None:
    # TODO: test with lookup
    pipe_dict: dict = {
        "nodes": [
            {
                "node1": {
                    "description": "This is node 1",
                    "sql": "SELECT * FROM source1",
                }
            },
            {
                "node2": {
                    "sql": "SELECT * FROM node1 WHERE x > 5",
                }
            },
        ]
    }

    pipe_yaml: str = yaml.dump(pipe_dict)
    data = yaml.safe_load(pipe_yaml)

    assert data == pipe_dict

    pipe_json: str = json.dumps(pipe_dict)
    data = json.loads(pipe_json)

    assert data == pipe_dict

    pipe: Pipe = parse(data, "test_pipe")

    pipe_nodes = pipe_dict["nodes"]
    assert len(pipe.nodes) == len(pipe_nodes)
    assert pipe.nodes[0].name == list(pipe_nodes[0].keys())[0]
    assert pipe.nodes[0].description == pipe_nodes[0]["node1"]["description"]
    assert pipe.nodes[0].sql == pipe_nodes[0]["node1"]["sql"]
    assert pipe.nodes[1].name == list(pipe_nodes[1].keys())[0]
    assert pipe.nodes[1].description is None
    assert pipe.nodes[1].sql == pipe_nodes[1]["node2"]["sql"]


def test_apply_ids(dialect) -> None:
    parser: SQLParser = SQLParser(dialect)
    pipe_dict: dict = {
        "nodes": [
            {
                "node1": {
                    "description": "This is node 1",
                    "sql": "SELECT * FROM source1",
                }
            },
            {
                "node2": {
                    "sql": "SELECT * FROM node1 WHERE x > 5",
                }
            },
        ]
    }

    pipe: Pipe = parse(pipe_dict, "test_pipe")

    pipe_nodes = pipe_dict["nodes"]
    assert len(pipe.nodes) == len(pipe_nodes)
    assert pipe.nodes[0].name == list(pipe_nodes[0].keys())[0]
    assert pipe.nodes[0].description == pipe_nodes[0]["node1"]["description"]
    assert pipe.nodes[0].sql == pipe_nodes[0]["node1"]["sql"]
    assert pipe.nodes[1].name == list(pipe_nodes[1].keys())[0]
    assert pipe.nodes[1].description is None
    assert pipe.nodes[1].sql == pipe_nodes[1]["node2"]["sql"]

    nodes: list[Node] = parser.apply_ids(pipe.nodes)
    pipe = Pipe(**{**pipe.dict(), "nodes": nodes})

    assert pipe.nodes[0].id == pipe.nodes[0].id
    assert pipe.nodes[1].id == pipe.nodes[1].id
    assert pipe.nodes[0].id != pipe.nodes[1].id

    assert pipe.nodes[0].id != uuid()
    assert pipe.nodes[1].id != uuid()
