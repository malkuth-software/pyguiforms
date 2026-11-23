#!/usr/bin/env python3
"""Builds pyguiforms' platform wheel from a gui_forms C ABI library archive.

    python3 tools/build_wheel.py --abi-archive gui-forms-abi-<version>-<platform>.zip [--out dist]
    python3 tools/build_wheel.py --check dist/pyguiforms-<version>-py3-none-<tag>.whl

The archive is what gui_forms' release workflow uploads per platform as the
artifact gui-forms-abi-<platform> (gui_forms tools/package_abi_library.py):
the library under its loader name, ABI_LIBRARY.json and licenses/. The
wheel is ``py3-none-<platform tag>``: the bindings are pure Python (ctypes)
and run on every CPython from 3.10, so one wheel per platform serves them
all. It holds:

  pyguiforms/*.py                  the package
  pyguiforms/_native/<library>     the library, where native.find_library looks
  pyguiforms/_native/ABI_LIBRARY.json   where it came from (gui_forms version and commit)
  pyguiforms/_native/licenses/     the notices that come with the library
  pyguiforms-<version>.dist-info/  METADATA, WHEEL, licenses/LICENSE, RECORD

Before writing, the archive is checked: its library's SHA-256, its name
against native.library_file_name for its platform, and its ABI version
against the pinned manifest (same major, a minor at least the pin's). The
platform tags: macosx_<minimum>_arm64 from the library's own
LC_BUILD_VERSION, win_amd64, and linux_x86_64 or linux_aarch64, which the
manylinux check (auditwheel repair) turns into a manylinux tag. The wheel is
reproducible: entries in name order, one fixed time.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import pathlib
import re
import struct
import sys
import zipfile

ROOT: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent
PACKAGE: pathlib.Path = ROOT / "pyguiforms"
PYPROJECT: pathlib.Path = ROOT / "pyproject.toml"
PINNED_MANIFEST: pathlib.Path = ROOT / "abi" / "gf_abi.json"
DESCRIPTION_NAME: str = "ABI_LIBRARY.json"
NATIVE: str = "pyguiforms/_native/"
FIXED_TIME: tuple[int, int, int, int, int, int] = (2026, 1, 1, 0, 0, 0)
LINUX_TAGS: dict[str, str] = {"linux-x64": "linux_x86_64", "linux-arm64": "linux_aarch64"}
# Mach-O: the 64-bit magic, and the load commands that carry the minimum macOS.
MACH_O_MAGIC_64: int = 0xFEEDFACF
LC_BUILD_VERSION: int = 0x32
LC_VERSION_MIN_MACOSX: int = 0x24
MAXIMUM_LOAD_COMMANDS: int = 4096


class WheelError(Exception):
    """An archive, library or wheel that does not check."""


def project_version() -> str:
    """The version pyproject.toml declares (``version = "..."`` under [project])."""
    match: re.Match | None = re.search(r'^version = "([^"]+)"$', PYPROJECT.read_text(encoding="utf-8"), re.M)
    if match is None:
        raise WheelError("pyproject.toml declares no version")
    return match.group(1)


def loader_name(platform: str, major: int) -> str:
    """The name pyguiforms.native.library_file_name gives on platform."""
    if platform.startswith("windows-"):
        return "gui_forms_abi" + str(major) + ".dll"
    if platform.startswith("macos-"):
        return "libgui_forms_abi." + str(major) + ".dylib"
    if platform.startswith("linux-"):
        return "libgui_forms_abi.so." + str(major)
    raise WheelError("no wheel for platform " + platform)


def macos_minimum(library: bytes) -> tuple[int, int]:
    """The minimum macOS (major, minor) a thin 64-bit Mach-O library declares."""
    if len(library) < 32 or struct.unpack_from("<I", library, 0)[0] != MACH_O_MAGIC_64:
        raise WheelError("the macOS library is not a thin 64-bit Mach-O image")
    command_count: int = struct.unpack_from("<I", library, 16)[0]
    if command_count > MAXIMUM_LOAD_COMMANDS:
        raise WheelError("the macOS library lists too many load commands")
    offset: int = 32
    for unused_index in range(command_count):
        if offset + 8 > len(library):
            break
        command, size = struct.unpack_from("<II", library, offset)
        if size < 8:
            break
        if command == LC_BUILD_VERSION and offset + 12 <= len(library):
            version: int = struct.unpack_from("<I", library, offset + 12)[0]
            return (version >> 16, (version >> 8) & 0xFF)
        if command == LC_VERSION_MIN_MACOSX and offset + 12 <= len(library):
            version = struct.unpack_from("<I", library, offset + 8)[0]
            return (version >> 16, (version >> 8) & 0xFF)
        offset += size
    raise WheelError("the macOS library declares no minimum macOS")


def platform_tag(platform: str, library: bytes) -> str:
    if platform == "macos-arm64":
        major, minor = macos_minimum(library)
        # From macOS 11 a wheel tag names the major version alone.
        return "macosx_" + str(major) + "_" + str(0 if major >= 11 else minor) + "_arm64"
    if platform == "windows-x64":
        return "win_amd64"
    tag: str | None = LINUX_TAGS.get(platform)
    if tag is None:
        raise WheelError("no wheel tag for platform " + platform)
    return tag


class AbiArchive:
    """A checked gui_forms C ABI library archive."""

    def __init__(self, path: pathlib.Path) -> None:
        self.path: pathlib.Path = path
        with zipfile.ZipFile(path) as archive:
            names: list[str] = archive.namelist()
            if DESCRIPTION_NAME not in names:
                raise WheelError(path.name + " lacks " + DESCRIPTION_NAME)
            self.description: dict = json.loads(archive.read(DESCRIPTION_NAME).decode("utf-8"))
            self.platform: str = self.description["platform"]
            self.library_name: str = self.description["library"]
            if self.library_name != loader_name(self.platform, self.description["abi_major"]):
                raise WheelError(path.name + ": the library is not named as pyguiforms loads it")
            self.library: bytes = archive.read(self.library_name)
            if hashlib.sha256(self.library).hexdigest() != self.description["sha256"]:
                raise WheelError(path.name + ": the library's SHA-256 is not the recorded one")
            self.licenses: dict[str, bytes] = {}
            for name in sorted(names):
                if name.startswith("licenses/") and not name.endswith("/"):
                    self.licenses[name[len("licenses/"):]] = archive.read(name)
        pinned: dict = json.loads(PINNED_MANIFEST.read_text(encoding="utf-8"))["abi"]
        if self.description["abi_major"] != pinned["major"] or self.description["abi_minor"] < pinned["minor"]:
            raise WheelError(path.name + " is ABI " + str(self.description["abi_major"]) + "." +
                             str(self.description["abi_minor"]) + "; the bindings are pinned at " +
                             str(pinned["major"]) + "." + str(pinned["minor"]))


def record_hash(data: bytes) -> str:
    digest: bytes = hashlib.sha256(data).digest()
    return "sha256=" + base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def metadata(version: str) -> str:
    readme: str = (ROOT / "README.md").read_text(encoding="utf-8")
    lines: list[str] = [
        "Metadata-Version: 2.4",
        "Name: pyguiforms",
        "Version: " + version,
        "Summary: Python bindings for GUI.Forms, over its C ABI",
        "Author: Malkuth Software",
        "License-Expression: MIT",
        "License-File: LICENSE",
        "Project-URL: Source, https://github.com/malkuth-software/pyguiforms",
        "Requires-Python: >=3.10",
        "Description-Content-Type: text/markdown",
        "",
        readme,
    ]
    return "\n".join(lines)


def package_files() -> list[pathlib.Path]:
    found: list[pathlib.Path] = []
    for path in sorted(PACKAGE.glob("*.py")):
        found.append(path)
    return found


def build(archive: AbiArchive, out: pathlib.Path) -> pathlib.Path:
    version: str = project_version()
    tag: str = "py3-none-" + platform_tag(archive.platform, archive.library)
    dist_info: str = "pyguiforms-" + version + ".dist-info/"
    entries: list[tuple[str, bytes, bool]] = []
    for path in package_files():
        entries.append(("pyguiforms/" + path.name, path.read_bytes(), False))
    entries.append((NATIVE + archive.library_name, archive.library, True))
    described: bytes = (json.dumps(archive.description, indent=2, sort_keys=True) + "\n").encode("utf-8")
    entries.append((NATIVE + DESCRIPTION_NAME, described, False))
    for name, data in archive.licenses.items():
        entries.append((NATIVE + "licenses/" + name, data, False))
    entries.append((dist_info + "METADATA", metadata(version).encode("utf-8"), False))
    wheel_text: str = "Wheel-Version: 1.0\nGenerator: pyguiforms tools/build_wheel.py\nRoot-Is-Purelib: false\n" + \
        "Tag: " + tag + "\n"
    entries.append((dist_info + "WHEEL", wheel_text.encode("utf-8"), False))
    entries.append((dist_info + "licenses/LICENSE", (ROOT / "LICENSE").read_bytes(), False))
    entries.sort()
    record_lines: list[str] = []
    for name, data, unused_executable in entries:
        record_lines.append(name + "," + record_hash(data) + "," + str(len(data)))
    record_lines.append(dist_info + "RECORD,,")
    entries.append((dist_info + "RECORD", ("\n".join(record_lines) + "\n").encode("utf-8"), False))
    out.mkdir(parents=True, exist_ok=True)
    target: pathlib.Path = out / ("pyguiforms-" + version + "-" + tag + ".whl")
    with zipfile.ZipFile(target, "w") as wheel:
        for name, data, executable in entries:
            entry: zipfile.ZipInfo = zipfile.ZipInfo(name, FIXED_TIME)
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = (0o755 if executable else 0o644) << 16
            wheel.writestr(entry, data)
    return target


def check_wheel(path: pathlib.Path) -> str:
    """The wheel's tag, after checking every RECORD hash and that the library and its provenance are in it."""
    with zipfile.ZipFile(path) as wheel:
        names: list[str] = wheel.namelist()
        records: list[str] = []
        for name in names:
            if name.endswith(".dist-info/RECORD"):
                records.append(name)
        if len(records) != 1:
            raise WheelError(path.name + " holds " + str(len(records)) + " RECORD files")
        listed: set[str] = set()
        for line in wheel.read(records[0]).decode("utf-8").splitlines():
            name, digest, unused_size = line.rsplit(",", 2)
            listed.add(name)
            if name == records[0]:
                continue
            if record_hash(wheel.read(name)) != digest:
                raise WheelError(path.name + ": " + name + " does not match its RECORD hash")
        if listed != set(names):
            raise WheelError(path.name + ": RECORD does not list exactly the wheel's files")
        if NATIVE + DESCRIPTION_NAME not in names:
            raise WheelError(path.name + " carries no " + NATIVE + DESCRIPTION_NAME)
        described: dict = json.loads(wheel.read(NATIVE + DESCRIPTION_NAME).decode("utf-8"))
        library: str = NATIVE + described["library"]
        if library not in names or hashlib.sha256(wheel.read(library)).hexdigest() != described["sha256"]:
            raise WheelError(path.name + ": the library is missing or not the recorded one")
        wheel_files: list[str] = []
        for name in names:
            if name.endswith(".dist-info/WHEEL"):
                wheel_files.append(name)
        match: re.Match | None = re.search(r"^Tag: (\S+)$", wheel.read(wheel_files[0]).decode("utf-8"), re.M)
    if match is None or not match.group(1).startswith("py3-none-"):
        raise WheelError(path.name + " is not tagged py3-none-<platform>")
    return match.group(1)


def main() -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--abi-archive", type=pathlib.Path)
    parser.add_argument("--out", type=pathlib.Path, default=ROOT / "dist")
    parser.add_argument("--check", type=pathlib.Path, nargs="*", default=None,
                        help="check these existing wheels; write nothing")
    arguments: argparse.Namespace = parser.parse_args()
    try:
        if arguments.check is not None:
            for path in arguments.check:
                print(path.name + ": " + check_wheel(path), flush=True)
            return 0
        if arguments.abi_archive is None:
            parser.error("--abi-archive is required to build")
        target: pathlib.Path = build(AbiArchive(arguments.abi_archive), arguments.out)
        print(target.name + ": " + check_wheel(target), flush=True)
    except WheelError as refused:
        print("build_wheel: " + str(refused), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
