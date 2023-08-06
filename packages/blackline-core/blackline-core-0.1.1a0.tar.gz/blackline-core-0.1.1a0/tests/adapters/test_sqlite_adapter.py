from datetime import timedelta
from sqlite3 import Connection
from typing import List

from blackline.adapters.sqlite.sqlite import SQLiteAdapter
from blackline.exceptions import (
    CollectionNotFoundError,
    FieldNotFoundError,
    InvalidFieldConstraintError,
)
from blackline.models.catalogue import (
    DatasetCollection,
    DatasetField,
    DatetimeField,
    Mask,
    Redact,
)
from blackline.models.datastores import DataStore


def test_sqlite_adapter_init(store: DataStore, profile: str, store_name: str) -> None:
    # Run
    SQLiteAdapter(config=store.config)

    # Assert
    assert True


def test_connection(sqlite_adapter: SQLiteAdapter) -> None:
    # Run
    conn = sqlite_adapter.connection()

    # Assert
    assert isinstance(conn, Connection)


def test_test_connection(sqlite_adapter: SQLiteAdapter) -> None:
    # Run & Assert
    assert sqlite_adapter.test_connection()


def test_execute(sqlite_adapter: SQLiteAdapter, mock_data: List) -> None:
    # Run
    res = sqlite_adapter.execute(sql="SELECT * FROM test_table")
    data = res.fetchall()

    # Assert
    assert len(data) == len(mock_data)


def test_table_exists(sqlite_adapter: SQLiteAdapter) -> None:
    # Run
    res = sqlite_adapter.table_exists(table="test_table")

    # Assert
    assert res


def test_columns_exist(sqlite_adapter: SQLiteAdapter) -> None:
    # Run
    res = sqlite_adapter.columns_exist(table="test_table", columns=["id", "name"])

    # Assert
    assert not res["id"]  # id is not in the test_table
    assert res["name"]


def test_invalid_column_constraints_with_valid_constraints(
    sqlite_adapter: SQLiteAdapter, test_table: str
) -> None:
    # Setup
    table = "mytable"
    with sqlite_adapter.connection() as con:
        con.execute(f"DROP TABLE IF EXISTS {table}")
        con.execute(f"CREATE TABLE {table} (id, name CHECK(name != ''))")

    columns = [
        DatasetField(
            name="id", deidentifier=Redact(type="redact"), period=timedelta(days=365)
        ),
        DatasetField(
            name="name",
            deidentifier=Mask(type="mask", value="#"),
            period=timedelta(days=30),
        ),
    ]

    # Run
    result = sqlite_adapter.invalid_column_constraints(table, columns)

    # Assert
    assert result == {}


def test_invalid_column_constraints_with_invalid_constraints(
    sqlite_adapter: SQLiteAdapter,
):
    # Setup
    table = "mytable"
    with sqlite_adapter.connection() as con:
        con.execute(f"DROP TABLE IF EXISTS {table}")
        con.execute("CREATE TABLE mytable (id INTEGER PRIMARY KEY, name TEXT)")

    columns = [
        DatasetField(
            name="id", deidentifier=Redact(type="redact"), period=timedelta(days=365)
        ),
        DatasetField(
            name="name",
            deidentifier=Mask(type="mask", value="#"),
            period=timedelta(days=30),
        ),
    ]

    # Run
    result = sqlite_adapter.invalid_column_constraints(table, columns)

    # Assert
    assert len(result) == 1
    assert result["id"]["constraint"] == "PRIMARY KEY"
    assert result["id"]["deidentification_method"] == "Redact"


def test_invalid_column_constraints_with_nonexistent_table(
    sqlite_adapter: SQLiteAdapter, test_table: str
):
    # Setup
    table = "notable"
    with sqlite_adapter.connection() as con:
        con.execute(f"DROP TABLE IF EXISTS {table}")
    columns = [
        DatasetField(
            name="id", deidentifier=Redact(type="redact"), period=timedelta(days=365)
        ),
        DatasetField(
            name="name",
            deidentifier=Mask(type="mask", value="#"),
            period=timedelta(days=30),
        ),
    ]

    # Run
    result = sqlite_adapter.invalid_column_constraints(table, columns)

    # Assert
    assert result == {}


def test_valididate_collection_no_table(
    sqlite_adapter: SQLiteAdapter,
):
    # Setup
    table = "notable"
    with sqlite_adapter.connection() as con:
        con.execute(f"DROP TABLE IF EXISTS {table}")

    fields = [
        DatasetField(
            name="id", deidentifier=Redact(type="redact"), period=timedelta(days=365)
        ),
        DatasetField(
            name="name",
            deidentifier=Mask(type="mask", value="#"),
            period=timedelta(days=30),
        ),
    ]

    collection = DatasetCollection(
        name=table,
        fields=fields,
        datetime_field=DatetimeField(name="created_at"),
    )

    # Run
    result = sqlite_adapter.validate_collection(collection=collection)

    # Assert
    assert result.name == table
    assert isinstance(result.not_found, CollectionNotFoundError)
    assert result.fields == {}


def test_valididate_collection_field_not_found(
    sqlite_adapter: SQLiteAdapter,
):
    # Setup
    table = "mytable"
    with sqlite_adapter.connection() as con:
        con.execute(f"DROP TABLE IF EXISTS {table}")
        con.execute(f"CREATE TABLE {table} (id)")

    fields = [
        DatasetField(
            name="id", deidentifier=Redact(type="redact"), period=timedelta(days=365)
        ),
        DatasetField(
            name="nonexistent_field",
            deidentifier=Mask(type="mask", value="#"),
            period=timedelta(days=30),
        ),
    ]

    collection = DatasetCollection(
        name=table, fields=fields, datetime_field=DatetimeField(name="created_at")
    )

    # Run
    result = sqlite_adapter.validate_collection(collection=collection)

    # Assert
    assert isinstance(result.fields["nonexistent_field"].not_found, FieldNotFoundError)


def test_valididate_collection_field_invalid_constraint(
    sqlite_adapter: SQLiteAdapter,
):
    # Setup
    table = "mytable"
    with sqlite_adapter.connection() as con:
        con.execute(f"DROP TABLE IF EXISTS {table}")
        con.execute(f"CREATE TABLE {table} (id INTEGER PRIMARY KEY, name TEXT)")

    fields = [
        DatasetField(
            name="id", deidentifier=Redact(type="redact"), period=timedelta(days=365)
        ),
        DatasetField(
            name="name",
            deidentifier=Mask(type="mask", value="#"),
            period=timedelta(days=30),
        ),
    ]

    collection = DatasetCollection(
        name=table, fields=fields, datetime_field=DatetimeField(name="created_at")
    )

    # Run
    result = sqlite_adapter.validate_collection(collection=collection)

    # Assert
    assert isinstance(
        result.fields["id"].invalid_constraint, InvalidFieldConstraintError
    )
    assert result.fields["name"].invalid_constraint is None
