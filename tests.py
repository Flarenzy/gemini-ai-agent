import pytest

from functions.get_files_info import get_files_info

EXPECTED_FOR_CURRENT = """
Result for current directory:
 - tests.py: file_size=1343 bytes, is_dir=False
 - main.py: file_size=576 bytes, is_dir=False
 - pkg: file_size=192 bytes, is_dir=True
 """

EXPECTED_FOR_PKG = """
Result for 'pkg' directory:
 - render.py: file_size=785 bytes, is_dir=False
 - __init__.py: file_size=0 bytes, is_dir=False
 - __pycache__: file_size=160 bytes, is_dir=True
 - calculator.py: file_size=1719 bytes, is_dir=False
"""

EXPECTED_FOR_BIN = """
Result for '/bin' directory:
    Error: Cannot list '/bin' as it is outside the permitted working directory
"""

EXPECTED_FOR_PARENT = """
Result for '../' directory:
    Error: Cannot list '../' as it is outside the permitted working directory
"""


@pytest.mark.parametrize(
        "workdir, directory, expected_res",
        [
            ("calculator", ".", EXPECTED_FOR_CURRENT),
            ("calculator", "pkg", EXPECTED_FOR_PKG),
            ("calculator", "/bin", EXPECTED_FOR_BIN),
            ("calculator", "../", EXPECTED_FOR_PARENT)
            ]
)
def test_get_files_info(workdir, directory, expected_res):
    res = get_files_info(workdir, directory)
    assert res.strip() == expected_res.strip()
