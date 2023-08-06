"""
In an effort to meet the requirements for the Creative Commons Attribution 4.0
International License, please be aware that the following code is based on the
following work:
- https://github.com/ethyca/fideslang/blob/main/src/fideslang/validation.py

The code has only been mildly modified to fit the needs of the Blackline project.

Contains all of the additional validation for the resource models.
"""

import re
from typing import Optional, Pattern, Union

from blackline.exceptions import (
    CollectionNotFoundError,
    FieldNotFoundError,
    InvalidFieldConstraintError,
)
from blackline.utils.default_fixtures import COUNTRY_CODES
from pydantic import BaseModel, ConstrainedStr, Field

VALID_COUNTRY_CODES = [country["alpha3Code"] for country in COUNTRY_CODES]


class Key(ConstrainedStr):
    """
    A Key type that creates a custom constrained string.
    """

    regex: Pattern[str] = re.compile(r"^[a-zA-Z0-9_.-]+$")

    # This overrides the default method to throw the custom ValidationError
    @classmethod
    def validate(cls, value: str) -> str:
        if not cls.regex.match(value):
            raise ValueError(
                "Key must only contain alphanumeric characters, '.', '_' or '-'."
            )

        return value


def sort_list_objects_by_name(values: list) -> list:
    """
    Sort objects in a list by their name.
    This makes resource comparisons deterministic.
    """
    values.sort(key=lambda value: value.name)
    return values


def no_self_reference(value: Key, values: dict) -> Key:
    """
    Check to make sure that the _key doesn't match other _key
    references within an object.

    i.e. DataCategory.parent_key != DataCategory.key
    """

    key = Key.validate(values.get("key", ""))
    if value == key:
        raise ValueError("Key can not self-reference!")
    return value


def check_valid_country_code(country_code_list: list) -> list:
    """
    Validate all listed countries (if present) are valid country codes.
    """
    if country_code_list is not None:
        for country_code in country_code_list:
            if country_code not in VALID_COUNTRY_CODES:
                raise ValueError(
                    f"The country identified as {country_code} is not a valid Alpha-3 code per ISO 3166."  # noqa: E501
                )

    return country_code_list


class ValidationBase(BaseModel):
    """
    Base class for validation models.
    """

    name: str = Field(..., exclude=True)

    class Config:
        """
        Config class for validation models.
        """

        arbitrary_types_allowed = True
        extra = "forbid"


class FieldValidation(ValidationBase):
    not_found: Optional[FieldNotFoundError] = None
    invalid_constraint: Optional[InvalidFieldConstraintError] = None

    @property
    def is_valid(self):
        return self.not_found is None and self.invalid_constraint is None

    def exceptions(self, flatten: bool = False) -> Union[list[Exception], dict]:
        if flatten:
            return [
                exc
                for exc in [self.not_found, self.invalid_constraint]
                if exc is not None
            ]
        return self.dict()


class CollectionValidation(ValidationBase):
    not_found: Optional[CollectionNotFoundError] = None
    fields: dict[str, FieldValidation] = {}

    @property
    def is_valid(self):
        return (
            all([field.is_valid for field in self.fields.values()])
            and self.not_found is None
        )

    def exceptions(self, flatten: bool = False) -> Union[dict, list[Exception]]:
        if flatten:
            return [
                exc
                for exc in [self.not_found]
                + [
                    item
                    for sublist in [
                        field.exceptions(flatten=True) for field in self.fields.values()
                    ]
                    for item in sublist
                ]
                if exc is not None
            ]
        return self.dict()


class DatasetCollectionValidation(BaseModel):
    collections: dict[str, CollectionValidation] = {}

    @property
    def is_valid(self):
        return all([collection.is_valid for collection in self.collections.values()])

    def exceptions(self, flatten: bool = False) -> Union[dict, list[Exception]]:
        if flatten:
            return [
                exc
                for exc in [
                    item
                    for sublist in [
                        collection.exceptions(flatten=True)
                        for collection in self.collections.values()
                    ]
                    for item in sublist
                ]
                if exc is not None
            ]
        return self.dict()
