"""A no-hardware robot interface for offline learning."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MockRobot:
    """Record planned robot commands without opening RTDE or socket connections."""

    commands: list[dict[str, Any]] = field(default_factory=list)

    def move_l(self, target_mm: list[float], speed: float, acceleration: float) -> dict[str, Any]:
        command = {
            "command": "moveL",
            "target_mm": [float(value) for value in target_mm],
            "speed_mm_s": float(speed),
            "acceleration_mm_s2": float(acceleration),
            "hardware_connected": False,
        }
        self.commands.append(command)
        return command

