from dataclasses import dataclass

import numpy as np
import pytest

from cryotypes.tomogram._validators import validate_tomogram


def test_validate_tomogram():
    @dataclass
    class WrongAttr:
        x = 1

    @dataclass
    class WrongData:
        data = 1
        experiment_id = "s"
        pixel_spacing = 1
        source = "file.mrc"

    @dataclass
    class WrongPixel:
        data = np.empty((3, 3, 3))
        experiment_id = "s"
        pixel_spacing = "a"
        source = "file.mrc"

    @dataclass
    class WrongExpID:
        data = np.empty((3, 3, 3))
        experiment_id = ()
        pixel_spacing = 1
        source = "file.mrc"

    @dataclass
    class WrongSource:
        data = np.empty((3, 3, 3))
        experiment_id = "s"
        pixel_spacing = 1
        source = 1

    @dataclass
    class Right:
        data = np.empty((3, 3, 3))
        experiment_id = "s"
        pixel_spacing = 1
        source = "file.mrc"

    @dataclass
    class CanCoerce:
        data = np.empty((3, 3, 3))
        experiment_id = 0
        pixel_spacing = 1
        source = "file.mrc"

    with pytest.raises(ValueError):
        validate_tomogram(WrongAttr())

    with pytest.raises(ValueError):
        validate_tomogram(WrongData())

    with pytest.raises(ValueError):
        validate_tomogram(WrongPixel())

    with pytest.raises(ValueError):
        validate_tomogram(WrongExpID())

    with pytest.raises(ValueError):
        validate_tomogram(WrongSource())

    validate_tomogram(Right())

    validate_tomogram(CanCoerce(), coerce=True)
