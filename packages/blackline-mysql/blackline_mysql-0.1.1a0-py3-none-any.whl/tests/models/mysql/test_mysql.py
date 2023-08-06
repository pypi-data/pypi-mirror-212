import yaml
from blackline.models.mysql.mysql import MySQLConfig
from pydantic.types import SecretStr


def test_MySQLConfig(
    stores_yaml: str,
    mysql_user: str,
    mysql_password: SecretStr,
    mysql_db: str,
    mysql_host: str,
    mysql_port: int,
) -> None:
    # Setup
    store_obj = yaml.safe_load(stores_yaml)
    mysql_obj = store_obj["profiles"]["dev"]

    # Run
    mysql_config = MySQLConfig.parse_obj(mysql_obj)

    # Assert
    assert mysql_config.type == "mysql"
    assert mysql_config.config.connection.host == mysql_host
    assert mysql_config.config.connection.port == mysql_port
    assert mysql_config.config.connection.database == mysql_db
    assert mysql_config.config.connection.user == mysql_user
    assert mysql_config.config.connection.password.get_secret_value() == mysql_password
