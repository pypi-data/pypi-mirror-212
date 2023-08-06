from pathlib import Path
from typing import Callable

from blackline.execution.report import create_report
from blackline.models.catalogue import Catalogue
from blackline.models.datastores import DataStore
from blackline.models.project_config import ProjectConfig


def test_create_report(project_root: Path, sample_project: Callable):
    # Setup

    # Run
    project, stores, catalogue = create_report(path=project_root)

    # Assert
    assert isinstance(project, ProjectConfig)
    for store in stores:
        assert isinstance(store, DataStore)
    assert isinstance(catalogue, Catalogue)
