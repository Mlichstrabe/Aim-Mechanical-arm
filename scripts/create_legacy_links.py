"""Create optional Windows directory junctions for pre-restructure paths."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.project_paths import (
    AIMOOE_OUTPUT_DIR,
    HAND_EYE_DIR,
    LEGACY_DATATIMO_DIR,
    LEGACY_HAND_EYE_DIRS,
    ensure_dir,
)


def _junction(link: Path, target: Path) -> str:
    if link.exists():
        return f"skip (exists): {link.name}"
    ensure_dir(target)
    cmd = ["cmd", "/c", "mklink", "/J", str(link), str(target.resolve())]
    subprocess.run(cmd, check=True)
    return f"created junction: {link.name} -> {target}"


def main() -> int:
    ensure_dir(HAND_EYE_DIR)
    ensure_dir(AIMOOE_OUTPUT_DIR)

    messages: list[str] = []
    try:
        for name in ("hand-eye calibration", "hand–eye calibration"):
            link = _REPO_ROOT / name
            if link.exists():
                messages.append(f"skip (exists): {name}")
                continue
            messages.append(_junction(link, HAND_EYE_DIR))

        if not LEGACY_DATATIMO_DIR.exists():
            messages.append(_junction(LEGACY_DATATIMO_DIR, AIMOOE_OUTPUT_DIR))
        else:
            messages.append("skip datatimo/ (already exists)")
    except subprocess.CalledProcessError:
        print("mklink failed — run this script in an elevated terminal (Administrator).")
        return 1

    for line in messages:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
