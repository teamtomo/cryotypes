from typing import Mapping, Optional, Sequence, TypeVar, Union

import einops
import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation

from ._data_labels import (
    CRYOPOSE_POSITION_X,
    CRYOPOSE_POSITION_Y,
    CRYOPOSE_POSITION_Z,
    CRYOPOSE_ROTATION,
    CRYOPOSE_TILT_SERIES_ID,
    CRYOPOSE_VOXEL_SPACING,
)
from ._utils import unstack_rotations

_T = TypeVar("_T")


def _construct_base_cryopose_df(
    xyz: np.ndarray, rotations: Optional[Rotation]
) -> pd.DataFrame:
    """Construct a base cryopose DataFrame with particle pose information."""
    xyz = np.asarray(xyz).reshape((-1, 3))
    if rotations is None:
        rotations = Rotation.from_matrix(
            einops.repeat(np.eye(3), pattern="i j -> n i j", n=xyz.shape[0])
        )
    rotations = unstack_rotations(rotations)
    df = pd.DataFrame(
        {
            CRYOPOSE_POSITION_X: xyz[:, 0],
            CRYOPOSE_POSITION_Y: xyz[:, 1],
            CRYOPOSE_POSITION_Z: xyz[:, 2],
            CRYOPOSE_ROTATION: rotations,
        }
    )
    return df


def construct_cryopose_df(
    xyz: np.ndarray,
    rotations: Optional[Rotation],
    tilt_series_ids: Optional[Sequence[str]],
    voxel_spacing_angstroms: Optional[Union[float, Sequence[float]]],
    metadata: Mapping[str, _T],
) -> pd.DataFrame:
    """Convenient constructor for a valid cryopose DataFrame."""
    df = _construct_base_cryopose_df(xyz, rotations)
    df[CRYOPOSE_TILT_SERIES_ID] = tilt_series_ids
    df[CRYOPOSE_VOXEL_SPACING] = voxel_spacing_angstroms
    for k, v in metadata.items():
        df[k] = v
    return df
