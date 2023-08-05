import yaml

from airfold.runtime.ch import ChNode


def test_settings():
    # language=YAML
    file = """
---
- node:
    sql: SELECT 1
    settings: |
      AggregatingMergeTree() ORDER BY tuple()
"""
    data = yaml.safe_load(file)
    s = ChNode(**{**data[0]["node"], "name": "node"}).settings_str()
    assert s == "AggregatingMergeTree() ORDER BY tuple()"

    # language=YAML
    file = """
---
- node:
    sql: SELECT 1
    settings:
      engine: AggregatingMergeTree()
      order_by: tuple()
"""
    data = yaml.safe_load(file)
    s = ChNode(**{**data[0]["node"], "name": "node"}).settings_str()
    assert s == "AggregatingMergeTree() ORDER BY tuple()"

    # language=YAML
    file = """
---
- node:
    sql: SELECT 1
    settings:
      engine: AggregatingMergeTree()
      primary_key: key
      order_by: tuple()
"""
    data = yaml.safe_load(file)
    s = ChNode(**{**data[0]["node"], "name": "node"}).settings_str()
    assert s == "AggregatingMergeTree() PRIMARY KEY key ORDER BY tuple()"

    # language=YAML
    file = """
---
- node:
    sql: SELECT 1
    settings:
      - 'AggregatingMergeTree()'
      - primary_key: key
        order_by: tuple()
"""
    data = yaml.safe_load(file)
    s = ChNode(**{**data[0]["node"], "name": "node"}).settings_str()
    assert s == "AggregatingMergeTree() PRIMARY KEY key ORDER BY tuple()"

    # language=YAML
    file = """
---
- node:
    sql: SELECT 1
    settings:
      - 'some new clickhouse syntax'
      - primary_key: key
        order_by: tuple()
      - 'some other new syntax'
"""
    data = yaml.safe_load(file)
    s = ChNode(**{**data[0]["node"], "name": "node"}).settings_str()
    assert s == "some new clickhouse syntax PRIMARY KEY key ORDER BY tuple() some other new syntax"

    # language=YAML
    file = """
---
- node:
    sql: SELECT 1
    settings:
      engine: MergeTree
      primary_key: (id, toStartOfDay(timestamp), timestamp)
      ttl_table: |
        timestamp + INTERVAL 1 DAY
        GROUP BY id, toStartOfDay(timestamp)
        SET
            max_hits = max(max_hits),
            sum_hits = sum(sum_hits)
"""
    data = yaml.safe_load(file)
    s = ChNode(**{**data[0]["node"], "name": "node"}).settings_str()
    assert (
        s
        == """MergeTree PRIMARY KEY (id, toStartOfDay(timestamp), timestamp) TTL timestamp + INTERVAL 1 DAY
GROUP BY id, toStartOfDay(timestamp)
SET
    max_hits = max(max_hits),
    sum_hits = sum(sum_hits)"""
    )

    # language=YAML
    file = """
---
- node:
    sql: SELECT 1
    settings:
      engine: AggregatingMergeTree()
      primary_key: key
      order_by: tuple()
      settings:
        max_suspicious_broken_parts: 500
        parts_to_throw_insert: 100
"""
    data = yaml.safe_load(file)
    s = ChNode(**{**data[0]["node"], "name": "node"}).settings_str()
    assert (
        s == "AggregatingMergeTree() PRIMARY KEY key ORDER BY tuple() SETTINGS max_suspicious_broken_parts=500 "
        "parts_to_throw_insert=100"
    )
