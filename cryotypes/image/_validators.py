from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import numpy as np

from ._protocol import ImageProtocol

if TYPE_CHECKING:
    from typing import Literal


def validate_image(
    image: Any,
    ndim: Literal[2, 3] = 3,
    stack: bool = False,
    coerce: bool = False,
) -> Any:
    """Validate an image."""
    if not isinstance(image, ImageProtocol):
        raise ValueError(f"{image.__class__} object does not follow the ImageProtocol")

    if not hasattr(image.data, "__array__"):
        if not coerce:
            raise ValueError(f"{image.__class__}.data is not an ArrayLike")
        else:
            image.data = np.asanyarray(image.data)

    total_ndim = ndim + stack
    if image.data.ndim != total_ndim:
        if not coerce:
            raise ValueError(f"data must be {total_ndim}D, got {image.data.ndim}D")
        elif image.data.ndim > total_ndim:
            raise ValueError(
                f"cannot coerce {image.data.ndim}D data to {total_ndim}D. "
                "Did you set stack correctly?"
            )
        else:
            image.data = np.expand_dims(
                image.data, axis=tuple(range(total_ndim - image.data.ndim))
            )

    if not isinstance(image.experiment_id, str):
        if not coerce:
            raise ValueError(
                "experiment_id must be a string, "
                f"got {image.experiment_id.__class__}"
            )
        else:
            image.experiment_id = str(image.experiment_id)

    if not isinstance(image.pixel_spacing, (int, float)):
        if not coerce:
            raise ValueError(
                "experiment_id must be a Number, "
                f"got {image.pixel_spacing.__class__}"
            )
        else:
            image.pixel_spacing = float(image.pixel_spacing)

    if not isinstance(image.source, (str, Path)):
        if not coerce:
            raise ValueError(
                "source must be a Path or str, " f"got {image.source.__class__}"
            )
        else:
            image.source = Path(image.source)

    return image
