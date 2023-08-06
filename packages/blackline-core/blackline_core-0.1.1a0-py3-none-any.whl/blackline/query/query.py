from datetime import datetime
from typing import Any, Optional

from blackline.adapters.base import AdapterBase
from blackline.models.catalogue import DatasetField


class Query:
    def __init__(
        self,
        adapter: AdapterBase,
        sql: str,
        fields: list[DatasetField],
        cutoff_date: datetime,
    ) -> None:
        self.adapter = adapter
        self.sql = sql
        self.fields = fields
        self.cutoff_date = cutoff_date

    def __str__(self) -> str:
        return f"{self.sql}"

    def execute(self) -> Any:
        values: dict[str, Optional[str]] = {
            f"{field.name}_value": field.deidentifier.value
            for field in self.fields
            if field.deidentifier is not None
        }
        values["cutoff"] = self.cutoff_date.strftime(self.adapter.date_format)
        return self.adapter.execute(self.sql, values)
