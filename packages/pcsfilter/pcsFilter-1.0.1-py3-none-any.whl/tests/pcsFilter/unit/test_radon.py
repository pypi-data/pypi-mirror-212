from pathlib import Path

import pytest  # noqa

from src.pcsFilter.file_handling.file_finder import file_from_path
from src.pcsFilter.tools.radon import run_radon
from tests.pcsFilter.unit.fixtures import create_temp_file  # noqa


@pytest.mark.unit
def test_radon():
    """Test that radon is launched"""
    expected_content = 'Average complexity'
    dir_path = str(Path(__file__))
    output_path = Path('.')
    run_radon(dir_path=dir_path, output_path=output_path)

    file_handler = file_from_path(output_path / "radon.txt")
    actual_content = file_handler.get_content()
    file_handler.delete()

    assert expected_content in actual_content
