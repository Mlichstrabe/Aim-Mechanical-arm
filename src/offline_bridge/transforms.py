"""Small 3D transform utilities for the offline CT -> optical -> robot chain."""

from __future__ import annotations

from typing import Any


Vector3 = list[float]
Matrix3 = list[list[float]]
Transform = dict[str, Any]


def _as_vector3(point: list[float]) -> Vector3:
    if len(point) != 3:
        raise ValueError(f"Expected a 3D point, got {len(point)} values")
    return [float(value) for value in point]


def _as_matrix3(matrix: list[list[float]]) -> Matrix3:
    if len(matrix) != 3 or any(len(row) != 3 for row in matrix):
        raise ValueError("Expected a 3x3 rotation matrix")
    return [[float(value) for value in row] for row in matrix]


def validate_transform(transform: Transform) -> Transform:
    if "from" not in transform or "to" not in transform:
        raise ValueError("Transform must include 'from' and 'to' frame names")
    return {
        "from": str(transform["from"]),
        "to": str(transform["to"]),
        "R": _as_matrix3(transform["R"]),
        "t": _as_vector3(transform["t"]),
    }


def apply_transform(transform: Transform, point: list[float]) -> Vector3:
    checked = validate_transform(transform)
    p = _as_vector3(point)
    return [
        sum(checked["R"][row][col] * p[col] for col in range(3)) + checked["t"][row]
        for row in range(3)
    ]


def compose_transform(first: Transform, second: Transform) -> Transform:
    """Return the transform produced by applying second, then first."""

    a = validate_transform(first)
    b = validate_transform(second)
    if b["to"] != a["from"]:
        raise ValueError(f"Cannot compose {b['from']}->{b['to']} with {a['from']}->{a['to']}")

    rotation = [
        [sum(a["R"][row][k] * b["R"][k][col] for k in range(3)) for col in range(3)]
        for row in range(3)
    ]
    translation = [
        sum(a["R"][row][k] * b["t"][k] for k in range(3)) + a["t"][row]
        for row in range(3)
    ]
    return {"from": b["from"], "to": a["to"], "R": rotation, "t": translation}


def transform_plan_ct_to_robot(
    plan: dict[str, list[float]],
    ct_to_optical: Transform,
    optical_to_robot: Transform,
) -> dict[str, Any]:
    ct_to_robot = compose_transform(optical_to_robot, ct_to_optical)
    return {
        "frame": ct_to_robot["to"],
        "entry": apply_transform(ct_to_robot, plan["entry"]),
        "target": apply_transform(ct_to_robot, plan["target"]),
        "source_frame": ct_to_robot["from"],
    }

