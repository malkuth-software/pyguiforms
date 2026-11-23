"""The platform wheel: built from a gui_forms C ABI archive, tagged py3-none-<platform>, RECORD checked."""

from __future__ import annotations

import hashlib
import json
import pathlib
import struct
import sys
import tempfile
import unittest
import zipfile

ROOT: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import build_wheel  # noqa: E402


def mach_o(minimum_major: int) -> bytes:
    """A thin 64-bit Mach-O header with one LC_BUILD_VERSION command naming minimum_major.0."""
    header: bytes = struct.pack("<IiiIIIII", build_wheel.MACH_O_MAGIC_64, 0x0100000C, 0, 6, 1, 24, 0, 0)
    command: bytes = struct.pack("<IIIIII", build_wheel.LC_BUILD_VERSION, 24, 1, minimum_major << 16, 0, 0)
    return header + command + b"\0" * 64


def write_archive(folder: pathlib.Path, platform: str, library: bytes, minor: int) -> pathlib.Path:
    name: str = build_wheel.loader_name(platform, 1)
    description: dict = {"schema": 1, "version": "0.6.0", "revision": "abc", "platform": platform, "abi_major": 1,
                         "abi_minor": minor, "library": name, "sha256": hashlib.sha256(library).hexdigest()}
    path: pathlib.Path = folder / ("gui-forms-abi-0.6.0-" + platform + ".zip")
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("ABI_LIBRARY.json", json.dumps(description))
        archive.writestr(name, library)
        archive.writestr("licenses/THIRD_PARTY_NOTICES.md", "notices\n")
    return path


class WheelTests(unittest.TestCase):

    def pinned_minor(self) -> int:
        manifest: dict = json.loads(build_wheel.PINNED_MANIFEST.read_text(encoding="utf-8"))
        return manifest["abi"]["minor"]

    def test_each_platform_builds_a_checked_wheel(self) -> None:
        expected: dict[str, str] = {"macos-arm64": "py3-none-macosx_14_0_arm64", "windows-x64": "py3-none-win_amd64",
                                    "linux-x64": "py3-none-linux_x86_64", "linux-arm64": "py3-none-linux_aarch64"}
        for platform, tag in expected.items():
            with self.subTest(platform=platform), tempfile.TemporaryDirectory() as folder:
                library: bytes = mach_o(14) if platform == "macos-arm64" else b"library bytes"
                archive: pathlib.Path = write_archive(pathlib.Path(folder), platform, library, self.pinned_minor())
                wheel: pathlib.Path = build_wheel.build(build_wheel.AbiArchive(archive), pathlib.Path(folder) / "dist")
                self.assertEqual(build_wheel.check_wheel(wheel), tag)
                self.assertTrue(wheel.name.endswith("-" + tag + ".whl"))
                with zipfile.ZipFile(wheel) as opened:
                    names: list[str] = opened.namelist()
                self.assertIn("pyguiforms/native.py", names)
                self.assertIn("pyguiforms/_native/" + build_wheel.loader_name(platform, 1), names)
                self.assertIn("pyguiforms/_native/licenses/THIRD_PARTY_NOTICES.md", names)

    def test_an_older_abi_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            archive: pathlib.Path = write_archive(pathlib.Path(folder), "linux-x64", b"x", self.pinned_minor() - 1)
            with self.assertRaises(build_wheel.WheelError):
                build_wheel.AbiArchive(archive)

    def test_a_changed_library_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            archive: pathlib.Path = write_archive(pathlib.Path(folder), "linux-x64", b"x", self.pinned_minor())
            tampered: pathlib.Path = pathlib.Path(folder) / "tampered.zip"
            with zipfile.ZipFile(archive) as source, zipfile.ZipFile(tampered, "w") as copy:
                for name in source.namelist():
                    data: bytes = source.read(name)
                    copy.writestr(name, data + b"!" if name.startswith("libgui") else data)
            with self.assertRaises(build_wheel.WheelError):
                build_wheel.AbiArchive(tampered)

    def test_the_wheel_is_reproducible(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            archive: pathlib.Path = write_archive(pathlib.Path(folder), "windows-x64", b"dll", self.pinned_minor())
            first: bytes = build_wheel.build(build_wheel.AbiArchive(archive), pathlib.Path(folder) / "a").read_bytes()
            second: bytes = build_wheel.build(build_wheel.AbiArchive(archive), pathlib.Path(folder) / "b").read_bytes()
            self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
