from pathlib import Path

import yaml
from blackline.constants import DEFAULT_ADAPTERS_FOLDER, DEFAULT_CATALOGUE_FOLDER
from pydantic import BaseModel, Field, root_validator


class ProjectConfig(BaseModel):
    """
    Pydantic model for the configuration of a Blackline project.
    """

    name: str = Field(..., description="Name of the project.")
    config_version: int = Field(
        default=1,
        alias="config-version",
        description="Version of the project configuration file.",
    )
    version: str = Field(default="1", description="Version of the project.")
    default_profile: str = Field(
        default="default",
        alias="default-profile",
        description="Default profile to use for the project.",
    )
    catalogue_path: Path = Field(
        alias="catalogue-path",
        description="Path to the directory containing the project's metadata catalogue.",  # noqa: E501
    )
    adapters_path: Path = Field(
        alias="adapters-path",
        description="Path to the directory containing the project's adapters.",
    )
    project_root: Path = Field(
        default=Path("."),
        alias="project-root",
        description="Path to the root directory of the project.",
    )

    class Config:
        allow_population_by_field_name = True

    @root_validator(pre=True)
    def add_root_to_path(cls, values):
        values["adapters-path"] = Path(
            values["project_root"], values.get("adapters-path", DEFAULT_ADAPTERS_FOLDER)
        )
        values["catalogue-path"] = Path(
            values["project_root"],
            values.get("catalogue-path", DEFAULT_CATALOGUE_FOLDER),
        )
        return values

    @classmethod
    def parse_config_file(cls, path: Path) -> "ProjectConfig":
        """
        Parse a project configuration file.

        Args:
            filepath (Path): Path to the project configuration file.

        Returns:
            ProjectConfig: A ProjectConfig instance.
        """
        with open(path, "rb") as f:
            info = yaml.safe_load(f)
            info["project_root"] = path.parent
            return cls.parse_obj(info)
