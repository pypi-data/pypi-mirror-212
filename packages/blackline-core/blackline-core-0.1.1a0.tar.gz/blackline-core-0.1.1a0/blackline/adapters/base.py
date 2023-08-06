from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from blackline.models.catalogue import Dataset
from blackline.models.validation import DatasetCollectionValidation

# from blackline.models.adapter import AdapterConfig
# TODO: Add type hinting for AdapterConfig, it currently causes a circular import.


class AdapterBase(ABC):
    date_format = "%Y-%m-%d"

    def __init__(self, config) -> None:
        # def __init__(self, config: AdapterConfig) -> None:
        self.config = config

    @abstractmethod
    def connection(self) -> Any:
        """
        Override this method to return a context manager that is
        connection object.
        """
        pass

    @abstractmethod
    def execute(self, sql: str, values: Optional[Dict[str, Any]] = None) -> Any:
        """
        Override this method to execute a query. It should run a self.connection()
        as a context manager and return the results of the query.

        Args:
            sql: The SQL query string to execute.
            values : The values to pass into the sql query if query parameters are used.
            Defaults to None.

        Returns:
            Any: A Cursor with an executed query.
        """
        with self.connection() as conn:
            with conn.cursor() as cur:
                return cur.execute(sql, values)

    @abstractmethod
    def test_connection(self) -> bool:
        pass

    @abstractmethod
    def update_template(self) -> str:
        pass

    @abstractmethod
    def set_template(self) -> str:
        pass

    @abstractmethod
    def redact_template(self) -> str:
        pass

    @abstractmethod
    def replace_template(self) -> str:
        pass

    @abstractmethod
    def mask_template(self) -> str:
        pass

    @abstractmethod
    def where_template(self) -> str:
        pass

    # @abstractmethod
    def validate_dataset(self, dataset: Dataset) -> DatasetCollectionValidation:
        return DatasetCollectionValidation()
