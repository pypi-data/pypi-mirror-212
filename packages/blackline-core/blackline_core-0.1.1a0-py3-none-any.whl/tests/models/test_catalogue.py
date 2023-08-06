from pathlib import Path

from blackline.models.catalogue import (
    Catalogue,
    Dataset,
    Organization,
    Resource,
    System,
)
from blackline.models.project_config import ProjectConfig


def test_dataset_parse_dir(project_config: ProjectConfig, dataset_dirs: list[Path]):
    # Setup
    dataset_dir = dataset_dirs[0]
    key = "dataset_foo"

    # Run
    dataset = Dataset.parse_dir(path=dataset_dir)

    # Assert
    assert isinstance(dataset, Dataset)
    assert dataset.key == key


def test_resource_parse_dir(project_config: ProjectConfig, resource_dirs: list[Path]):
    # Setup
    resource_dir = resource_dirs[0]
    key = "resource_foo"

    # Run
    resource = Resource.parse_dir(path=resource_dir)

    assert isinstance(resource, Resource)
    assert resource.key == key
    assert isinstance(resource["dataset_foo"], Dataset)


def test_system_parse_dir(project_config: ProjectConfig, system_dirs: list[Path]):
    # Setup
    system_dir = system_dirs[0]
    key = "system_foo"

    # Run
    system = System.parse_dir(path=system_dir)

    # Assert
    assert isinstance(system, System)
    assert system.key == key
    assert isinstance(system["resource_foo"], Resource)
    assert isinstance(system["resource_foo.dataset_foo"], Dataset)


def test_organization_parse_dir(
    project_config: ProjectConfig, organization_dirs: list[Path]
):
    # Setup
    organization_dir = organization_dirs[0]

    # Run
    organization = Organization.parse_dir(path=organization_dir)

    assert isinstance(organization, Organization)
    assert organization.key == "organization_foo"
    assert isinstance(organization["system_foo"], System)
    assert isinstance(organization["system_foo.resource_foo"], Resource)


def test_catalogue_parse_dir(project_config: ProjectConfig, catalogue_dir: list[Path]):
    # Run
    catalogue = Catalogue.parse_dir(path=catalogue_dir)

    assert isinstance(catalogue, Catalogue)
    assert isinstance(catalogue["organization_foo"], Organization)
    assert isinstance(catalogue["organization_foo.system_foo"], System)
    assert isinstance(catalogue["organization_foo.system_foo.resource_foo"], Resource)
    assert isinstance(
        catalogue["organization_foo.system_foo.resource_foo.dataset_foo"], Dataset
    )
