from typing import List, Sequence, Union

from scipy.spatial.transform import Rotation


def unstack_rotations(rotations: Union[Rotation, Sequence[Rotation]]) -> List[Rotation]:
    """Unstack multiple rotations if concatenated."""
    return [rot for rot in rotations]


def stack_rotations(rotations: Sequence[Rotation]) -> Rotation:
    """Stack a sequence of Rotations into one Rotation object."""
    return Rotation.concatenate(rotations)
