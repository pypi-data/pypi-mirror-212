from pathlib import Path

from blackline.constants import PROJECT_CONFIG_FILE
from blackline.models.catalogue import Catalogue
from blackline.models.datastores import DataStore, DataStores
from blackline.models.project_config import ProjectConfig


def create_report(
    path: Path, filename: str = PROJECT_CONFIG_FILE
) -> tuple[ProjectConfig, list[DataStore], Catalogue]:
    project = ProjectConfig.parse_config_file(path=Path(path, filename))
    stores = DataStores.parse_folder(path=project.adapters_path).stores
    catalogue = Catalogue.parse_dir(path=project.catalogue_path)
    return project, stores, catalogue
