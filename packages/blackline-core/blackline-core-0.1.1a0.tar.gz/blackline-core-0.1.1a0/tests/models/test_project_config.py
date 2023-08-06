from pathlib import Path
from typing import Callable

from blackline.constants import DEFAULT_ADAPTERS_FOLDER, DEFAULT_CATALOGUE_FOLDER
from blackline.models.project_config import ProjectConfig


def test_parse_project_config(
    project_root: Path,
    project_config_file: Path,
    sample_project: Callable,
):
    project_config_filepath = Path(project_root, project_config_file)
    config = ProjectConfig.parse_config_file(path=project_config_filepath)

    assert isinstance(config, ProjectConfig)
    assert config.name == "test_project"
    assert config.config_version == 1
    assert config.version == "0.0.1"
    assert config.default_profile == "dev"
    assert config.catalogue_path == Path(project_root, DEFAULT_CATALOGUE_FOLDER)
    assert config.adapters_path == Path(project_root, DEFAULT_ADAPTERS_FOLDER)
    assert config.project_root == project_root
