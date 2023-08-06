"""
Some fixtures are mocked to avoid having to connect to a real database.
A postgres database is available while running tests locally using docker-compose.
The database is not available when running tests on github actions.
The envionment variable GITHUB_ACTIONS is set to true when running on github actions.
https://docs.github.com/en/actions/learn-github-actions/variables#default-environment-variables
"""


import os
from typing import Callable, Generator

import pytest
import yaml
from blackline.adapters.postgres.postgres import PostgresAdapter
from blackline.factories.query import QueryFactory
from blackline.models.postgres.postgres import PostgresConfig
from blackline.utils.testing.conftest_shared import *  # noqa: F403, F401
from psycopg import Connection, Cursor
from psycopg.pq import PGconn
from psycopg.sql import SQL, Identifier
from pytest import MonkeyPatch


@pytest.fixture
def github_actions_pg() -> bool:
    if os.getenv("GITHUB_ACTIONS") == "true":
        """This will help testing the monkeypatches locally.
        If set to true, the connections to postgres will fail if not correctly mocked.
        """
        return True
    return False


@pytest.fixture
def postgres_store_name() -> str:
    return "test_postgres"


@pytest.fixture
def postgres_user() -> str:
    return os.environ.get("POSTGRES_USER", "no_user_set")


@pytest.fixture
def postgres_password() -> str:
    return os.environ.get("POSTGRES_PASSWORD", "no_password_set")


@pytest.fixture
def postgres_host() -> str:
    return os.environ.get("POSTGRES_HOST", "127.0.0.1")


@pytest.fixture
def postgres_port() -> int:
    if os.getenv("GITHUB_ACTIONS") == "true":
        """This will help testing the monkeypatches locally.
        If set to true, the connections to postgres will fail if not correctly mocked.
        """
        return 5555
    return int(os.environ.get("POSTGRES_PORT", 5432))


@pytest.fixture
def postgres_db() -> str:
    return os.environ.get("POSTGRES_DB", "no_db_set")


@pytest.fixture
def stores_yaml(
    postgres_store_name: str,
    postgres_user: str,
    postgres_password: str,
    postgres_host: str,
    postgres_port: str,
    postgres_db: str,
) -> str:
    """https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS"""
    return f"""
    name: {postgres_store_name}
    profiles:
      dev:
        type: postgres
        config:
          connection:
            conninfo:
              host: {postgres_host}
              port: {postgres_port}
              dbname: {postgres_db}
              user: {postgres_user}
              password: {postgres_password}
        """


@pytest.fixture
def postgres_connection(
    postgres_user: str,
    postgres_password: str,
    postgres_host: str,
    postgres_port: str,
    postgres_db: str,
    github_actions_pg: bool,
    monkeypatch: MonkeyPatch,
) -> Connection:
    conninfo = f"host={postgres_host} port={postgres_port} dbname={postgres_db} user={postgres_user} password={postgres_password}"  # noqa: E501

    if github_actions_pg:

        def _connect(*args, **kwargs):
            conn_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"  # noqa: E501
            conn_str = f"host={postgres_host} port={postgres_port} dbname={postgres_db} user={postgres_user} password={postgres_password}"  # noqa: E501
            if args:
                assert args[0] == conn_str or args[0] == conn_url
            if kwargs:
                assert kwargs["conninfo"] == conn_str or kwargs["conninfo"] == conn_url
            return Connection(pgconn=PGconn())

        monkeypatch.setattr(Connection, "connect", _connect)
        monkeypatch.setattr(Connection, "commit", lambda self: None)
        monkeypatch.setattr(Connection, "close", lambda self: None)
        monkeypatch.setattr(
            Connection, "cursor", lambda self, *args, **kwargs: Cursor(self)
        )
        monkeypatch.setattr(
            Connection, "execute", lambda self, *args, **kwargs: Cursor(self)
        )
        monkeypatch.setattr(Cursor, "execute", lambda self, *args, **kwargs: None)
        monkeypatch.setattr(Cursor, "executemany", lambda self, *args, **kwargs: None)

    return Connection.connect(conninfo)


@pytest.fixture
def load_database(
    postgres_connection: Connection, mock_data: list, test_table: str
) -> Generator[Connection, None, None]:
    with postgres_connection as conn:
        with conn.cursor() as cursor:
            cursor.execute(SQL("DROP TABLE IF EXISTS {table}").format(table=test_table))
            cursor.execute(
                SQL(
                    """
                CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
                CREATE TABLE {table} (
                    id UUID DEFAULT uuid_generate_v4() ,
                    created_at TIMESTAMP NOT NULL CHECK (created_at > '2020-01-01'),
                    name VARCHAR(255),
                    email VARCHAR(255) NOT NULL UNIQUE,
                    postal_code VARCHAR(15),
                    active BOOLEAN,
                    ip VARCHAR(15) NOT NULL,
                    CONSTRAINT pkey_tbl PRIMARY KEY ( id )
                    )"""
                ).format(table=Identifier(test_table))
            )
            cursor.executemany(
                SQL(
                    """INSERT INTO {table} (
                    created_at,
                    name,
                    email,
                    postal_code,
                    active,
                    ip
                    ) VALUES (%s, %s, %s, %s, %s, %s)"""
                ).format(table=Identifier(test_table)),
                mock_data,
            )
            conn.commit()

            yield conn

            cursor.execute(SQL("DROP TABLE IF EXISTS {table}").format(table=test_table))


@pytest.fixture
def postgres_adapter(
    stores_yaml: str,
    postgres_connection: Connection,
) -> PostgresAdapter:
    store_obj = yaml.safe_load(stores_yaml)
    postgres_obj = store_obj["profiles"]["dev"]
    pg_config = PostgresConfig.parse_obj(postgres_obj)
    return PostgresAdapter(config=pg_config.config)


@pytest.fixture
def postgres_query_factory(
    query_factory_factory: Callable,
    postgres_adapter: PostgresAdapter,
) -> QueryFactory:
    return query_factory_factory(adapter=postgres_adapter)
