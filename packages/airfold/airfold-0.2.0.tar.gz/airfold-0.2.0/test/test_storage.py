from airfold.models import SourceType, EventTarget, EventType, Source, PipeEntry, NodeEntry, Kafka, Table, Event
from airfold.storage.storage import (
    Storage,
    get_pipe_deps,
)
from airfold.type import Schema


def test_init_state(storage: Storage) -> None:
    storage.drop_state()
    assert not storage.state_exists()

    storage.init_state()
    assert storage.state_exists()


def test_sources(storage: Storage) -> None:
    test_init_state(storage)

    sources: list[Source] = storage.get_sources()
    assert len(sources) == 0

    source: Source = Source(target_id="1", name="test", type=SourceType.KAFKA)
    ids: list[str] = [source.id]
    storage.insert_source(source)
    sources = storage.get_sources()
    assert len(sources) == 1
    assert sources[0].target_id == "1"
    assert sources[0].name == "test"

    source = Source(target_id="2", name="test2", type=SourceType.KAFKA)
    ids.append(source.id)
    storage.insert_source(source)
    sources = storage.get_sources()
    assert len(sources) == 2
    assert any(s.target_id == "1" for s in sources)
    assert any(s.target_id == "2" for s in sources)
    assert any(s.name == "test" for s in sources)
    assert any(s.name == "test2" for s in sources)

    storage.rename_source(ids[0], "test1")
    sources = storage.get_sources()
    assert len(sources) == 2
    assert any(s.target_id == "1" for s in sources)
    assert any(s.target_id == "2" for s in sources)
    assert any(s.name == "test1" for s in sources)
    assert any(s.name == "test2" for s in sources)

    storage.delete_source(ids[0])
    sources = storage.get_sources()
    assert len(sources) == 1
    assert sources[0].target_id == "2"
    assert sources[0].name == "test2"

    storage.delete_source(ids[1])
    sources = storage.get_sources()
    assert len(sources) == 0


def test_pipes(storage: Storage) -> None:
    test_init_state(storage)

    pipes: list[PipeEntry] = storage.get_pipes()
    assert len(pipes) == 0

    pipe: PipeEntry = PipeEntry(id="1", source_id="s1", nodes=["1"], last_node=0)
    storage.insert_pipe(pipe)
    pipes = storage.get_pipes()
    assert len(pipes) == 1
    assert pipes[0].id == "1"
    assert pipes[0].nodes == ["1"]

    pipe = PipeEntry(id="2", source_id="s1", nodes=["1", "2"], last_node=1)
    storage.insert_pipe(pipe)
    pipes = storage.get_pipes()
    assert len(pipes) == 2
    assert any(p.id == "1" for p in pipes)
    assert any(p.id == "2" for p in pipes)

    storage.delete_pipe("1")
    pipes = storage.get_pipes()
    assert len(pipes) == 1
    assert pipes[0].id == "2"
    assert pipes[0].nodes == ["1", "2"]

    storage.delete_pipe("2")
    pipes = storage.get_pipes()
    assert len(pipes) == 0


def test_nodes(storage: Storage) -> None:
    test_init_state(storage)

    nodes: list[NodeEntry] = storage.get_nodes()
    assert len(nodes) == 0

    node: NodeEntry = NodeEntry(
        id="1",
        name="test",
        sql="select 1",
        deps=["1"],
        pipe_id="1",
    )
    storage.insert_node(node)
    nodes = storage.get_nodes()
    assert len(nodes) == 1
    assert nodes[0].id == "1"
    assert nodes[0].name == "test"
    assert nodes[0].sql == "select 1"
    assert nodes[0].deps == ["1"]
    assert nodes[0].pipe_id == "1"

    node = NodeEntry(
        id="2",
        name="test2",
        sql="select 2",
        deps=["2"],
        pipe_id="2",
    )
    storage.insert_node(node)
    nodes = storage.get_nodes()
    assert len(nodes) == 2
    assert any(n.id == "1" for n in nodes)
    assert any(n.id == "2" for n in nodes)
    assert any(n.name == "test" for n in nodes)
    assert any(n.name == "test2" for n in nodes)

    storage.rename_node("1", "test1")
    nodes = storage.get_nodes()
    assert len(nodes) == 2
    assert any(n.id == "1" for n in nodes)
    assert any(n.id == "2" for n in nodes)
    assert any(n.name == "test1" for n in nodes)
    assert any(n.name == "test2" for n in nodes)

    storage.delete_node("1")
    nodes = storage.get_nodes()
    assert len(nodes) == 1
    assert nodes[0].id == "2"
    assert nodes[0].name == "test2"

    storage.delete_node("2")
    nodes = storage.get_nodes()
    assert len(nodes) == 0


def test_kafkas(storage: Storage) -> None:
    test_init_state(storage)

    kafkas: list[Kafka] = storage.get_kafkas()
    assert len(kafkas) == 0

    kafka: Kafka = Kafka(
        id="1",
        topic="test",
        host="localhost",
        port=9092,
        cols=Schema({"col1": "String", "col2": "String"}),
    )
    storage.insert_kafka(kafka)
    kafkas = storage.get_kafkas()
    assert len(kafkas) == 1
    assert kafkas[0].id == "1"
    assert kafkas[0].topic == "test"
    assert kafkas[0].host == "localhost"
    assert kafkas[0].port == 9092
    assert kafkas[0].cols == Schema({"col1": "String", "col2": "String"})

    kafka = Kafka(
        id="2",
        topic="test2",
        host="localhost",
        port=9092,
        cols=Schema({"col1": "String", "col2": "String"}),
    )
    storage.insert_kafka(kafka)
    kafkas = storage.get_kafkas()
    assert len(kafkas) == 2
    assert any(k.id == "1" for k in kafkas)
    assert any(k.id == "2" for k in kafkas)
    assert any(k.topic == "test" for k in kafkas)
    assert any(k.topic == "test2" for k in kafkas)

    storage.delete_kafka("1")
    kafkas = storage.get_kafkas()
    assert len(kafkas) == 1
    assert kafkas[0].id == "2"
    assert kafkas[0].topic == "test2"

    storage.delete_kafka("2")
    kafkas = storage.get_kafkas()
    assert len(kafkas) == 0


def test_tables(storage: Storage) -> None:
    test_init_state(storage)

    tables: list[Table] = storage.get_tables()
    assert len(tables) == 0

    table: Table = Table(id="1", cols=Schema({"col1": "String", "col2": "String"}))
    storage.insert_table(table)
    tables = storage.get_tables()
    assert len(tables) == 1
    assert tables[0].id == "1"
    assert tables[0].cols == Schema({"col1": "String", "col2": "String"})

    table = Table(id="2", cols=Schema({"col3": "String", "col4": "String"}))
    storage.insert_table(table)
    tables = storage.get_tables()
    assert len(tables) == 2
    assert any(t.id == "1" for t in tables)
    assert any(t.id == "2" for t in tables)
    assert any(t.cols == Schema({"col1": "String", "col2": "String"}) for t in tables)
    assert any(t.cols == Schema({"col3": "String", "col4": "String"}) for t in tables)

    storage.delete_table("1")
    tables = storage.get_tables()
    assert len(tables) == 1
    assert tables[0].id == "2"
    assert tables[0].cols == Schema({"col3": "String", "col4": "String"})

    storage.delete_table("2")
    tables = storage.get_tables()
    assert len(tables) == 0


def test_events(storage: Storage) -> None:
    test_init_state(storage)

    events: list[Event] = storage.get_events()
    assert len(events) == 0

    event: Event = Event(
        id="1",
        target_id="1",
        type=EventType.CREATE,
        target=EventTarget.PIPE,
        timestamp=1,
        result="ok",
        error="",
        message="",
    )
    storage.insert_event(event)
    events = storage.get_events()
    assert len(events) == 1
    assert events[0].id == "1"
    assert events[0].target_id == "1"
    assert events[0].type == EventType.CREATE
    assert events[0].target == EventTarget.PIPE
    assert events[0].timestamp == 1
    assert events[0].result == "ok"
    assert events[0].error == ""
    assert events[0].message == ""

    event = Event(
        id="2",
        target_id="2",
        type=EventType.CREATE,
        target=EventTarget.PIPE,
        timestamp=2,
        result="ok",
        error="",
        message="",
    )
    storage.insert_event(event)
    events = storage.get_events()
    assert len(events) == 2
    assert any(e.id == "1" for e in events)
    assert any(e.id == "2" for e in events)
    assert any(e.target_id == "1" for e in events)
    assert any(e.target_id == "2" for e in events)
    assert any(e.type == EventType.CREATE for e in events)
    assert any(e.target == EventTarget.PIPE for e in events)
    assert any(e.timestamp == 1 for e in events)
    assert any(e.timestamp == 2 for e in events)
    assert any(e.result == "ok" for e in events)
    assert any(e.error == "" for e in events)
    assert any(e.message == "" for e in events)


def test_get_pipe_deps() -> None:
    # class NodeEntry(BaseModel, frozen=True):
    #     id: str
    #     name: str
    #     sql: str
    #     deps: list[str]
    #     pipe_id: str

    nodes: list[NodeEntry] = [
        NodeEntry(
            id="11",
            name="test11",
            sql="select 1",
            deps=["source1", "source2"],
            pipe_id="1",
        ),
        NodeEntry(
            id="12",
            name="test12",
            sql="select 1",
            deps=["inner.11", "source1"],
            pipe_id="1",
        ),
        NodeEntry(
            id="21",
            name="test21",
            sql="select 1",
            deps=["source3"],
            pipe_id="2",
        ),
        NodeEntry(
            id="22",
            name="test22",
            sql="select 1",
            deps=["source3", "source1"],
            pipe_id="2",
        ),
    ]

    lookup: dict[str, str] = {"11": "inner.11", "22": "inner.22"}

    deps: set[str] = get_pipe_deps(nodes, lookup, "1")
    assert deps == {"source1", "source2", "inner.11"}

    deps = get_pipe_deps(nodes, lookup, "1", source_only=True)
    assert deps == {"source1", "source2"}

    deps = get_pipe_deps(nodes, lookup, "2")
    assert deps == {"source3", "source1"}

    deps = get_pipe_deps(nodes, lookup, "2", source_only=True)
    assert deps == {"source3", "source1"}


def test_nodes_sql(storage: Storage) -> None:
    test_init_state(storage)

    nodes: list[NodeEntry] = storage.get_nodes()
    assert len(nodes) == 0

    node: NodeEntry = NodeEntry(
        id="1",
        name="test",
        sql='select * from "table1"',
        deps=["1"],
        pipe_id="1",
    )
    storage.insert_node(node)
    nodes = storage.get_nodes()
    assert len(nodes) == 1
    assert nodes[0].sql == 'select * from "table1"'


def test_archive(storage: Storage) -> None:
    test_init_state(storage)

    pipes: list[PipeEntry] = storage.get_pipes()
    assert len(pipes) == 0

    node11 = NodeEntry(
        id="11",
        name="test11",
        sql="select 1",
        deps=["source1", "source2"],
        pipe_id="1",
    )
    node12 = NodeEntry(
        id="12",
        name="test12",
        sql="select 1",
        deps=["inner.11", "source1"],
        pipe_id="1",
    )

    pipe: PipeEntry = PipeEntry(id="1", source_id="s1", nodes=["11", "12"], last_node=1)
    storage.insert_pipe(pipe)
    pipes = storage.get_pipes()
    assert len(pipes) == 1
    assert pipes[0].id == "1"
    assert pipes[0].nodes == ["11", "12"]

    for node in [node11, node12]:
        storage.insert_node(node)
    nodes = storage.get_nodes()
    assert len(nodes) == 2

    storage.delete_node("11", archive=True)
    nodes = storage.get_nodes()
    assert len(nodes) == 1
    assert nodes[0].id == "12"

    storage.delete_node("12", archive=True)
    nodes = storage.get_nodes()
    assert len(nodes) == 0

    nodes = storage.get_nodes(archived=True)
    assert len(nodes) == 2

    storage.delete_pipe("1", archive=True)
    pipes = storage.get_pipes()
    assert len(pipes) == 0

    pipes = storage.get_pipes(archived=True)
    assert len(pipes) == 1
    assert pipes[0].id == "1"
