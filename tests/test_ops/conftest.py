import pytest

from nyx_usd import ops


@pytest.fixture(autouse=True)
def close_stages():
    yield
    ops.close_all()


@pytest.fixture
def stage() -> str:
    """Handle of an empty stage in memory."""
    return ops.create_stage()
