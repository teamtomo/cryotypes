import numpy as np
import pandas as pd
import pytest

from cryopose._validators import validate_positions, validate_cryopose_dataframe


def test_position_validator():
    pos3d = np.random.rand(10, 3)
    valid = validate_positions(pos3d, 3)
    assert valid.shape == (10, 3)

    with pytest.raises(ValueError):
        validate_positions(pos3d, 2)

    pos2d = np.random.rand(10, 2)
    valid = validate_positions(pos2d, 2)
    assert valid.shape == (10, 2)

    with pytest.raises(ValueError):
        validate_positions(pos2d, 3)

    wrong = np.random.rand(10, 4)
    with pytest.raises(ValueError):
        validate_positions(wrong, 2)
    with pytest.raises(ValueError):
        validate_positions(wrong, 3)


def test_validate_cryopose_dataframe():
    df = pd.DataFrame()

    with pytest.raises(KeyError):
        validate_cryopose_dataframe(df)

    print(validate_cryopose_dataframe(df, coerce=True))
