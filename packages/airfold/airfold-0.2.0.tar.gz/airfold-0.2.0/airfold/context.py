from contextlib import contextmanager, ExitStack

from airfold import parse
from airfold.config import Profile
from airfold.log import log
from airfold.models import SourceType, Source, PipeEntry, NodeEntry, Kafka, Table, View, Node, Pipe
from airfold.parse import SQLParser
from airfold.runtime.runtime import Runtime
from airfold.runtime.type import RUNTIME
from airfold.storage.storage import Storage
from airfold.storage.type import STORAGE


def load_storage(profile: Profile) -> Storage:
    return STORAGE[profile.storage.type](**profile.storage.settings)


def load_runtime(profile: Profile) -> Runtime:
    return RUNTIME[profile.runtime.type](**profile.runtime.settings)


def get_union_target(union: str, nodes: list[Node]) -> str | None:
    target_node: Node | None = next((n for n in nodes if n.name == union), None)
    assert target_node
    return target_node.target_id


PipeObject = NodeEntry | PipeEntry | Table | Node | Source


class AirfoldContext:
    def __init__(self, runtime: Runtime, storage: Storage) -> None:
        self.runtime: Runtime = runtime
        self.storage: Storage = storage

    def _push_table(self, table: Table) -> Table:
        res = self.runtime.parse(table, storage=self.storage)
        self.runtime.create_table(res)
        return res

    def _drop_objects(self, objects: list[PipeObject], archive: bool = False) -> None:
        for obj in reversed(objects):
            if isinstance(obj, Table):
                self.storage.delete_table(obj.id, archive)
                self.runtime.delete_table(obj.id)
            elif isinstance(obj, Node):
                self.runtime.drop_node(obj.id)
            elif isinstance(obj, Source):
                self.storage.delete_source(obj.id, archive)
            elif isinstance(obj, PipeEntry):
                self.storage.delete_pipe(obj.id, archive)
            elif isinstance(obj, NodeEntry):
                self.storage.delete_node(obj.id, archive)

    def _store_objects(self, objects: list[PipeObject]) -> None:
        for obj in objects:
            if isinstance(obj, NodeEntry):
                self.storage.insert_node(obj)
            elif isinstance(obj, Table):
                self.storage.insert_table(obj)
            elif isinstance(obj, Source):
                self.storage.insert_source(obj)
            elif isinstance(obj, PipeEntry):
                self.storage.insert_pipe(obj)

    def push_pipe(self, data: dict, pipe_name: str) -> None:
        log.info(f"Pushing pipe: {pipe_name}")
        log.info(f"Using data: {data}")

        pipe: Pipe = parse.parse(data, pipe_name)

        sources: list[Source] = self.storage.get_sources()

        existing_sources: list[Source] = [source for source in sources if source.name == pipe.name]
        existing_pipe_sources: list[Source] = [source for source in existing_sources if source.type == SourceType.PIPE]

        # TODO: maybe this check should be replaced with some "doctor" command to verify integrity before any operation.
        if existing_sources and len(existing_sources) > 1:
            raise ValueError(f"Multiple sources with name {pipe.name} found, the state is corrupted")

        if not existing_pipe_sources and existing_sources:
            raise ValueError(f"Source {pipe.name} already exists and it's not a pipe")

        parser: SQLParser = self.runtime.get_parser()
        parser.check_sequentiality(pipe.nodes)

        pipe = self.runtime.parse(pipe, self.storage)

        tables: list[Table] = []
        nodes: list[Node]

        source_ids: dict[str, str] = {source.name: source.target_id for source in self.storage.get_sources()}
        nodes = [Node(**{**node.dict(), "sql": parser.replace(node.sql, source_ids)}) for node in pipe.nodes]
        pipe = Pipe(**{**pipe.dict(), "nodes": nodes})

        last_node: Node = pipe.nodes[pipe.last_node]
        last_table: Table | None = None
        if pipe.to is not None:
            to_list: list[Source] = [source for source in sources if source.name == pipe.to]
            if not to_list:
                raise ValueError(f"No source found for: `to: {pipe.to}`")
            last_table = Table(id=to_list[0].target_id)
        new_nodes: list[Node] = []
        for node in pipe.nodes:
            if node.union is not None:
                target_id = get_union_target(node.union, new_nodes)
            elif node.id == last_node.id and last_table is not None:
                target_id = last_table.id
            else:
                target = Table(sql=node.sql, settings=node.settings)
                tables.append(target)
                target_id = target.id
                if node.id == last_node.id:
                    last_table = target
            new_nodes.append(Node(**{**node.dict(), "target_id": target_id}))

        nodes = parser.apply_ids(new_nodes)
        tables = parser.apply_node_ids(nodes, tables)

        pipe = Pipe(**{**pipe.dict(), "nodes": nodes})

        objects: list[PipeObject] = []

        try:
            for table in tables:
                self._push_table(table)
                objects.append(table)
            for node in pipe.nodes:
                self.runtime.create_node(node)
                objects.append(node)

                node_entry = NodeEntry(**node.dict(), pipe_id=pipe.id, deps=parser.get_table_names(node.sql))
                objects.append(node_entry)

            assert last_table
            to_source = Source(
                target_id=last_table.id,
                name=pipe.name,
                type=SourceType.PIPE,
            )
            objects.append(to_source)
            ids: list[str] = [node.id for node in pipe.nodes]
            objects.append(PipeEntry(id=pipe.id, source_id=to_source.id, nodes=ids, last_node=pipe.last_node))

            self._store_objects(objects)
        except Exception as e:
            log.error(f"Failed to create pipe {pipe.id}: {e}")
            self._drop_objects(objects)
            raise e

        if existing_pipe_sources:
            log.warning(f"Pipe {pipe.name} already exists, overwriting.")
            existing_source = existing_pipe_sources[0]
            pipe_entry: PipeEntry | None = self.get_pipe_from_source(existing_source)
            assert pipe_entry
            self.drop_pipe(pipe_id=pipe_entry.id)

        self.runtime.create_view(View(id=f"{pipe.id}", target=to_source.target_id))
        self.runtime.create_view(View(id=f'"source.{pipe.name}"', target=to_source.target_id))
        self.runtime.create_view(View(id=f'"pipe.{pipe.name}"', target=to_source.target_id))

    def get_pipe_from_source(self, source: Source) -> PipeEntry | None:
        existing_pipes: list[PipeEntry] = self.storage.get_pipes()
        pipes: list[PipeEntry] = [pipe for pipe in existing_pipes if pipe.source_id == source.id]
        if len(pipes) > 0:
            return pipes[0]
        return None

    def drop_pipe(self, name: str | None = None, pipe_id: str | None = None) -> None:
        log.info(f"Dropping pipe: {name or pipe_id}")
        if name is None and pipe_id is None:
            raise ValueError("Either name or id must be specified")

        if name is not None and pipe_id is not None:
            raise ValueError("Either name or id must be specified, not both")

        objects: list[PipeObject] = []

        source: Source
        pipe: PipeEntry | None
        if name is not None:
            sources: list[Source] = [
                source
                for source in self.storage.get_sources()
                if source.type == SourceType.PIPE and source.name == name
            ]
            if not sources:
                raise ValueError(f"Pipe {pipe_id or name} not found")
            if len(sources) > 1:
                raise ValueError(f"Multiple pipes identified as {pipe_id or name} found, the state is corrupted")
            source = sources[0]
            pipe = self.get_pipe_from_source(source)
            if not pipe:
                raise ValueError(f"Pipe {pipe_id or name} not found")
            assert pipe
        else:
            pipes: list[PipeEntry] = [pipe for pipe in self.storage.get_pipes() if pipe.id == pipe_id]
            if not pipes:
                raise ValueError(f"Pipe {pipe_id or name} not found")
            pipe = pipes[0]
            sources = [
                source
                for source in self.storage.get_sources()
                if source.type == SourceType.PIPE and pipe.source_id == source.id
            ]
            if not sources:
                raise ValueError(f"Pipe {pipe_id or name} not found")
            source = sources[0]

        objects.append(pipe)
        objects.append(source)

        nodes: list[NodeEntry] = [node for node in self.storage.get_nodes() if node.pipe_id == pipe.id]
        tables: dict[str, Table] = dict([(table.id, table) for table in self.storage.get_tables()])
        for node in nodes:
            if node.target_id and node.target_id in tables:
                objects.append(tables[node.target_id])
            objects.append(Node.from_node_entry(node))
            objects.append(node)

        self._drop_objects(objects, archive=True)
        self.runtime.drop_view(id=f'"source.{source.name}"')
        self.runtime.drop_view(id=f'"pipe.{source.name}"')
        self.runtime.drop_view(id=f"{pipe.id}")

    def push_source(self, data: dict, name: str) -> None:
        log.info(f"Pushing source: {name}")

        sources: list[Source] = [source for source in self.storage.get_sources() if source.name == name]

        # TODO: maybe this check should be replaced with some "doctor" command to verify integrity before any operation.
        if len(sources) > 1:
            raise ValueError(f"Multiple sources identified as {name} found, the state is corrupted")

        if "topic" in data:
            if sources and sources[0].type != SourceType.KAFKA:
                raise ValueError(f"Source {name} already exists and it's not a kafka source")

            kafka = Kafka(**data)
            kafka = self.runtime.create_kafka(kafka, name)

            self.storage.insert_kafka(kafka)
            self.storage.insert_source(Source(target_id=kafka.id, name=name, type=SourceType.KAFKA))

            if sources:
                log.warning(f"Kafka source {name} already exists, overwriting.")
                self.drop_kafka(id=sources[0].target_id)
                self.runtime.drop_view(id=f'"source.{name}"')
                self.runtime.drop_view(id=f'"kafka.{name}"')

            self.runtime.create_view(View(id=f'"source.{name}"', target=kafka.id))
            self.runtime.create_view(View(id=f'"kafka.{name}"', target=kafka.id))
        else:
            if sources and sources[0].type != SourceType.TABLE:
                raise ValueError(f"Source {name} already exists and it's not a table source")

            table: Table = self.runtime.parse(Table(**data), self.storage)
            table = self.runtime.create_table(table)

            self.storage.insert_table(table)
            self.storage.insert_source(Source(target_id=table.id, name=name, type=SourceType.TABLE))

            if sources:
                log.warn(f"Table source {name} already exists, overwriting.")
                self.drop_table(id=sources[0].target_id)
                self.runtime.drop_view(id=f'"source.{name}"')
                self.runtime.drop_view(id=f'"table.{name}"')

            self.runtime.create_view(View(id=f'"table.{name}"', target=table.id))
            self.runtime.create_view(View(id=f'"source.{name}"', target=table.id))

    def drop_kafka(self, id: str | None = None, name: str | None = None) -> None:
        log.info(f"Dropping kafka: {name or id}")
        if name is None and id is None:
            raise ValueError("Either name or id must be specified")

        if name is not None and id is not None:
            raise ValueError("Either name or id must be specified, not both")

        sources: list[Source] = [
            source
            for source in self.storage.get_sources()
            if source.type == SourceType.KAFKA and (source.target_id == id or source.name == name)
        ]
        if not sources:
            raise ValueError(f"Kafka source {id or name} not found")
        if len(sources) > 1:
            raise ValueError(f"Multiple kafka sources identified as {id or name} found, the state is corrupted")
        source: Source = sources[0]

        self.runtime.delete_kafka(source.target_id)

        self.storage.delete_kafka(source.target_id, True)
        self.storage.delete_source(source.id)

    def drop_table(self, id: str | None = None, name: str | None = None) -> None:
        log.info(f"Dropping table: {name or id}")
        if name is None and id is None:
            raise ValueError("Either name or id must be specified")

        if name is not None and id is not None:
            raise ValueError("Either name or id must be specified, not both")

        sources: list[Source] = [
            source
            for source in self.storage.get_sources()
            if source.type == SourceType.TABLE and (source.target_id == id or source.name == name)
        ]

        if not sources:
            raise ValueError(f"Table source {id or name} not found")
        if len(sources) > 1:
            raise ValueError(f"Multiple table sources identified as {id or name} found, the state is corrupted")
        source: Source = sources[0]

        self.runtime.delete_table(source.target_id)

        self.storage.delete_table(source.target_id, True)
        self.storage.delete_source(source.id)

    def check_state(self) -> bool:
        self.storage.init_state()
        return self.storage.state_exists()


class Airfold(ExitStack):
    def __init__(self, profile: Profile, force_lock=False) -> None:
        super().__init__()
        self.profile: Profile = profile
        self.force_lock: bool = force_lock

    @contextmanager
    def _cleanup_on_error(self):
        with ExitStack() as stack:
            stack.push(self)
            yield
            stack.pop_all()

    # yes, we cannot define type here, as that's what contextlib does in any derived classes too
    # why? because type hinting is expectedly brain-dead in python, wake me up when it changes
    def __enter__(self) -> AirfoldContext:  # type: ignore
        def unlock(s: Storage) -> None:
            s.unlock_state()

        runtime: Runtime = load_runtime(self.profile)
        storage: Storage = load_storage(self.profile)
        storage.lock_state(force=self.force_lock)
        self.callback(unlock, storage)
        ctx = AirfoldContext(runtime, storage)
        with self._cleanup_on_error():
            if not ctx.check_state():
                raise RuntimeError("Could not create storage state")
        return ctx
