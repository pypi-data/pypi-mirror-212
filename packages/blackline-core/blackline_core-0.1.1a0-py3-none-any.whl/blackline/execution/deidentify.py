import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Type

from blackline.constants import PROJECT_CONFIG_FILE
from blackline.execution.validate import Validate
from blackline.models.catalogue import Catalogue
from blackline.models.datastores import DataStores
from blackline.models.project_config import ProjectConfig
from blackline.models.validation import DatasetCollectionValidation

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class Deidentify:
    """Deidentify class to orchestrate deidentification process."""

    def __init__(self, path: Path, profile: str, start_date: datetime) -> None:
        self.path = path
        self.profile = profile
        self.start_date = start_date
        self.project = ProjectConfig.parse_config_file(
            path=Path(path, PROJECT_CONFIG_FILE)
        )
        self.stores = DataStores.parse_folder(path=self.project.adapters_path)
        self.catalogue = Catalogue.parse_dir(path=self.project.catalogue_path)
        self.validate = Validate(path=path, profile=profile)

    def deidentify(self) -> None:
        for organization in self.catalogue.organizations.values():
            for system in organization.children.values():
                for resource in system.children.values():
                    for dataset_key, dataset in resource.children.items():
                        store = self.stores.store_by_key(
                            key=dataset_key, profile=self.profile
                        )
                        store.deidentify(catalogue=dataset, start_date=self.start_date)

    def validate_catalogue_dataset(self) -> list[DatasetCollectionValidation]:
        dataset_validations = self.validate.validate_catalogue_dataset()
        exceptions = []
        for dataset_validation in dataset_validations.values():
            for collection_validation in dataset_validation.collections.values():
                if collection_validation.not_found is not None:
                    exceptions.append(collection_validation.not_found)
                for field_validation in collection_validation.fields.values():
                    if field_validation.not_found is not None:
                        exceptions.append(field_validation.not_found)
                    if field_validation.invalid_constraint is not None:
                        exceptions.append(field_validation.invalid_constraint)
        return exceptions


def deidentify(
    path: Path, profile: str, start_date: datetime
) -> Optional[list[Type[Exception]]]:
    """Run method to orchestrate deidentification process."""
    deidentify = Deidentify(path=path, profile=profile, start_date=start_date)
    exceptions = deidentify.validate_catalogue_dataset()
    if exceptions:
        return exceptions
    deidentify.deidentify()
    return None
