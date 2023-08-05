import json
import sqlite3
from sqlite3 import Cursor, Connection

from airfold.log import log
from airfold.models import EventTarget, EventType, Source, PipeEntry, NodeEntry, Kafka, Table, Event
from airfold.storage.storage import (
    SqlStorage,
)
from airfold.utils import matches_schema


def _table_name(target: EventTarget):
    custom_map: dict[str, str] = {
        EventTarget.TABLE.value: "tables",
        EventTarget.NODE_ENTRY.value: "node",
    }
    return custom_map.get(target.value, target.value)


class Sqlite(SqlStorage):
    def __init__(self, *args, database: str | None = None, **kwargs) -> None:
        log.info(f"Initializing storage: Sqlite")
        if database is not None and len(args) == 0:
            args = (database,)
        self.conn: Connection = sqlite3.connect(*args, **kwargs)

    def state_exists(self) -> bool:
        log.info(f"Checking if state exists")
        cur: Cursor = self.conn.cursor()
        cur.execute(
            """
            SELECT name FROM sqlite_master WHERE type='table'
        """
        )
        tables: set = {
            ("node",),
            ("pipe",),
            ("source",),
            ("event",),
            ("tables",),
            ("kafka",),
        }
        current_tables: set = set(cur.fetchall())
        if not current_tables.intersection(tables) == tables:
            log.warning(f"State does not exist")
            log.warning(f"Expected tables: {tables}")
            log.warning(f"Current tables: {current_tables}")
            return False

        cur.execute("PRAGMA table_info(source)")
        state: list = cur.fetchall()
        if not matches_schema(
            state,
            [
                (0, "id", "text", 1, None, 1),
                (1, "archived", "integer", 0, None, 0),
                (2, "target_id", "text", 0, None, 0),
                (3, "name", "text", 0, None, 0),
                (4, "type", "text", 0, None, 0),
            ],
        ):
            log.error(f"Unexpected source schema: {state}")
            raise Exception(f"Source schema is not correct: {state}")

        cur.execute("PRAGMA table_info(pipe)")
        state = cur.fetchall()
        if not matches_schema(
            state,
            [
                (0, "id", "text", 1, None, 1),
                (1, "archived", "integer", 0, None, 0),
                (2, "source_id", "text", 0, None, 0),
                (3, "nodes", "text", 0, None, 0),
                (4, "last_node", "integer", 0, None, 0),
            ],
        ):
            log.error(f"Unexpected pipe schema: {state}")
            raise Exception("Pipe schema is not correct")

        cur.execute("PRAGMA table_info(node)")
        state = cur.fetchall()
        if not matches_schema(
            state,
            [
                (0, "id", "text", 1, None, 1),
                (1, "archived", "integer", 0, None, 0),
                (2, "name", "text", 0, None, 0),
                (3, "sql", "text", 0, None, 0),
                (4, "description", "text", 0, None, 0),
                (5, "deps", "text", 0, None, 0),
                (6, "pipe_id", "text", 0, None, 0),
                (7, "union", "text", 0, None, 0),
                (8, "target_id", "text", 0, None, 0),
                (9, "settings", "text", 0, None, 0),
            ],
        ):
            log.error(f"Unexpected node schema: {state}")
            raise Exception("Node schema is not correct")

        cur.execute("PRAGMA table_info(kafka)")
        state = cur.fetchall()
        if not matches_schema(
            state,
            [
                (0, "id", "text", 1, None, 1),
                (1, "archived", "integer", 0, None, 0),
                (2, "topic", "text", 0, None, 0),
                (3, "host", "text", 0, None, 0),
                (4, "port", "text", 0, None, 0),
                (5, "cols", "text", 0, None, 0),
            ],
        ):
            log.error(f"Unexpected kafka schema: {state}")
            raise Exception("Kafka schema is not correct")

        cur.execute("PRAGMA table_info(tables)")
        state = cur.fetchall()
        if not matches_schema(
            state,
            [
                (0, "id", "text", 1, None, 1),
                (1, "archived", "integer", 0, None, 0),
                (2, "cols", "text", 0, None, 0),
                (3, "sql", "text", 0, None, 0),
                (4, "settings", "text", 0, None, 0),
            ],
        ):
            log.error(f"Unexpected tables schema: {state}")
            raise Exception("Tables schema is not correct")

        cur.execute("PRAGMA table_info(event)")
        state = cur.fetchall()
        if not matches_schema(
            state,
            [
                (0, "id", "text", 1, None, 1),
                (1, "target_id", "text", 0, None, 0),
                (2, "type", "text", 0, None, 0),
                (3, "target", "text", 0, None, 0),
                (4, "timestamp", "integer", 0, None, 0),
                (5, "result", "text", 0, None, 0),
                (6, "error", "text", 0, None, 0),
                (7, "message", "text", 0, None, 0),
            ],
        ):
            log.error(f"Unexpected event schema: {state}")
            raise Exception("Event schema is not correct")

        return True

    def drop_state(self) -> None:
        log.info(f"Dropping state")
        self.conn.execute("DROP TABLE IF EXISTS source")
        self.conn.execute("DROP TABLE IF EXISTS pipe")
        self.conn.execute("DROP TABLE IF EXISTS node")
        self.conn.execute("DROP TABLE IF EXISTS kafka")
        self.conn.execute("DROP TABLE IF EXISTS tables")
        self.conn.execute("DROP TABLE IF EXISTS event")

    def execute_sql(self, sql: str, *args, **kwargs) -> None:
        log.info(f"Executing sql: {sql}")
        self.conn.execute(sql, *args, **kwargs)
        self.conn.commit()

    def get_sources(self, archived: bool = False) -> list[Source]:
        log.info(f"Getting sources")
        cur: Cursor = self.conn.cursor()
        cur.execute("SELECT id, target_id, name, type FROM source WHERE archived = ?", ((1 if archived else 0),))
        return [Source(**dict(zip(("id", "target_id", "name", "type"), row))) for row in cur.fetchall()]

    def _delete(self, target: EventTarget, _id: str, archive: bool = False) -> None:
        log.info(f"{'Archiving' if archive else 'Deleting'} {target.value}: {_id}")
        message: str = json.dumps({"id": _id, "archived": archive})
        table = _table_name(target)
        sql: str
        if archive:
            sql = f"""
                UPDATE {table} SET archived = 1 WHERE id = ?
                """
        else:
            sql = f"""
                DELETE FROM {table} WHERE id = ?
                """
        self.execute(_id, target, EventType.DELETE, message, sql, (_id,))

    def delete_source(self, source_id: str, archive: bool = False) -> None:
        return self._delete(EventTarget.SOURCE, source_id, archive=archive)

    def rename_source(self, source_id: str, new_name: str) -> None:
        log.info(f"Renaming source: {source_id} to {new_name}")
        message: str = json.dumps({"id": source_id, "name": new_name})
        sql: str = f"""
                UPDATE source SET name = ? WHERE id = ?
                """
        self.execute(source_id, EventTarget.SOURCE, EventType.UPDATE, message, sql, (new_name, source_id))

    def insert_source(self, source: Source) -> None:
        log.info(f"Inserting source: {source}")
        message: str = source.json()
        sql: str = f"""
                INSERT INTO source (id, archived, target_id, name, type)
                VALUES (?, ?, ?, ?, ?)
                """
        self.execute(
            source.id,
            EventTarget.SOURCE,
            EventType.CREATE,
            message,
            sql,
            (source.id, 0, source.target_id, source.name, source.type.value),
        )

    def get_pipes(self, archived: bool = False) -> list[PipeEntry]:
        log.info("Getting pipes")
        cur: Cursor = self.conn.cursor()
        cur.execute("SELECT id, source_id, nodes, last_node FROM pipe WHERE archived = ?", ((1 if archived else 0),))
        return [
            PipeEntry(
                **dict(zip(("id", "source_id", "nodes", "last_node"), (row[0], row[1], json.loads(row[2]), row[3])))
            )
            for row in cur.fetchall()
        ]

    def delete_pipe(self, pipe_id: str, archive: bool = False) -> None:
        return self._delete(EventTarget.PIPE, pipe_id, archive=archive)

    def insert_pipe(self, pipe: PipeEntry) -> None:
        log.info(f"Inserting pipe: {pipe.id}")
        message: str = pipe.json()
        sql: str = f"""
                INSERT INTO pipe (id, archived, source_id, nodes, last_node)
                VALUES (?, ?, ?, json(?), ?)
                """
        self.execute(
            pipe.id,
            EventTarget.PIPE,
            EventType.CREATE,
            message,
            sql,
            (pipe.id, 0, pipe.source_id, json.dumps(pipe.nodes), pipe.last_node),
        )

    def get_nodes(self, archived: bool = False) -> list[NodeEntry]:
        log.info(f"Getting nodes")
        cur: Cursor = self.conn.cursor()
        cur.execute(
            """
                SELECT
                    id,
                    name,
                    sql,
                    description,
                    deps,
                    pipe_id,
                    "union",
                    target_id,
                    settings
                FROM node
                WHERE archived = ?
            """,
            ((1 if archived else 0),),
        )
        return [
            NodeEntry(
                **dict(
                    zip(
                        ("id", "name", "sql", "description", "deps", "pipe_id", "union", "target_id", "settings"),
                        (row[0], row[1], row[2], row[3], json.loads(row[4]), row[5], row[6], row[7], row[8]),
                    )
                )
            )
            for row in cur.fetchall()
        ]

    def delete_node(self, node_id: str, archive: bool = False) -> None:
        return self._delete(EventTarget.NODE_ENTRY, node_id, archive=archive)

    def rename_node(self, node_id: str, new_name: str) -> None:
        log.info(f"Renaming node: {node_id} to {new_name}")
        message: str = json.dumps({"id": node_id, "name": new_name})
        sql: str = f"""
            UPDATE node SET name = ?
            WHERE id = ?
            """
        self.execute(node_id, EventTarget.NODE_ENTRY, EventType.UPDATE, message, sql, (new_name, node_id))

    def insert_node(self, node: NodeEntry) -> None:
        log.info(f"Inserting node: {node}")
        message: str = node.json()
        sql: str = f"""
            INSERT INTO node (
                id,
                archived,
                name,
                sql,
                description,
                deps,
                pipe_id,
                "union",
                target_id,
                settings
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        self.execute(
            node.id,
            EventTarget.NODE_ENTRY,
            EventType.CREATE,
            message,
            sql,
            (
                node.id,
                0,
                node.name,
                node.sql,
                node.description,
                json.dumps(node.deps),
                node.pipe_id,
                node.union,
                node.target_id,
                node.settings,
            ),
        )

    def get_tables(self, archived: bool = False) -> list[Table]:
        log.info(f"Getting tables")
        cur: sqlite3.Cursor = self.conn.cursor()
        cur.execute("SELECT id, cols, sql, settings FROM tables WHERE archived = ?", ((1 if archived else 0),))
        return [
            Table(
                **dict(
                    zip(
                        ("id", "cols", "sql", "settings"),
                        (row[0], json.loads(row[1]), row[2], row[3]),
                    )
                )
            )
            for row in cur.fetchall()
        ]

    def insert_table(self, table: Table) -> None:
        log.info(f"Inserting table {table.id}")
        message: str = table.json()
        sql: str = f"""
            INSERT INTO tables (id, archived, cols, sql, settings)
            VALUES (?, ?, ?, ?, ?)
            """
        self.execute(
            table.id,
            EventTarget.TABLE,
            EventType.CREATE,
            message,
            sql,
            (
                table.id,
                0,
                json.dumps(table.cols),
                table.sql,
                table.dict()["settings"],
            ),
        )

    def delete_table(self, table_id: str, archive: bool = False) -> None:
        return self._delete(EventTarget.TABLE, table_id, archive=archive)

    def get_kafkas(self, archived: bool = False) -> list[Kafka]:
        log.info(f"Getting kafkas")
        cur: Cursor = self.conn.cursor()
        cur.execute("SELECT id, topic, host, port, cols FROM kafka WHERE archived = ?", ((1 if archived else 0),))
        return [
            Kafka(
                **dict(
                    zip(
                        ("id", "topic", "host", "port", "cols"),
                        row[:4] + (json.loads(row[4]),),
                    )
                )
            )
            for row in cur.fetchall()
        ]

    def insert_kafka(self, kafka: Kafka) -> None:
        log.info(f"Inserting kafka {kafka.id}")
        message: str = kafka.json()
        sql: str = f"""
            INSERT INTO kafka (id, archived, topic, host, port, cols)
            VALUES (?, ?, ?, ?, ?, ?)
            """
        self.execute(
            kafka.id,
            EventTarget.KAFKA,
            EventType.CREATE,
            message,
            sql,
            (
                kafka.id,
                0,
                kafka.topic,
                kafka.host,
                kafka.port,
                json.dumps(kafka.cols),
            ),
        )

    def delete_kafka(self, kafka_id: str, archive: bool = False) -> None:
        return self._delete(EventTarget.KAFKA, kafka_id, archive=archive)

    def get_events(self) -> list[Event]:
        log.info(f"Getting events")
        cur: Cursor = self.conn.cursor()
        cur.execute(
            """
            SELECT "id",
                   "target_id",
                   "type",
                   "target",
                   "timestamp",
                   "result",
                   "error",
                   "message"
            FROM event
            """
        )
        return [
            Event(
                **dict(
                    zip(
                        (
                            "id",
                            "target_id",
                            "type",
                            "target",
                            "timestamp",
                            "result",
                            "error",
                            "message",
                        ),
                        row,
                    )
                )
            )
            for row in cur.fetchall()
        ]

    def insert_event(self, event: Event) -> None:
        log.info(f"Inserting event {event}")
        self.conn.execute(
            f"""
            INSERT INTO event
            (id, target_id, type, target, timestamp, result, error, message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                event.id,
                event.target_id,
                event.type.value,
                event.target.value,
                event.timestamp,
                event.result,
                event.error,
                event.message,
            ),
        )

    def init_state(self) -> None:
        log.info("Initializing state")
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS source (
                id text primary key not null,
                archived integer,
                target_id text,
                name text,
                type text
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS pipe (
                id text primary key not null,
                archived integer,
                source_id text,
                nodes text,
                last_node integer
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS node (
                id text primary key not null,
                archived integer,
                name text,
                sql text,
                description text,
                deps text,
                pipe_id text,
                "union" text,
                target_id text,
                settings text
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS kafka (
                id text primary key not null,
                archived integer,
                topic text,
                host text,
                port text,
                cols text
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tables (
                id text primary key not null,
                archived integer,
                cols text,
                sql text,
                settings text
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS event (
                id text primary key not null,
                target_id text,
                type text,
                target text,
                timestamp integer,
                result text,
                error text,
                message text
            )
            """
        )

    def lock_state(self, force: bool = False) -> None:
        log.info("Locking state")
        if force:
            log.info("Forcing lock")
            self.conn.execute("CREATE TABLE IF NOT EXISTS state_locked (ts TIMESTAMP" " DATETIME)")
        else:
            log.info("Checking lock")
            self.conn.execute("CREATE TABLE state_locked (ts TIMESTAMP DATETIME)")

        log.info("Inserting lock")
        self.conn.execute("INSERT INTO state_locked VALUES (STRFTIME('%Y-%m-%d %H:%M:%f'," " 'NOW'))")
        self.conn.commit()

    def unlock_state(self) -> None:
        log.info("Unlocking state")
        self.conn.execute("DROP TABLE state_locked")
        self.conn.commit()
