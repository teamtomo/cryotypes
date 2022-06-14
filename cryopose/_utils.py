from typing import List, Sequence

from scipy.spatial.transform import Rotation


def unstack_rotations(rotations: Rotation) -> List[Rotation]:
    """Unstack multiple rotations from a Rotation object."""
    return [rot for rot in rotations]


def stack_rotations(rotations: Sequence[Rotation]) -> Rotation:
    """Stack a sequence of Rotations into one Rotation object."""
    return Rotation.concatenate(rotations)
