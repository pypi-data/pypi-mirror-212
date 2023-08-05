import tempfile
from pathlib import Path

import pytest  # noqa

from src.pcsFilter.file_handling.abstract_file_handler import AFileHandler
from src.pcsFilter.file_handling.file_finder import file_from_path


@pytest.fixture
def create_temp_file(request) -> AFileHandler:
    """Create temporary test file"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file = file_from_path(Path(temp_dir) / request.param["file_name"])
        yield temp_file.write(request.param["file_content"])
