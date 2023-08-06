from datetime import datetime, timedelta
from typing import Optional

from blackline.adapters.base import AdapterBase
from blackline.models.catalogue import DatasetCollection, DatasetField
from blackline.query.query import Query
from blackline.query.template import Template


class QueryFactory:
    """Query builder class to build query object."""

    def __init__(
        self,
        adapter: AdapterBase,
        collection: DatasetCollection,
        start_date: Optional[datetime] = None,
    ) -> None:
        """
        _summary_

        Args:
            adapter (AdapterBase): _description_
            collection (DatasetCollection): _description_
            start_date (Optional[datetime], optional): _description_. Defaults to None.
        """
        self.adapter = adapter
        self.collection = collection
        self.start_date = start_date or datetime.now()
        self.template = Template(self.adapter, trim_blocks=True, lstrip_blocks=True)

    def queries(self) -> list[Query]:
        """Get queries."""
        return [
            self.query_by_period(period=period, fields=fields)
            for period, fields in self.fields_by_period().items()
        ]

    def query_by_period(self, period: timedelta, fields: list[DatasetField]) -> Query:
        return Query(
            adapter=self.adapter,
            sql=self.render_sql(fields=fields),
            fields=fields,
            cutoff_date=self.cutoff_date(period=period),
        )

    def render_sql(self, fields: list[DatasetField]) -> str:
        return self.template.template.render(
            table=self.collection.name,
            columns=fields,
            datetime_column=self.collection.datetime_field.name,
        )

    def cutoff_date(self, period: timedelta) -> datetime:
        """Get cutoff date."""
        return self.start_date - period

    def fields_by_period(self) -> dict[timedelta, list[DatasetField]]:
        """Get columns by retention period."""
        fields: dict[timedelta, list[DatasetField]] = {
            field.period: [
                _field
                for _field in self.collection.fields
                if field.period == _field.period
            ]
            for field in self.collection.fields
        }
        return fields
