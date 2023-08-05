import re
from typing import Any

import sqlglot
from clickhouse_connect.driver.query import quote_identifier as I  # type: ignore
from sqlglot import Expression, exp

from airfold.log import log
from airfold.models import Kafka, Table, View, Node
from airfold.runtime.ch import Clickhouse, get_field, get_settings_str, ChTable, to_db_schema

DIALECT = sqlglot.Dialect.get_or_raise("clickhouse")


def get_cluster_settings_str(settings: Any, database: str) -> str | None:
    settings_str: str | None = get_settings_str(settings)
    if not settings_str:
        return settings_str
    create: Expression = sqlglot.parse_one(f"CREATE TABLE t (i UInt8) ENGINE = {settings_str}", read=DIALECT)
    engine: Expression | None = create.find(exp.EngineProperty)
    assert engine is not None
    engine_name: str = engine.this.this
    if engine_name.endswith("MergeTree"):
        engine.this.set("this", f"Replicated{engine_name}")
        path: Expression = exp.Literal.string(f"/clickhouse/tables/{{shard}}/{database}/{{uuid}}")
        replica: Expression = exp.Literal.string("{replica}")
        engine.this.args["expressions"].insert(0, path)
        engine.this.args["expressions"].insert(1, replica)
    return re.sub(r"^ENGINE\s*=\s*", "", create.args["properties"].sql(DIALECT))


def get_cluster_sharding(settings: Any) -> str:
    sharding_key = get_field(settings, "sharding_key")
    if sharding_key is None:
        sharding_key = "rand32()"
    return f", {sharding_key}"


class ClickhouseCluster(Clickhouse):
    def __init__(self, cluster: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cluster: str = cluster

    def local_table(self, name: str) -> str:
        return f"{name}_local"

    def local_mv(self, name: str) -> str:
        return f"{name}_mv_local"

    def create_node(self, node: Node) -> None:
        log.info(f"Creating node {node.id}")

        local_mv = self.local_mv(node.id)
        # language=SQL
        cmd = f"""
            CREATE MATERIALIZED VIEW IF NOT EXISTS {I(local_mv)} ON CLUSTER {I(self.cluster)}
            TO {I(node.target_id)}
            AS {node.sql} """
        log.info(cmd)
        self.execute(cmd)

    def _drop_table(self, name: str, view: bool = False):
        self.execute(
            f"""
            DROP {'VIEW' if view else 'TABLE'} IF EXISTS {I(name)}
            ON CLUSTER {I(self.cluster)} SYNC
        """
        )

    def drop_node(self, id: str) -> None:
        log.info(f"Deleting node {id}")
        self._drop_table(self.local_mv(id))

    def create_view(self, view: View) -> View:
        log.info(f"Creating view {view.id}")
        sql = view.sql
        if view.target is not None:
            sql = f"SELECT * FROM {I(view.target)}"
        log.debug(f"Database: {self.client.database}")
        cmd: str = f"""
            CREATE VIEW IF NOT EXISTS {I(view.id)} ON CLUSTER {I(self.cluster)}
            AS {sql} """
        self.execute(cmd)
        return view

    def drop_view(self, id: str) -> None:
        log.info(f"Deleting view {I(id)}")
        self._drop_table(id, view=True)

    def create_table(self, table: Table) -> Table:
        assert isinstance(table, ChTable)
        log.info(f"Creating table {table.id}")

        settings = table.dict()["settings"]
        if not settings:
            settings = "MergeTree() ORDER BY tuple()"

        settings_str: str | None = get_cluster_settings_str(settings, self.client.database)
        assert settings_str is not None

        schema, query = self._get_schema_query(table)
        local_table = self.local_table(table.id)
        cmd: str = f"""
            CREATE TABLE IF NOT EXISTS {I(local_table)}
            ON CLUSTER {I(self.cluster)}
            {schema}
            ENGINE = {settings_str}
            {query}
            """
        try:
            self.execute(cmd)
        except Exception as e:
            log.error(f"Error creating table {table.id}")
            log.error(e)
            log.error("Rolling back")
            self.delete_table(table.id)
            raise e

        sharding: str = get_cluster_sharding(table.settings)
        # language=SQL
        cmd = f"""
            CREATE TABLE IF NOT EXISTS {I(table.id)} ON CLUSTER {I(self.cluster)}
            AS {I(local_table)}
            ENGINE = Distributed(
                {I(self.cluster)},
                {I(self.client.database)},
                {I(local_table)}
                {sharding}
            )"""
        log.info(cmd)
        self.execute(cmd)
        return table

    def delete_table(self, table_id: str) -> None:
        log.info(f"Deleting table {I(table_id)}")
        self._drop_table(table_id)
        self._drop_table(self.local_table(table_id))

    def create_kafka(self, kafka: Kafka, name: str) -> Kafka:
        log.info(f"Creating kafka {kafka.id}")
        local_table = self.local_table(kafka.id)
        cmd: str = f"""
            CREATE TABLE IF NOT EXISTS {I(local_table)}
            ON CLUSTER {I(self.cluster)}
            ({to_db_schema(kafka.cols)})
            ENGINE = Kafka()
            SETTINGS
              kafka_broker_list = '{kafka.host}',
              kafka_topic_list = '{kafka.topic}',
              kafka_group_name = 'airfold.{kafka.topic}',
              kafka_format = 'JSONEachRow'
            """
        try:
            self.execute(cmd)
        except Exception as e:
            log.error(f"Error creating kafka {kafka.id}")
            log.error(e)
            log.error("Rolling back")
            self.delete_kafka(kafka.id)
            raise e
        sharding: str = get_cluster_sharding(kafka.settings)
        # language=SQL
        cmd = f"""
            CREATE TABLE IF NOT EXISTS {I(kafka.id)} ON CLUSTER {I(self.cluster)}
            AS {I(local_table)}
            ENGINE = Distributed(
                {I(self.cluster)},
                {I(self.client.database)},
                {I(local_table)}
                {sharding}
            )"""
        log.info(cmd)
        self.execute(cmd)
        return kafka

    def delete_kafka(self, table_id: str) -> None:
        log.info(f"Deleting kafka {I(table_id)}")
        self._drop_table(table_id)
        self._drop_table(self.local_table(table_id))
