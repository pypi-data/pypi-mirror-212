import pytest
from blackline.adapters.sqlite.sqlite import SQLiteAdapter
from blackline.factories.adapter import AdapterFactory
from blackline.models.sqlite.sqlite import SQLiteConnectionConfig


def test__init__() -> None:
    """Test that the factory is initialised correctly."""
    # Run
    factory = AdapterFactory()

    # Assert
    assert isinstance(factory, AdapterFactory)


def test_adapter(adapter_factory: AdapterFactory) -> None:
    """Test that the adapter is returned correctly."""
    # Run
    adapter = adapter_factory.adapter(name="sqlite")

    # Assert
    assert isinstance(adapter, type(SQLiteAdapter))
    assert isinstance(adapter.config_model, type(SQLiteConnectionConfig))


def test_load_adapter(adapter_factory: AdapterFactory) -> None:
    """Test that the adapter can load."""
    # Run
    adapter = adapter_factory.load_adapter(name="sqlite")

    # Assert
    assert isinstance(adapter, type(SQLiteAdapter))
    assert isinstance(adapter.config_model, type(SQLiteConnectionConfig))


def test_load_adapter_raises_error(
    adapter_factory: AdapterFactory,
) -> None:
    """Test load_plugin raises a ModuleNotFoundError."""
    # Setup
    with pytest.raises(ModuleNotFoundError):
        # Run
        adapter_factory.load_adapter(name="bad_plugin")
