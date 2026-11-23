#!/usr/bin/env python3
"""Pins the gui_forms inputs the generator reads, at one gui_forms commit.

    python3 tools/pin_gui_forms.py <gui_forms checkout> <commit>

Copies ``manifests/abi/gf_abi.json`` (the C ABI) and
``manifests/control-schema.json`` (the control schema: types, properties,
interactions) as they are at ``commit`` into ``abi/``, and records the
commit and each file's SHA-256 in ``abi/gui_forms.lock``. The generator
reads only these copies, so the bindings move to a new ABI when, and only
when, the pin moves; ``tools/abi_python.py --check`` then shows what changed.
"""

from __future__ import annotations

import hashlib
import pathlib
import subprocess
import sys

ROOT: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent
PINNED: tuple[tuple[str, str], ...] = (
    ("manifests/abi/gf_abi.json", "gf_abi.json"),
    ("manifests/control-schema.json", "control-schema.json"),
)


def read_at(checkout: pathlib.Path, commit: str, path: str) -> bytes:
    completed: subprocess.CompletedProcess = subprocess.run(
        ["git", "-C", str(checkout), "show", commit + ":" + path], check=True, capture_output=True)
    return completed.stdout


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    checkout: pathlib.Path = pathlib.Path(sys.argv[1])
    requested: str = sys.argv[2]
    resolved: subprocess.CompletedProcess = subprocess.run(
        ["git", "-C", str(checkout), "rev-parse", requested + "^{commit}"], check=True, capture_output=True, text=True)
    commit: str = resolved.stdout.strip()
    lines: list[str] = ["# The gui_forms commit the bindings are generated from (tools/pin_gui_forms.py).",
                        "commit " + commit]
    for source, target in PINNED:
        content: bytes = read_at(checkout, commit, source)
        (ROOT / "abi" / target).write_bytes(content)
        digest: str = hashlib.sha256(content).hexdigest()
        lines.append("sha256 " + digest + " " + target + " " + source)
    (ROOT / "abi" / "gui_forms.lock").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("pinned gui_forms " + commit)
    return 0


if __name__ == "__main__":
    sys.exit(main())
