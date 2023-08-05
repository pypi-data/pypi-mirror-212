import multiprocessing as mp
import sqlite3

import pytest
from clickhouse_connect.driver.exceptions import DatabaseError  # type: ignore

from airfold.storage.ch import Clickhouse
from airfold.storage.sqlite import Sqlite


def test_lock_clickhouse(wait_for_clickhouse, start_method) -> None:
    storage = Clickhouse(host="localhost")
    storage.client.command("DROP DATABASE IF EXISTS test")
    storage.client.command("CREATE DATABASE test")
    storage.drop_state()
    storage.init_state()

    assert storage.state_exists()

    def child1():
        storage = Clickhouse(host="localhost")

        with pytest.raises(DatabaseError):
            storage.lock_state()

    storage.lock_state()
    p = mp.Process(target=child1)
    p.start()
    p.join(5)

    assert p.exitcode == 0

    storage.unlock_state()

    def child2():
        storage = Clickhouse(host="localhost")

        storage.lock_state()
        assert storage.state_exists()
        storage.unlock_state()

    p = mp.Process(target=child2)
    p.start()
    p.join(5)

    assert p.exitcode == 0


def test_lock_sqlite(tmp_file, start_method) -> None:
    storage = Sqlite(tmp_file.name)
    storage.drop_state()
    storage.init_state()

    assert storage.state_exists()

    def child1():
        storage = Sqlite(tmp_file.name)

        with pytest.raises(sqlite3.OperationalError):
            storage.lock_state()

    storage.lock_state()
    p = mp.Process(target=child1)
    p.start()
    p.join(5)

    assert p.exitcode == 0

    storage.unlock_state()

    def child2():
        storage = Sqlite(tmp_file.name)

        storage.lock_state()
        assert storage.state_exists()
        storage.unlock_state()

    p = mp.Process(target=child2)
    p.start()
    p.join(5)

    assert p.exitcode == 0
