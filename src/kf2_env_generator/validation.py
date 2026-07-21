from __future__ import annotations

from .models import Decoration, EnvironmentProject, Light, Room, SpawnPoint


class ValidationError(ValueError):
    """Raised when the project violates validation rules."""


def validate_project(project: EnvironmentProject) -> None:
    if not project.name.strip():
        raise ValidationError("Project name cannot be empty")

    room_ids = {room.id for room in project.rooms}
    for room in project.rooms:
        if room.width <= 0 or room.height <= 0 or room.depth <= 0:
            raise ValidationError(f"Room '{room.id}' has invalid dimensions")

    for spawn in project.spawn_points:
        if spawn.room_id not in room_ids:
            raise ValidationError(f"Spawn point '{spawn.id}' references missing room '{spawn.room_id}'")

    for decoration in project.decorations:
        if decoration.room_id not in room_ids:
            raise ValidationError(f"Decoration '{decoration.id}' references missing room '{decoration.room_id}'")

    for light in project.lights:
        if light.room_id not in room_ids:
            raise ValidationError(f"Light '{light.id}' references missing room '{light.room_id}'")
