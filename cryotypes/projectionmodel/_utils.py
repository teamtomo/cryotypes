from typing import Tuple

import numpy as np

from ._typing import ProjectionModel
from ._data_labels import ProjectionModelDataLabels as PMDL
from ._transformations import Rx, Ry, Rz, S


def projection_model_to_projection_matrices(
        df: ProjectionModel,
        tilt_image_center: Tuple[int, int],
        tomogram_dimensions: Tuple[int, int, int]
) -> np.ndarray:
    """Calculate 4x4 projection matrices from a ProjectionModel dataframe.

    The resulting 4x4 projection matrices left-multiply xyzw column vectors containing any position
    in the tomogram to produce the projected position (xyzw) in the camera plane.


    Parameters
    ----------
    df: ProjectionModel
        A pandas DataFrame adhering to the `ProjectionModel` specification.
    tilt_image_center: Tuple[int, int]
        Rotation center in the 2D tilt-images, ordered xy.
    tomogram_dimensions: Tuple[int, int, int]
        dimensions of the tomogram, ordered xyz.

    Returns
    -------
    projection_matrices: np.ndarray
        An `(n, 4, 4)` array of projection matrices which left-multiply xyzw column vectors.
    """
    specimen_center = np.array(tomogram_dimensions) // 2
    s0 = S(-specimen_center)
    r0 = Rx(df[PMDL.ROTATION_X])
    r1 = Ry(df[PMDL.ROTATION_Y])
    r2 = Rz(df[PMDL.ROTATION_Z])
    s1 = S(df[PMDL.SHIFT])
    s2 = S(tilt_image_center)
    return s2 @ s1 @ r2 @ r1 @ r0 @ s0
