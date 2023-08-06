from sqlite3 import Connection
from typing import Any, Literal

from blackline.models.adapter import AdapterConfig, ConnectionConfig
from blackline.models.collection import Column as SQLColumn
from pydantic import BaseModel, Field


class SQLiteConnectionConfig(ConnectionConfig):
    """
    A data model representing a connection configuration for a SQLite database.
    """

    database: str = Field(
        ..., description="The name or path to the SQLite database file."
    )
    timeout: float = Field(
        default=5.0,
        description="The number of seconds to wait before timing out the connection.",
    )
    detect_types: int = Field(
        default=0,
        description="The type detection flags to use when parsing column types.",
    )
    isolation_level: str = Field(
        default="DEFERRED",
        description="The isolation level to use for the connection.",
    )
    check_same_thread: bool = Field(
        default=True,
        description="Whether to check if the connection is being used in the same thread it was created in.",  # noqa: E501
    )
    factory: Any = Field(
        default=Connection,
        description="The name of the factory function to use for creating the connection.",  # noqa: E501
    )
    cached_statements: int = Field(
        default=100,
        description="The maximum number of prepared statements to cache.",
    )
    uri: bool = Field(
        default=False, description="Whether to use a URI-style connection string."
    )

    class Config:
        env_prefix = ""


class SQLiteConfig(AdapterConfig):
    """
    A data model representing the configuration for the SQLite adapter.

    Args:
        Config (BaseModel): A nested BaseModel class representing the SQLite connection configuration.  # noqa: E501

    Returns:
        SQLiteConfig: An instance of the SQLiteConfig class.

    """

    class _Config(BaseModel):
        connection: SQLiteConnectionConfig = Field(
            ..., description="The connection configuration for the adapter."
        )

    type: Literal["sqlite"] = Field(..., description="The type of adapter.")
    config: _Config = Field(..., description="The configuration for the adapter.")


class Column(SQLColumn):
    ...
