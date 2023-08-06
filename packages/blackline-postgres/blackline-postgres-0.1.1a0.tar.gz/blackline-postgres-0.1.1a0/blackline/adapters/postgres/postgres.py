from typing import Union

from blackline.adapters.sql.sql import SQLAdapter
from blackline.models.collection import Column
from blackline.models.postgres.postgres import PostgresConfig
from psycopg import Connection
from psycopg.sql import SQL, Identifier


class PostgresAdapter(SQLAdapter):
    def __init__(self, config: PostgresConfig.Config, *args, **kwargs):
        super().__init__(config=config, *args, **kwargs)

    def connection(self) -> Connection:
        conn = self.config.connection.dict()
        conninfo = conn["conninfo"]
        conn[
            "conninfo"
        ] = f"postgresql://{conninfo['user']}:{conninfo['password'].get_secret_value()}@{conninfo['host']}:{conninfo['port']}/{conninfo['dbname']}"  # noqa: E501
        return Connection.connect(**conn)

    def test_connection(self) -> bool:
        return not self.connection().closed

    def mask_template(self) -> str:
        return "{{ name }} = REGEXP_REPLACE(ip,'\\w',%({{ value }})s,'g')"

    def table_exists(self, table: str) -> bool:
        """Check if a table exists.

        Args:
            table (str): Table name.

        Returns:
            bool: True if the table exists.
        """
        sql = SQL(
            """
        SELECT *
        FROM
          pg_tables
        WHERE
          tablename = '{table}'
        """
        ).format(table=Identifier(table))

        with self.connection() as con:
            with con.cursor() as cur:
                cur.execute(sql)
                res = cur.fetchone()
        return res is not None

    def columns(self, table: str) -> list[Column]:
        """
        Return a list of columns for a given table.

        Args:
            table: Table name.

        Returns:
            A list of Column.
        """
        columns_from_table = self._columns_from_table(table=table)
        return [
            Column(
                name=column[0],
                data_type=column[1],
                nullable=True if column[2] == "YES" else False,
                unique=True
                if column[3] == "UNIQUE" or column[3] == "PRIMARY KEY"
                else False,
                primary_key=True if column[3] == "PRIMARY KEY" else False,
                foreign_key=True if column[3] == "FOREIGN KEY" else False,
                check=column[4] if column[3] == "CHECK" else None,
                default=column[5],
            )
            for column in columns_from_table
        ]

    def _columns_from_table(
        self, table: str
    ) -> list[tuple[str, str, str, str, Union[str, None], str]]:
        with self.connection() as con:
            with con.cursor() as cur:
                cur.execute(
                    SQL(
                        """
                    SELECT
                      c.column_name,
                      c.data_type,
                      c.is_nullable,
                      tc.constraint_type,
                      pg_get_constraintdef(con.oid),
                      c.column_default
                    FROM information_schema.columns c
                    LEFT JOIN information_schema.constraint_column_usage cu
                      ON c.column_name = cu.column_name
                    LEFT JOIN information_schema.table_constraints tc
                      ON cu.constraint_name = tc.constraint_name
                    LEFT JOIN pg_catalog.pg_constraint con
                      ON tc.constraint_name = con.conname
                    WHERE c.table_name = '{table}'
                    """
                    ).format(table=Identifier(table))
                )
                res = cur.fetchall()
        return res
