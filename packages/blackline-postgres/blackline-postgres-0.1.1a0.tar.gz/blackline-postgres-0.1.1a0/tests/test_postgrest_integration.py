import os
from typing import List

import pytest
import yaml
from blackline.factories.query import QueryFactory
from blackline.models.datastores import DataStore
from blackline.models.postgres.postgres import PostgresConfig
from psycopg import Connection


def test_postgrest_store_config(stores_yaml: str):
    # Setup
    pg_store_info = yaml.safe_load(stores_yaml)

    # Run
    store_config = DataStore.parse_obj(pg_store_info)

    # Assert
    isinstance(store_config.profiles["dev"], PostgresConfig)


def test_query_factory_postgres_queries(
    postgres_query_factory: QueryFactory,
):
    # Run
    queries = postgres_query_factory.queries()

    # Assert
    assert (
        queries[0].sql
        == "UPDATE test_table\nSET\n  email = %(email_value)s,\n  name = null\nWHERE created_at < %(cutoff)s"  # noqa: E501
    )
    assert (
        queries[1].sql
        == "UPDATE test_table\nSET\n  ip = REGEXP_REPLACE(ip,'\\w',%(ip_value)s,'g')\nWHERE created_at < %(cutoff)s"  # noqa: E501
    )


@pytest.mark.skipif(
    os.getenv("GITHUB_ACTIONS") == "true",
    reason="Github Actions does not have a local postgres",
)
def test_query_factory_postgres_execution(
    load_database: Connection,
    postgres_query_factory: QueryFactory,
    test_table: str,
    deidentified_mock_data: List,
):
    # Run
    queries = postgres_query_factory.queries()
    queries[0].execute()
    queries[1].execute()

    # Assert
    with queries[0].adapter.connection() as conn:
        cur = conn.execute(f"SELECT * FROM {test_table}")
        rows = cur.fetchall()

    # Remove the id UUID from the rows
    rows = [row[1:] for row in rows]

    assert set(deidentified_mock_data) == set(rows)
