from datetime import timedelta

from blackline.factories.query import QueryFactory
from blackline.models.catalogue import Catalogue, DatasetField
from blackline.models.datastores import DataStore
from blackline.query.query import Query


def test__init__(
    catalogue: Catalogue, store: DataStore, test_table: str, store_name: str
) -> None:
    """Test init method."""
    # Setup
    store_catalogue = catalogue["organization_foo.system_foo.resource_foo.dataset_foo"]
    collection = [
        collection
        for collection in store_catalogue.collections
        if collection.name == test_table
    ][0]

    # Run
    factory = QueryFactory(adapter=store.adapter, collection=collection)

    # Assert
    assert isinstance(factory, QueryFactory)
    assert factory.adapter == store.adapter
    assert factory.collection == collection


def test_queries(query_factory: QueryFactory) -> None:
    """Test query construction."""

    sql_0 = """UPDATE test_table\nSET\n  email = :email_value,\n  name = null\nWHERE created_at < :cutoff"""  # noqa E501
    sql_1 = """UPDATE test_table\nSET\n  ip = REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(ip, '0', :ip_value), '1', :ip_value), '2', :ip_value), '3', :ip_value), '4', :ip_value), '5', :ip_value), '6', :ip_value), '7', :ip_value), '8', :ip_value), '9', :ip_value)\nWHERE created_at < :cutoff"""  # noqa E501

    # Run
    queries = query_factory.queries()

    # Assert
    assert len(queries) == len(query_factory.fields_by_period())
    assert queries[0].sql == sql_0
    assert queries[1].sql == sql_1
    for query in queries:
        assert isinstance(query, Query)
        assert query.adapter == query_factory.adapter


def test_columns_by_period(query_factory: QueryFactory) -> None:
    """Test columns by retention period method."""
    # Run
    columns = query_factory.fields_by_period()

    # Assert
    assert isinstance(columns, dict)
    assert len(columns) == 2
    for key, value in columns.items():
        assert isinstance(key, timedelta)
        assert isinstance(value, list)
        for column in value:
            assert isinstance(column, DatasetField)
