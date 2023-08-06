import os
from typing import List

import pytest
import yaml
from blackline.factories.query import QueryFactory
from blackline.models.datastores import DataStore
from blackline.models.mysql.mysql import MySQLConfig
from mysql.connector import MySQLConnection


def test_mysql_store_config(stores_yaml: str):
    # Setup
    pg_store_info = yaml.safe_load(stores_yaml)

    # Run
    store_config = DataStore.parse_obj(pg_store_info)

    # Assert
    isinstance(store_config.profiles["dev"], MySQLConfig)


def test_query_factory_mysql_queries(
    mysql_query_factory: QueryFactory,
):
    # Run
    queries = mysql_query_factory.queries()

    # Assert
    assert (
        queries[0].sql
        == "UPDATE test_table\nSET\n  email = %(email_value)s,\n  name = null\nWHERE created_at < %(cutoff)s"  # noqa: E501
    )
    assert (
        queries[1].sql
        == "UPDATE test_table\nSET\n  ip = REGEXP_REPLACE(ip,'[:alnum:]',%(ip_value)s)\nWHERE created_at < %(cutoff)s"  # noqa: E501
    )


@pytest.mark.skipif(
    os.getenv("GITHUB_ACTIONS") == "true",
    reason="Github Actions does not have a local mysql",
)
def test_query_factory_mysql_execution(
    load_database: MySQLConnection,
    mysql_query_factory: QueryFactory,
    test_table: str,
    deidentified_mock_data: List,
):
    # Run
    queries = mysql_query_factory.queries()
    queries[0].execute()
    queries[1].execute()

    # Assert
    with queries[0].adapter.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {test_table}")
            rows = cursor.fetchall()

    # Remove the UUIS from the rows
    rows = [row[1:] for row in rows]

    # breakpoint()
    assert set(deidentified_mock_data) == set(rows)
