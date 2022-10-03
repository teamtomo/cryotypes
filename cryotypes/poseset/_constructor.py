from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Mapping, Sequence

import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation

from ._data_labels import PoseSetDataLabels as PSDL
from ._validators import (
    validate_orientations,
    validate_poseset_dataframe,
    validate_positions,
)

if TYPE_CHECKING:
    import Literal


def _construct_empty_poseset_df(ndim: Literal[2, 3] = 3) -> pd.DataFrame:
    return pd.DataFrame(
        columns=[
            *PSDL.POSITION[:ndim],
            *PSDL.SHIFT[:ndim],
            PSDL.ORIENTATION,
            PSDL.PIXEL_SPACING,
            PSDL.EXPERIMENT_ID,
            PSDL.SOURCE,
        ]
    )


def construct_poseset_df(
    positions: np.ndarray,
    shifts: np.ndarray | None = None,
    orientations: Rotation | None = None,
    experiment_ids: str | Sequence[str] | None = None,
    pixel_spacing_angstroms: float | Sequence[float] | None = None,
    sources: Sequence[str | Path | None] | None = None,
    metadata: Mapping[str, Sequence] | None = None,
    ndim: Literal[2, 3] = 3,
) -> pd.DataFrame:
    """Constructor for a valid poseset DataFrame."""
    df = _construct_empty_poseset_df(ndim)
    df[PSDL.POSITION[:ndim]] = validate_positions(positions, ndim)

    if shifts is None:
        shifts = np.zeros((len(positions), ndim))
    df[PSDL.SHIFT[:ndim]] = validate_positions(shifts, ndim)

    if orientations is None:
        orientations = Rotation.identity(len(positions))
    df[PSDL.ORIENTATION] = validate_orientations(orientations, ndim)

    if pixel_spacing_angstroms is None:
        pixel_spacing_angstroms = 1.0
    df[PSDL.PIXEL_SPACING] = pixel_spacing_angstroms

    if experiment_ids is None:
        experiment_ids = "0"
    df[PSDL.EXPERIMENT_ID] = experiment_ids

    df[PSDL.SOURCE] = sources

    # optional columns
    if metadata is not None:
        for k, v in metadata.items():
            df[k] = v

    return validate_poseset_dataframe(df, ndim=ndim)
