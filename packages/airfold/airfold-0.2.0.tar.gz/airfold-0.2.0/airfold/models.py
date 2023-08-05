from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, constr, validator

from airfold.type import Schema
from airfold.utils import uuid


def validate_sql_cols(sql: str | None, cols: Schema | None) -> None:
    if sql and cols:
        raise ValueError(f"Cannot define both `sql` ({sql}) and `cols`: ({cols})")


class SourceType(Enum):
    """Source type"""

    KAFKA = "kafka"
    """Kafka producer source"""
    PIPE = "pipe"
    """Airfold pipe as a source"""
    TABLE = "table"
    """SQL table as a source"""


class EventTarget(Enum):
    """Event target type for event log"""

    KAFKA = "kafka"
    """Kafka producer"""
    PIPE = "pipe"
    """Airfold pipe"""
    SOURCE = "source"
    """Airfold source"""
    NODE = "node"
    """Airfold parsed node"""
    TABLE = "table"
    """SQL table source"""
    NODE_ENTRY = "node_entry"
    """Airfold stored node"""


class EventType(Enum):
    """Event action type"""

    CREATE = "create"
    """Target was created"""
    DELETE = "delete"
    """Target was deleted"""
    UPDATE = "update"
    """Target was updated"""


class Source(BaseModel, frozen=True):
    """Airfold source definition"""

    id: str = Field(default_factory=lambda: uuid())
    """unique source id"""
    target_id: str
    """target source id"""
    name: str  # name for indirection and display
    """source display name"""
    type: SourceType = Field(default=SourceType.TABLE)
    """source type"""


class PipeEntry(BaseModel, frozen=True):
    """Airfold pipe definition"""

    id: str = Field(default_factory=lambda: uuid())
    """unique pipe id"""
    source_id: str
    """source id"""
    nodes: list[str]  # To preserve order when reconstructing the pipe
    """ordered list of node ids"""
    last_node: int
    """index of the last node in pipe"""


class NodeEntry(BaseModel, frozen=True):
    """Airfold stored node definition"""

    id: str = Field(default_factory=lambda: uuid())  # internal physical name
    """unique node id"""
    name: str  # name for indirection and display
    """node display name"""
    sql: str
    """node transformation SQL"""
    description: str | None
    """node description"""
    deps: list[str]
    """node dependencies (list of ids)"""
    pipe_id: str
    """node parent pipe"""
    union: str | None
    """union all results with that node"""
    target_id: str | None
    """target id for materialization"""
    settings: str | None
    """runtime-specific node settings"""


class Kafka(BaseModel, frozen=True):
    """Kafka producer definition"""

    id: str = Field(default_factory=lambda: uuid())  # internal physical name
    """kafka unique id"""
    topic: str
    """kafka topic"""
    host: str
    """kafka host"""
    port: int
    """kafka port"""
    cols: Schema
    """columns definition, schema"""
    settings: Any | None = Field(title="settings", description="runtime-specific settings for kafka")


class Table(BaseModel, frozen=True):
    """ "Airfold table source definition"""

    id: str = Field(default_factory=lambda: uuid())  # internal physical name
    """table unique id"""
    cols: Schema | None
    """columns definition, schema"""
    sql: str | None
    """columns definition, from SQL"""
    settings: Any | None = Field(title="settings", description="runtime-specific settings for the table")

    @validator("sql")
    def validate_sql(cls, v: Any, values: dict):
        if v and "cols" in values:
            validate_sql_cols(sql=v, cols=values["cols"])
        return v

    @validator("cols")
    def validate_cols(cls, v: Any, values: dict):
        if v and "sql" in values:
            validate_sql_cols(sql=values["sql"], cols=v)
        return v


class View(BaseModel, frozen=True):
    """View definition"""

    id: str = Field(default_factory=lambda: uuid())  # internal physical name
    """view unique id"""
    sql: str | None
    """view SQL"""
    target: str | None
    """view target: `SELECT * FROM target`"""
    settings: Any | None = Field(title="settings", description="runtime-specific settings for the view")


class Event(BaseModel, frozen=True):
    """Event log entry"""

    id: str = Field(default_factory=lambda: uuid())  # internal physical name
    """event id"""
    target_id: str
    """event target id"""
    type: EventType
    """event action type"""
    target: EventTarget
    """event target type"""
    timestamp: int
    """event timestamp"""
    result: str
    """event status"""
    error: str
    """event error, if present"""
    message: str
    """event log message"""


class Node(BaseModel, frozen=True):
    """
    SQL transformation node
    """

    id: str = Field(default_factory=lambda: uuid())
    name: str = Field(title="name", description="node name")
    description: constr(strip_whitespace=True) | None = Field(  # type: ignore
        title="description", description="short description of the node"
    )
    sql: constr(strip_whitespace=True) = Field(title="sql", description="SQL query definition")  # type: ignore
    union: str | None = Field(title="union", description="union all results with that node")
    target_id: str | None = Field(title="target_id", description="node target, if materialized")
    settings: Any | None = Field(title="settings", description="runtime-specific settings for the node")

    @classmethod
    def from_node_entry(cls, node_entry: NodeEntry) -> "Node":
        return Node(**node_entry.dict())


class Pipe(BaseModel, frozen=True):
    """
    Chain of SQL transformation nodes
    """

    id: str = Field(default_factory=lambda: uuid())
    name: str = Field(title="name", description="pipe name")
    nodes: list[Node] = Field(title="nodes", description="ordered list of pipe nodes")
    last_node: int = Field(title="last_node", description="index of the last node in the pipe")
    to: str | None = Field(title="to", description="source to materialize to")
