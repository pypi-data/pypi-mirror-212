import time

# Import abstract types
from abc import ABC, abstractmethod

from airfold.log import log
from airfold.models import EventTarget, EventType, Source, PipeEntry, NodeEntry, Kafka, Table, Event
from airfold.type import Lookup
from airfold.utils import uuid


class Storage(ABC):
    """Airfold Storage interface.
    Every storage class should implement it.
    """

    # --- GENERAL ---
    @abstractmethod
    def init_state(self) -> None:
        """Init storage state.
        Must be idempotent.
        """
        pass

    @abstractmethod
    def state_exists(self) -> bool:
        """Check if state exists.

        Returns:
            True if state exists
        """
        pass

    @abstractmethod
    def drop_state(self) -> None:
        """Delete storage state completely."""
        pass

    # --- SOURCE ---
    @abstractmethod
    def get_sources(self, archived: bool = False) -> list[Source]:
        """Get the list of sources in the state.

        Args:
            archived: get archived sources only

        Returns:
            list of Source objects
        """
        pass

    @abstractmethod
    def delete_source(self, source_id: str, archive: bool = False) -> None:
        """Delete source from storage.

        Args:
            source_id: unique source id
            archive: archive, instead of actually deleting
        """
        pass

    @abstractmethod
    def rename_source(self, source_id: str, new_name: str) -> None:
        """Rename source.

        Args:
            source_id: unique source id
            new_name: new source name
        """
        pass

    @abstractmethod
    def insert_source(self, source: Source) -> None:
        """Add new source.
        Should fail if that source id already exists.

        Args:
            source: Source object to add
        """
        pass

    # --- PIPE ---
    @abstractmethod
    def get_pipes(self, archived: bool = False) -> list[PipeEntry]:
        """Get list of pipes.

        Args:
            archived: get archived pipes only

        Returns:
            list of Pipe objects in the storage
        """
        pass

    @abstractmethod
    def delete_pipe(self, pipe_id: str, archive: bool = False) -> None:
        """Delete pipe from storage.

        Args:
            pipe_id: unique pipe id
            archive: archive, instead of actually deleting
        """
        pass

    @abstractmethod
    def insert_pipe(self, pipe: PipeEntry) -> None:
        """Add new pipe.
        Should fail if that pipe id already exists.

        Args:
            pipe: Pipe object to add
        """
        pass

    # --- NODE ---
    @abstractmethod
    def get_nodes(self, archived: bool = False) -> list[NodeEntry]:
        """Get a list of nodes in the storage.

        Args:
            archived: get archived nodes only

        Returns:
            list of NodeEntry objects
        """
        pass

    @abstractmethod
    def delete_node(self, node_id: str, archive: bool = False) -> None:
        """Delete node from the storage.

        Args:
            node_id: unique node id
            archive: archive, instead of actually deleting
        """
        pass

    @abstractmethod
    def rename_node(self, node_id: str, new_name: str) -> None:
        """Rename a node.

        Args:
            node_id: unique node id
            new_name: new node name
        """
        pass

    @abstractmethod
    def insert_node(self, node: NodeEntry) -> None:
        """Add a node to storage.
        Should fail if that node id already exists.

        Args:
            node: Node object to add
        """
        pass

    # --- KAFKA ---
    @abstractmethod
    def get_kafkas(self, archived: bool = False) -> list[Kafka]:
        """Get a list of kafka sources in the storage.

        Args:
            archived: get archived kafka sources only

        Returns:
            list of Kafka objects
        """
        pass

    @abstractmethod
    def insert_kafka(self, kafka: Kafka) -> None:
        """Add a new kafka source to storage.
        Should fail if that source id already exists.

        Args:
            kafka: Kafka object to add
        """
        pass

    @abstractmethod
    def delete_kafka(self, kafka_id: str, archive: bool = False) -> None:
        """Delete kafka source from the storage.

        Args:
            kafka_id: unique kafka source id
            archive: archive, instead of actually deleting
        """
        pass

    # --- TABLE ---
    @abstractmethod
    def get_tables(self, archived: bool = False) -> list[Table]:
        """Get a list of table sources in the storage.

        Args:
            archived: get archived table sources only

        Returns:
            list of Table objects
        """
        pass

    @abstractmethod
    def insert_table(self, table: Table) -> None:
        """Add a new table source to storage.
        Should fail if that table id already exists.

        Args:
            table: Table object to add
        """
        pass

    @abstractmethod
    def delete_table(self, table_id: str, archive: bool = False) -> None:
        """Delete table source from the storage.

        Args:
            table_id: unique table source id
            archive: archive, instead of actually deleting
        """
        pass

    # --- EVENT ---
    @abstractmethod
    def get_events(self) -> list[Event]:
        """Get all events from the storage log.

        Returns:
            list of events
        """
        pass

    @abstractmethod
    def insert_event(self, event: Event) -> None:
        """Append a new event to the storage log.

        Args:
            event: Event object
        """
        pass

    # --- LOCK ---
    @abstractmethod
    def lock_state(self, force: bool = False) -> None:
        """Lock storage state exclusively.
        Will be called at the beginning of every storage session.

        Args:
            force: force lock, even if locked by somebody already
        """
        pass

    @abstractmethod
    def unlock_state(self) -> None:
        """Unlock storage state
        Will be called at the end of every storage session.
        """
        pass


class SqlStorage(Storage):
    """Storage engine that uses SQL (DBAPI) to mutate the state."""

    @abstractmethod
    def execute_sql(self, sql: str, *args, **kwargs) -> None:
        """Run SQL command.
        Use ``*args`` and ``**kwargs`` to pass parameters or any other driver-specific data.

        Args:
            sql: SQL query
            *args: DBAPI driver-specific arguments
            **kwargs: DBAPI driver-specific kwargs
        """
        pass

    def execute(
        self,
        target_id: str,
        target: EventTarget,
        type: EventType,
        message: str,
        sql: str,
        *args,
        **kwargs,
    ) -> None:
        """Execute state mutation using an SQL query.
        Essentially will call ``execute_sql`` and then append entry to the event log.

        Args:
            target_id: unique id of the item we process
            target: type of the item
            type: type of the operation
            message: message we want to use in the event log
            sql: SQL query to execute
            *args: DBAPI driver-specific arguments
            **kwargs: DBAPI driver-specific kwargs
        """
        event: Event = Event(
            id=uuid(),
            target_id=target_id,
            type=type,
            target=target,
            timestamp=int(time.time() * 100),
            result="",
            error="",
            message=message,
        )

        try:
            self.execute_sql(sql, *args, **kwargs)
        except Exception as e:
            error: str = str(e)
            if "Stack trace:" in error:
                error = error[: error.index("Stack trace:")]
            if len(error) > 1000:
                error = error[:1000]

            error = error

            log.error(f"ERRORRRR {error}")

            self.insert_event(
                Event(
                    **{**event.dict(), "error": error},
                ),
            )
            raise Exception(f"Error executing {event}: {e}")

        self.insert_event(Event(**{**event.dict(), "result": "ok"}))


def get_pipe_deps(nodes: list[NodeEntry], lookup: Lookup, pipe_id: str, source_only=None) -> set[str]:
    log.info(f"Getting pipe dependencies for {pipe_id}")
    nodes = [n for n in nodes if n.pipe_id == pipe_id]
    deps: set[str] = {d for n in nodes for d in n.deps}

    log.info(f"Found {len(deps)} dependencies")

    if source_only:
        mvs: set[str] = {v for k, v in lookup.items() if k in [n.id for n in nodes]}
        deps = deps - mvs

    log.info(f"Found {deps} dependencies")

    return deps
