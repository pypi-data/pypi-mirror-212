from datetime import datetime

from blackline.factories.query import QueryFactory
from blackline.query.query import Query


def test__init__(query_factory: QueryFactory) -> None:
    """Test that the Query class is initialised correctly."""
    # Setup
    adapter = query_factory.adapter
    fields_by_period = query_factory.fields_by_period()
    period = list(fields_by_period.keys())[0]
    fields = fields_by_period[period]
    sql = query_factory.render_sql(fields=fields)
    cuttoff_date = query_factory.cutoff_date(period=period)

    # Run

    query = Query(adapter=adapter, sql=sql, fields=fields, cutoff_date=cuttoff_date)

    # Run & Assert
    assert isinstance(query, Query)


def test_execute(query_factory: QueryFactory) -> None:
    """Test that a query is executed correctly."""
    # Setup
    adapter = query_factory.adapter
    fields_by_period = query_factory.fields_by_period()
    period = list(fields_by_period.keys())[0]
    fields = fields_by_period[period]
    sql = query_factory.render_sql(fields=fields)
    cuttoff_date = query_factory.cutoff_date(period=period)
    query = Query(adapter=adapter, sql=sql, fields=fields, cutoff_date=cuttoff_date)
    old_data = query.adapter.execute(sql="SELECT * FROM test_table").fetchall()
    cutoff = query_factory.start_date - period

    # Run
    query.execute()

    # Assert
    with query.adapter.connection() as conn:
        new_data = conn.execute("SELECT * FROM test_table").fetchall()

    diff = [new_data[i] for i, row in enumerate(old_data) if row != new_data[i]]

    diff_date_above_cutoff = [
        row for row in diff if datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") > cutoff
    ]

    assert not diff_date_above_cutoff
    assert list({row[1] for row in diff})[0] == fields[1].deidentifier.value
    assert list({row[2] for row in diff})[0] == fields[0].deidentifier.value
