from datetime import datetime
from pathlib import Path
from sqlite3 import Connection
from typing import Callable

from blackline.execution.deidentify import Deidentify
from blackline.execution.deidentify import deidentify as deidentify_func
from blackline.models.catalogue import Catalogue
from blackline.models.datastores import DataStores
from blackline.models.project_config import ProjectConfig


def test__init__(project_root: Path, sample_project: Callable, profile: str) -> None:
    """Test that the Deidentify class is initialised correctly."""
    # Setup
    deidentify = Deidentify(
        path=project_root, profile=profile, start_date=datetime.now()
    )

    # Assert
    assert isinstance(deidentify, Deidentify)
    assert isinstance(deidentify.project, ProjectConfig)
    assert isinstance(deidentify.stores, DataStores)
    assert isinstance(deidentify.catalogue, Catalogue)


def test_deidentify_deidentify(
    deidentify: Deidentify,
    mock_sqlite_store: Connection,
    deidentified_mock_data_sqlite: list[tuple],
    test_table: str,
    profile: str,
) -> None:
    # Run
    deidentify.deidentify()

    # Assert
    assert deidentify.catalogue is not None
    adapter = deidentify.stores.store(name="dataset_foo", profile=profile).adapter

    with adapter.connection() as conn:
        deidentified_data = conn.execute(f"SELECT * FROM {test_table}").fetchall()
    assert deidentified_data == deidentified_mock_data_sqlite


def test_deidentify_validate_catalogue_dataset_no_exceptions(
    deidentify: Deidentify,
    mock_sqlite_store: Connection,
    deidentified_mock_data_sqlite: list[tuple],
    test_table: str,
    profile: str,
) -> None:
    # Run
    excs = deidentify.validate_catalogue_dataset()

    # Assert
    assert len(excs) == 0


def test_deidentify_validate_catalogue_dataset_with_exceptions(
    deidentify: Deidentify,
) -> None:
    # Run
    excs = deidentify.validate_catalogue_dataset()  # No test db created

    # Assert
    assert len(excs) > 0
    for exc in excs:
        assert isinstance(exc, Exception)


def test_deidentify(
    deidentify: Deidentify,
    mock_sqlite_store: Connection,
    deidentified_mock_data_sqlite: list[tuple],
    test_table: str,
    profile: str,
) -> None:
    # Run
    excs = deidentify_func(
        path=deidentify.path, profile=profile, start_date=deidentify.start_date
    )

    # Assert
    assert excs is None
    adapter = deidentify.stores.store(name="dataset_foo", profile=profile).adapter

    with adapter.connection() as conn:
        deidentified_data = conn.execute(f"SELECT * FROM {test_table}").fetchall()
    assert deidentified_data == deidentified_mock_data_sqlite


def test_deidentify_with_exceptions(
    profile: str,
    project_root: Path,
    sample_project: Callable,
    start_date: datetime,
) -> None:
    # Run
    excs = deidentify_func(path=project_root, profile=profile, start_date=start_date)

    # Assert
    assert len(excs) > 0
