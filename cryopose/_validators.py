import pandas as pd

from ._data_labels import (
    CRYOPOSE_ORIENTATION,
    CRYOPOSE_POSITION_X,
    CRYOPOSE_POSITION_Y,
    CRYOPOSE_POSITION_Z,
)


def validate_cryopose_df_3d(df: pd.DataFrame) -> bool:
    """Validate a cryopose dataframe for particle poses in 3D."""
    required_columns = [
        CRYOPOSE_POSITION_X,
        CRYOPOSE_POSITION_Y,
        CRYOPOSE_POSITION_Z,
        CRYOPOSE_ORIENTATION,
    ]
    return all(k in df for k in required_columns)


def validate_cryopose_df_2d(df: pd.DataFrame) -> bool:
    """Validate a cryopose dataframe for particle poses in 3D."""
    required_columns = [
        CRYOPOSE_POSITION_X,
        CRYOPOSE_POSITION_Y,
        CRYOPOSE_ORIENTATION,
    ]
    return all(k in df for k in required_columns)
