import pandas as pd

from ._data_labels import CryoPoseDataLabels


def is_valid_3d_cryopose(df: pd.DataFrame) -> bool:
    """Validate a cryopose dataframe for particle poses in 3D."""
    required_columns = [
        CryoPoseDataLabels.POSITION_X,
        CryoPoseDataLabels.POSITION_Y,
        CryoPoseDataLabels.POSITION_Z,
        CryoPoseDataLabels.ORIENTATION,
    ]
    return all(k in df for k in required_columns)


def is_valid_2d_cryopose(df: pd.DataFrame) -> bool:
    """Validate a cryopose dataframe for particle poses in 3D."""
    required_columns = [
        CryoPoseDataLabels.POSITION_X,
        CryoPoseDataLabels.POSITION_Y,
        CryoPoseDataLabels.ORIENTATION,
    ]
    return all(k in df for k in required_columns)
