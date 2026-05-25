"""Repository-root path helpers shared by SDK, UR5e, and offline code."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNTIME_DIR = ROOT / "runtime"
AIMTOOLS_CANONICAL = ROOT / "AimTools"
DATA_DIR = ROOT / "data"
SAMPLE_DIR = DATA_DIR / "sample"
CALIBRATION_DIR = Path(os.environ.get("AIMOOE_CALIB_DIR", str(DATA_DIR / "calibration")))
AIMOOE_OUTPUT_DIR = DATA_DIR / "outputs" / "aimooe_tool_data"
CAMERA_OUTPUT_DIR = DATA_DIR / "outputs" / "camera"
EXPERIMENTS_DIR = DATA_DIR / "experiments"
HAND_EYE_DIR = EXPERIMENTS_DIR / "hand_eye"
FORCE_DIR = EXPERIMENTS_DIR / "force"

# Pre-restructure folder names (repo root)
LEGACY_DATATIMO_DIR = ROOT / "datatimo"
LEGACY_DATAMARK_DIR = ROOT / "datamark"
LEGACY_DATA_TCP_DIR = ROOT / "data_tcp"
LEGACY_AIMTOOLS_DIR = ROOT / "Aimtools"
LEGACY_HAND_EYE_DIRS = (
    ROOT / "hand–eye calibration",
    ROOT / "hand-eye calibration",
)

REQUIRED_AIMTOOLS = ("PTM-4.aimtool", "PTM-99.aimtool")
HAND_EYE_MATRIX_NAME = "HandEye_Calibration_Matrix.npz"
SPACE_REG_NAME = "space_reg.npz"


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def _dir_has_aimtool_files(directory: Path) -> bool:
    if not directory.is_dir():
        return False
    return any((directory / name).is_file() for name in REQUIRED_AIMTOOLS)


def resolve_aimtools_dir() -> Path:
    """Prefer a folder that already contains .aimtool files (AimTools or legacy Aimtools)."""
    for candidate in (AIMTOOLS_CANONICAL, LEGACY_AIMTOOLS_DIR):
        if _dir_has_aimtool_files(candidate):
            return candidate
    return AIMTOOLS_CANONICAL


def aimtools_path() -> str:
    return str(resolve_aimtools_dir()) + os.sep


def list_missing_aimtools(required: tuple[str, ...] = REQUIRED_AIMTOOLS) -> list[str]:
    tools_dir = resolve_aimtools_dir()
    if not tools_dir.is_dir():
        return list(required)
    return [name for name in required if not (tools_dir / name).is_file()]


def hand_eye_datamark_dir() -> Path:
    return ensure_dir(HAND_EYE_DIR / "datamark")


def hand_eye_tcp_dir() -> Path:
    return ensure_dir(HAND_EYE_DIR / "data_tcp")


def legacy_datatimo_dir() -> Path:
    """Post-restructure output path (replaces root datatimo/)."""
    return ensure_dir(AIMOOE_OUTPUT_DIR)


def find_data_file(filename: str, *, search_dirs: tuple[Path, ...] | None = None) -> Path | None:
    dirs = search_dirs or (CALIBRATION_DIR, HAND_EYE_DIR, *LEGACY_HAND_EYE_DIRS)
    for base in dirs:
        if not base.exists():
            continue
        direct = base / filename
        if direct.is_file():
            return direct
        if base.is_dir():
            for match in base.rglob(filename):
                if match.is_file():
                    return match
    return None


def hand_eye_matrix_path() -> Path | None:
    return find_data_file(HAND_EYE_MATRIX_NAME)


def space_reg_path() -> Path | None:
    return find_data_file(SPACE_REG_NAME)


def _migrate_tree(source: Path, target: Path) -> None:
    ensure_dir(target)
    for item in source.iterdir():
        dest = target / item.name
        if item.is_dir():
            if dest.exists():
                _migrate_tree(item, dest)
            else:
                shutil.move(str(item), str(dest))
        elif not dest.exists():
            shutil.move(str(item), str(dest))


def migrate_legacy_layout(*, dry_run: bool = False) -> list[str]:
    """Move pre-restructure root folders into the new data/ layout."""
    actions: list[str] = []

    def act(msg: str, fn) -> None:
        actions.append(msg)
        if not dry_run:
            fn()

    if LEGACY_DATAMARK_DIR.is_dir() and any(LEGACY_DATAMARK_DIR.iterdir()):
        act(
            f"datamark/ -> {HAND_EYE_DIR / 'datamark'}/",
            lambda: _migrate_tree(LEGACY_DATAMARK_DIR, hand_eye_datamark_dir()),
        )

    if LEGACY_DATA_TCP_DIR.is_dir() and any(LEGACY_DATA_TCP_DIR.iterdir()):
        act(
            f"data_tcp/ -> {HAND_EYE_DIR / 'data_tcp'}/",
            lambda: _migrate_tree(LEGACY_DATA_TCP_DIR, hand_eye_tcp_dir()),
        )

    if LEGACY_DATATIMO_DIR.is_dir() and any(LEGACY_DATATIMO_DIR.iterdir()):
        act(
            f"datatimo/ -> {AIMOOE_OUTPUT_DIR}/",
            lambda: _migrate_tree(LEGACY_DATATIMO_DIR, ensure_dir(AIMOOE_OUTPUT_DIR)),
        )

    for legacy_he in LEGACY_HAND_EYE_DIRS:
        if not legacy_he.is_dir():
            continue
        for npz in legacy_he.glob("*.npz"):
            dest = ensure_dir(CALIBRATION_DIR) / npz.name
            if not dest.exists():
                act(
                    f"{npz} -> {dest}",
                    lambda s=npz, d=dest: shutil.copy2(s, d),
                )
        for sub in ("datamark", "data_tcp"):
            src = legacy_he / sub
            if src.is_dir() and any(src.iterdir()):
                tgt = HAND_EYE_DIR / sub
                act(
                    f"{src} -> {tgt}/",
                    lambda s=src, t=tgt: _migrate_tree(s, ensure_dir(t)),
                )

    tools_src = resolve_aimtools_dir()
    if tools_src != AIMTOOLS_CANONICAL and _dir_has_aimtool_files(tools_src):
        ensure_dir(AIMTOOLS_CANONICAL)
        for name in REQUIRED_AIMTOOLS:
            src = tools_src / name
            dest = AIMTOOLS_CANONICAL / name
            if src.is_file() and not dest.exists():
                act(
                    f"{src} -> {dest}",
                    lambda s=src, d=dest: shutil.copy2(s, d),
                )

    return actions
