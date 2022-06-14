import pandas as pd

from ._data_labels import CryoPoseDataLabels as CPDL


def validate_3d_cryopose_df(df: pd.DataFrame) -> bool:
    """Validate a cryopose dataframe for particle poses in 3D."""
    required_columns_3d = [
        CPDL.POSITION_X,
        CPDL.POSITION_Y,
        CPDL.POSITION_Z,
        CPDL.ORIENTATION,
    ]
    return all(k in df for k in required_columns_3d)


def validate_2d_cryopose_df(df: pd.DataFrame) -> bool:
    """Validate a cryopose dataframe for particle poses in 3D."""
    required_columns_2d = [
        CPDL.POSITION_X,
        CPDL.POSITION_Y,
        CPDL.ORIENTATION,
    ]
    return all(k in df for k in required_columns_2d)
