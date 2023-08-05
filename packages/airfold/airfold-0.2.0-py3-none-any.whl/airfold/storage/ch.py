import json

from clickhouse_connect import create_client  # type: ignore
from clickhouse_connect.driver.client import Client  # type: ignore

from airfold.log import log
from airfold.models import EventTarget, EventType, Source, PipeEntry, NodeEntry, Kafka, Table, Event
from airfold.storage.storage import (
    SqlStorage,
)

INSERT_SQL: str = """
                INSERT INTO state (id, ts, deleted, archived, type, data)
                VALUES ({id:String}, now64(), 0, 0, {type:String}, {data:String})
                """

DELETE_SQL: str = """
                INSERT INTO state (id, ts, deleted, archived, type, data)
                VALUES ({id:String}, now64(), 1, 0, {type:String}, '')
                """

ARCHIVE_SQL: str = """
                INSERT INTO state (id, ts, deleted, archived, type, data)
                VALUES ({id:String}, now64(), 0, 1, {type:String}, '')
                """

TABLES: dict[str, str] = {
    "state": """
        (
            id String,
            ts DateTime64,
            deleted UInt8,
            archived UInt8,
            type String,
            data String
        )
    """,
    "event": """
        (
            id String,
            target_id String,
            type String,
            target String,
            timestamp UInt64,
            result String,
            error String,
            message String
        )
    """,
}

VIEWS: dict[str, str] = {
    "source": f"""
        SELECT
            r.id,
            r.ts as changed_at,
            r.archived,
            JSONExtractString(data, 'target_id') AS target_id,
            JSONExtractString(data, 'name') AS name,
            JSONExtractString(data, 'type') AS type
        FROM
        (
            SELECT
                id,
                ts,
                deleted,
                archived,
                data,
                row_number() OVER (PARTITION BY id ORDER BY ts DESC)
                    AS rn
            FROM state
            WHERE type = '{EventTarget.SOURCE.value}'
        ) AS r
        WHERE r.rn = 1 AND r.deleted = 0
    """,
    "pipe": f"""
        SELECT
            r.id,
            r.ts as changed_at,
            r.archived,
            JSONExtractString(data, 'source_id') AS source_id,
            JSONExtract(data, 'nodes', 'Array(String)') AS nodes,
            JSONExtractUInt(data, 'last_node') AS last_node
        FROM
        (
            SELECT
                id,
                ts,
                deleted,
                archived,
                data,
                row_number() OVER (PARTITION BY id ORDER BY ts DESC)
                    AS rn
            FROM state
            WHERE type = '{EventTarget.PIPE.value}'
        ) AS r
        WHERE r.rn = 1 AND r.deleted = 0
    """,
    "node": f"""
        SELECT
            r.id,
            r.ts as changed_at,
            r.archived,
            JSONExtractString(data, 'name') AS name,
            JSONExtractString(data, 'sql') AS sql,
            JSONExtractString(data, 'description') AS description,
            JSONExtract(data, 'deps', 'Array(String)') AS deps,
            JSONExtractString(data, 'pipe_id') AS pipe_id,
            JSONExtractString(data, 'union') AS "union",
            JSONExtractString(data, 'target_id') AS target_id,
            JSONExtractString(data, 'settings') AS settings
        FROM
        (
            SELECT
                id,
                ts,
                deleted,
                archived,
                data,
                row_number() OVER (PARTITION BY id ORDER BY ts DESC)
                    AS rn
            FROM state
            WHERE type = '{EventTarget.NODE_ENTRY.value}'
        ) AS r
        WHERE r.rn = 1 AND r.deleted = 0
    """,
    "kafka": f"""
        SELECT
            r.id,
            r.ts as changed_at,
            r.archived,
            JSONExtractString(data, 'topic') AS topic,
            JSONExtractString(data, 'host') AS host,
            JSONExtract(data, 'port', 'UInt16') AS port,
            JSONExtractString(data, 'cols') AS cols
        FROM
        (
            SELECT
                id,
                ts,
                deleted,
                archived,
                data,
                row_number() OVER (PARTITION BY id ORDER BY ts DESC)
                    AS rn
            FROM state
            WHERE type = '{EventTarget.KAFKA.value}'
        ) AS r
        WHERE r.rn = 1 AND r.deleted = 0
    """,
    "tables": f"""
        SELECT
            r.id,
            r.ts as changed_at,
            r.archived,
            JSONExtractString(data, 'cols') AS cols,
            JSONExtractString(data, 'sql') AS sql,
            JSONExtractString(data, 'settings') AS settings
        FROM
        (
            SELECT
                id,
                ts,
                deleted,
                archived,
                data,
                row_number() OVER (PARTITION BY id ORDER BY ts DESC)
                    AS rn
            FROM state
            WHERE type = '{EventTarget.TABLE.value}'
        ) AS r
        WHERE r.rn = 1 AND r.deleted = 0
    """,
}


class Clickhouse(SqlStorage):
    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        log.info(f"Initializing storage: Clickhouse")
        self.client: Client = create_client(*args, **kwargs)

    def execute_sql(self, sql, *args, **kwargs) -> None:
        log.info(f"Executing sql: {sql}; {kwargs.get('parameters')}")
        self.client.command(sql, *args, **kwargs)

    def init_state(self) -> None:
        log.info("Initializing state")
        self.client.command(f"CREATE DATABASE IF NOT EXISTS {self.client.database}")

        # language=SQL
        self.client.command(
            f"""
            CREATE TABLE IF NOT EXISTS state
            {TABLES["state"]}
            ENGINE = ReplacingMergeTree(ts, deleted)
            ORDER BY id SETTINGS clean_deleted_rows = 'Always'
            """
        )

        self.client.command(
            f"""
            CREATE VIEW IF NOT EXISTS source AS
            {VIEWS["source"]}
            """
        )

        self.client.command(
            f"""
            CREATE VIEW IF NOT EXISTS pipe AS
            {VIEWS["pipe"]}
            """
        )

        self.client.command(
            f"""
            CREATE VIEW IF NOT EXISTS node AS
            {VIEWS["node"]}
            """
        )

        self.client.command(
            f"""
            CREATE VIEW IF NOT EXISTS kafka AS
            {VIEWS["kafka"]}
            """
        )

        self.client.command(
            f"""
            CREATE VIEW IF NOT EXISTS tables AS
            {VIEWS["tables"]}
            """
        )

        # language=SQL
        self.client.command(
            f"""
            CREATE TABLE IF NOT EXISTS event
            {TABLES["event"]}
            ENGINE = ReplacingMergeTree()
            ORDER BY id
            """
        )

    def state_exists(self) -> bool:
        log.info(f"Checking if state exists")
        tables: set = {
            ("state",),
            ("node",),
            ("pipe",),
            ("source",),
            ("event",),
            ("kafka",),
            ("tables",),
        }
        current_tables: set = set(self.client.query(f"SHOW TABLES IN {self.client.database}").result_set)
        if not current_tables.intersection(tables) == tables:
            log.warning(f"State does not exist")
            log.warning(f"Expected tables: {tables}")
            log.warning(f"Current tables: {current_tables}")
            return False

        schema = self.client.query("DESCRIBE TABLE state").result_set
        if not schema == [
            ("id", "String", "", "", "", "", ""),
            ("ts", "DateTime64(3)", "", "", "", "", ""),
            ("deleted", "UInt8", "", "", "", "", ""),
            ("archived", "UInt8", "", "", "", "", ""),
            ("type", "String", "", "", "", "", ""),
            ("data", "String", "", "", "", "", ""),
        ]:
            log.error(f"Unexpected state schema: {schema}")
            raise Exception("State schema is not correct")

        schema = self.client.query("DESCRIBE TABLE source").result_set
        if not schema == [
            ("id", "String", "", "", "", "", ""),
            ("changed_at", "DateTime64(3)", "", "", "", "", ""),
            ("archived", "UInt8", "", "", "", "", ""),
            ("target_id", "String", "", "", "", "", ""),
            ("name", "String", "", "", "", "", ""),
            ("type", "String", "", "", "", "", ""),
        ]:
            log.error(f"Unexpected source schema: {schema}")
            raise Exception("Source schema is not correct")

        schema = self.client.query("DESCRIBE TABLE pipe").result_set
        if not schema == [
            ("id", "String", "", "", "", "", ""),
            ("changed_at", "DateTime64(3)", "", "", "", "", ""),
            ("archived", "UInt8", "", "", "", "", ""),
            ("source_id", "String", "", "", "", "", ""),
            ("nodes", "Array(String)", "", "", "", "", ""),
            ("last_node", "UInt64", "", "", "", "", ""),
        ]:
            log.error(f"Unexpected pipe schema: {schema}")
            raise Exception("Pipe schema is not correct")

        schema = self.client.query("DESCRIBE TABLE node").result_set
        if not schema == [
            ("id", "String", "", "", "", "", ""),
            ("changed_at", "DateTime64(3)", "", "", "", "", ""),
            ("archived", "UInt8", "", "", "", "", ""),
            ("name", "String", "", "", "", "", ""),
            ("sql", "String", "", "", "", "", ""),
            ("description", "String", "", "", "", "", ""),
            ("deps", "Array(String)", "", "", "", "", ""),
            ("pipe_id", "String", "", "", "", "", ""),
            ("union", "String", "", "", "", "", ""),
            ("target_id", "String", "", "", "", "", ""),
            ("settings", "String", "", "", "", "", ""),
        ]:
            log.error(f"Unexpected node schema: {schema}")
            raise Exception("Node schema is not correct")

        schema = self.client.query("DESCRIBE TABLE kafka").result_set
        if not schema == [
            ("id", "String", "", "", "", "", ""),
            ("changed_at", "DateTime64(3)", "", "", "", "", ""),
            ("archived", "UInt8", "", "", "", "", ""),
            ("topic", "String", "", "", "", "", ""),
            ("host", "String", "", "", "", "", ""),
            ("port", "UInt16", "", "", "", "", ""),
            ("cols", "String", "", "", "", "", ""),
        ]:
            log.error(f"Unexpected kafka schema: {schema}")
            raise Exception("Kafka schema is not correct")

        schema = self.client.query("DESCRIBE TABLE tables").result_set
        if not schema == [
            ("id", "String", "", "", "", "", ""),
            ("changed_at", "DateTime64(3)", "", "", "", "", ""),
            ("archived", "UInt8", "", "", "", "", ""),
            ("cols", "String", "", "", "", "", ""),
            ("sql", "String", "", "", "", "", ""),
            ("settings", "String", "", "", "", "", ""),
        ]:
            log.error(f"Unexpected tables schema: {schema}")
            raise Exception("Tables schema is not correct")

        schema = self.client.query("DESCRIBE TABLE event").result_set
        if not schema == [
            ("id", "String", "", "", "", "", ""),
            ("target_id", "String", "", "", "", "", ""),
            ("type", "String", "", "", "", "", ""),
            ("target", "String", "", "", "", "", ""),
            ("timestamp", "UInt64", "", "", "", "", ""),
            ("result", "String", "", "", "", "", ""),
            ("error", "String", "", "", "", "", ""),
            ("message", "String", "", "", "", "", ""),
        ]:
            log.error(f"Unexpected event schema: {schema}")
            raise Exception("Event schema is not correct")

        return True

    def drop_state(self) -> None:
        log.info("Dropping state")
        self.client.command("DROP TABLE IF EXISTS event")
        self.client.command("DROP TABLE IF EXISTS kafka")
        self.client.command("DROP TABLE IF EXISTS tables")
        self.client.command("DROP TABLE IF EXISTS node")
        self.client.command("DROP TABLE IF EXISTS pipe")
        self.client.command("DROP TABLE IF EXISTS source")
        self.client.command("DROP TABLE IF EXISTS state")

    def _insert(self, target: EventTarget, model: NodeEntry | PipeEntry | Source | Kafka | Table) -> None:
        log.info(f"Inserting {target.value}: {model}")
        message: str = model.json()
        parameters: dict[str, str] = {
            "id": model.id,
            "type": target.value,
            "data": message,
        }
        self.execute(
            model.id,
            target,
            EventType.CREATE,
            message=message,
            sql=INSERT_SQL,
            parameters=parameters,
        )

    def _delete(self, target: EventTarget, _id: str, archive: bool = False) -> None:
        log.info(f"{'Archiving' if archive else 'Deleting'} {target.value}: {_id}")
        message: str = json.dumps({"id": _id, "archived": archive})
        parameters: dict[str, str] = {"id": _id, "type": target.value}
        self.execute(
            _id,
            target,
            EventType.DELETE,
            message=message,
            sql=(ARCHIVE_SQL if archive else DELETE_SQL),
            parameters=parameters,
        )

    def get_sources(self, archived: bool = False) -> list[Source]:
        log.info("Getting sources")
        return [
            Source(**dict(zip(("id", "target_id", "name", "type"), row)))
            for row in self.client.query(
                "SELECT id, target_id, name, type FROM source WHERE archived = {ar:UInt8}",
                parameters={"ar": (1 if archived else 0)},
            ).result_set
        ]

    def insert_source(self, source: Source) -> None:
        return self._insert(EventTarget.SOURCE, source)

    def delete_source(self, source_id: str, archive: bool = False) -> None:
        return self._delete(EventTarget.SOURCE, source_id, archive=archive)

    def rename_source(self, source_id: str, new_name: str) -> None:
        message: str = json.dumps({"id": source_id, "name": new_name})
        sql: str = """
                INSERT INTO state (id, ts, deleted, type, data)
                SELECT
                    id,
                    now64(),
                    0,
                    {type:String},
                    toJSONString(map('name', {new_name:String}, 'type', type, 'target_id', target_id))
                FROM source
                WHERE id = {id:String}
                """
        parameters: dict[str, str] = {
            "id": source_id,
            "type": EventTarget.SOURCE.value,
            "new_name": new_name,
        }
        self.execute(
            source_id,
            EventTarget.SOURCE,
            EventType.UPDATE,
            message=message,
            sql=sql,
            parameters=parameters,
        )

    def get_pipes(self, archived: bool = False) -> list[PipeEntry]:
        log.info(f"Getting pipes")
        return [
            PipeEntry(**dict(zip(("id", "source_id", "nodes", "last_node"), row)))
            for row in self.client.query(
                "SELECT id, source_id, nodes, last_node FROM pipe WHERE archived = {ar:UInt8}",
                parameters={"ar": (1 if archived else 0)},
            ).result_set
        ]

    def insert_pipe(self, pipe: PipeEntry) -> None:
        return self._insert(EventTarget.PIPE, pipe)

    def delete_pipe(self, pipe_id: str, archive: bool = False) -> None:
        return self._delete(EventTarget.PIPE, pipe_id, archive=archive)

    def get_events(self) -> list[Event]:
        log.info(f"Getting events")
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
            for row in self.client.query(
                "SELECT id, target_id, type, target, timestamp, result, error, message FROM event"
            ).result_set
        ]

    def insert_event(self, event: Event) -> None:
        log.info(f"Inserting event {event}")
        data: list[list] = [
            [
                event.id,
                event.target_id,
                event.type.value,
                event.target.value,
                event.timestamp,
                event.result,
                event.error,
                event.message,
            ]
        ]
        self.client.insert(
            "event",
            data,
            column_names=[
                "id",
                "target_id",
                "type",
                "target",
                "timestamp",
                "result",
                "error",
                "message",
            ],
        )

    def get_nodes(self, archived: bool = False) -> list[NodeEntry]:
        log.info(f"Getting nodes")
        return [
            NodeEntry(
                **dict(
                    zip(
                        ("id", "name", "sql", "description", "deps", "pipe_id", "union", "target_id", "settings"),
                        row,
                    )
                )
            )
            for row in self.client.query(
                """
                SELECT id, name, sql, description, deps, pipe_id, "union", target_id, settings
                FROM node
                WHERE archived = {ar:UInt8}
                """,
                parameters={"ar": (1 if archived else 0)},
            ).result_set
        ]

    def insert_node(self, node: NodeEntry) -> None:
        return self._insert(EventTarget.NODE_ENTRY, node)

    def delete_node(self, node_id: str, archive: bool = False) -> None:
        return self._delete(EventTarget.NODE_ENTRY, node_id, archive=archive)

    def rename_node(self, node_id: str, new_name: str) -> None:
        message: str = json.dumps({"id": node_id, "name": new_name})
        # the ugly trim/concat combo below is because of:
        # https://github.com/ClickHouse/ClickHouse/issues/48979
        sql: str = """
            INSERT INTO state (id, ts, deleted, type, data)
            SELECT
                id,
                now64(),
                0,
                {type:String},
                concat(
                  trim(TRAILING '}' from
                    toJSONString(map(
                        'name', {new_name:String},
                        'sql', sql,
                        'pipe_id', pipe_id,
                        'union', "union",
                        'target_id', target_id,
                        'settings', settings
                    ))
                  ),
                  ',',
                  trim(LEADING '{' from toJSONString(map('deps', deps))))
            FROM node
            WHERE id = {id:String}
            """
        parameters: dict[str, str] = {
            "id": node_id,
            "type": EventTarget.NODE_ENTRY.value,
            "new_name": new_name,
        }
        self.execute(
            node_id,
            EventTarget.NODE_ENTRY,
            EventType.UPDATE,
            message=message,
            sql=sql,
            parameters=parameters,
        )

    def get_kafkas(self, archived: bool = False) -> list[Kafka]:
        log.info(f"Getting kafkas")
        return [
            Kafka(
                **dict(
                    zip(
                        ("id", "topic", "host", "port", "cols"),
                        (row[0], row[1], row[2], row[3], json.loads(row[4])),
                    )
                )
            )
            for row in self.client.query(
                "SELECT id, topic, host, port, cols FROM kafka WHERE archived = {ar:UInt8}",
                parameters={"ar": (1 if archived else 0)},
            ).result_set
        ]

    def insert_kafka(self, kafka: Kafka) -> None:
        return self._insert(EventTarget.KAFKA, kafka)

    def delete_kafka(self, kafka_id: str, archive: bool = False) -> None:
        return self._delete(EventTarget.KAFKA, kafka_id, archive=archive)

    def get_tables(self, archived: bool = False) -> list[Table]:
        log.info(f"Getting tables")
        return [
            Table(
                **dict(
                    zip(
                        ("id", "cols", "sql", "settings"),
                        (row[0], json.loads(row[1] or "null"), row[2], row[3]),
                    )
                )
            )
            for row in self.client.query(
                "SELECT id, cols, sql, settings FROM tables WHERE archived = {ar:UInt8}",
                parameters={"ar": (1 if archived else 0)},
            ).result_set
        ]

    def insert_table(self, table: Table) -> None:
        return self._insert(EventTarget.TABLE, table)

    def delete_table(self, table_id: str, archive: bool = False) -> None:
        return self._delete(EventTarget.TABLE, table_id, archive=archive)

    def lock_state(self, force: bool = False) -> None:
        if force:
            self.client.command(
                """
                CREATE TABLE IF NOT EXISTS
                state_locked (ts DateTime64(3))
                ENGINE = TinyLog()
            """
            )
        else:
            # create will fail if state is already locked (table exists)
            self.client.command(
                """
                CREATE TABLE state_locked (ts DateTime64(3))
                ENGINE = TinyLog()
                """
            )
        self.client.command("INSERT INTO state_locked VALUES (now64(3))")

    def unlock_state(self) -> None:
        self.client.command(
            """
            DROP TABLE IF EXISTS state_locked
            """
        )


class ClickhouseCluster(Clickhouse):
    def __init__(self, *args, cluster: str = "default", **kwargs) -> None:
        log.info(f"Initializing storage: ClickhouseCluster")
        self.cluster: str = cluster
        self.args = args
        self.kwargs = kwargs
        super().__init__(*args, **kwargs)
        self.client.command("SET insert_distributed_sync = 1")

    def _validate_cluster(self) -> None:
        res = self.client.query(
            "SELECT DISTINCT cluster FROM system.clusters WHERE cluster = {c:String}", parameters={"c": self.cluster}
        ).result_set
        if len(res) == 0:
            raise ValueError(f"Cluster name not found: {self.cluster}")

    def _validate_macros(self) -> None:
        res = self.client.query("SELECT DISTINCT macro FROM system.macros").result_set
        macros = [r[0] for r in res]
        if "shard" not in macros:
            raise ValueError(f"Macro not found: 'shard' not in {macros}")
        if "replica" not in macros:
            raise ValueError(f"Macro not found: 'replica' not in {macros}")

    def init_state(self) -> None:
        log.info("Initializing state")
        self._validate_cluster()
        self._validate_macros()
        self.client.command(f"CREATE DATABASE IF NOT EXISTS {self.client.database} ON CLUSTER {self.cluster}")

        self.client.command(
            f"""
            CREATE TABLE IF NOT EXISTS state_replica ON CLUSTER {self.cluster}
            {TABLES["state"]}
            ENGINE = ReplicatedReplacingMergeTree(
                '/clickhouse/tables/{{shard}}/{self.client.database}/{{uuid}}',
                '{{replica}}', ts, deleted)
            ORDER BY id SETTINGS clean_deleted_rows = 'Always'
            """
        )

        self.client.command(
            f"""
            CREATE TABLE IF NOT EXISTS state ON CLUSTER {self.cluster}
            AS {self.client.database}.state_replica
            ENGINE = Distributed({self.cluster}, {self.client.database}, state_replica, cityHash64(id))
            """
        )

        self.client.command(
            f"""
            CREATE TABLE IF NOT EXISTS event_replica ON CLUSTER {self.cluster}
            {TABLES["event"]}
            ENGINE = ReplicatedReplacingMergeTree(
                '/clickhouse/tables/{{shard}}/{self.client.database}/{{uuid}}',
                '{{replica}}')
            ORDER BY id
            """
        )

        self.client.command(
            f"""
            CREATE TABLE IF NOT EXISTS event ON CLUSTER {self.cluster}
            AS {self.client.database}.event_replica
            ENGINE = Distributed({self.cluster}, {self.client.database}, event_replica, cityHash64(id))
            """
        )

        self.client.command(
            f"""
            CREATE VIEW IF NOT EXISTS source ON CLUSTER {self.cluster} AS
            {VIEWS["source"]}
            """
        )

        self.client.command(
            f"""
            CREATE VIEW IF NOT EXISTS pipe ON CLUSTER {self.cluster} AS
            {VIEWS["pipe"]}
            """
        )

        self.client.command(
            f"""
            CREATE VIEW IF NOT EXISTS node ON CLUSTER {self.cluster} AS
            {VIEWS["node"]}
            """
        )

        self.client.command(
            f"""
            CREATE VIEW IF NOT EXISTS kafka ON CLUSTER {self.cluster} AS
            {VIEWS["kafka"]}
            """
        )

        self.client.command(
            f"""
            CREATE VIEW IF NOT EXISTS tables ON CLUSTER {self.cluster} AS
            {VIEWS["tables"]}
            """
        )

    def drop_state(self) -> None:
        self.client.command(f"DROP TABLE IF EXISTS event ON CLUSTER {self.cluster} SYNC")
        self.client.command(f"DROP TABLE IF EXISTS kafka ON CLUSTER {self.cluster} SYNC")
        self.client.command(f"DROP TABLE IF EXISTS tables ON CLUSTER {self.cluster} SYNC")
        self.client.command(f"DROP TABLE IF EXISTS node ON CLUSTER {self.cluster} SYNC")
        self.client.command(f"DROP TABLE IF EXISTS pipe ON CLUSTER {self.cluster} SYNC")
        self.client.command(f"DROP TABLE IF EXISTS source ON CLUSTER {self.cluster} SYNC")
        self.client.command(f"DROP TABLE IF EXISTS state ON CLUSTER {self.cluster} SYNC")
        self.client.command(f"DROP TABLE IF EXISTS event_replica ON CLUSTER {self.cluster} SYNC")
        self.client.command(f"DROP TABLE IF EXISTS state_replica ON CLUSTER {self.cluster} SYNC")

    def lock_state(self, force: bool = False) -> None:
        if force:
            self.client.command(
                f"""
                CREATE TABLE IF NOT EXISTS state_locked ON CLUSTER {self.cluster}
                (ts DateTime64(3))
                ENGINE = ReplicatedMergeTree(
                '/clickhouse/tables/{{shard}}/{self.client.database}/{{uuid}}',
                '{{replica}}')
                ORDER BY ts
            """
            )
        else:
            # create will fail if state is already locked (table exists)
            self.client.command(
                f"""
                CREATE TABLE state_locked ON CLUSTER {self.cluster}
                (ts DateTime64(3))
                ENGINE = ReplicatedMergeTree(
                '/clickhouse/tables/{{shard}}/{self.client.database}/{{uuid}}',
                '{{replica}}')
                ORDER BY ts
                """
            )
        self.client.command("INSERT INTO state_locked VALUES (now64(3))")

    def unlock_state(self) -> None:
        self.client.command(
            f"""
            DROP TABLE IF EXISTS state_locked ON CLUSTER {self.cluster} SYNC
            """
        )


class ClickhouseCloud(Clickhouse):
    def __init__(self, *args, **kwargs):
        kwargs = kwargs or {}
        kwargs["secure"] = True
        super().__init__(*args, **kwargs)

    def drop_state(self) -> None:
        self.client.command(f"DROP TABLE IF EXISTS event SYNC")
        self.client.command(f"DROP TABLE IF EXISTS kafka SYNC")
        self.client.command(f"DROP TABLE IF EXISTS tables SYNC")
        self.client.command(f"DROP TABLE IF EXISTS node SYNC")
        self.client.command(f"DROP TABLE IF EXISTS pipe SYNC")
        self.client.command(f"DROP TABLE IF EXISTS source SYNC")
        self.client.command(f"DROP TABLE IF EXISTS state SYNC")

    def lock_state(self, force: bool = False) -> None:
        if force:
            self.client.command(
                """
                CREATE TABLE IF NOT EXISTS
                state_locked (ts DateTime64(3))
                ENGINE = MergeTree() ORDER BY ts
            """
            )
        else:
            # create will fail if state is already locked (table exists)
            self.client.command(
                """
                CREATE TABLE state_locked (ts DateTime64(3))
                ENGINE = MergeTree() ORDER BY ts
                """
            )
        self.client.command("INSERT INTO state_locked VALUES (now64(3))")

    def unlock_state(self) -> None:
        self.client.command(
            """
            DROP TABLE IF EXISTS state_locked SYNC
            """
        )
