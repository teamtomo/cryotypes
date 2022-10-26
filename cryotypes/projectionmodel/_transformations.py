import numpy as np
import einops


def Rx(theta: np.ndarray) -> np.ndarray:
    """Generate 4x4 matrices which rotate vectors around the X-axis by the angle `theta`.

    The rotation angle `theta` is expected to be in degrees.
    Application of these matrices is performed by left-multiplying xyzw column vectors.

    Parameters
    ----------
    theta: np.ndarray
        An `(n, )` array of rotation angles in degrees.

    Returns
    -------
    matrices: np.ndarray
        An `(n, 4, 4)` array of matrices which left-multiply xyzw column vectors.
    """
    theta = np.asarray(theta).reshape(-1)
    c = np.cos(np.deg2rad(theta))
    s = np.sin(np.deg2rad(theta))
    matrices = einops.repeat(
        np.eye(4), 'i j -> n i j', n=len(theta)
    )
    matrices[:, 1, 1] = c
    matrices[:, 1, 2] = -s
    matrices[:, 2, 1] = s
    matrices[:, 2, 2] = c
    return matrices


def Ry(theta: np.ndarray) -> np.ndarray:
    """Generate 4x4 matrices which rotate vectors around the Y-axis by the angle `theta`.

    The rotation angle `theta` is expected to be in degrees.
    Application of these matrices is performed by left-multiplying xyzw column vectors.

    Parameters
    ----------
    theta: np.ndarray
        An `(n, )` array of rotation angles in degrees.

    Returns
    -------
    matrices: np.ndarray
        An `(n, 4, 4)` array of matrices which left-multiply xyzw column vectors."""
    theta = np.asarray(theta).reshape(-1)
    c = np.cos(np.deg2rad(theta))
    s = np.sin(np.deg2rad(theta))
    matrices = einops.repeat(np.eye(4), 'i j -> n i j', n=len(theta))
    matrices[:, 0, 0] = c
    matrices[:, 0, 2] = s
    matrices[:, 2, 0] = -s
    matrices[:, 2, 2] = c
    return matrices


def Rz(theta: float) -> np.ndarray:
    """Generate 4x4 matrices which rotate vectors around the Z-axis by the angle `theta`.

    The rotation angle `theta` is expected to be in degrees.
    Application of these matrices is performed by left-multiplying xyzw column vectors.

    Parameters
    ----------
    theta: np.ndarray
        An `(n, )` array of rotation angles in degrees.

    Returns
    -------
    matrices: np.ndarray
        An `(n, 4, 4)` array of matrices which left-multiply xyzw column vectors."""
    theta = np.asarray(theta).reshape(-1)
    c = np.cos(np.deg2rad(theta))
    s = np.sin(np.deg2rad(theta))
    matrices = einops.repeat(
        np.eye(4), 'i j -> n i j', n=len(theta)
    )
    matrices[:, 0, 0] = c
    matrices[:, 0, 1] = -s
    matrices[:, 1, 0] = s
    matrices[:, 1, 1] = c
    return np.squeeze(matrices)


def S(shifts: np.ndarray) -> np.ndarray:
    """Generate 4x4 matrices for 2D (xy) or 3D (xyz) shifts.

    Application of these matrices is performed by left-multiplying xyzw column vectors.

    Parameters
    ----------
    shifts: np.ndarray
        An `(n, 2)` or `(n, 3)` array of xy(z) shifts.

    Returns
    -------
    matrices: np.ndarray
        An `(n, 4, 4)` array of
    """
    shifts = np.asarray(shifts, dtype=float)
    if shifts.shape[-1] == 2:
        shifts = _promote_2d_to_3d(shifts)
    shifts = np.array(shifts).reshape((-1, 3))
    matrices = einops.repeat(np.eye(4), 'i j -> n i j', n=shifts.shape[0])
    matrices[:, 0:3, 3] = shifts
    return np.squeeze(matrices)


def _promote_2d_to_3d(shifts: np.ndarray) -> np.ndarray:
    """Promote 2D vectors to 3D with zeros in the last dimension."""
    shifts = np.asarray(shifts).reshape(-1, 2)
    shifts = np.c_[shifts, np.zeros(len(shifts))]
    return np.squeeze(shifts)
