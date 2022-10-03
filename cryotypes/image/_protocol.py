from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from numpy.typing import ArrayLike
from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class ImageProtocol(Protocol):
    data: ArrayLike
    experiment_id: str
    pixel_spacing: float
    source: Path | str
    stack: bool


@dataclass
class Image:
    data: ArrayLike
    experiment_id: str
    pixel_spacing: float
    source: Path | str
    stack: bool
