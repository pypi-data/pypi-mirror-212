"""
Postgres adapter configuration. This shouldn't be here but will move is
later and have it dynamically loaded from blackline-postgres.
"""

from typing import Literal

from blackline.models.adapter import AdapterConfig, ConnectionConfig
from pydantic import BaseModel, SecretStr


class PostgresConnInfo(BaseModel):
    host: str
    port: int
    dbname: str
    user: str
    password: SecretStr


class PostgresConnectionConfig(ConnectionConfig):
    conninfo: PostgresConnInfo


class PostgresConfig(AdapterConfig):
    class Config(BaseModel):
        connection: PostgresConnectionConfig

    type: Literal["postgres"]
    config: Config
