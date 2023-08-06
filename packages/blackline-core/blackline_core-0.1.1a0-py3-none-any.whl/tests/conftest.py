from datetime import datetime
from pathlib import Path
from sqlite3 import Connection
from typing import Callable

import pytest
from blackline.execution.deidentify import Deidentify
from blackline.factories.adapter import AdapterFactory
from blackline.factories.query import QueryFactory
from blackline.models.datastores import DataStore, DataStores
from blackline.models.project_config import ProjectConfig
from blackline.utils.testing.conftest_shared import *  # noqa: F403, F401

pytest_plugins = [
    "tests.conftest_sqlite",
]


@pytest.fixture
def adapter_factory() -> AdapterFactory:
    return AdapterFactory()


@pytest.fixture
def stores(
    project_config: ProjectConfig,
) -> DataStores:
    path = Path(project_config.project_root, project_config.adapters_path)
    return DataStores.parse_folder(path=path)


@pytest.fixture
def store(
    stores: DataStores,
    profile: str,
    store_name: str,
) -> DataStore:
    return stores.store(name=store_name, profile=profile)


@pytest.fixture
def query_factory(
    query_factory_factory: Callable,
    store: DataStore,
    mock_sqlite_store: Connection,
) -> QueryFactory:
    return query_factory_factory(adapter=store.adapter)


@pytest.fixture
def deidentify(
    project_root: Path, sample_project: Callable, profile: str, start_date: datetime
) -> None:
    return Deidentify(path=project_root, profile=profile, start_date=start_date)
