import yaml
from blackline.models.postgres.postgres import PostgresConfig
from pydantic.types import SecretStr


def test_PostgresConfig(stores_yaml: str) -> None:
    # Setup
    store_obj = yaml.safe_load(stores_yaml)
    postgres_obj = store_obj["profiles"]["dev"]

    # Run
    pg_config = PostgresConfig.parse_obj(postgres_obj)

    # Assert
    assert pg_config.type == "postgres"
    isinstance(pg_config.config.connection.conninfo.host, str)
    isinstance(pg_config.config.connection.conninfo.port, int)
    isinstance(pg_config.config.connection.conninfo.dbname, str)
    isinstance(pg_config.config.connection.conninfo.user, str)
    isinstance(pg_config.config.connection.conninfo.password, SecretStr)
