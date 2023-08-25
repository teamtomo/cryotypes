from __future__ import annotations

from copy import copy
from pathlib import Path
from typing import TYPE_CHECKING, Any

import numpy as np

from ._protocol import PoseSetProtocol

if TYPE_CHECKING:
    from typing import Literal


def validate_poseset(
    poseset: Any,
    ndim: Literal[2, 3] = 3,
    coerce: bool = False,
    inplace: bool = False,
) -> Any:
    """Validate an poseset."""
    if not inplace:
        # shallow copy so we don't change the input
        poseset = copy(poseset)

    if not isinstance(poseset, PoseSetProtocol):
        raise ValueError(
            f"{poseset.__class__} object does not follow the PosesetProtocol"
        )

    if not hasattr(poseset.position, "__array__"):
        if not coerce:
            raise ValueError(f"{poseset.__class__}.position is not an ArrayLike")
        else:
            poseset.position = np.asanyarray(poseset.position)

    if poseset.position.ndim != 2 or poseset.position.shape[1] > ndim:
        raise ValueError(
            f"position must be (N, D) with D <= {ndim}, got {poseset.position.shape}"
        )
    elif poseset.position.shape[1] < ndim:
        if not coerce:
            raise ValueError(
                f"position must be (N, {ndim}), got {poseset.position.shape}"
            )
        else:
            padding = ndim - poseset.position.shape[1]
            poseset.position = np.pad(poseset.position, ((0, 0), (0, padding)))

    if poseset.shift is not None:
        if not hasattr(poseset.shift, "__array__"):
            if not coerce:
                raise ValueError(f"{poseset.__class__}.shift is not an ArrayLike")
            else:
                poseset.shift = np.asanyarray(poseset.shift)

        if poseset.shift.ndim != 2 or poseset.shift.shape[1] > ndim:
            raise ValueError(
                f"shift must be (N, D) with D <= {ndim}, got {poseset.shift.shape}"
            )
        elif poseset.shift.shape != poseset.position.shape:
            if not coerce:
                raise ValueError(
                    f"shift must have the same shape as position "
                    f" {poseset.position.shape}, got {poseset.shift.shape}"
                )
            elif poseset.shift.shape[1] < ndim:
                padding = ndim - poseset.shift.shape[1]
                poseset.shift = np.pad(poseset.shift, ((0, 0), (0, padding)))

    ori = poseset.orientation
    if ori is not None:
        if len(ori) != len(poseset.position):
            raise ValueError(
                f"orientation must have the same length as position "
                f"{len(poseset.position)}, got {len(ori)}"
            )

    if not isinstance(poseset.experiment_id, str):
        if not coerce:
            raise ValueError(
                "experiment_id must be a string, "
                f"got {poseset.experiment_id.__class__}"
            )
        else:
            poseset.experiment_id = str(poseset.experiment_id)

    if not isinstance(poseset.pixel_spacing, (int, float)):
        if not coerce:
            raise ValueError(
                "experiment_id must be a Number, "
                f"got {poseset.pixel_spacing.__class__}"
            )
        else:
            poseset.pixel_spacing = float(poseset.pixel_spacing)

    if not isinstance(poseset.source, (str, Path)):
        if not coerce:
            raise ValueError(
                "source must be a Path or str, " f"got {poseset.source.__class__}"
            )
        else:
            poseset.source = Path(poseset.source)

    return poseset
