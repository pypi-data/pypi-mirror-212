from typing import Any, Optional

from pydantic import BaseModel


class Constant(BaseModel):
    """Base class for constants"""

    value: Any
    doc: Optional[str] = None


# Profject
SAMPLE_PROJECT_NAME = "blackline_sample"
SAMPLE_DATABASE = "blackline_sample.db"

# Project init constants
PROJECT_CONFIG_VERSION = 1
PROJECT_VERSION = "0.0.1"

# Project defaults
PROJECT_CONFIG_FILE = "blackline_project.yml"
DEFAULT_CATALOGUE_FOLDER = "./catalogue"
DEFAULT_ADAPTERS_FOLDER = "./adapters"
DEFAULT_PROFILE = "default"

# Logging constants
LOG_FORMAT = "%(asctime)s %(levelname)s: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Catalogue constants
CATALOGUE_CONFIG_FILE = "blackline_catalogue.yml"
CATALOGUE_CONFIG_VERSION = 1
CATALOGUE_VERSION = "0.0.1"

# SQL constants
NOT_NULL = "NOT NULL"
UNIQUE = "UNIQUE"
PRIMARY_KEY = "PRIMARY KEY"
FOREIGN_KEY = "FOREIGN KEY"
CHECK = "CHECK"
DEFAULT = "DEFAULT"
