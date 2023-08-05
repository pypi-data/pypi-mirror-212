import pytest  # noqa

from src.pcsFilter.tools.isort import run_isort
from tests.pcsFilter.unit.fixtures import create_temp_file  # noqa


@pytest.mark.parametrize(
    "create_temp_file",
    [{"file_name": "temp_test_isort.py", "file_content": "import pathlib\nimport os"}],
    indirect=True,
)
@pytest.mark.unit
def test_isort(create_temp_file):
    """Test that isort is launched"""
    expected = "import os\nimport pathlib\n"

    run_isort(str(create_temp_file.file_path()))
    actual = create_temp_file.get_content()

    assert actual == expected
