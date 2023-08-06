from contextlib import contextmanager
from typing import Generator, Union

from blackline.adapters.sql.sql import SQLAdapter
from blackline.models.collection import Column
from blackline.models.mysql.mysql import MySQLConfig
from mysql.connector import MySQLConnection


class MySQLAdapter(SQLAdapter):
    def __init__(self, config: MySQLConfig.Config, *args, **kwargs):
        super().__init__(config=config, *args, **kwargs)
        self.database = self.config.connection.database

    @contextmanager
    def connection(self) -> Generator[MySQLConnection, None, None]:
        conn_args = self.config.connection.dict()
        conn_args["password"] = conn_args["password"].get_secret_value()
        conn = MySQLConnection(**conn_args)
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            raise e
        else:
            conn.commit()
        finally:
            conn.close()

    def test_connection(self) -> bool:
        return self.is_connected()

    def is_connected(self) -> bool:
        with self.connection() as conn:
            return conn.is_connected()

    def mask_template(self) -> str:
        return "{{ name }} = REGEXP_REPLACE(ip,'[:alnum:]',%({{ value }})s)"

    def table_exists(self, table: str) -> bool:
        """Check if a table exists.

        Args:
            table (str): Table name.

        Returns:
            bool: True if the table exists.
        """
        with self.connection() as con:
            with con.cursor() as cur:
                cur.execute(
                    f"SHOW TABLES LIKE '{table}'",
                )
                res = cur.fetchall()
        return len(res) > 0

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
                unique=True if column[3] == "UNI" or column[3] == "PRI" else False,
                primary_key=True if column[3] == "PRI" else False,
                foreign_key=False,
                check=None,
                default=column[4],
            )
            for column in columns_from_table
        ]

    def _columns_from_table(
        self, table: str
    ) -> list[tuple[str, str, str, str, Union[str, None], str]]:
        with self.connection() as con:
            with con.cursor() as cur:
                cur.execute(f"SHOW COLUMNS FROM {table}")
                res = cur.fetchall()
        return res
