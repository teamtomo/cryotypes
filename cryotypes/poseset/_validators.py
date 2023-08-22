from __future__ import annotations

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
) -> Any:
    """Validate an poseset."""
    if not isinstance(poseset, PoseSetProtocol):
        raise ValueError(
            f"{poseset.__class__} object does not follow the PosesetProtocol"
        )

    if not hasattr(poseset.position, "__array__"):
        if not coerce:
            raise ValueError(f"{poseset.__class__}.position is not an ArrayLike")
        else:
            poseset.position = np.asanyarray(poseset.position)

    if not hasattr(poseset.shift, "__array__"):
        if not coerce:
            raise ValueError(f"{poseset.__class__}.shift is not an ArrayLike")
        else:
            poseset.shift = np.asanyarray(poseset.shift)

    pos = poseset.position
    if pos.ndim != 2 or pos.shape[1] > ndim:
        raise ValueError(f"position must be (N, D) with D <= {ndim}, got {pos.shape}")
    elif pos.shape[1] < ndim:
        if not coerce:
            raise ValueError(f"position must be (N, {ndim}), got {pos.shape}")
        else:
            pos = np.expand_dims(pos, axis=tuple(range(ndim - pos.ndim)))

    shift = poseset.shift
    if shift is not None:
        if shift.ndim != 2 or shift.shape[1] > ndim:
            raise ValueError(
                f"shift must be (N, D) with D <= {ndim}, got {shift.shape}"
            )
        elif shift.shape != pos.shape:
            if not coerce:
                raise ValueError(
                    f"shift must have the same shape as position {pos.shape}, "
                    f"got {shift.shape}"
                )
            elif shift.shape[1] < ndim:
                shift = np.expand_dims(shift, axis=tuple(range(ndim - shift.ndim)))

    ori = poseset.orientation
    if ori is not None:
        if len(ori) != len(pos):
            raise ValueError(
                f"orientation must have the same length as position {len(pos)}, "
                f"got {len(ori)}"
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
