from pathlib import Path

import pytest
from blackline.adapters.sqlite.sqlite import SQLiteAdapter
from blackline.models.adapter import AdapterConfig
from blackline.models.datastores import DataStore, DataStores
from blackline.models.project_config import ProjectConfig
from blackline.models.sqlite.sqlite import SQLiteConfig
from yaml import safe_load


def test_DataStore(profile: str, sqlite_store_yml: str) -> None:
    info = safe_load(sqlite_store_yml)
    info["name"] = "foo"
    config = DataStore.parse_obj(info)
    assert config.name == "foo"
    assert isinstance(config.profiles[profile], SQLiteConfig)


def test_DataStores(profile: str, sqlite_store_yml: str) -> None:
    info = safe_load(sqlite_store_yml)
    info["name"] = "foo"
    config = DataStore.parse_obj(info)
    stores = DataStores(stores=[config])
    for store in stores.stores:
        assert isinstance(store, DataStore)


def test_DataStores_store_with_profile(profile: str, sqlite_store_yml: str) -> None:
    info = safe_load(sqlite_store_yml)
    info["name"] = "foo"
    config = DataStore.parse_obj(info)
    stores = DataStores(stores=[config])
    store = stores.store(name="foo", profile=profile)
    assert isinstance(store, SQLiteConfig)


def test_DataStores_store_no_profile(profile: str, sqlite_store_yml: str) -> None:
    info = safe_load(sqlite_store_yml)
    info["name"] = "foo"
    config = DataStore.parse_obj(info)
    stores = DataStores(stores=[config])
    store = stores.store(name="foo")
    assert isinstance(store, dict)


def test_DataStores_store_not_found(profile: str, sqlite_store_yml: str) -> None:
    info = safe_load(sqlite_store_yml)
    info["name"] = "foo"
    config = DataStore.parse_obj(info)
    stores = DataStores(stores=[config])
    with pytest.raises(ValueError) as excinfo:
        stores.store(name="bar")
        assert "Store bar not found" in str(excinfo.value)


def test_DataStores_parse_folder(
    project_config: ProjectConfig, profile: str, store_name: str
):
    path = Path(project_config.project_root, project_config.adapters_path)

    # Run
    stores = DataStores.parse_folder(path=path)
    store = stores.store(name=store_name, profile=profile)

    # Assert
    assert isinstance(store, AdapterConfig)
    assert isinstance(store.adapter, SQLiteAdapter)
    assert store.config.connection.database == "file::memory:?cache=shared"
