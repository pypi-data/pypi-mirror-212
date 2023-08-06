from blackline.adapters.sqlite.sqlite import SQLiteAdapter
from blackline.models.sqlite.sqlite import SQLiteConfig, SQLiteConnectionConfig
from yaml import safe_load


def test_SQLiteConnectionConfig(profile: str, sqlite_store_yml: str) -> None:
    info = safe_load(sqlite_store_yml)
    info = info["profiles"][profile]["config"]["connection"]
    config = SQLiteConnectionConfig.parse_obj(info)
    assert config.database == "file::memory:"
    assert config.uri is True


def test_SQLLiteConfig(profile: str, sqlite_store_yml: str) -> None:
    info = safe_load(sqlite_store_yml)
    sqlite_info = info["profiles"][profile]
    config = SQLiteConfig.parse_obj(sqlite_info)
    assert config.type == "sqlite"
    isinstance(config.adapter, SQLiteAdapter)
