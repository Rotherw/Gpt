from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import Decoration, EnvironmentProject, Light, Room, SpawnPoint, Wall


class ConfigError(ValueError):
    """Raised when the input configuration is invalid."""


def load_project(path: str | Path) -> EnvironmentProject:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    project_name = data.get("name")
    if not isinstance(project_name, str) or not project_name.strip():
        raise ConfigError("Project name is required")

    rooms = []
    for raw_room in data.get("rooms", []):
        if not isinstance(raw_room, dict):
            raise ConfigError("Each room must be an object")
        room_id = raw_room.get("id")
        name = raw_room.get("name")
        width = raw_room.get("width")
        height = raw_room.get("height")
        depth = raw_room.get("depth")
        if not isinstance(room_id, str) or not room_id.strip():
            raise ConfigError("Room id is required")
        if not isinstance(name, str) or not name.strip():
            raise ConfigError("Room name is required")
        for field_name, value in (("width", width), ("height", height), ("depth", depth)):
            if not isinstance(value, (int, float)) or value <= 0:
                raise ConfigError(f"Room field '{field_name}' must be a positive number")

        walls = []
        for raw_wall in raw_room.get("walls", []):
            if not isinstance(raw_wall, dict):
                raise ConfigError("Each wall must be an object")
            start = raw_wall.get("start")
            end = raw_wall.get("end")
            height = raw_wall.get("height", 256.0)
            if not _is_coordinate_pair(start) or not _is_coordinate_pair(end):
                raise ConfigError("Wall start and end must be coordinate pairs")
            if not isinstance(height, (int, float)) or height <= 0:
                raise ConfigError("Wall height must be a positive number")
            walls.append(Wall(start=tuple(start), end=tuple(end), height=float(height)))

        room = Room(
            id=room_id,
            name=name,
            width=float(width),
            height=float(height),
            depth=float(depth),
            walls=walls,
            decorations=[str(item) for item in raw_room.get("decorations", [])],
            lights=[str(item) for item in raw_room.get("lights", [])],
        )
        rooms.append(room)

    spawn_points = []
    for raw_spawn in data.get("spawn_points", []):
        if not isinstance(raw_spawn, dict):
            raise ConfigError("Each spawn point must be an object")
        spawn_id = raw_spawn.get("id")
        room_id = raw_spawn.get("room_id")
        x = raw_spawn.get("x")
        y = raw_spawn.get("y")
        z = raw_spawn.get("z")
        if not isinstance(spawn_id, str) or not spawn_id.strip():
            raise ConfigError("Spawn point id is required")
        if not isinstance(room_id, str) or not room_id.strip():
            raise ConfigError("Spawn point room_id is required")
        if not all(isinstance(value, (int, float)) for value in (x, y, z)):
            raise ConfigError("Spawn point coordinates must be numbers")
        spawn_points.append(SpawnPoint(id=spawn_id, room_id=room_id, x=float(x), y=float(y), z=float(z)))

    decorations = []
    for raw_decoration in data.get("decorations", []):
        if not isinstance(raw_decoration, dict):
            raise ConfigError("Each decoration must be an object")
        dec_id = raw_decoration.get("id")
        room_id = raw_decoration.get("room_id")
        name = raw_decoration.get("name")
        x = raw_decoration.get("x")
        y = raw_decoration.get("y")
        z = raw_decoration.get("z")
        if not isinstance(dec_id, str) or not dec_id.strip():
            raise ConfigError("Decoration id is required")
        if not isinstance(room_id, str) or not room_id.strip():
            raise ConfigError("Decoration room_id is required")
        if not isinstance(name, str) or not name.strip():
            raise ConfigError("Decoration name is required")
        if not all(isinstance(value, (int, float)) for value in (x, y, z)):
            raise ConfigError("Decoration coordinates must be numbers")
        decorations.append(Decoration(id=dec_id, room_id=room_id, name=name, x=float(x), y=float(y), z=float(z)))

    lights = []
    for raw_light in data.get("lights", []):
        if not isinstance(raw_light, dict):
            raise ConfigError("Each light must be an object")
        light_id = raw_light.get("id")
        room_id = raw_light.get("room_id")
        name = raw_light.get("name")
        x = raw_light.get("x")
        y = raw_light.get("y")
        z = raw_light.get("z")
        intensity = raw_light.get("intensity", 1.0)
        if not isinstance(light_id, str) or not light_id.strip():
            raise ConfigError("Light id is required")
        if not isinstance(room_id, str) or not room_id.strip():
            raise ConfigError("Light room_id is required")
        if not isinstance(name, str) or not name.strip():
            raise ConfigError("Light name is required")
        if not all(isinstance(value, (int, float)) for value in (x, y, z)):
            raise ConfigError("Light coordinates must be numbers")
        if not isinstance(intensity, (int, float)) or intensity <= 0:
            raise ConfigError("Light intensity must be a positive number")
        lights.append(Light(id=light_id, room_id=room_id, name=name, x=float(x), y=float(y), z=float(z), intensity=float(intensity)))

    return EnvironmentProject(name=project_name, rooms=rooms, spawn_points=spawn_points, decorations=decorations, lights=lights)


def _is_coordinate_pair(value: Any) -> bool:
    return isinstance(value, list) and len(value) == 2 and all(isinstance(item, (int, float)) for item in value)
