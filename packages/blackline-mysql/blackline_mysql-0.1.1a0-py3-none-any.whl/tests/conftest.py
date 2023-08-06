"""
Some fixtures are mocked to avoid having to connect to a real database.
A mysql database is available while running tests locally using docker-compose.
The database is not available when running tests on github actions.
The envionment variable GITHUB_ACTIONS is set to true when running on github actions.
https://docs.github.com/en/actions/learn-github-actions/variables#default-environment-variables
"""


import os
from typing import Callable, Generator

import pytest
import yaml
from blackline.adapters.mysql.mysql import MySQLAdapter
from blackline.factories.query import QueryFactory
from blackline.models.mysql.mysql import MySQLConfig
from blackline.utils.testing.conftest_shared import *  # noqa: F403, F401
from mysql.connector import MySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.cursor import MySQLCursor
from pytest import MonkeyPatch


@pytest.fixture
def github_actions_mysql() -> bool:
    if os.getenv("GITHUB_ACTIONS") == "true":
        """This will help testing the monkeypatches locally.
        If set to true, the connections to mysql will fail if not correctly mocked.
        """
        return True
    return False


@pytest.fixture
def mysql_store_name() -> str:
    return "test_mysql"


@pytest.fixture
def mysql_user() -> str:
    return os.environ.get("MYSQL_USER", "no_user_set")


@pytest.fixture
def mysql_password() -> str:
    return os.environ.get("MYSQL_PASSWORD", "no_password_set")


@pytest.fixture
def mysql_host() -> str:
    return os.environ.get("MYSQL_HOST", "127.0.0.1")


@pytest.fixture
def mysql_port() -> int:
    if os.getenv("GITHUB_ACTIONS") == "true":
        """This will help testing the monkeypatches locally.
        If set to true, the connections to mysql will fail if not correctly mocked.
        """
        return 5555
    return int(os.environ.get("MYSQL_PORT", 3306))


@pytest.fixture
def mysql_db() -> str:
    return os.environ.get("MYSQL_DB", "no_db_set")


@pytest.fixture
def stores_yaml(
    mysql_store_name: str,
    mysql_user: str,
    mysql_password: str,
    mysql_host: str,
    mysql_port: int,
    mysql_db: str,
) -> str:
    """https://www.mysqlql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS"""
    return f"""
    name: {mysql_store_name}
    profiles:
      dev:
        type: mysql
        config:
          connection:
            user: {mysql_user}
            password: {mysql_password}
            database: {mysql_db}
            host: {mysql_host}
            port: {mysql_port}
        """


@pytest.fixture
def mysql_connection(
    mysql_user: str,
    mysql_password: str,
    mysql_host: str,
    mysql_port: str,
    mysql_db: str,
    github_actions_mysql: bool,
    monkeypatch: MonkeyPatch,
) -> MySQLConnection:
    if github_actions_mysql:

        def __init__(self, **kwargs):
            self._consume_results = False
            self._unread_result = False
            if kwargs:
                self.connect(**kwargs)

        def cursor(self, *args, **kwargs) -> MySQLCursor:
            return MySQLCursor(self)

        monkeypatch.setattr(MySQLConnection, "__init__", __init__)
        monkeypatch.setattr(MySQLConnection, "close", lambda self: None)
        monkeypatch.setattr(MySQLConnection, "cursor", cursor)
        monkeypatch.setattr(MySQLConnection, "commit", lambda self: None)
        monkeypatch.setattr(MySQLConnection, "is_connected", lambda self: True)
        monkeypatch.setattr(
            MySQLConnectionAbstract, "connect", lambda self, **kwargs: None
        )
        monkeypatch.setattr(MySQLCursor, "execute", lambda self, *args, **kwargs: None)
        monkeypatch.setattr(
            MySQLCursor, "executemany", lambda self, *args, **kwargs: None
        )

    return MySQLConnection(
        user=mysql_user,
        password=mysql_password,
        host=mysql_host,
        port=mysql_port,
        database=mysql_db,
    )


@pytest.fixture
def load_database(
    mysql_connection: MySQLConnection, mock_data: list, test_table: str
) -> Generator[MySQLConnectionAbstract, None, None]:
    with mysql_connection as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"DROP TABLE IF EXISTS {test_table}")
            cursor.execute(
                f"""
                CREATE TABLE {test_table} (
                    id CHAR(36) DEFAULT (UUID()) UNIQUE,
                    created_at TIMESTAMP,
                    name VARCHAR(255),
                    email VARCHAR(255) NOT NULL,
                    postal_code VARCHAR(15) UNIQUE,
                    active BOOLEAN,
                    ip VARCHAR(15),
                    CHECK (created_at > '2020-01-01 00:00:00'),
                    PRIMARY KEY (`id`)
                    )"""
            )
            cursor.executemany(
                f"INSERT INTO {test_table} (created_at, name, email, postal_code, active, ip) VALUES (%s, %s, %s, %s, %s, %s)",  # noqa: E501
                mock_data,
            )
            conn.commit()

            yield conn

            cursor.execute(f"DROP TABLE IF EXISTS {test_table}")


@pytest.fixture
def mysql_adapter(
    stores_yaml: str,
    mysql_connection: MySQLConnection,
) -> MySQLAdapter:
    store_obj = yaml.safe_load(stores_yaml)
    mysql_obj = store_obj["profiles"]["dev"]
    pg_config = MySQLConfig.parse_obj(mysql_obj)
    return MySQLAdapter(config=pg_config.config)


@pytest.fixture
def mysql_query_factory(
    query_factory_factory: Callable,
    mysql_adapter: MySQLAdapter,
) -> QueryFactory:
    return query_factory_factory(adapter=mysql_adapter)
