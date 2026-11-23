"""The generated layers agree with the pinned manifests, and ctypes lays out every record as the manifest says."""

from __future__ import annotations

import hashlib
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

from pyguiforms import _abi
from pyguiforms import _controls
from pyguiforms import controls

ROOT: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import abi_python  # noqa: E402


class GeneratedTests(unittest.TestCase):

    def test_generated_files_match_the_pinned_manifests(self) -> None:
        completed: subprocess.CompletedProcess = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "abi_python.py"), "--check"], capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_the_lock_pins_both_copies(self) -> None:
        problems: list[str] = abi_python.verify_pins(abi_python.LOCK, (abi_python.DEFAULT_MANIFEST, abi_python.SCHEMA))
        self.assertEqual(problems, [])

    def test_an_edited_copy_fails_the_lock(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            copy: pathlib.Path = pathlib.Path(folder) / "gf_abi.json"
            shutil.copyfile(abi_python.DEFAULT_MANIFEST, copy)
            with copy.open("ab") as appended:
                appended.write(b"\n")
            problems: list[str] = abi_python.verify_pins(abi_python.LOCK, (copy,))
        self.assertEqual(len(problems), 1)
        self.assertIn("is not the copy", problems[0])

    def test_every_record_is_laid_out_as_the_manifest_says(self) -> None:
        self.assertEqual(_abi.check_layout(), [])
        manifest: dict = abi_python.json.loads(abi_python.DEFAULT_MANIFEST.read_text(encoding="utf-8"))
        for record in manifest["structs"]:
            with self.subTest(record=record["name"]):
                self.assertIn(record["name"], _abi.LAYOUT)

    def test_every_constant_is_generated(self) -> None:
        manifest: dict = abi_python.json.loads(abi_python.DEFAULT_MANIFEST.read_text(encoding="utf-8"))
        for constant in manifest["constants"]:
            with self.subTest(constant=constant["name"]):
                self.assertTrue(hasattr(_abi, constant["name"]))

    def test_every_schema_type_but_the_window_has_a_class(self) -> None:
        schema: dict = abi_python.json.loads(abi_python.SCHEMA.read_text(encoding="utf-8"))
        for listed in schema["types"]:
            if listed["id"] in abi_python.HAND_WRITTEN_TYPES:
                continue
            with self.subTest(type=listed["id"]):
                generated: type = _controls.TYPES[listed["id"]]
                self.assertEqual(generated.TYPE_ID, listed["id"])
                for listed_property in listed.get("properties", []):
                    self.assertIsInstance(getattr(generated, listed_property["name"]), controls.Property)
                interactions: list[str] = []
                for interaction in listed.get("interactions", []):
                    interactions.append(interaction["name"])
                self.assertEqual(list(generated.INTERACTIONS), interactions)

    def test_a_click_raises_through_the_control_hooks(self) -> None:
        raiser: controls.Raiser = controls.RAISERS["click"]
        self.assertEqual(raiser.class_id, _abi.GF_CLASS_CONTROL)
        offset: int = _abi.gf_control_hooks.on_click.offset
        self.assertEqual(raiser.entry, (offset - 8) // 8)

    def test_the_lock_names_the_commit(self) -> None:
        pins: dict[str, str] = abi_python.read_lock(abi_python.LOCK)
        self.assertEqual(len(pins["commit"]), 40)
        digest: str = hashlib.sha256(abi_python.SCHEMA.read_bytes()).hexdigest()
        self.assertEqual(pins["control-schema.json"], digest)


if __name__ == "__main__":
    unittest.main()
