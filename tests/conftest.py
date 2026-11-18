import importlib.util
import pathlib

import pytest

if importlib.util.find_spec("pxr") is None:
    # The operations need USD, without it there is nothing to run them against.
    collect_ignore_glob = ["test_ops/*"]


@pytest.fixture(scope="session")
def output_dir() -> pathlib.Path:
    """Output directory for tests.

    Returns:
        pathlib.Path: path to test output directory.

    """
    out_dir = pathlib.Path.cwd() / ".test_output"
    out_dir.mkdir(exist_ok=True)
    return out_dir
