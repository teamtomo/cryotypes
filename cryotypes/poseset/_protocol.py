from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from numpy.typing import ArrayLike
from scipy.spatial.transform import Rotation
from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class PoseSetProtocol(Protocol):
    position: ArrayLike
    shift: ArrayLike | None
    orientation: Rotation | None
    experiment_id: str
    pixel_spacing: float
    source: Path | str


@dataclass
class PoseSet:
    position: ArrayLike
    shift: ArrayLike | None
    orientation: Rotation | None
    experiment_id: str
    pixel_spacing: float
    source: Path | str
