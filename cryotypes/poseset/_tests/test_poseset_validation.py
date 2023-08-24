from dataclasses import dataclass

import numpy as np
import pytest
from scipy.spatial.transform import Rotation

from cryotypes.poseset._validators import validate_poseset


def test_validate_poseset():
    @dataclass
    class WrongAttr:
        x = 1

    @dataclass
    class WrongPos:
        position = 1
        shift = None
        orientation = None
        experiment_id = "s"
        pixel_spacing = 1
        source = "file.star"

    @dataclass
    class WrongShift:
        position = np.empty((10, 3))
        shift = 1
        orientation = None
        experiment_id = "s"
        pixel_spacing = 1
        source = "file.star"

    @dataclass
    class WrongOri:
        position = np.empty((10, 3))
        shift = np.empty((10, 3))
        orientation = Rotation.identity(2)
        experiment_id = "s"
        pixel_spacing = 1
        source = "file.star"

    @dataclass
    class WrongPixel:
        position = np.empty((10, 3))
        shift = None
        orientation = None
        experiment_id = "s"
        pixel_spacing = "a"
        source = "file.star"

    @dataclass
    class WrongExpID:
        position = np.empty((10, 3))
        shift = None
        orientation = None
        experiment_id = ()
        pixel_spacing = 1
        source = "file.star"

    @dataclass
    class WrongSource:
        position = np.empty((10, 3))
        shift = None
        orientation = None
        experiment_id = "s"
        pixel_spacing = 1
        source = 1

    @dataclass
    class Right:
        position = np.empty((10, 3))
        shift = np.empty((10, 3))
        orientation = Rotation.identity(10)
        experiment_id = "s"
        pixel_spacing = 1
        source = "file.star"

    @dataclass
    class CanCoerce:
        position = np.empty((10, 3))
        shift = np.empty((10, 2))
        orientation = None
        experiment_id = "s"
        pixel_spacing = 1
        source = "file.star"

    with pytest.raises(ValueError):
        validate_poseset(WrongAttr())

    with pytest.raises(ValueError):
        validate_poseset(WrongPos())

    with pytest.raises(ValueError):
        validate_poseset(WrongShift())

    with pytest.raises(ValueError):
        validate_poseset(WrongOri())

    with pytest.raises(ValueError):
        validate_poseset(WrongPixel())

    with pytest.raises(ValueError):
        validate_poseset(WrongExpID())

    with pytest.raises(ValueError):
        validate_poseset(WrongSource())

    validate_poseset(Right())

    can_coerce = CanCoerce()
    coerced = validate_poseset(CanCoerce(), coerce=True)
    assert can_coerce.shift.shape != coerced.shift.shape
