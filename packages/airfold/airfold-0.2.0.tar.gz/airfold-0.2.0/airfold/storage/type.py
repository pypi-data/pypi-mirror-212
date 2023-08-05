from typing import Any

from airfold.storage.ch import Clickhouse, ClickhouseCluster, ClickhouseCloud
from airfold.storage.sqlite import Sqlite

STORAGE: dict[str, Any] = {
    "clickhouse": Clickhouse,
    "clickhouse_cluster": ClickhouseCluster,
    "clickhouse_cloud": ClickhouseCloud,
    "sqlite": Sqlite,
}
