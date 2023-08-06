"""
MySQL adapter configuration. This shouldn't be here but will move is
later and have it dynamically loaded from blackline-postgres.
"""

from typing import Literal, Optional

from blackline.models.adapter import AdapterConfig, ConnectionConfig
from pydantic import BaseModel, Field, SecretStr


class MySQLConnectionConfig(ConnectionConfig):
    user: str = Field(
        ..., description="The user name used to authenticate with the MySQL server."
    )
    password: SecretStr = Field(
        ..., description="The password to authenticate the user with the MySQL server."
    )
    password1: Optional[SecretStr] = Field(
        None,
        description="For Multi-Factor Authentication (MFA); password1 is an alias for password.",  # noqa: E501
    )
    password2: Optional[SecretStr] = Field(
        None, description="For Multi-Factor Authentication (MFA)"
    )
    password3: Optional[SecretStr] = Field(
        None, description="For Multi-Factor Authentication (MFA)"
    )
    database: str = Field(
        ...,
        description="The database name to use when connecting with the MySQL server.",
    )
    host: str = Field(
        "127.0.0.1", description="The host name or IP address of the MySQL server."
    )
    port: int = Field(3306, description="The port number of the MySQL server.")
    unix_socket: Optional[str] = Field(
        None, description="The path to a Unix domain socket."
    )

    class Config:
        extra = "allow"


class MySQLConfig(AdapterConfig):
    class Config(BaseModel):
        connection: MySQLConnectionConfig

    type: Literal["mysql"]
    config: Config
