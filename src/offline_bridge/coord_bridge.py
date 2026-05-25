"""Load calibration files and transform points along CT -> optical -> robot."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from src.offline_bridge.io import load_json
from src.offline_bridge.transforms import Transform, apply_transform, compose_transform, validate_transform
from src.project_paths import (
    CALIBRATION_DIR,
    HAND_EYE_MATRIX_NAME,
    SAMPLE_DIR,
    SPACE_REG_NAME,
    ensure_dir,
    hand_eye_matrix_path,
    space_reg_path,
)


def calibration_root() -> Path:
    return Path(os.environ.get("AIMOOE_CALIB_DIR", str(CALIBRATION_DIR)))


def _npz_to_transform(
    path: Path,
    r_key: str,
    t_key: str,
    from_frame: str,
    to_frame: str,
) -> Transform:
    import numpy as np

    data = np.load(path, allow_pickle=True)
    if r_key not in data.files or t_key not in data.files:
        raise KeyError(f"{path.name} must contain {r_key} and {t_key}; found {list(data.files)}")
    return validate_transform(
        {
            "from": from_frame,
            "to": to_frame,
            "R": np.asarray(data[r_key], dtype=float).tolist(),
            "t": np.asarray(data[t_key], dtype=float).reshape(3).tolist(),
        }
    )


def load_hand_eye_transform(calib_dir: Path | None = None) -> Transform:
    path = None
    if calib_dir is not None:
        path = calib_dir / HAND_EYE_MATRIX_NAME
        if not path.is_file():
            path = None
    if path is None:
        path = hand_eye_matrix_path()
    if path is None:
        raise FileNotFoundError(
            f"Hand-eye file not found: {HAND_EYE_MATRIX_NAME}\n"
            "Place it in data/calibration/ or data/experiments/hand_eye/ "
            "(see data/calibration/README.md)."
        )
    return _npz_to_transform(path, "R_opt2rob", "t_opt2rob", "optical_mm", "robot_base_mm")


def load_ct_to_optical_transform(calib_dir: Path | None = None) -> Transform:
    path = None
    if calib_dir is not None:
        path = calib_dir / SPACE_REG_NAME
        if not path.is_file():
            path = None
    if path is None:
        path = space_reg_path()
    if path is None:
        raise FileNotFoundError(
            f"Space registration file not found: {SPACE_REG_NAME}\n"
            "Run demo1.py case 62 or collect_space_reg.py, then save under data/calibration/."
        )
    return _npz_to_transform(path, "R_ct2opt", "t_ct2opt", "ct_scene_mm", "optical_mm")


def load_calibration_chain(calib_dir: Path | None = None) -> dict[str, Transform]:
    root = calib_dir or calibration_root()
    json_path = root / "calibration_chain.json"
    if json_path.is_file():
        payload = load_json(json_path)
        return {
            "ct_to_optical": validate_transform(payload["ct_to_optical"]),
            "optical_to_robot": validate_transform(payload["optical_to_robot"]),
        }
    ensure_dir(root)
    return {
        "ct_to_optical": load_ct_to_optical_transform(root),
        "optical_to_robot": load_hand_eye_transform(root),
    }


def load_sample_calibration_chain() -> dict[str, Transform]:
    payload = load_json(SAMPLE_DIR / "calibration_chain.json")
    return {
        "ct_to_optical": validate_transform(payload["ct_to_optical"]),
        "optical_to_robot": validate_transform(payload["optical_to_robot"]),
    }


def compose_ct_to_robot(chain: dict[str, Transform]) -> Transform:
    return compose_transform(chain["optical_to_robot"], chain["ct_to_optical"])


def transform_ct_point_to_robot(chain: dict[str, Transform], point_mm: list[float]) -> list[float]:
    return apply_transform(compose_ct_to_robot(chain), point_mm)


def transform_plan_ct_to_robot(plan: dict[str, list[float]], chain: dict[str, Transform]) -> dict[str, Any]:
    ct_to_robot = compose_ct_to_robot(chain)
    return {
        "frame": ct_to_robot["to"],
        "entry": apply_transform(ct_to_robot, plan["entry"]),
        "target": apply_transform(ct_to_robot, plan["target"]),
        "source_frame": ct_to_robot["from"],
    }
