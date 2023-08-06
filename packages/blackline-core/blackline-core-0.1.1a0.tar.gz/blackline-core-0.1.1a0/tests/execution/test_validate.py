from pathlib import Path
from sqlite3 import Connection
from typing import Callable

from blackline.execution.validate import Validate
from blackline.models.validation import (
    CollectionValidation,
    DatasetCollectionValidation,
    FieldValidation,
)


def test_validate_catalogue_dataset(
    project_root: Path,
    sample_project: Callable,
    profile: str,
    mock_sqlite_store: Connection,
) -> None:
    # Setup
    validate = Validate(path=project_root, profile=profile)

    # Run
    results = validate.validate_catalogue_dataset()

    # Assert
    for dataset_validation in results.values():
        assert isinstance(dataset_validation, DatasetCollectionValidation)
        for collection_validation in dataset_validation.collections.values():
            assert isinstance(collection_validation, CollectionValidation)
            for field_validation in collection_validation.fields.values():
                assert isinstance(field_validation, FieldValidation)
