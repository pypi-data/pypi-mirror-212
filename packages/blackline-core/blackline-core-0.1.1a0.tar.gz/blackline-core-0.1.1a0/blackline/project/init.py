from pathlib import Path
from typing import Tuple

from blackline.constants import (
    DEFAULT_ADAPTERS_FOLDER,
    DEFAULT_CATALOGUE_FOLDER,
    DEFAULT_PROFILE,
    PROJECT_CONFIG_FILE,
    PROJECT_CONFIG_VERSION,
    PROJECT_VERSION,
)
from blackline.models.project_config import ProjectConfig
from jinja2 import Environment, PackageLoader

DEFAULT_ORGANIZATION_FOLDER = "organization"
DEFAULT_SYSTEM_FOLDER = "system"
DEFAULT_RESOURCE_FOLDER = "resource"
DEFAULT_DATASET_FOLDER = "dataset"

INIT_ORGANIZATION_FOLDER = "organization"
INIT_SYSTEM_FOLDER = "system"
INIT_RESOURCE_FOLDER = "resource"
INIT_DATASET_FOLDER = "dataset"

INIT_ORGANIZATION_FILENAME = "organization.yaml"
INIT_SYSTEM_FILENAME = "system.yaml"
INIT_RESOURCE_FILENAME = "resource.yaml"
INIT_DATASET_FILENAME = "dataset.yaml"

INIT_ADAPTER = f"""
# See details docs at https://docs.getblackline.com/
# Only required fields are shown here.
profiles:
  {DEFAULT_PROFILE}:
    type: <type_name>
    config:
    ...
"""

INIT_ORGANIZATION = """
# See details docs at https://docs.getblackline.com/
# Only required fields are shown here.
organization:
  - key: <requred_key>
  ...
"""

INIT_SYSTEM = """
# See details docs at https://docs.getblackline.com/
# Only required fields are shown here.
system:
  - key: <requred_key>
  ...
"""

INIT_RESOURCE = """
# See details docs at https://docs.getblackline.com/
# Only required fields are shown here.
resource:
  - key: <requred_key>
    resource_type: <requred_resource_type>
    privacy_declarations:
        - name: <requred_name>
          data_categories:
            - <requred_data_category>
          data_use: <requred_data_use>
          data_subjects:
            - <requred_data_subject>
          data_qualifier: <requred_data_qualifier>
  ...
"""

INIT_DATASET = """
# See details docs at https://docs.getblackline.com/
# Only required fields are shown here.
dataset:
  - key: <requred_key>
  ...
"""


class InitProject:
    def __init__(
        self,
        path: Path,
        name: str,
        overwrite: bool = False,
        default_profile: str = DEFAULT_PROFILE,
        catalogue: str = DEFAULT_CATALOGUE_FOLDER,
        adapters: str = DEFAULT_ADAPTERS_FOLDER,
        organization: str = DEFAULT_ORGANIZATION_FOLDER,
        system: str = DEFAULT_SYSTEM_FOLDER,
        resource: str = DEFAULT_RESOURCE_FOLDER,
        dataset: str = DEFAULT_DATASET_FOLDER,
        init_organization: str = INIT_ORGANIZATION,
        init_system: str = INIT_SYSTEM,
        init_resource: str = INIT_RESOURCE,
        init_dataset: str = INIT_DATASET,
        init_adapter: str = INIT_ADAPTER,
    ) -> None:
        """
        A class for initializing a new Blackline project.

        Args:
            path: The path to the directory where the project should be created.
            name : The name of the project.
            overwrite : Whether to overwrite an existing project with the same name.
            default_profile : The default profile to use.
            catalogue : The name of the catalogue folder.
            adapters: The name of the adapters folder.
            organization: The name of the organization folder.
            system: The name of the system folder.
            resource: The name of the resource folder.
            dataset: The name of the dataset folder.
            init_organization: The initial organization configuration.
            init_system: The initial system configuration.
            init_resource: The initial resource configuration.
            init_dataset: The initial dataset configuration.
            init_adapter: The initial adapter configuration.

        Attributes:
            path (Path): The path to the directory where the project should be created.
            name (str): The name of the project.
            overwrite (bool): Whether to overwrite an existing project with the same name. # noqa: E501
            default_profile (str): The default profile to use.
            catalogue_path (Path): The path to the catalogue folder.
            adapters_path (Path): The path to the adapters folder.
            organization (str): The name of the organization folder.
            system (str): The name of the system folder.
            resource (str): The name of the resource folder.
        """
        self.path = path
        self.name = name
        self.overwrite = overwrite
        self.default_profile = default_profile
        self.catalogue_path = Path(path, catalogue or DEFAULT_CATALOGUE_FOLDER)
        self.adapters_path = Path(path, adapters or DEFAULT_ADAPTERS_FOLDER)
        self.organization = organization
        self.system = system
        self.resource = resource
        self.dataset = dataset
        self.init_organization: str = init_organization
        self.init_system = init_system
        self.init_resource = init_resource
        self.init_dataset = init_dataset
        self.init_adapter = init_adapter
        self.project_config = ProjectConfig(
            name=self.name,
            config_version=PROJECT_CONFIG_VERSION,
            version=PROJECT_VERSION,
            default_profile=self.default_profile,
            catalogue_path=self.catalogue_path,
            adapters_path=self.adapters_path,
            project_root=self.path,
        )

    def init_project(self) -> None:
        """Creates a new project."""

        self.create_project_yaml()
        self.create_adapter()
        self.create_catalogue()

    def create_project_yaml(self) -> None:
        """Creates a YAML file for the project configuration."""

        self.path.mkdir(exist_ok=True)
        env = Environment(loader=PackageLoader("blackline.project", "templates"))
        template = env.get_template("blackline_project.yml")
        project = template.render(config=self.project_config)
        Path(self.path, PROJECT_CONFIG_FILE).write_text(project)

    def create_adapter(
        self,
    ) -> Path:
        """Creates an adapter for the project.

        Returns:
            Path: The path of the adapter.
        """
        adapter_path = self.create_adapter_folders()
        self.create_adapter_file(resource_path=adapter_path)
        return adapter_path

    def create_adapter_folders(
        self,
    ) -> Path:
        """Creates folders for the adapter.

        Returns:
            Path: The path of the adapter folder.
        """

        resource_path = Path(
            self.adapters_path,
            self.organization,
            self.system,
            self.resource,
        )
        resource_path.mkdir(parents=True, exist_ok=True)
        return resource_path

    def create_adapter_file(
        self,
        resource_path: Path,
    ) -> None:
        """Creates a file for the adapter.

        Args:
            resource_path: The path of the adapter folder.

        Returns:
            None
        """
        Path(resource_path, INIT_DATASET_FILENAME).write_text(self.init_adapter)

    def create_catalogue(self) -> None:
        """Creates the catalogue folder and files.

        Args:
            None

        Returns:
            None
        """
        (
            organization_path,
            system_path,
            resource_path,
            dataset_path,
        ) = self.create_catalogue_folders()
        self.create_catalogue_files(
            organization_path=organization_path,
            system_path=system_path,
            resource_path=resource_path,
            dataset_path=dataset_path,
        )

    def create_catalogue_folders(self) -> Tuple[Path, Path, Path, Path]:
        """Creates folders for the catalogue.


        Returns:
            A tuple containing the paths of the organisation, system, resource and dataset folders. # noqa: E501
        """
        catalogue_path = self.catalogue_path
        organisation_path = Path(catalogue_path, self.organization)
        system_path = Path(organisation_path, self.system)
        resource_path = Path(system_path, self.resource)
        dataset_path = Path(resource_path, self.dataset)
        dataset_path.mkdir(parents=True, exist_ok=True)
        return organisation_path, system_path, resource_path, dataset_path

    def create_catalogue_files(
        self,
        organization_path: Path,
        system_path: Path,
        resource_path: Path,
        dataset_path: Path,
    ) -> None:
        """Create the catalogue files in the specified paths.

        Args:
            organization_path: Path to the organization folder.
            system_path: Path to the system folder.
            resource_path: Path to the resource folder.
            dataset_path: Path to the dataset folder.

        Returns:
            None
        """
        Path(organization_path, INIT_ORGANIZATION_FILENAME).write_text(
            self.init_organization
        )
        Path(system_path, INIT_SYSTEM_FILENAME).write_text(self.init_system)
        Path(resource_path, INIT_RESOURCE_FILENAME).write_text(self.init_resource)
        Path(dataset_path, INIT_DATASET_FILENAME).write_text(self.init_dataset)
