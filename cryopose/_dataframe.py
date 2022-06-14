from typing import Mapping, Optional, Sequence, TypeVar, Union

import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation

from ._data_labels import CryoPoseDataLabels as CPDL

_T = TypeVar("_T")


def _construct_base_cryopose_df(
    xyz: np.ndarray, orientations: Optional[Rotation]
) -> pd.DataFrame:
    """Construct a base cryopose DataFrame with particle pose information."""
    xyz = np.asarray(xyz).reshape((-1, 3))
    if orientations is None:
        orientations = Rotation.identity(len(xyz))
    df = pd.DataFrame(
        {
            CPDL.POSITION_X: xyz[:, 0],
            CPDL.POSITION_Y: xyz[:, 1],
            CPDL.POSITION_Z: xyz[:, 2],
            CPDL.ORIENTATION: orientations,
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
    df[CPDL.EXPERIMENT_ID] = tilt_series_ids
    df[CPDL.PIXEL_SPACING] = voxel_spacing_angstroms
    for k, v in metadata.items():
        df[k] = v
    return df
