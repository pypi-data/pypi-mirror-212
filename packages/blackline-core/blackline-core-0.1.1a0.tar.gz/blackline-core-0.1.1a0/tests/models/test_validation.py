from blackline.exceptions import (
    CollectionNotFoundError,
    FieldNotFoundError,
    InvalidFieldConstraintError,
)
from blackline.models.validation import (
    CollectionValidation,
    DatasetCollectionValidation,
    FieldValidation,
)


def test_field_validation_is_valid_when_no_exceptions():
    # Setup
    validation = FieldValidation(name="field")

    # Run
    is_valid = validation.is_valid

    # Assert
    assert is_valid is True


def test_field_validation_is_not_valid_when_exceptions_present():
    # Setup
    not_found_error = FieldNotFoundError(collection="my_collection", field="field")
    invalid_constraint_error = InvalidFieldConstraintError(
        constraint_name="NOT NULL", deidentification_method="Redact"
    )

    # Run
    validation = FieldValidation(
        name="field",
        not_found=not_found_error,
        invalid_constraint=invalid_constraint_error,
    )
    is_valid = validation.is_valid

    # Assert
    assert is_valid is False


def test_field_validation_exceptions_returns_list_of_exceptions():
    # Setup
    not_found_error = FieldNotFoundError(collection="my_collection", field="field")
    invalid_constraint_error = InvalidFieldConstraintError(
        constraint_name="NOT NULL", deidentification_method="Redact"
    )

    validation = FieldValidation(
        name="field",
        not_found=not_found_error,
        invalid_constraint=invalid_constraint_error,
    )

    # Run
    exceptions = validation.exceptions(flatten=True)

    # Assert
    assert isinstance(exceptions, list)
    assert len(exceptions) == 2
    assert not_found_error in exceptions
    assert invalid_constraint_error in exceptions


def test_field_validation_exceptions_returns_dict_of_exceptions():
    # Setup
    not_found_error = FieldNotFoundError(collection="my_collection", field="field")
    invalid_constraint_error = InvalidFieldConstraintError(
        constraint_name="NOT NULL", deidentification_method="Redact"
    )

    validation = FieldValidation(
        name="field",
        not_found=not_found_error,
        invalid_constraint=invalid_constraint_error,
    )

    # Run
    exceptions = validation.exceptions(flatten=False)

    # Assert
    assert isinstance(exceptions, dict)
    assert len(exceptions) == 2
    assert exceptions["not_found"] == not_found_error
    assert exceptions["invalid_constraint"] == invalid_constraint_error


def test_collection_validation_is_valid_when_no_exceptions():
    # Setup
    field_validation = FieldValidation(name="field")
    collection_validation = CollectionValidation(
        name="collection", not_found=None, fields={"field": field_validation}
    )

    # Run
    is_valid = collection_validation.is_valid

    # Assert
    assert is_valid is True


def test_collection_validation_is_not_valid_when_exceptions_present():
    # Setup
    not_found_error = CollectionNotFoundError(collection="my_collection")
    field_not_found_error = FieldNotFoundError(
        collection="my_collection", field="field"
    )
    field_validation = FieldValidation(name="field", not_found=field_not_found_error)
    collection_validation = CollectionValidation(
        name="collection", not_found=not_found_error, fields={"field": field_validation}
    )

    # Run
    is_valid = collection_validation.is_valid

    # Assert
    assert is_valid is False


def test_collection_validation_exceptions_returns_list_of_exceptions():
    # Setup
    not_found_error = CollectionNotFoundError(collection="my_collection")
    field_not_found_error = FieldNotFoundError(
        collection="my_collection", field="field"
    )
    field_validation = FieldValidation(name="field", not_found=field_not_found_error)
    collection_validation = CollectionValidation(
        name="collection", not_found=not_found_error, fields={"field": field_validation}
    )

    # Run
    exceptions = collection_validation.exceptions(flatten=True)

    # Assert
    assert isinstance(exceptions, list)
    assert len(exceptions) == 2
    assert not_found_error in exceptions
    assert field_not_found_error in exceptions


def test_collection_validation_exceptions_returns_dict_of_exceptions():
    # Setup
    collection_not_found_error = CollectionNotFoundError(collection="my_collection")
    field_not_found_error = FieldNotFoundError(
        collection="my_collection", field="field"
    )
    field_validation = FieldValidation(name="field", not_found=field_not_found_error)
    collection_validation = CollectionValidation(
        name="collection",
        not_found=collection_not_found_error,
        fields={"field": field_validation},
    )

    # Run
    exceptions = collection_validation.exceptions(flatten=False)

    # Assert
    assert isinstance(exceptions, dict)
    assert len(exceptions) == 2
    assert exceptions["not_found"] == collection_not_found_error
    assert exceptions["fields"]["field"] == field_validation


def test_dataset_collection_validation_is_valid_when_no_exceptions():
    # Setup
    collection_validation = CollectionValidation(
        name="collection", not_found=None, fields={}
    )
    dataset_collection_validation = DatasetCollectionValidation(
        collections={"collection": collection_validation}
    )

    # Run
    is_valid = dataset_collection_validation.is_valid

    # Assert
    assert is_valid is True


def test_dataset_collection_validation_is_not_valid_when_exceptions_present():
    # Setup
    not_found_error = CollectionNotFoundError(collection="my_collection")
    collection_validation = CollectionValidation(
        name="collection", not_found=not_found_error, fields={}
    )
    dataset_collection_validation = DatasetCollectionValidation(
        collections={"collection": collection_validation}
    )

    # Run
    is_valid = dataset_collection_validation.is_valid

    # Assert
    assert is_valid is False


def test_dataset_collection_validation_exceptions_returns_list_of_exceptions():
    # Setup
    not_found_error = CollectionNotFoundError(collection="my_collection")
    collection_validation = CollectionValidation(
        name="collection", not_found=not_found_error, fields={}
    )
    dataset_collection_validation = DatasetCollectionValidation(
        collections={"collection": collection_validation}
    )

    # Run
    exceptions = dataset_collection_validation.exceptions(flatten=True)

    # Assert
    assert isinstance(exceptions, list)
    assert len(exceptions) == 1
    assert not_found_error in exceptions


def test_dataset_collection_validation_exceptions_returns_dict_of_exceptions():
    # Setup
    not_found_error = CollectionNotFoundError(collection="my_collection")
    collection_validation = CollectionValidation(
        name="collection", not_found=not_found_error, fields={}
    )
    dataset_collection_validation = DatasetCollectionValidation(
        collections={"collection": collection_validation}
    )

    # Run
    exceptions = dataset_collection_validation.exceptions(flatten=False)

    # Assert
    assert isinstance(exceptions, dict)
    assert len(exceptions) == 1
    assert exceptions["collections"]["collection"]["not_found"] == not_found_error


def test_dataset_collection_validation_exceptions_returns_list_of_exception():
    # Setup
    not_found_error = CollectionNotFoundError(collection="my_collection")
    field_not_found_error = FieldNotFoundError(
        collection="my_collection", field="field"
    )
    field_validation = FieldValidation(name="field", not_found=field_not_found_error)
    collection_validation = CollectionValidation(
        name="collection", not_found=not_found_error, fields={"field": field_validation}
    )
    dataset_collection_validation = DatasetCollectionValidation(
        collections={"collection": collection_validation}
    )

    # Run
    exceptions = dataset_collection_validation.exceptions(flatten=True)

    # Assert
    assert isinstance(exceptions, list)
    assert len(exceptions) == 2
    assert not_found_error in exceptions
    assert field_not_found_error in exceptions


def test_dataset_collection_validation_exceptions_returns_dict_of_exception():
    # Setup
    not_found_error = CollectionNotFoundError(collection="my_collection")
    field_not_found_error = FieldNotFoundError(
        collection="my_collection", field="field"
    )
    field_validation = FieldValidation(name="field", not_found=field_not_found_error)
    collection_validation = CollectionValidation(
        name="collection", not_found=not_found_error, fields={"field": field_validation}
    )
    dataset_collection_validation = DatasetCollectionValidation(
        collections={"collection": collection_validation}
    )

    # Run
    exceptions = dataset_collection_validation.exceptions(flatten=False)

    # Assert
    assert isinstance(exceptions, dict)
    assert len(exceptions) == 1
    assert exceptions["collections"]["collection"]["not_found"] == not_found_error
    assert (
        exceptions["collections"]["collection"]["fields"]["field"] == field_validation
    )
