import string
from sqlite3 import Connection, Cursor, connect
from typing import Any, Optional, Union

from blackline.adapters.sql.sql import SQLAdapter
from blackline.models.collection import Column
from blackline.models.sqlite.sqlite import SQLiteConfig
from sqlglot import exp, parse_one


class SQLiteAdapter(SQLAdapter):
    config_model = SQLiteConfig

    def __init__(self, config: SQLiteConfig.Config, *args, **kwargs):
        super().__init__(config=config, *args, **kwargs)

    def connection(self) -> Connection:
        return connect(**self.config.connection.dict())

    def execute(self, sql: str, values: Optional[dict[str, Any]] = None) -> Any:
        with self.connection() as conn:
            return conn.execute(sql, values or ())

    def fetchall(self, results: Cursor) -> list[tuple]:
        return results.fetchall()

    def update_template(self) -> str:
        return "UPDATE {{ table }}"

    def set_template(self) -> str:
        return "SET"

    def redact_template(self) -> str:
        return "{{ name }} = null"

    def replace_template(self) -> str:
        return "{{ name }} = :{{ value }}"

    def mask_template(self) -> str:
        """Mask template for SQLite.

        SQLite does not support regex, so we have to use a nested replace
        function to mask digits in a column. We are limited to digits because
        if we mask mask characters will will run into an OperationalError: parser
        stack overflow

        Returns:
            str: Mask template for SQLite.
        """

        replace_str = "{{ name }}"
        for c in string.digits:
            replace_str = f"REPLACE({replace_str}, '{c}', :{{{{ value }}}})"

        return f"{{{{ name }}}} = {replace_str}"

    def where_template(self) -> str:
        return "WHERE {{ datetime_column }} < :cutoff"

    def test_connection(self) -> bool:
        try:
            with self.connection() as conn:
                conn.execute("SELECT 1")
                return True
        except Exception:
            return False

    def table_exists(self, table: str) -> bool:
        """Check if a table exists.

        Args:
            table (str): Table name.

        Returns:
            bool: True if the table exists.
        """
        with self.connection() as conn:
            results = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=:table",
                {"table": table},
            ).fetchall()
        return len(results) > 0

    def columns(self, table: str) -> list[Column]:
        """
        Return a list of columns for a given table.

        Args:
            table: Table name.

        Returns:
            A list of Column.
        """
        info = self.column_table_info(table=table)
        check_info = self.column_check_info(table=table)
        for column, check in check_info.items():
            info[column]["check"] = check
        return [Column.parse_obj(result) for result in info.values()]

    def column_table_info(
        self, table: str
    ) -> dict[str, dict[str, Union[str, bool, None]]]:
        """
        Return a dictionary of columns for a given table.

        Args:
            table: Table name.

        Returns:
            A dictionary of column info.
        """
        with self.connection() as con:
            info = con.execute(f"PRAGMA table_info({table})").fetchall()
        return {
            result[1]: {
                "name": result[1],
                "data_type": result[2],
                "nullable": not bool(result[3]),
                "default": result[4],
                "primary_key": bool(result[5]),
            }
            for result in info
        }

    def column_check_info(self, table: str) -> dict[str, str]:
        with self.connection() as con:
            schema = con.execute(
                f"select sql from sqlite_master where type='table' and name='{table}'"
            ).fetchone()
        if schema is None:
            return {}
        return {
            constraint.find(exp.Identifier).name: constraint.sql()
            for constraint in parse_one(schema[0]).find_all(exp.CheckColumnConstraint)
        }
