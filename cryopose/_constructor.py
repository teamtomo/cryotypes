from __future__ import annotations

from typing import TYPE_CHECKING, Mapping, Sequence

import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation

from ._data_labels import CryoPoseDataLabels as CPDL
from ._validators import validate_cryopose, validate_orientations, validate_positions

if TYPE_CHECKING:
    import Literal


def _construct_empty_cryopose_df(ndim: Literal[2, 3] = 3) -> pd.DataFrame:
    return pd.DataFrame(
        columns=[
            *CPDL.POSITION[:ndim],
            CPDL.ORIENTATION,
            CPDL.PIXEL_SPACING,
            CPDL.EXPERIMENT_ID,
        ]
    )


def construct_cryopose_df(
    positions: np.ndarray,
    orientations: Rotation | None = None,
    experiment_ids: str | Sequence[str] | None = None,
    pixel_spacing_angstroms: float | Sequence[float] | None = None,
    metadata: Mapping[str, Sequence] | None = None,
    ndim: Literal[2, 3] = 3,
) -> pd.DataFrame:
    """Constructor for a valid cryopose DataFrame."""
    df = _construct_empty_cryopose_df(ndim)
    df[CPDL.POSITION[:ndim]] = validate_positions(positions, ndim)

    if orientations is None:
        orientations = Rotation.identity(len(positions))
    df[CPDL.ORIENTATION] = validate_orientations(orientations, ndim)

    if pixel_spacing_angstroms is None:
        pixel_spacing_angstroms = 1.0
    df[CPDL.PIXEL_SPACING] = pixel_spacing_angstroms

    if experiment_ids is None:
        experiment_ids = "0"
    df[CPDL.EXPERIMENT_ID] = experiment_ids

    # optional columns
    if metadata is not None:
        for k, v in metadata.items():
            df[k] = v

    return validate_cryopose(df, ndim=ndim)
