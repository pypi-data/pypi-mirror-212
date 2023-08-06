from blackline.adapters.mysql.mysql import MySQLAdapter
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from pytest import MonkeyPatch


def test_connection(
    stores_yaml: str,
    monkeypatch: MonkeyPatch,
    github_actions_mysql: bool,
    mysql_adapter: MySQLAdapter,
) -> None:
    # Setup

    if github_actions_mysql:
        monkeypatch.setattr(MySQLCursor, "fetchone", lambda self: (1,))

    # Run
    with mysql_adapter.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            result = cur.fetchone()

    # Assert
    assert result is not None
    assert result[0] == 1


def test_is_connected(
    mysql_adapter: MySQLAdapter, monkeypatch: MonkeyPatch, github_actions_mysql: bool
) -> None:
    # Run & Assert
    assert mysql_adapter.is_connected()


def test_columns(
    monkeypatch: MonkeyPatch,
    github_actions_mysql: bool,
    load_database: MySQLConnection,
    test_table: str,
    mysql_adapter: MySQLAdapter,
):
    # Setup
    def _columns_from_table(self, table: str):
        return [
            ("id", "char(36)", "NO", "PRI", "uuid()", "DEFAULT_GENERATED"),
            ("created_at", "timestamp", "YES", "", None, ""),
            ("name", "varchar(255)", "YES", "", None, ""),
            ("email", "varchar(255)", "NO", "", None, ""),
            ("postal_code", "varchar(15)", "YES", "UNI", None, ""),
            ("active", "tinyint(1)", "YES", "", None, ""),
            ("ip", "varchar(15)", "YES", "", None, ""),
        ]

    if github_actions_mysql:
        monkeypatch.setattr(MySQLAdapter, "_columns_from_table", _columns_from_table)
        monkeypatch.setattr(
            MySQLCursor,
            "fetchall",
            lambda self: _columns_from_table(self, test_table),
        )

    # Run
    columns = mysql_adapter.columns(test_table)

    with mysql_adapter.connection() as con:
        with con.cursor() as cur:
            cur.execute(f"SHOW COLUMNS FROM {test_table}")
            result = cur.fetchall()

    # Assert
    for i, column in enumerate(columns):
        assert column.name == result[i][0]
        assert column.data_type == result[i][1]
        assert column.default == result[i][4]

        if result[i][2] == "YES":
            assert column.nullable is True

        if result[i][3] == "PRI":
            assert column.primary_key is True
            assert column.unique is True

        if result[i][3] == "UNI":
            assert column.unique is True


def test_table_exist(
    monkeypatch: MonkeyPatch,
    github_actions_mysql: bool,
    load_database: MySQLConnection,
    test_table: str,
    mysql_adapter: MySQLAdapter,
):
    # Setup
    if github_actions_mysql:
        monkeypatch.setattr(MySQLCursor, "fetchall", lambda self: [(f"{test_table}",)])

    # Run
    exists = mysql_adapter.table_exists(table=test_table)

    assert exists is True


def test_table_exist_does_not_exist(
    monkeypatch: MonkeyPatch,
    github_actions_mysql: bool,
    mysql_adapter: MySQLAdapter,
):
    # Setup
    nonexistent_table = "nonexistent_table"
    if github_actions_mysql:
        monkeypatch.setattr(MySQLCursor, "fetchall", lambda self: [])

    # Run
    exists = mysql_adapter.table_exists(table=nonexistent_table)

    assert exists is False
