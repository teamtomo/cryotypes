from typing import List, Optional, Sequence, Union

import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation

from ._data_labels import CryoPoseDataLabels as CPDL


def unstack_rotations(rotations: Union[Rotation, Sequence[Rotation]]) -> List[Rotation]:
    """Unstack multiple rotations if concatenated."""
    return [rot for rot in rotations]


def stack_rotations(rotations: Sequence[Rotation]) -> Rotation:
    """Stack a sequence of Rotations into one Rotation object."""
    return Rotation.concatenate(rotations)


def guess_ndim(positions: np.ndarray) -> int:
    """Guess dimensionality or 2D or 3D coordinate data."""
    try:
        positions.reshape((-1, 2))
        ndim = 2
    except ValueError:
        positions.reshape((-1, 3))
        ndim = 3
    return ndim


def add_particle_orientations(
    df: pd.DataFrame, orientations: Optional[Rotation]
) -> pd.DataFrame:
    """Add particle orientations to a cryopose dataframe."""
    if orientations is None:
        n_particles = df.shape[0]
        orientations = Rotation.identity(num=n_particles)
    df[CPDL.ORIENTATION] = unstack_rotations(orientations)
    return df
