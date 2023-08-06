from pathlib import Path

from blackline.constants import (
    DEFAULT_ADAPTERS_FOLDER,
    DEFAULT_CATALOGUE_FOLDER,
    PROJECT_CONFIG_FILE,
)
from blackline.project.init import (
    INIT_DATASET_FILENAME,
    INIT_DATASET_FOLDER,
    INIT_ORGANIZATION_FILENAME,
    INIT_ORGANIZATION_FOLDER,
    INIT_RESOURCE_FILENAME,
    INIT_RESOURCE_FOLDER,
    INIT_SYSTEM_FILENAME,
    INIT_SYSTEM_FOLDER,
    InitProject,
)
from yaml import Loader, load


def test_init_project(tmp_path: Path, fake_project_name: str) -> None:
    """Test that the project is initialised correctly."""
    # Setup
    project_config_path = Path(tmp_path, PROJECT_CONFIG_FILE)
    init_project = InitProject(path=tmp_path, name=fake_project_name)
    project_config = init_project.project_config

    # Run
    init_project.init_project()

    # Assert
    assert project_config_path.is_file()
    assert project_config.catalogue_path.is_dir()
    assert project_config.adapters_path.is_dir()
    assert Path(tmp_path, DEFAULT_ADAPTERS_FOLDER) == project_config.adapters_path
    assert Path(tmp_path, DEFAULT_CATALOGUE_FOLDER) == project_config.catalogue_path
    adapter_path = project_config.adapters_path
    catalogue_path = project_config.catalogue_path

    assert Path(
        adapter_path,
        INIT_ORGANIZATION_FOLDER,
        INIT_SYSTEM_FOLDER,
        INIT_RESOURCE_FOLDER,
        INIT_DATASET_FILENAME,
    ).is_file()

    assert Path(
        catalogue_path, INIT_ORGANIZATION_FOLDER, INIT_ORGANIZATION_FILENAME
    ).is_file()
    assert Path(
        catalogue_path,
        INIT_ORGANIZATION_FOLDER,
        INIT_SYSTEM_FOLDER,
        INIT_SYSTEM_FILENAME,
    ).is_file()
    assert Path(
        catalogue_path,
        INIT_ORGANIZATION_FOLDER,
        INIT_SYSTEM_FOLDER,
        INIT_RESOURCE_FOLDER,
        INIT_RESOURCE_FILENAME,
    ).is_file()
    assert Path(
        catalogue_path,
        INIT_ORGANIZATION_FOLDER,
        INIT_SYSTEM_FOLDER,
        INIT_RESOURCE_FOLDER,
        INIT_DATASET_FOLDER,
        INIT_DATASET_FILENAME,
    ).is_file()


def test_create_project_yml(tmp_path: Path, fake_project_name: str) -> None:
    """Test that the project is initialised correctly."""
    # Setup
    project = InitProject(path=tmp_path, name=fake_project_name)
    project_config = project.project_config
    project_config_path = Path(project.path, PROJECT_CONFIG_FILE)

    # Run
    project.create_project_yaml()

    # Assert
    project_text = project_config_path.read_text()
    project_obj = load(project_text, Loader=Loader)

    assert project_config_path.is_file()
    assert project_config.name == project_obj["name"]
    assert project_config.config_version == project_obj["config-version"]
    assert project_config.version == project_obj["version"]
    assert project_config.default_profile == project_obj["default-profile"]
    assert Path(project_config.catalogue_path.name) == Path(
        project_obj["catalogue-path"]
    )
    assert Path(project_config.adapters_path.name) == Path(project_obj["adapters-path"])
