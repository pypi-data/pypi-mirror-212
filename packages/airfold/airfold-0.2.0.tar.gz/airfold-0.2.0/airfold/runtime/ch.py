import json
from typing import Any, Dict, overload, Optional, Union, Callable, cast

from clickhouse_connect import create_client  # type: ignore
from clickhouse_connect.driver.client import Client  # type: ignore
from clickhouse_connect.driver.query import quote_identifier as I  # type: ignore
from pydantic import BaseModel, Field, typing
from pydantic.utils import ROOT_KEY
from sqlglot.dialects import ClickHouse

from airfold.log import log
from airfold.models import Kafka, Table, View, Node, Pipe
from airfold.parse import SQLParser
from airfold.runtime.runtime import SqlRuntime
from airfold.storage.storage import Storage
from airfold.type import Schema

if typing.TYPE_CHECKING:
    from pydantic.typing import AbstractSetIntStr, MappingIntStrAny


def to_db_schema(cols: Schema) -> str:
    return ", ".join([f"{I(col)} {cols[col]}" for col in cols])


def get_field(obj: Any, field: str) -> str | None:
    return getattr(obj, field, getattr(obj, "get", lambda x: None)(field))


def get_engine_settings(settings: Any) -> str | None:
    if settings is None:
        return settings
    elif isinstance(settings, str):
        return settings.strip()
    elif isinstance(settings, list):
        return " ".join([v for s in settings if (v := get_engine_settings(s)) is not None]).strip()
    elif isinstance(settings, dict):
        return " ".join([f"{k}={v}" for k, v in settings.items()]).strip()
    return ""


def get_settings_str(settings: Any) -> str | None:
    if settings is None:
        return settings
    elif isinstance(settings, str):
        return settings.strip()
    elif isinstance(settings, list):
        return " ".join([v for s in settings if (v := get_settings_str(s)) is not None]).strip()
    result: list[str] = []
    engine = get_field(settings, "engine")
    if engine:
        result.append(engine)
    partition_by = get_field(settings, "partition_by")
    if partition_by:
        result.append(f"PARTITION BY {partition_by}")
    primary_key = get_field(settings, "primary_key")
    if primary_key:
        result.append(f"PRIMARY KEY {primary_key}")
    order_by = get_field(settings, "order_by")
    if order_by:
        result.append(f"ORDER BY {order_by}")
    sample_by = get_field(settings, "sample_by")
    if sample_by:
        result.append(f"SAMPLE BY {sample_by}")
    ttl_table = get_field(settings, "ttl_table")
    if ttl_table:
        result.append(f"TTL {ttl_table}")
    engine_settings = get_field(settings, "settings")
    if engine_settings:
        result.append(f"SETTINGS {get_engine_settings(engine_settings)}")
    return " ".join(result).strip()


EngineSettingsDict = Dict[str, Any]


class SettingsDict(BaseModel):
    engine: str | None = Field(description="Name and parameters of the engine, ex. `AggregatingMergeTree()`")
    partition_by: str | None = Field(description="The partitioning key, if needed")
    primary_key: str | None = Field(description="The primary key, if it differs from the sorting key")
    order_by: str | None = Field(description="The sorting key, ex. `(CounterID, EventDate)`")
    sample_by: str | None = Field(description="An expression for sampling")
    sharding_key: str | None = Field(description="Sharding key for clustered sharded tables")
    ttl_table: str | None = Field(
        description="A list of rules specifying storage duration of rows and "
        "defining logic of automatic parts movement between disks and volumes"
    )
    settings: EngineSettingsDict | list[EngineSettingsDict | str] | str | None = Field(
        description="Additional parameters that control the behavior of the engine"
    )


class ChNode(Node):
    """
    ClickHouse-specific SQL transformation node
    """

    settings: SettingsDict | list[SettingsDict | str] | str | None

    @classmethod
    def from_node(cls, node: Node) -> "ChNode":
        return cls(**node.dict())

    def settings_str(self) -> str | None:
        return get_settings_str(self.settings)

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        res: Dict[str, Any] = super().dict(*args, **kwargs)
        res["settings"] = self.settings_str()
        return res


class ChTable(Table):
    settings: SettingsDict | list[SettingsDict | str] | str | None

    @classmethod
    def from_table(cls, table: Table) -> "ChTable":
        return cls(**table.dict())

    def settings_str(self) -> str | None:
        return get_settings_str(self.settings)

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        res: Dict[str, Any] = super().dict(*args, **kwargs)
        res["settings"] = self.settings_str()
        return res

    def json(
        self,
        *,
        include: Optional[Union["AbstractSetIntStr", "MappingIntStrAny"]] = None,
        exclude: Optional[Union["AbstractSetIntStr", "MappingIntStrAny"]] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        models_as_dict: bool = True,
        **dumps_kwargs: Any,
    ) -> str:
        encoder = cast(Callable[[Any], Any], self.__json_encoder__)
        data = self.dict(
            by_alias=by_alias,
            include=include,
            exclude=exclude,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
        if self.__custom_root_type__:
            data = data[ROOT_KEY]
        return json.dumps(data, default=encoder, **dumps_kwargs)


class Clickhouse(SqlRuntime):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        log.info(f"Initializing runtime: Clickhouse")
        self.client: Client = create_client(*args, **kwargs)
        # language=SQL
        self.client.command("SET allow_experimental_object_type=1")
        self.parser = SQLParser(ClickHouse())

    def sql_command(self, sql: str, *args, **kwargs) -> None:
        log.debug(f"SQL command: {sql}, params={kwargs.get('parameters')}")
        self.client.command(sql, *args, **kwargs)

    @overload
    def parse(self, obj: Pipe, storage: Storage) -> Pipe:
        ...

    @overload
    def parse(self, obj: Table, storage: Storage) -> Table:
        ...

    def parse(self, obj: Pipe | Table, storage: Storage) -> Pipe | Table:
        if isinstance(obj, Pipe):
            pipe: Pipe = obj
            log.info(f"Parsing pipe {pipe}")

            nodes = [ChNode.from_node(node) for node in pipe.nodes]
            pipe = Pipe(**{**pipe.dict(), "nodes": nodes})

            return pipe
        elif isinstance(obj, Table):
            table: Table = obj
            log.info(f"Parsing table {table}")

            return ChTable.from_table(table)
        else:
            raise RuntimeError(f"Unknown object to parse: {obj}")

    def create_node(self, node: Node) -> None:
        log.info(f"Creating node {node.id}")

        # language=SQL
        cmd = f"""
            CREATE MATERIALIZED VIEW IF NOT EXISTS {I(node.id + '_mv')}
            TO {I(node.target_id)}
            AS {node.sql} """
        log.info(cmd)
        self.execute(cmd)

    def drop_node(self, id: str) -> None:
        log.info(f"Deleting node {id}")
        self.execute(f"DROP TABLE IF EXISTS {I(id + '_mv')}")

    def create_view(self, view: View) -> View:
        log.info(f"Creating view {view.id}")
        sql = view.sql
        if view.target is not None:
            sql = f"SELECT * FROM {I(view.target)}"
        cmd: str = f"""
            CREATE VIEW IF NOT EXISTS {I(view.id)}
            AS {sql} """
        self.execute(cmd)
        return view

    def drop_view(self, id: str) -> None:
        log.info(f"Deleting view {id}")
        self.execute(f"DROP VIEW IF EXISTS {I(id)}")

    def _get_schema_query(self, table: Table) -> tuple[str, str]:
        schema: str
        query: str
        if table.sql is not None:
            schema = ""
            query = f"EMPTY AS {table.sql}"
        else:
            assert table.cols
            schema = f"({to_db_schema(table.cols)})"
            query = ""
        return schema, query

    def create_table(self, table: Table) -> Table:
        assert isinstance(table, ChTable)
        log.info(f"Creating table {table.id}")

        settings = table.dict()["settings"]
        if not settings:
            settings = "MergeTree() ORDER BY tuple()"

        schema, query = self._get_schema_query(table)
        cmd: str = f"""
            CREATE TABLE IF NOT EXISTS {I(table.id)}
            {schema}
            ENGINE = {settings}
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
        return table

    def delete_table(self, id: str) -> None:
        log.info(f"Deleting table {id}")
        self.execute(f"DROP TABLE IF EXISTS {I(id)}")

    def create_kafka(self, kafka: Kafka, name: str) -> Kafka:
        log.info(f"Creating kafka {kafka.id}")
        cmd: str = f"""
            CREATE TABLE IF NOT EXISTS {I(kafka.id)}
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
        return kafka

    def delete_kafka(self, table_id: str) -> None:
        log.info(f"Deleting kafka {table_id}")
        self.execute(f"DROP TABLE IF EXISTS {I(table_id)}")

    def get_parser(self) -> SQLParser:
        return self.parser


class ClickhouseCloud(Clickhouse):
    def __init__(self, *args, **kwargs):
        kwargs = kwargs or {}
        kwargs["secure"] = True
        super().__init__(*args, **kwargs)
