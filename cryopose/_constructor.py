from typing import Mapping, Optional, Sequence, TypeVar, Union

import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation

from ._data_labels import CryoPoseDataLabels as CPDL
from ._utils import add_particle_orientations, guess_ndim

_T = TypeVar("_T")


def _construct_base_cryopose_df(positions: np.ndarray) -> pd.DataFrame:
    """Construct a base cryopose DataFrame with particle positions only.

    Coordinates for positions can be 2D (n, 2) or 3D (n, 3). The X-coordinates
    should be in the first column, Y in the second, Z in the third (if present).
    """
    ndim = guess_ndim(positions)
    positions = np.asarray(positions).astype(float).reshape((-1, ndim))
    df = pd.DataFrame(
        {
            CPDL.POSITION_X: positions[:, 0],
            CPDL.POSITION_Y: positions[:, 1],
        }
    )
    if ndim == 3:
        df[CPDL.POSITION_Z] = positions[:, 2]
    return df


def construct_cryopose_df(
    positions: np.ndarray,
    orientations: Optional[Rotation],
    experiment_ids: Optional[Union[str, Sequence[str]]],
    pixel_spacing_angstroms: Optional[Union[float, Sequence[float]]],
    metadata: Mapping[str, _T],
) -> pd.DataFrame:
    """Constructor for a valid cryopose DataFrame."""
    df = _construct_base_cryopose_df(positions)
    df = add_particle_orientations(df, orientations)
    df[CPDL.EXPERIMENT_ID] = experiment_ids
    df[CPDL.PIXEL_SPACING] = (
        1 if pixel_spacing_angstroms is None else pixel_spacing_angstroms
    )
    for k, v in metadata.items():
        df[k] = v
    return df
