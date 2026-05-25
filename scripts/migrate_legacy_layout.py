"""One-time migration from pre-restructure root folders to data/ layout."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.project_paths import migrate_legacy_layout


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Print planned moves only.")
    args = parser.parse_args()

    actions = migrate_legacy_layout(dry_run=args.dry_run)
    if not actions:
        print("No legacy folders with data found at repo root.")
        return 0

    prefix = "Would" if args.dry_run else "Did"
    for line in actions:
        print(f"{prefix}: {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
