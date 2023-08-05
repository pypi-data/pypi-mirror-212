from typing import Iterator

from sqlglot import Expression, exp, parse_one, Dialect

from airfold.log import log
from airfold.models import Node, Pipe, Table
from airfold.type import Lookup


class ParsingError(Exception):
    pass


IS_UNION = "<union>"


def get_last_node_index(nodes: list[Node]) -> int:
    idx = -1
    for i, n in enumerate(nodes):
        if n.union is None:
            idx = i
    return idx


def parse(data: dict, name: str) -> Pipe:
    log.info(f"Parsing pipe {data}")
    nodes: list[Node] = [Node(name=k, **v) for d in data["nodes"] for k, v in d.items()]
    idx = get_last_node_index(nodes)
    if idx < 0:
        raise ParsingError(f"Pipe has only union nodes")
    pipe: Pipe = Pipe(name=name, nodes=nodes, last_node=idx, to=data.get("to"))
    log.info(f"Parsed pipe {pipe}")
    return pipe


class SQLParser:
    def __init__(self, dialect) -> None:
        self.dialect: Dialect = dialect

    def get_table_names(self, sql: str) -> list[str]:
        expr: Expression = parse_one(sql, read=self.dialect)
        tables: Iterator[exp.Table] = expr.find_all(exp.Table)

        return [table.name for table in tables if table.name]

    def get_all_deps(self, node: Node):
        tables = self.get_table_names(node.sql)
        unions = [node.union] if node.union else []
        return tables + unions

    def check_sequentiality(self, nodes: list[Node]) -> None:
        log.info(f"Checking sequentiality of {nodes}")
        deps: list[list[str]] = [self.get_all_deps(node) for node in nodes]
        log.info(f"Found dependencies {deps}")

        indexes: list[list[int]] = [[i for i, node in enumerate(nodes) if node.name in dep] for dep in deps]
        log.info(f"Found indexes {indexes}")

        for i, index in enumerate(indexes):
            if any(j >= i for j in index):
                raise ParsingError(f"Node {nodes[i].name} depends on a later node")

    def replace(self, sql: str, lookup: Lookup, expr_type=exp.Table) -> str:
        expression_tree: Expression = parse_one(sql, read=self.dialect)

        log.info(f"Replacing {lookup} in {expression_tree}")

        def transformer(node):
            if isinstance(node, expr_type):
                if node.name in lookup:
                    node_id = lookup[node.name]
                    if node_id == IS_UNION:
                        raise ParsingError(f"Node {node.name} is a union node, other nodes cannot SELECT from it")
                    return expr_type(this=exp.Identifier(this=node_id, quoted=True))
            return node

        transformed_tree = expression_tree.transform(transformer)
        return transformed_tree.sql(dialect=self.dialect)

    def validate_deps(self, nodes: list[Node], sources: set[str]) -> bool:
        self.check_sequentiality(nodes)

        ids: set[str] = {node.id for node in nodes}
        froms: set[str] = sources | ids
        deps: set[str] = {dep for node in nodes for dep in self.get_all_deps(node)}

        if not deps.issubset(froms):
            raise Exception(f"Missing dependencies: {deps - froms}")

        return True

    def apply_ids(self, nodes: list[Node]) -> list[Node]:
        log.info(f"Applying ids to {nodes}")
        name_ids: Lookup = {
            node.name: node.target_id if node.union is None else IS_UNION for node in nodes if node.target_id
        }
        sqls: list[str] = [self.replace(node.sql, name_ids) for node in nodes]
        ret: list[Node] = [Node(**{**node.dict(), "sql": sql}) for node, sql in zip(nodes, sqls)]
        log.info(f"Applied ids to {ret}")
        return ret

    def apply_node_ids(self, nodes: list[Node], tables: list[Table]) -> list[Table]:
        log.info(f"Applying ids to {tables}")
        name_ids: Lookup = {
            node.name: node.target_id if node.union is None else IS_UNION for node in nodes if node.target_id
        }
        sqls: list[str | None] = [self.replace(table.sql, name_ids) if table.sql else table.sql for table in tables]
        ret: list[Table] = [Table(**{**table.dict(), "sql": sql}) for table, sql in zip(tables, sqls)]
        log.info(f"Applied ids to {ret}")
        return ret

    def parse_one(self, sql: str) -> Expression:
        return parse_one(sql, read=self.dialect)

    def sql(self, expression: Expression) -> str:
        return expression.sql(self.dialect)
