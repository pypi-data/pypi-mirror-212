import pytest  # noqa

from src.pcsFilter.tools.black import run_black
from tests.pcsFilter.unit.fixtures import create_temp_file  # noqa


@pytest.mark.parametrize(
    "create_temp_file",
    [{"file_name": "temp_test_black.py", "file_content": "\nimport os"}],
    indirect=True,
)
@pytest.mark.unit
def test_black(create_temp_file):
    """Test that black is launched"""
    expected = "import os\n"

    run_black(path=str(create_temp_file.file_path()))
    actual = create_temp_file.get_content()

    assert actual == expected
