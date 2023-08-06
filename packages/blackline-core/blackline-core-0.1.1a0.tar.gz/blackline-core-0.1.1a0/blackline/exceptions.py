class CollectionNotFoundError(Exception):
    """
    Exception raised when an collection does not exist.

    Attributes:
        name (str): The name of the missing collection.

    Args:
        name (str): The name of the missing collection.

    Raises:
        CollectionNotFoundError: If an collection is not found.

    Example:
        try:
            fetch_collection_data(name)
        except CollectionNotFoundError as e:
            print(f"Collection '{e.name}' does not exist.")
    """

    def __init__(self, collection: str) -> None:
        self.collection = collection
        super().__init__(f"Collection '{collection}' does not exist.")


class FieldNotFoundError(Exception):
    """
    Exception raised when an SQLite collection does not include a given column.

    Attributes:
        collection_name (str): The name of the collection.
        field_name (str): The name of the missing column.

    Args:
        collection_name (str): The name of the collection.
        field_name (str): The name of the missing column.

    Raises:
        FieldNotFoundError: If an SQLite collection does not include the given column.

    Example:
        try:
            fetch_column_data(name, field_name)
        except FieldNotFoundError as e:
            print(f"Field '{e.field_name}' not found in collection '{e.name}'.")
    """

    def __init__(self, collection: str, field: str) -> None:
        self.collection = collection
        self.field = field
        super().__init__(f"Field '{field}' not found in collection '{collection}'.")


class InvalidFieldConstraintError(Exception):
    """
    Exception raised when a SQLite column constraint is invalid for a given de-identification method.

    Attributes:
        constraint_name (str): The name of the invalid column constraint.
        deidentification_method (str): The de-identification method being applied.

    Args:
        constraint_name (str): The name of the invalid column constraint.
        deidentification_method (str): The de-identification method being applied.

    Raises:
        InvalidFieldConstraintError: If a column constraint is not compatible with the de-identification method.

    Example:
        try:
            apply_deidentification_method(
                field_name,
                constraint_name,
                deidentification_method
                )
        except InvalidFieldConstraintError as e:
            print(f"Invalid column constraint '{e.constraint_name}' for de-identification method '{e.deidentification_method}'.") # noqa: E501
    """

    def __init__(self, constraint_name: str, deidentification_method: str) -> None:
        self.constraint_name = constraint_name
        self.deidentification_method = deidentification_method
        super().__init__(
            f"Invalid column constraint '{constraint_name}' for de-identification method '{deidentification_method}'."  # noqa: E501
        )


class InvalidDatsetError(Exception):
    """
    Exception raised when a Dataset is invalid.

    Attributes:
        name: The name of the invalid dataset.

    Args:
        name: The name of the invalid dataset.

    Raises:
        InvalidDatasetError: If a catalogue is invalid.

    Example:
        try:
            validate_catalogue(name)
        except InvalidDatasetError as e:
            print(f"Dataset '{e.name}' is invalid.")
    """

    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Dataset '{name}' is invalid.")
