from pathlib import Path
from typing import Optional

from blackline.models.catalogue import Dataset, Organization, Resource, System
from blackline.models.datastores import DataStore
from blackline.utils.doc_examples import DATASET, ORGANIZATION, RESOURCE, SQLITE, SYSTEM
from yaml import Loader, load


def test_organization_example(tmp_path: Path):
    class OrganizationExample(Organization):
        children: Optional[dict[str, System]]

    obj = load(ORGANIZATION, Loader=Loader)
    OrganizationExample(**obj["organization"]).dict()
    assert True


def test_system_example(tmp_path: Path):
    class SystemExample(System):
        children: Optional[dict[str, Resource]]

    obj = load(SYSTEM, Loader=Loader)
    SystemExample(**obj["system"])
    assert True


def test_resource_example(tmp_path: Path):
    class ResourceExample(Resource):
        children: Optional[dict[str, Dataset]]

    obj = load(RESOURCE, Loader=Loader)
    assert ResourceExample(**obj["resource"])


def test_dataset_example(tmp_path: Path):
    obj = load(DATASET, Loader=Loader)
    Dataset(**obj["dataset"]).dict()
    assert True


def test_sqlite_config_example(tmp_path: Path):
    obj = load(SQLITE, Loader=Loader)
    obj["name"] = "test"
    obj["organization_name"] = "test"
    obj["system_name"] = "test"
    obj["resource_name"] = "test"
    DataStore.parse_obj(obj)
    assert True
