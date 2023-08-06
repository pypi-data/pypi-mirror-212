import yaml
from blackline.adapters.postgres.postgres import PostgresAdapter
from blackline.models.postgres.postgres import PostgresConfig
from psycopg import Connection, Cursor
from pytest import MonkeyPatch


def test_connection(
    stores_yaml: str,
    monkeypatch: MonkeyPatch,
    postgres_connection: Connection,
    github_actions_pg: bool,
) -> None:
    # Setup
    store_obj = yaml.safe_load(stores_yaml)
    postgres_obj = store_obj["profiles"]["dev"]
    pg_config = PostgresConfig.parse_obj(postgres_obj)

    if github_actions_pg:
        monkeypatch.setattr(Cursor, "fetchone", lambda self: (1,))
        monkeypatch.setattr(
            Connection, "execute", lambda self, *args, **kwargs: Cursor(self)
        )

    # Run
    postgres_adapter = PostgresAdapter(config=pg_config.config)
    with postgres_adapter.connection() as conn:
        cur = conn.execute("SELECT 1")
        result = cur.fetchone()

    # Assert
    assert result is not None
    assert result[0] == 1


def test_test_connection(
    postgres_adapter: PostgresAdapter, monkeypatch: MonkeyPatch, github_actions_pg: bool
) -> None:
    # Setup
    if github_actions_pg:
        monkeypatch.setattr(Connection, "closed", 0)

    # Run & Assert
    assert postgres_adapter.test_connection()


def test_table_exists(
    monkeypatch: MonkeyPatch,
    github_actions_pg: bool,
    load_database: Connection,
    test_table: str,
    postgres_adapter: PostgresAdapter,
):
    # Setup
    if github_actions_pg:
        monkeypatch.setattr(
            Cursor,
            "fetchone",
            lambda self: (
                "public",
                test_table,
                "user",
                None,
                False,
                False,
                False,
                False,
            ),
        )

    # Run
    exists = postgres_adapter.table_exists(table=test_table)

    assert exists is True


def test_table_exists_does_not_exist(
    monkeypatch: MonkeyPatch,
    github_actions_pg: bool,
    load_database: Connection,
    test_table: str,
    postgres_adapter: PostgresAdapter,
):
    # Setup
    nonexistent_table = "nonexistent_table"
    if github_actions_pg:
        monkeypatch.setattr(
            Cursor,
            "fetchone",
            lambda self: None,
        )

    # Run
    exists = postgres_adapter.table_exists(table=nonexistent_table)

    # Assert
    assert exists is False


def test_columns(
    monkeypatch: MonkeyPatch,
    github_actions_pg: bool,
    load_database: Connection,
    test_table: str,
    postgres_adapter: PostgresAdapter,
):
    # Setup
    def _columns_from_table(self, table: str):
        return [
            (
                "created_at",
                "timestamp without time zone",
                "NO",
                "CHECK",
                "CHECK ((created_at > '2020-01-01 00:00:00'::timestamp without time zone))",  # noqa: E501
                None,
            ),
            (
                "id",
                "uuid",
                "NO",
                "PRIMARY KEY",
                "PRIMARY KEY (id)",
                "uuid_generate_v4()",
            ),
            ("email", "character varying", "NO", "UNIQUE", "UNIQUE (email)", None),
            ("active", "boolean", "YES", None, None, None),
            ("name", "character varying", "YES", None, None, None),
            ("ip", "character varying", "NO", None, None, None),
            ("postal_code", "character varying", "YES", None, None, None),
        ]

    table = "test_table"
    if github_actions_pg:
        monkeypatch.setattr(
            PostgresAdapter,
            "_columns_from_table",
            _columns_from_table,
        )

    # Run
    columns = postgres_adapter.columns(table=table)

    # Assert
    for column in columns:
        if column.name == "created_at":
            assert not column.nullable
            assert not column.unique
            assert not column.primary_key
            assert not column.foreign_key
            assert column.check is not None
            assert column.default is None
        if column.name == "id":
            assert not column.nullable
            assert column.unique
            assert column.primary_key
            assert not column.foreign_key
            assert column.check is None
            assert column.default == "uuid_generate_v4()"
        if column.name == "postal_code":
            assert column.nullable
            assert not column.unique
            assert not column.primary_key
            assert not column.foreign_key
            assert column.check is None
            assert column.default is None
        if column.name == "name":
            assert column.nullable
            assert not column.unique
            assert not column.primary_key
            assert not column.foreign_key
            assert column.check is None
            assert column.default is None
        if column.name == "ip":
            assert not column.nullable
            assert not column.unique
            assert not column.primary_key
            assert not column.foreign_key
            assert column.check is None
            assert column.default is None
        if column.name == "email":
            assert not column.nullable
            assert column.unique
            assert not column.primary_key
            assert not column.foreign_key
            assert column.check is None
            assert column.default is None
        if column.name == "active":
            assert column.nullable
            assert not column.unique
            assert not column.primary_key
            assert not column.foreign_key
            assert column.check is None
            assert column.default is None
