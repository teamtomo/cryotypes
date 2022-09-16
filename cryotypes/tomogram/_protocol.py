from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from numpy.typing import ArrayLike

if TYPE_CHECKING:
    from typing import Protocol, runtime_checkable


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
