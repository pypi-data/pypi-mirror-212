import inspect
import re
from importlib import import_module
from pathlib import Path
from typing import Annotated, Any, Optional, Type, Union

import yaml
from blackline.models.adapter import AdapterConfig
from blackline.models.sqlite.sqlite import SQLiteConfig
from pydantic import BaseModel, BaseSettings, Field, create_model, root_validator


def load_adapter_configs_from_submodules(name: str) -> set:
    mod = import_module(name)
    model_modules = inspect.getmembers(
        mod,
        lambda member: inspect.ismodule(member)
        and re.match(r"^blackline\.models(?:\.(\w+))*$", member.__name__) is not None,
    )

    configs = {
        member[1]
        for member in inspect.getmembers(
            mod,
            lambda member: inspect.isclass(member)
            and issubclass(member, AdapterConfig)
            and member != AdapterConfig,
        )
    }

    for module in model_modules:
        configs.update(load_adapter_configs_from_submodules(module[1].__name__))

    return configs


def assign_store(
    adapter_configs: set,
) -> Union[Type[AdapterConfig], Type[object]]:
    if len(adapter_configs) == 1:
        return SQLiteConfig
    return Annotated[
        Union[tuple(adapter_configs)],  # type: ignore
        Field(discriminator="type"),
    ]


adapter_configs = load_adapter_configs_from_submodules(name="blackline.models")
Adapter: Any = assign_store(adapter_configs=adapter_configs)


def config_files(folderpath: Path) -> list[Path]:
    return list(folderpath.glob("**/*.yml")) + list(folderpath.glob("**/*.yaml"))


class DataStore(BaseSettings):
    """
    A data model representing a data store, with profiles for connecting to different adapters. # noqa: E501
    """

    profiles: dict[str, Adapter]
    name: str
    key: str
    env_prefix: str = ""

    class Config:
        extra = "allow"
        env_prefix = ""
        env_nested_delimiter = "__"

    @root_validator(pre=True)
    def validate_store(cls, values):
        values["key"] = cls.build_key(values)
        return values

    def build_key(values):
        organization_name = values.get("organization_name", "")
        system_name = values.get("system_name", "")
        resource_name = values.get("resource_name", "")
        name = values.get("name", "")
        return f"{organization_name}.{system_name}.{resource_name}.{name}"


class DataStores(BaseModel):
    """
    A data model representing a collection of data stores.
    """

    stores: list[DataStore] = Field(..., description="A list of DataStore objects.")

    def store(self, name: str, profile: Optional[str] = None):
        """
        Retrieves a data store by name and returns its adapter profiles or a specific profile. # noqa: E501

        Args:
            name (str): The name of the data store to retrieve.
            profile (Optional[str], optional): The name of the adapter profile to retrieve. If None, returns all profiles. Defaults to None.  # noqa: E501

        Raises:
            ValueError: If the specified data store is not found.

        Returns:
            (Union[dict[str, Adapter], Adapter]): The adapter profiles for the specified data store, or a specific adapter profile. # noqa: E501
        """
        for store in self.stores:
            if store.name == name:
                if profile:
                    return store.profiles[profile]
                return store.profiles
        raise ValueError(f"Store {name} not found")

    def store_by_key(self, key: str, profile: str) -> AdapterConfig:
        """
        Retrieves a data store by key and returns the specified adapter profile.

        Args:
            key (str): The unique key of the data store to retrieve.
            profile (str): The name of the adapter profile to retrieve.

        Raises:
            ValueError: If the specified data store is not found.

        Returns:
            AdapterConfig: The adapter configuration for the specified data store and profile. # noqa: E501
        """
        for store in self.stores:
            if store.key == key:
                return store.profiles[profile]
        raise ValueError(f"Store {key} not found")

    @classmethod
    def parse_folder(cls, path: Path) -> "DataStores":
        """
        Parses a folder of data store configuration files and adds them to the collection. # noqa: E501

        Args:
            path: The path to the folder containing the data store configuration files.
        """
        _datastores: list[DataStore] = []
        files = config_files(folderpath=path)
        for file in files:
            with open(file, "rb") as f:
                adapter_info = yaml.safe_load(f)
                adapter_info["name"] = file.stem
                adapter_info["organization_name"] = file.parent.parent.parent.name
                adapter_info["system_name"] = file.parent.parent.name
                adapter_info["resource_name"] = file.parent.name
                DataStore.__config__.env_prefix = adapter_info.get("env_prefix", "")
                _DataStore = create_model("_DataStore", __base__=DataStore)
                _DataStore.__name__ = _DataStore.__qualname__ = "DataStore"
                _store = _DataStore.parse_obj(adapter_info)
            _datastores.append(_store)
        return cls(stores=_datastores)
