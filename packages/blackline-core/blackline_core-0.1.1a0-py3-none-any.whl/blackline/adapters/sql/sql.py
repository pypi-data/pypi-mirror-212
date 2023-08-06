# from abc import abstractmethod
from datetime import datetime
from typing import Any, Dict, Optional, Union

from blackline.adapters.base import AdapterBase
from blackline.constants import (
    CHECK,
    DEFAULT,
    FOREIGN_KEY,
    NOT_NULL,
    PRIMARY_KEY,
    UNIQUE,
)
from blackline.exceptions import (
    CollectionNotFoundError,
    FieldNotFoundError,
    InvalidFieldConstraintError,
)
from blackline.factories.query import QueryFactory
from blackline.models.catalogue import Dataset, DatasetCollection, DatasetField
from blackline.models.collection import Column
from blackline.models.validation import (
    CollectionValidation,
    DatasetCollectionValidation,
    FieldValidation,
)
from blackline.query.query import Query

CONSTRINT_MAP: dict[str, dict[str, Union[str, object]]] = {
    NOT_NULL: {"arg": "nullable", "value": False},
    UNIQUE: {"arg": "unique", "value": True},
    PRIMARY_KEY: {"arg": "primary_key", "value": True},
    FOREIGN_KEY: {"arg": "foreign_key", "value": True},
    CHECK: {"arg": "check", "value": not None},
    DEFAULT: {"arg": "default", "value": not None},
}


class SQLAdapter(AdapterBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # @abstractmethod
    def columns(self, table: str) -> list[Column]:
        pass

    # @abstractmethod
    def table_exists(self, table: str) -> bool:
        pass

    def execute(self, sql: str, values: Optional[Dict[str, Any]] = None) -> Any:
        with self.connection() as conn:
            with conn.cursor() as cur:
                return cur.execute(sql, values)

    def update_template(self) -> str:
        return "UPDATE {{ table }}"

    def set_template(self) -> str:
        return "SET"

    def redact_template(self) -> str:
        return "{{ name }} = null"

    def replace_template(self) -> str:
        return "{{ name }} = %({{ value }})s"

    def where_template(self) -> str:
        return "WHERE {{ datetime_column }} < %(cutoff)s"

    def deidentify(self, catalogue, start_date: datetime = datetime.now()):
        for collection in catalogue.collections:
            queries = QueryFactory(
                adapter=self,
                collection=collection,
                start_date=start_date,
            ).queries()
            self.execute_queries(queries=queries)

    def execute_queries(self, queries: list[Query]) -> None:
        for query in queries:
            query.execute()

    def column_exists(self, table: str, column: str) -> bool:
        """Check if a column exists in a table.

        Args:
            table (str): Table name.
            column (str): Column name.

        Returns:
            bool: True if the column exists.
        """
        return column in [column.name for column in self.columns(table)]

    def columns_exist(self, table, columns: list[str]) -> dict[str, bool]:
        """Check if columns exist in a table.

        Args:
            table (str): Table name.
            columns (list[str]): List of columns to check.

        Returns:
            bool: True if all columns exist in the table.
        """
        return {
            column: self.column_exists(table=table, column=column) for column in columns
        }

    def invalid_column_constraints(
        self, table: str, columns: list[DatasetField]
    ) -> dict[str, dict[str, Union[str, None]]]:
        invalid_constraints: dict[str, dict[str, Union[str, None]]] = {}

        table_columns = {column.name: column for column in self.columns(table=table)}
        if not table_columns:
            return {}

        for column in columns:
            if column.deidentifier is None:
                continue
            if column.name not in table_columns:
                continue
            for invalid_constraint in column.deidentifier.invalid_constraints:
                _cons = CONSTRINT_MAP[invalid_constraint]
                if _cons["value"] == getattr(
                    table_columns[column.name], str(_cons["arg"])
                ):
                    invalid_constraints[column.name] = {
                        "constraint": invalid_constraint,
                        "deidentification_method": column.deidentifier.__class__.__name__,  # noqa: E501
                    }
        return invalid_constraints

    def validate_fields(
        self, table: str, fields: list[DatasetField]
    ) -> dict[str, FieldValidation]:
        """
        Validate a list of filds.

        Args:
            table: Table name
            fields (list[DatasetField]): List of fields to validate.

        Returns:
            dict[str, FieldValidation]: A dictionary of FieldValidation objects.
        """
        field_names = [field.name for field in fields]
        fields_exist = self.columns_exist(table=table, columns=field_names)
        invalid_constraints = self.invalid_column_constraints(
            table=table, columns=fields
        )
        return {
            field: FieldValidation.parse_obj(
                {
                    "name": field,
                    "not_found": FieldNotFoundError(table, field)
                    if not fields_exist.get(field)
                    else None,
                    "invalid_constraint": InvalidFieldConstraintError(
                        constraint_name=invalid_constraints[field]["constraint"],
                        deidentification_method=invalid_constraints[field][
                            "deidentification_method"
                        ],
                    )
                    if field in invalid_constraints
                    else None,
                }
            )
            for field in field_names
        }

    def validate_collection(
        self, collection: DatasetCollection
    ) -> CollectionValidation:
        """Assert that a collection if valid.

        Args:
            collection: Dataset collection.

        Returns:
            A CollectionValidation object
        ""
        """

        table_exists = self.table_exists(collection.name)

        if not table_exists:
            return CollectionValidation(
                name=collection.name, not_found=CollectionNotFoundError(collection.name)
            )
        return CollectionValidation.parse_obj(
            {
                "name": collection.name,
                "not_found": None,
                "fields": self.validate_fields(
                    table=collection.name, fields=collection.fields
                ),
            }
        )

    def validate_dataset(self, dataset: Dataset) -> DatasetCollectionValidation:
        """Assert that a Dataset if valid.

        Args:
            collection (DatasetCollection): Dataset collection.

        Returns:
            bool: True if the collection exists.
        """

        return DatasetCollectionValidation(
            collections={
                collection.name: self.validate_collection(collection)
                for collection in dataset.collections
            }
        )
