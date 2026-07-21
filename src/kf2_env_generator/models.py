from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Wall:
    start: tuple[float, float]
    end: tuple[float, float]
    height: float = 256.0


@dataclass
class Room:
    id: str
    name: str
    width: float
    height: float
    depth: float
    walls: List[Wall] = field(default_factory=list)
    decorations: List[str] = field(default_factory=list)
    lights: List[str] = field(default_factory=list)


@dataclass
class SpawnPoint:
    id: str
    room_id: str
    x: float
    y: float
    z: float


@dataclass
class Decoration:
    id: str
    room_id: str
    name: str
    x: float
    y: float
    z: float


@dataclass
class Light:
    id: str
    room_id: str
    name: str
    x: float
    y: float
    z: float
    intensity: float = 1.0


@dataclass
class EnvironmentProject:
    name: str
    rooms: List[Room] = field(default_factory=list)
    spawn_points: List[SpawnPoint] = field(default_factory=list)
    decorations: List[Decoration] = field(default_factory=list)
    lights: List[Light] = field(default_factory=list)
