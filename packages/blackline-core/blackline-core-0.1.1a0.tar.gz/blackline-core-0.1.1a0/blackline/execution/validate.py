from functools import cache
from pathlib import Path

from blackline.constants import PROJECT_CONFIG_FILE
from blackline.models.catalogue import Catalogue
from blackline.models.datastores import DataStores
from blackline.models.project_config import ProjectConfig
from blackline.models.validation import DatasetCollectionValidation


class Validate:
    """Deidentify class to orchestrate deidentification process."""

    def __init__(self, path: Path, profile: str) -> None:
        self.profile = profile

        self.project = ProjectConfig.parse_config_file(
            path=Path(path, PROJECT_CONFIG_FILE)
        )
        self.stores = DataStores.parse_folder(path=self.project.adapters_path)
        self.catalogue = Catalogue.parse_dir(path=self.project.catalogue_path)

    @cache
    def valid_dataset(self, dataset_key: str) -> bool:
        return self.validate_catalogue_dataset()[dataset_key].is_valid

    @cache
    def validate_catalogue_dataset(self) -> dict[str, DatasetCollectionValidation]:
        validated_datasets = {}
        for organization in self.catalogue.organizations.values():
            for system in organization.children.values():
                for resource in system.children.values():
                    for dataset_key, dataset in resource.children.items():
                        store = self.stores.store_by_key(
                            key=dataset_key, profile=self.profile
                        )
                        validated_datasets[
                            dataset_key
                        ] = store.adapter.validate_dataset(dataset=dataset)
        return validated_datasets
