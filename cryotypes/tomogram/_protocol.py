from __future__ import annotations

from dataclasses import dataclass

from numpy.typing import ArrayLike
from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class TomogramProtocol(Protocol):
    data: ArrayLike
    experiment_id: str
    pixel_spacing: float


@dataclass
class Tomogram:
    data: ArrayLike
    experiment_id: str
    pixel_spacing: float
