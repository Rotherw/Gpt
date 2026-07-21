from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import EnvironmentProject, Room


class GenerationError(Exception):
    """Raised when an environment project cannot be generated."""


def generate_project(project: EnvironmentProject, output_path: str | Path) -> Path:
    if not project.rooms:
        raise GenerationError("At least one room is required")

    payload: dict[str, Any] = {
        "name": project.name,
        "rooms": [],
        "spawn_points": [
            {
                "id": spawn.id,
                "room_id": spawn.room_id,
                "x": spawn.x,
                "y": spawn.y,
                "z": spawn.z,
            }
            for spawn in project.spawn_points
        ],
        "decorations": [
            {
                "id": decoration.id,
                "room_id": decoration.room_id,
                "name": decoration.name,
                "x": decoration.x,
                "y": decoration.y,
                "z": decoration.z,
            }
            for decoration in project.decorations
        ],
        "lights": [
            {
                "id": light.id,
                "room_id": light.room_id,
                "name": light.name,
                "x": light.x,
                "y": light.y,
                "z": light.z,
                "intensity": light.intensity,
            }
            for light in project.lights
        ],
    }

    for room in project.rooms:
        payload["rooms"].append(
            {
                "id": room.id,
                "name": room.name,
                "width": room.width,
                "height": room.height,
                "depth": room.depth,
                "walls": [
                    {
                        "start": list(wall.start),
                        "end": list(wall.end),
                        "height": wall.height,
                    }
                    for wall in room.walls
                ],
                "decorations": list(room.decorations),
                "lights": list(room.lights),
            }
        )

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return output
