import pandas as pd

from ._data_labels import Cryopose


def is_valid_3d_cryopose(df: pd.DataFrame) -> bool:
    """Validate a cryopose dataframe for particle poses in 3D."""
    required_columns = [
        Cryopose.POSITION_X,
        Cryopose.POSITION_Y,
        Cryopose.POSITION_Z,
        Cryopose.ROTATION,
    ]
    return all(k in df for k in required_columns)


def is_valid_2d_cryopose(df: pd.DataFrame) -> bool:
    """Validate a cryopose dataframe for particle poses in 3D."""
    required_columns = [
        Cryopose.POSITION_X,
        Cryopose.POSITION_Y,
        Cryopose.ROTATION,
    ]
    return all(k in df for k in required_columns)
