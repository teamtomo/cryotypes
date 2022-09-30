from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from ._protocol import TomogramProtocol


def validate_tomogram(
    tomogram: Any,
    coerce: bool = False,
) -> Any:
    """Validate a tomogram."""
    if not isinstance(tomogram, TomogramProtocol):
        raise ValueError(
            f"{tomogram.__class__} object does not follow the TomogramProtocol"
        )

    if not hasattr(tomogram.data, "__array__"):
        if not coerce:
            raise ValueError(f"{tomogram.__class__}.data is not an ArrayLike")
        else:
            tomogram.data = np.asanyarray(tomogram.data)

    if tomogram.data.ndim != 3:
        raise ValueError(f"data must be 3D, got {tomogram.data.ndim}D")

    if not isinstance(tomogram.experiment_id, str):
        if not coerce:
            raise ValueError(
                "experiment_id must be a string, "
                f"got {tomogram.experiment_id.__class__}"
            )
        else:
            tomogram.experiment_id = str(tomogram.experiment_id)

    if not isinstance(tomogram.pixel_spacing, (int, float)):
        if not coerce:
            raise ValueError(
                "experiment_id must be a Number, "
                f"got {tomogram.pixel_spacing.__class__}"
            )
        else:
            tomogram.pixel_spacing = float(tomogram.pixel_spacing)

    if not isinstance(tomogram.source, (str, Path)):
        if not coerce:
            raise ValueError(
                "source must be a Path or str, " f"got {tomogram.source.__class__}"
            )
        else:
            tomogram.source = Path(tomogram.source)

    return tomogram
