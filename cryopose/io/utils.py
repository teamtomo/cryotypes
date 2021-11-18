import numpy as np
import pandas as pd

from ..constants import (
    CRYOPOSE_EULER_1,
    CRYOPOSE_EULER_2,
    CRYOPOSE_EULER_3,
    CRYOPOSE_PARTICLE_SOURCE,
    CRYOPOSE_X,
    CRYOPOSE_Y,
    CRYOPOSE_Z,
)
from .io_constants import RAW_DATA_COLUMN_NAME_PREFIX


def cryoposes_from_data(
    xyz: np.ndarray, euler_angles: np.ndarray, particle_sources: np.ndarray
) -> pd.DataFrame:
    cryopose_data = {
        CRYOPOSE_X: xyz[:, 0],
        CRYOPOSE_Y: xyz[:, 1],
        CRYOPOSE_Z: xyz[:, 2],
        CRYOPOSE_EULER_1: euler_angles[:, 0],
        CRYOPOSE_EULER_2: euler_angles[:, 1],
        CRYOPOSE_EULER_3: euler_angles[:, 2],
        CRYOPOSE_PARTICLE_SOURCE: particle_sources,
    }
    return pd.DataFrame.from_dict(cryopose_data)


def combine_cryoposes_and_raw_data(
    cryoposes: pd.DataFrame, raw_df: pd.DataFrame
) -> pd.DataFrame:
    raw_df_renamed = prepend_df_column_names(raw_df, RAW_DATA_COLUMN_NAME_PREFIX)
    return pd.concat(cryoposes, raw_df_renamed, axis=1)


def prepend_df_column_names(df: pd.DataFrame, prefix: str):
    df = df.rename(
        columns={column_name: f"{prefix}{column_name}" for column_name in df.columns},
        inplace=True,
    )
    return df
