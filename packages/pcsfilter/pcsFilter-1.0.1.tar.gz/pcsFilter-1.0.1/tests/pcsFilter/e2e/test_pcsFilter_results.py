"""
This test is designed to be run as part of e2e flow.
It is expected to fail if runs separately
"""
from pathlib import Path

import pytest

from src.pcsFilter.file_handling.existing_file import ExistingFile


@pytest.mark.e2e
def test_pcsFilter_results():
    actual_dir = Path('./actual')
    expected_dir = Path('./expected')

    _assert_files_are_the_same_in(actual_dir, expected_dir)
    _assert_file_contents_are_the_same_in(actual_dir, expected_dir)


def _assert_files_are_the_same_in(dir_1, dir_2):
    dir_1_contents = [path.name for path in dir_1.iterdir()]
    dir_2_contents = [path.name for path in dir_2.iterdir()]
    assert dir_1_contents == dir_2_contents


def _assert_file_contents_are_the_same_in(dir_1, dir_2):
    dir_1_paths = [path for path in dir_1.iterdir()]
    dir_2_paths = [path for path in dir_2.iterdir()]

    for file_1, file_2 in zip(dir_1_paths, dir_2_paths):
        assert ExistingFile(file_1).get_content() == \
               ExistingFile(file_2).get_content()

