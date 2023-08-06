from datetime import datetime
from os import listdir
from pathlib import Path
from sqlite3 import connect

from blackline.execution.demo import (
    INIT_ORGANIZATION,
    INIT_RESOURCE,
    INIT_SYSTEM,
    create_demo,
    demo_adapter,
    demo_dataset,
    load_shipments,
    load_users,
)
from blackline.models.catalogue import Catalogue
from blackline.models.datastores import DataStores
from blackline.project.init import (
    INIT_DATASET_FILENAME,
    INIT_ORGANIZATION_FILENAME,
    INIT_RESOURCE_FILENAME,
    INIT_SYSTEM_FILENAME,
)


def test_create_demo(tmp_path: Path):
    # Setup
    name = "sample_project"
    # Run
    demo = create_demo(path=tmp_path, name=name, overwrite=True)

    # Assert
    assert "adapters" in listdir(Path(tmp_path))
    assert "catalogue" in listdir(Path(tmp_path))

    init_project = demo.init_project
    adapter_path = Path(
        init_project.adapters_path,
        init_project.organization,
        init_project.system,
        init_project.resource,
        INIT_DATASET_FILENAME,
    )

    organization_yaml = Path(
        init_project.catalogue_path,
        init_project.organization,
        INIT_ORGANIZATION_FILENAME,
    )
    system_yaml = Path(
        init_project.catalogue_path,
        init_project.organization,
        init_project.system,
        INIT_SYSTEM_FILENAME,
    )
    resource_yaml = Path(
        init_project.catalogue_path,
        init_project.organization,
        init_project.system,
        init_project.resource,
        INIT_RESOURCE_FILENAME,
    )
    dataset_yaml = Path(
        init_project.catalogue_path,
        init_project.organization,
        init_project.system,
        init_project.resource,
        init_project.dataset,
        INIT_DATASET_FILENAME,
    )
    assert organization_yaml.read_text() == INIT_ORGANIZATION
    assert system_yaml.read_text() == INIT_SYSTEM
    assert resource_yaml.read_text() == INIT_RESOURCE
    assert dataset_yaml.read_text() == demo_dataset()
    assert adapter_path.read_text() == demo_adapter(project_root=tmp_path)

    with connect(Path(tmp_path, "blackline_sample.db")) as conn:
        cur = conn.execute("SELECT * FROM user")
        users = cur.fetchall()
        cur = conn.execute("SELECT * FROM shipment")
        shipments = cur.fetchall()

        users = [
            [
                u[0],
                u[1],
                u[2],
                u[3],
                bool(u[4]),
                datetime.strptime(u[5], "%Y-%m-%d %H:%M:%S"),
            ]
            for u in users
        ]
        shipments = [
            [
                s[0],
                s[1],
                datetime.strptime(s[2], "%Y-%m-%d %H:%M:%S"),
                s[3],
                s[4],
                s[5],
                s[6],
            ]
            for s in shipments
        ]
        assert users == load_users()
        assert shipments == load_shipments()


def test_demo_adapter_parses_to_DataStores(tmp_path: Path):
    # Setup
    name = "sample_project"

    # Run
    create_demo(path=tmp_path, name=name, overwrite=True)
    data_stores = DataStores.parse_folder(path=Path(tmp_path, "adapters"))

    # Assert
    assert isinstance(data_stores, DataStores)


def test_demo_catalogue_parses_to_catalogue(tmp_path: Path):
    # Setup
    name = "sample_project"

    # Run
    create_demo(path=tmp_path, name=name, overwrite=True)
    catalogue = Catalogue.parse_dir(path=Path(tmp_path, "catalogue"))

    # Assert
    assert isinstance(catalogue, Catalogue)
