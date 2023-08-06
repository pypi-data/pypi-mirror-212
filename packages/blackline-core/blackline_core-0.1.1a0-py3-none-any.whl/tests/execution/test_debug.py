from pathlib import Path
from typing import Callable

from blackline.execution.debug import Debug


def test__init__(project_root: Path, sample_project: Callable, profile: str):
    """Test the __init__ method."""
    # Run
    debug = Debug(path=project_root, profile=profile)

    # Assert
    assert isinstance(debug, Debug)


def test_debug(project_root: Path, sample_project: Callable, profile: str):
    """Test the debug method."""
    # Setup
    debug = Debug(path=project_root, profile=profile)

    # Run
    result = debug.debug()

    # Assert
    assert isinstance(result, dict)
    assert [store.name for store in debug.stores.stores] == list(result.keys())
    for debug_result in result.values():
        assert debug_result
