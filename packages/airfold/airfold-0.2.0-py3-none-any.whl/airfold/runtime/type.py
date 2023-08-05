from typing import Any

from airfold.runtime.ch import Clickhouse, ClickhouseCloud
from airfold.runtime.ch_cluster import ClickhouseCluster

RUNTIME: dict[str, Any] = {
    "clickhouse": Clickhouse,
    "clickhouse_cluster": ClickhouseCluster,
    "clickhouse_cloud": ClickhouseCloud,
}
