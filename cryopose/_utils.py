from typing import List, Optional, Sequence, Union

import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation

from ._data_labels import CRYOPOSE_ORIENTATION


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


def generate_default_orientations(n: int) -> List[Rotation]:
    """Generate default unrotated particle orientations."""
    return [Rotation.from_matrix(np.eye(3)) for _ in range(n)]


def add_particle_orientations(
    df: pd.DataFrame, orientations: Optional[Rotation]
) -> pd.DataFrame:
    """Add particle orientations to a cryopose dataframe."""
    if orientations is None:
        n_particles = df.shape[0]
        orientations = generate_default_orientations(n_particles)
    df[CRYOPOSE_ORIENTATION] = unstack_rotations(orientations)
