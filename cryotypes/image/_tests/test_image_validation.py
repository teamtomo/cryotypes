from dataclasses import dataclass

import numpy as np
import pytest

from cryotypes.image._validators import validate_image


def test_validate_image():
    @dataclass
    class WrongAttr:
        x = 1

    @dataclass
    class WrongData:
        data = 1
        experiment_id = "s"
        pixel_spacing = 1
        source = "file.mrc"
        stack = False

    @dataclass
    class WrongPixel:
        data = np.empty((3, 3, 3))
        experiment_id = "s"
        pixel_spacing = "a"
        source = "file.mrc"
        stack = False

    @dataclass
    class WrongExpID:
        data = np.empty((3, 3, 3))
        experiment_id = ()
        pixel_spacing = 1
        source = "file.mrc"
        stack = False

    @dataclass
    class WrongSource:
        data = np.empty((3, 3, 3))
        experiment_id = "s"
        pixel_spacing = 1
        source = 1
        stack = False

    @dataclass
    class WrongStack:
        data = np.empty((3, 3, 3))
        experiment_id = "s"
        pixel_spacing = 1
        source = 1
        stack = "s"

    @dataclass
    class Right:
        data = np.empty((3, 3, 3))
        experiment_id = "s"
        pixel_spacing = 1
        source = "file.mrc"
        stack = False

    @dataclass
    class CanCoerce:
        data = np.empty((3, 3, 3))
        experiment_id = 0
        pixel_spacing = 1
        source = "file.mrc"
        stack = False

    with pytest.raises(ValueError):
        validate_image(WrongAttr())

    with pytest.raises(ValueError):
        validate_image(WrongData())

    with pytest.raises(ValueError):
        validate_image(WrongPixel())

    with pytest.raises(ValueError):
        validate_image(WrongExpID())

    with pytest.raises(ValueError):
        validate_image(WrongSource())

    with pytest.raises(ValueError):
        validate_image(WrongStack())

    validate_image(Right())

    validate_image(CanCoerce(), coerce=True)
