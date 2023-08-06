"""
In an effort to meet the requirements for the Creative Commons Attribution 4.0
International License, please be aware that the following code is based on the
following work:
- https://github.com/ethyca/fideslang/blob/main/src/fideslang/models.py

The code has only been mildly modified to fit the needs of the Blackline project.

Contains all Pydantic models.
"""
from __future__ import annotations

from datetime import timedelta
from enum import Enum
from pathlib import Path
from typing import ClassVar, Literal, Optional, Type, Union

import yaml
from blackline.constants import CHECK, FOREIGN_KEY, NOT_NULL, PRIMARY_KEY, UNIQUE

# from blackline.constants import CHECK, NOT_NULL
from blackline.models.validation import (
    Key,
    check_valid_country_code,
    no_self_reference,
    sort_list_objects_by_name,
)
from pydantic import AnyUrl, BaseModel, Field, HttpUrl, validator

country_code_validator = validator("third_country_transfers", allow_reuse=True)(
    check_valid_country_code
)


name_field = Field(description="Human-Readable name for this resource.")
description_field = Field(
    description="A detailed description of what this resource is."
)


class DataResponsibilityTitle(str, Enum):
    """
    The model defining the responsibility or role over
    the system that processes personal data.

    Used to identify whether the organization is a
    Controller, Processor, or Sub-Processor of the data
    """

    CONTROLLER = "Controller"
    PROCESSOR = "Processor"
    SUB_PROCESSOR = "Sub-Processor"


class IncludeExcludeEnum(str, Enum):
    """
    Determine whether or not defined rights are
    being included or excluded.
    """

    ALL = "ALL"
    EXCLUDE = "EXCLUDE"
    INCLUDE = "INCLUDE"
    NONE = "NONE"


class DataSubjectRightsEnum(str, Enum):
    """
    The model for data subject rights over
    personal data.

    Based upon chapter 3 of the GDPR
    """

    INFORMED = "Informed"
    ACCESS = "Access"
    RECTIFICATION = "Rectification"
    ERASURE = "Erasure"
    PORTABILITY = "Portability"
    RESTRICT_PROCESSING = "Restrict Processing"
    WITHDRAW_CONSENT = "Withdraw Consent"
    OBJECT = "Object"
    OBJECT_TO_AUTOMATED_PROCESSING = "Object to Automated Processing"


class LegalBasisEnum(str, Enum):
    """
    The model for allowable legal basis categories

    Based upon article 6 of the GDPR
    """

    CONSENT = "Consent"
    CONTRACT = "Contract"
    LEGAL_OBLIGATION = "Legal Obligation"
    VITAL_INTEREST = "Vital Interest"
    PUBLIC_INTEREST = "Public Interest"
    LEGITIMATE_INTEREST = "Legitimate Interests"


class SpecialCategoriesEnum(str, Enum):
    """
    The model for processing special categories
    of personal data.

    Based upon article 9 of the GDPR
    """

    CONSENT = "Consent"
    EMPLOYMENT = "Employment"
    VITAL_INTEREST = "Vital Interests"
    NON_PROFIT_BODIES = "Non-profit Bodies"
    PUBLIC_BY_DATA_SUBJECT = "Public by Data Subject"
    LEGAL_CLAIMS = "Legal Claims"
    PUBLIC_INTEREST = "Substantial Public Interest"
    MEDICAL = "Medical"
    PUBLIC_HEALTH_INTEREST = "Public Health Interest"


class ResourceTypeEnum(str, Enum):
    """The model for resource types."""

    APPLICATION = "Application"
    SERVICE = "Service"
    DATABASE = "Database"
    DATALAKE = "Datalake"
    DATA_WAREHOUSE = "Data Warehouse"


class ImpactAssessmentStatusEnum(str, Enum):
    """The model for impact assessment statuses."""

    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    WAITING_FOR_APPROVAL = "Waiting for Approval"
    COMPLETE = "Complete"


class BlacklineModel(BaseModel):
    """The base model for all Resources."""

    key: Key = Field(description="A unique key used to identify this resource.")
    tags: Optional[list[str]] = Field(description="A list of tags for this resource.")
    name: Optional[str] = name_field
    description: Optional[str] = description_field

    children: Optional[dict[str, Type[BlacklineModel]]] = Field(
        None, description="The children resources."
    )
    stem: ClassVar[str] = Field(description="The stem of the resource.")
    children_stem: ClassVar[Optional[str]] = Field(
        description="The stem of the children resources."
    )
    children_cls: ClassVar[Optional[type[BlacklineModel]]] = Field(
        description="The children class."
    )

    class Config:
        "Config for the BlacklineModel"
        extra = "forbid"
        orm_mode = True

    def __getitem__(self, key: str) -> Type[BlacklineModel]:
        parts = key.split(".")
        key = ".".join([self.key, parts[0]])
        if self.children is None:
            raise KeyError(f"No children for {self.key}")
        model = self.children[key]

        for part in parts[1:]:
            model = model[part]  # type: ignore[index]
        return model

    @classmethod
    def parse_dir(cls, path: Path, key_prefix: Optional[str] = None):
        """
        Parse a directory of YAML files into a dictionary of Dataset objects.

        Args:
            path: The path to the directory of YAML files.
            path: Path

        Returns:
            A dictionary of Dataset objects.
        """
        key = ".".join([key_prefix, path.name]) if key_prefix is not None else path.name
        children = cls.parse_children(path=path, key_prefix=key)
        filepath = cls.find_definition_file(path=path)
        return cls.parse_yaml(path=filepath, key=key, children=children)

    @classmethod
    def find_definition_file(cls, path: Path) -> Path:
        file = list(path.glob(f"{cls.stem}.yml")) + list(path.glob(f"{cls.stem}.yaml"))
        file_len = len(list(file))
        if file_len == 0:
            raise FileNotFoundError(
                f"No {cls.stem} file found in directory: {path.absolute()}"
            )
        if file_len > 1:
            raise ValueError(
                f"Multiple {cls.stem} files found in directory: {path.absolute()}, only include one of resource.yaml or resource.yml"
            )
        return file[0]

    @classmethod
    def parse_yaml(
        cls,
        path: Path,
        key: str,
        children: Optional[dict[str, Type[BlacklineModel]]] = {},
    ):
        """
        Parse a yaml file into a the children_cls object.

        Args:
            path: Path location of the yaml file.
            key: Key to identify the dataset.

        Returns:
            Dataset object.
        """
        with open(path, "r") as f:
            info = yaml.safe_load(f)[cls.stem][0]
            info["key"] = key
            if cls.children_stem is not None:
                info[cls.children_stem] = children
            return cls.parse_obj(info)

    @classmethod
    def parse_children(
        cls, path: Path, key_prefix: Optional[str] = None
    ) -> dict[str, Type[BlacklineModel]]:
        """
        Parse a directory of YAML files into a dictionary of Dataset objects.

        Args:
            path: The path to the directory of YAML files.
            path: Path

        Returns:
            A dictionary of Dataset objects.
        """
        children: dict[str, Type[BlacklineModel]] = {}
        if cls.children_cls is None:
            return children
        for child_path in path.iterdir():
            if child_path.is_dir():
                child = cls.children_cls.parse_dir(
                    path=child_path, key_prefix=key_prefix
                )
                children[child.key] = child
        return children


class ContactDetails(BaseModel):
    """
    The contact details information model.

    Used to capture contact information for controllers, used
    as part of exporting a data map / ROPA.

    This model is nested under an Organization and
    potentially under a system/dataset.
    """

    name: Optional[str] = Field(
        description="An individual name used as part of publishing contact information.",
    )
    address: Optional[str] = Field(
        description="An individual address used as part of publishing contact information.",
    )
    email: Optional[str] = Field(
        description="An individual email used as part of publishing contact information.",
    )
    phone: Optional[str] = Field(
        description="An individual phone number used as part of publishing contact information.",
    )


class PrivacyDeclaration(BaseModel):
    """
    The PrivacyDeclaration resource model.

    States a function of a system, and describes how it relates
    to the privacy data types.
    """

    name: str = Field(
        description="The name of the privacy declaration on the system.",
    )
    data_categories: list[Key] = Field(
        description="An array of data categories describing a system in a privacy declaration.",
    )
    data_use: Key = Field(
        description="The Data Use describing a system in a privacy declaration.",
    )
    data_qualifier: Optional[Key] = Field(
        default=Key(
            "aggregated.anonymized.unlinked_pseudonymized.pseudonymized.identified"
        ),
        description="The key of the data qualifier describing a system in a privacy declaration.",
    )
    data_subjects: list[Key] = Field(
        description="An array of data subjects describing a system in a privacy declaration.",
    )
    dataset_references: Optional[list[Key]] = Field(
        description="Referenced Dataset keys used by the system.",
    )


class DataProtectionImpactAssessment(BaseModel):
    """
    The DataProtectionImpactAssessment (DPIA) resource model.

    Contains information in regard to the data protection
    impact assessment exported on a data map or Record of
    Processing Activities (RoPA).

    A legal requirement under GDPR for any project that
    introduces a high risk to personal information.
    """

    is_required: bool = Field(
        default=False,
        description="A boolean value determining if a data protection impact assessment is required. Defaults to False.",
    )
    status: Optional[ImpactAssessmentStatusEnum] = Field(
        default=None,
        description="The optional status of a Data Protection Impact Assessment. Returned on an exported data map or RoPA.",
    )
    link: Optional[AnyUrl] = Field(
        default=None,
        description="The optional link to the Data Protection Impact Assessment. Returned on an exported data map or RoPA.",
    )


class DatasetFieldBase(BaseModel):
    """Base DatasetField Resource model.

    This model is available for cases where the DatasetField information needs to be
    customized. In general this will not be the case and you will instead want to use
    the DatasetField model.

    When this model is used you will need to implement your own recursive field in
    to adding any new needed fields.

    Example:

    ```py
    from typing import list, Optional
    from . import DatasetFieldBase

    class MyDatasetField(DatasetFieldBase):
        custom: str
        fields: Optional[list[MyDatasetField]] = []
    ```
    """

    name: str = name_field
    description: Optional[str] = description_field
    data_categories: Optional[list[Key]] = Field(
        description="Arrays of Data Categories, identified by `key`, that applies to this field.",
    )
    data_qualifier: Key = Field(
        default=Key(
            "aggregated.anonymized.unlinked_pseudonymized.pseudonymized.identified"
        ),
        description="A Data Qualifier that applies to this field. Note that this field holds a single value, therefore, the property name is singular.",
    )
    deidentifier: Optional[Union[Redact, Mask, Replace]] = Field(
        ...,
        discriminator="type",
        description="The deidentifier to apply to this field.",
    )
    period: timedelta = Field(description="The period of time to retain data.")


class DatasetField(DatasetFieldBase):
    """
    The DatasetField resource model.

    This resource is nested within a DatasetCollection.
    """

    fields: Optional[list[DatasetField]] = Field(
        description="An optional array of objects that describe hierarchical/nested fields (typically found in NoSQL databases).",
    )


class DatetimeField(BaseModel):
    name: str = Field(description="The name of the field to use datetime information.")


class DatasetCollection(BaseModel):
    """
    The DatasetCollection resource model.

    This resource is nested witin a Dataset.
    """

    name: str = name_field
    description: Optional[str] = description_field
    data_categories: Optional[list[Key]] = Field(
        description="Array of Data Category resources identified by `key`, that apply to all fields in the collection.",
    )
    data_qualifier: Key = Field(
        default=Key(
            "aggregated.anonymized.unlinked_pseudonymized.pseudonymized.identified"
        ),
        description="Array of Data Qualifier resources identified by `key`, that apply to all fields in the collection.",
    )
    fields: list[DatasetField] = Field(
        description="An array of objects that describe the collection's fields.",
    )
    datetime_field: DatetimeField = Field(
        description="The datetime field to use for the retention limit calculations."
    )

    _sort_fields: classmethod = validator("fields", allow_reuse=True)(
        sort_list_objects_by_name
    )


class DeidentifierBase(BaseModel):
    description: Optional[str] = None
    valid_constraints: ClassVar[list] = []
    invalid_constraints: ClassVar[list] = []


class Redact(BaseModel):
    type: Literal["redact"]
    value: None = None
    invalid_constraints: ClassVar[list] = [
        NOT_NULL,
        UNIQUE,
        PRIMARY_KEY,
        FOREIGN_KEY,
        CHECK,
    ]


class Mask(BaseModel):
    type: Literal["mask"]
    value: str
    invalid_constraints: ClassVar[list] = [
        UNIQUE,
        PRIMARY_KEY,
        FOREIGN_KEY,
    ]


class Replace(BaseModel):
    type: Literal["replace"]
    value: str
    invalid_constraints: ClassVar[list] = [
        UNIQUE,
        PRIMARY_KEY,
        FOREIGN_KEY,
    ]


DatasetField.update_forward_refs()


class Dataset(BlacklineModel):
    """The Dataset resource model.

    Todo: This breaks the Liskov substitution principle because it restrics the BlacklineModel,
    not expand it. This model has no children.
    """

    meta: Optional[dict[str, str]] = Field(
        description=Key(
            "An optional object that provides additional information about the Dataset. You can structure the object however you like. It can be a simple set of `key: value` properties or a deeply nested hierarchy of objects."
        ),
    )
    data_categories: Optional[list[Key]] = Field(
        description="Array of Data Category resources identified by `key`, that apply to all collections in the Dataset.",
    )
    data_qualifier: Key = Field(
        default=Key(
            "aggregated.anonymized.unlinked_pseudonymized.pseudonymized.identified"
        ),
        description="Array of Data Qualifier resources identified by `key`, that apply to all collections in the Dataset.",
    )
    joint_controller: Optional[ContactDetails] = Field(
        description=ContactDetails.__doc__,
    )
    third_country_transfers: Optional[list[str]] = Field(
        description="An optional array to identify any third countries where data is transited to. For consistency purposes, these fields are required to follow the Alpha-3 code set in [ISO 3166-1](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3).",
    )
    collections: list[DatasetCollection] = Field(
        description="An array of objects that describe the Dataset's collections.",
    )
    _sort_collections: classmethod = validator("collections", allow_reuse=True)(
        sort_list_objects_by_name
    )
    _check_valid_country_code: classmethod = country_code_validator

    stem = "dataset"
    children_stem = None
    children_cls = None


class Resource(BlacklineModel):
    """
    The System resource model.

    Describes an application and includes a list of PrivacyDeclaration resources.
    """

    resource_type: ResourceTypeEnum = Field(
        description="A required value to describe the type of system being modeled",
    )
    data_responsibility_title: DataResponsibilityTitle = Field(
        default=DataResponsibilityTitle.CONTROLLER,
        description=DataResponsibilityTitle.__doc__,
    )
    privacy_declarations: list[PrivacyDeclaration] = Field(
        description=PrivacyDeclaration.__doc__,
    )
    dependencies: Optional[list[Key]] = Field(
        description="A list of keys to model dependencies."
    )
    joint_controller: Optional[ContactDetails] = Field(
        description=ContactDetails.__doc__,
    )
    third_country_transfers: Optional[list[str]] = Field(
        description="An optional array to identify any countries where data is transited to. For consistency purposes, these fields are required to follow the Alpha-3 code set in ISO 3166-1.",
    )
    administrating_department: Optional[str] = Field(
        description="The department or group that owns the resource",
    )
    data_protection_impact_assessment: DataProtectionImpactAssessment = Field(
        default=DataProtectionImpactAssessment(),
        description=DataProtectionImpactAssessment.__doc__,
    )

    children: dict[str, Dataset] = Field(description="Dataset dict", alias="datasets")  # type: ignore[assignment]

    stem = "resource"
    children_stem = "datasets"
    children_cls = Dataset

    _sort_privacy_declarations: classmethod = validator(
        "privacy_declarations", allow_reuse=True
    )(sort_list_objects_by_name)

    _no_self_reference: classmethod = validator(
        "dependencies", allow_reuse=True, each_item=True
    )(no_self_reference)

    _check_valid_country_code: classmethod = country_code_validator

    class Config:
        "Class for the System config"
        use_enum_values = True


class System(BlacklineModel):
    """
    The System resource model.

    Systems can be assigned to this resource, but it doesn't inherently
    point to any other resources.
    """

    children: dict[str, Resource] = Field(..., alias="resources")  # type: ignore[assignment]

    stem = "system"
    children_stem = "resources"
    children_cls = Resource


class Organization(BlacklineModel):
    """
    The Organization resource model.

    This resource is used as a way to organize all other resources.
    """

    controller: Optional[ContactDetails] = Field(
        description=ContactDetails.__doc__,
    )
    data_protection_officer: Optional[ContactDetails] = Field(
        description=ContactDetails.__doc__,
    )
    representative: Optional[ContactDetails] = Field(
        description=ContactDetails.__doc__,
    )
    security_policy: Optional[HttpUrl] = Field(
        description="Am optional URL to the organization security policy."
    )
    children: dict[str, System] = Field(description="System dict", alias="systems")  # type: ignore[assignment]

    stem = "organization"
    children_stem = "systems"
    children_cls = System


class Catalogue(BaseModel):
    organizations: dict[str, Organization]

    @classmethod
    def parse_dir(cls, path: Path) -> Catalogue:
        return cls(
            organizations={
                org_dir.stem: Organization.parse_dir(path=org_dir)
                for org_dir in path.iterdir()
            }
        )

    def __getitem__(self, key) -> Type[BlacklineModel]:
        parts = key.split(".")
        model: Type[BlacklineModel] = self.organizations[parts[0]]  # type: ignore[assignment]
        for part in parts[1:]:
            model = model[part]  # type: ignore[index]
        return model
