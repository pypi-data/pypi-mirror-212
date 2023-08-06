from pathlib import Path

from blackline.constants import PROJECT_CONFIG_FILE
from blackline.models.datastores import DataStores
from blackline.models.project_config import ProjectConfig


class Debug:
    def __init__(self, path: Path, profile: str):
        self.path = path
        self.profile = profile
        self.project = ProjectConfig.parse_config_file(
            path=Path(path, PROJECT_CONFIG_FILE)
        )

        self.stores = DataStores.parse_folder(path=self.project.adapters_path)

    def debug(self):
        return {
            store.name: store.profiles[self.profile].adapter.test_connection()
            for store in self.stores.stores
        }
