import pathlib

import pytest

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

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
def test_get_files_info(
                        workdir: str,
                        directory: str,
                        expected_res: str
                        ) -> None:
    res = get_files_info(workdir, directory)
    assert res.strip() == expected_res.strip()


with open("./calculator/main.py", "r") as f:
    EXPECTED_MAIN_PY = f.read()

with open("./calculator/pkg/calculator.py", "r") as f:
    EXPECTED_CALC_PY = f.read()

EXPECTED_BIN_CAT = (
                    "Error: Cannot read '/bin/cat' as it is"
                    " outside the permitted working directory")

EXPECTED_NOT_EXISTS = (
                       "Error: File not found or is not a "
                       "regular file: 'pkg/does_not_exist.py'"
                      )


@pytest.mark.parametrize(
        "workdir, file_path, expected_res",
        [
            ("calculator", "main.py", EXPECTED_MAIN_PY),
            ("calculator", "pkg/calculator.py", EXPECTED_CALC_PY),
            ("calculator", "/bin/cat", EXPECTED_BIN_CAT),
            ("calculator", "pkg/does_not_exist.py", EXPECTED_NOT_EXISTS)
        ]
)
def test_get_file_content(
                          workdir: str,
                          file_path: str,
                          expected_res: str
                          ) -> None:
    res = get_file_content(workdir, file_path)
    assert res.strip() == expected_res.strip()


@pytest.mark.parametrize(
    "file_path, content, expect_error",
    [
        (
            "lorem.txt",
            "wait, this isn't lorem ipsum",
            False,
        ),
        (
            "pkg/morelorem.txt",
            "lorem ipsum dolor sit amet",
            False,
        ),
        (
            "/tmp/temp.txt",
            "this should not be allowed",
            True,
        ),
    ],
)
def test_write_file(
                    tmp_path: pathlib.Path,
                    file_path: str, content: str,
                    expect_error: bool
                    ) -> None:
    workdir = tmp_path

    target_path = workdir / file_path
    if target_path.parent != workdir:
        target_path.parent.mkdir(parents=True, exist_ok=True)

    res = write_file(str(workdir), file_path, content)

    if expect_error:
        assert "Error: Cannot write" in res
        assert not target_path.exists()
    else:
        assert "Successfully wrote" in res
        # Verify file contents were written correctly
        assert target_path.read_text() == content


if __name__ == "__main__":
    print(run_python_file("calculator", "main.py"))
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print(run_python_file("calculator", "tests.py"))
    print(run_python_file("calculator", "../main.py"))
    print(run_python_file("calculator", "nonexistent.py"))
