import json
import os
from abc import ABC, abstractmethod
from io import TextIOWrapper
from typing import overload

from airfold.models import Kafka, Table, View, Node, Pipe
from airfold.parse import SQLParser
from airfold.storage.storage import Storage


class Runtime(ABC):
    """Airfold runtime interface.
    Every runtime class should implement it.
    """

    @overload
    def parse(self, obj: Pipe, storage: Storage) -> Pipe:
        ...

    @overload
    def parse(self, obj: Table, storage: Storage) -> Table:
        ...

    @abstractmethod
    def parse(self, obj: Pipe | Table, storage: Storage) -> Pipe | Table:
        """Parses pipe.
        Resolve the identifiers, transpile dialect, etc.

        Args:
            obj: Object to be parsed
            storage: Storage to be queried for metadata

        Returns:
            parsed Pipe
        """
        ...

    @abstractmethod
    def create_table(self, table: Table) -> Table:
        """Create source table.
        Pipelines can be driven off tables, if needed.

        Args:
            table: Table object

        Returns:
            runtime-specific Table object
        """
        pass

    @abstractmethod
    def delete_table(self, id: str) -> None:
        """Delete a table source,

        Args:
            id: table unique id
        """
        pass

    @abstractmethod
    def create_node(self, node: Node) -> None:
        """Create a node.

        Args:
            node: Node object
            table_id: target table id
        """
        pass

    @abstractmethod
    def drop_node(self, id: str) -> None:
        """Drop a node.

        Args:
            id: node unique id
        """
        pass

    @abstractmethod
    def create_view(self, view: View) -> View:
        """Create a new view.

        Args:
            view: View object

        Returns:
            runtime-specific view object
        """
        pass

    @abstractmethod
    def drop_view(self, id: str) -> None:
        """Drop a view.

        Args:
            id: view unique id
        """
        pass

    @abstractmethod
    def create_kafka(self, kafka: Kafka, name: str) -> Kafka:
        """Create a Kafka source.

        Args:
            kafka: Kafka object
            name: name of the source
        """
        pass

    @abstractmethod
    def delete_kafka(self, id: str) -> None:
        """Delete Kafka source.

        Args:
            id: unique id
        """
        pass

    @abstractmethod
    def get_parser(self) -> SQLParser:
        """Get SQL parser for the runtime

        Returns:
            SQL parser class
        """
        pass


class SqlRuntime(Runtime):
    def __init__(self) -> None:
        dump_path = os.environ.get("AIRFOLD_DUMP_SQL", None)
        self.dump: TextIOWrapper | None = None
        if dump_path:
            self.dump = open(dump_path, "a")

    @abstractmethod
    def sql_command(self, sql: str, *args, **kwargs) -> None:
        pass

    def execute(self, sql: str, *args, **kwargs) -> None:
        if self.dump:
            self.dump.write(f"{sql};\n")
            if kwargs and len(kwargs) > 0:
                self.dump.write(json.dumps(kwargs) + "\n")
            self.dump.flush()
        return self.sql_command(sql, *args, **kwargs)
