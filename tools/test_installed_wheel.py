#!/usr/bin/env python3
"""Installs a platform wheel into a fresh virtual environment per Python and runs the tests against it.

    python3 tools/test_installed_wheel.py dist/pyguiforms-*.whl --python python3.10 --python python3.14

The tests run from a copy outside the checkout, so they import the
installed package and its bundled library (GUI_FORMS_ABI_LIBRARY is
removed from their environment). The tests that read the checkout itself
(test_generated, test_wheel) stay behind. The run fails unless the
installed package finds its library, so no window test is skipped.
"""

from __future__ import annotations

import argparse
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent
CHECKOUT_TESTS: tuple[str, ...] = ("test_generated.py", "test_wheel.py")
FINDS_LIBRARY: str = ("import pyguiforms.native as native; found = native.find_library(); "
                      "print(found); raise SystemExit(0 if found.is_file() else 1)")


def environment_python(environment: pathlib.Path) -> pathlib.Path:
    if sys.platform == "win32":
        return environment / "Scripts" / "python.exe"
    return environment / "bin" / "python"


def run(command: list[str], folder: pathlib.Path, environment: dict[str, str]) -> None:
    print("$ " + " ".join(command), flush=True)
    subprocess.run(command, cwd=folder, env=environment, check=True)


def test_one(wheel: pathlib.Path, python: str, work: pathlib.Path) -> None:
    environment_folder: pathlib.Path = work / "environment"
    subprocess.run([python, "-m", "venv", str(environment_folder)], check=True)
    installed: str = str(environment_python(environment_folder))
    clean: dict[str, str] = dict(os.environ)
    clean.pop("GUI_FORMS_ABI_LIBRARY", None)
    run([installed, "-m", "pip", "install", "--quiet", "--no-index", str(wheel)], work, clean)
    copy: pathlib.Path = work / "copy"
    shutil.copytree(ROOT / "tests", copy / "tests")
    shutil.copytree(ROOT / "examples", copy / "examples")
    for name in CHECKOUT_TESTS:
        (copy / "tests" / name).unlink()
    run([installed, "-c", FINDS_LIBRARY], copy, clean)
    run([installed, "-X", "dev", "-m", "unittest", "discover", "-v", "-s", "tests", "-t", "."], copy, clean)


def main() -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("wheel", type=pathlib.Path)
    parser.add_argument("--python", action="append", required=True, help="an interpreter to test under")
    arguments: argparse.Namespace = parser.parse_args()
    wheel: pathlib.Path = arguments.wheel.resolve()
    for python in arguments.python:
        with tempfile.TemporaryDirectory() as folder:
            test_one(wheel, python, pathlib.Path(folder))
    return 0


if __name__ == "__main__":
    sys.exit(main())
