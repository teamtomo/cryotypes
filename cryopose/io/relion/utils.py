from typing import Optional, Sequence

import numpy as np
import pandas as pd

from .constants import RELION_EULER_HEADINGS


def positions_from_star_df(
    star_df: pd.DataFrame,
    position_headings: Sequence[str],
    shift_headings: Sequence[str],
    rescale_shifts: Optional[bool] = None,
    pixel_size_heading: Optional[str] = None,
):
    shifts_in_data = all(heading in star_df.columns for heading in shift_headings)
    xyz = star_df[position_headings].to_numpy()
    if shifts_in_data:
        shifts = star_df[shift_headings].to_numpy()
        if rescale_shifts is True and pixel_size_heading in star_df.columns:
            shifts /= star_df[pixel_size_heading].to_numpy()
        xyz -= shifts
    return xyz


def euler_angles_from_star_df(star_df: pd.DataFrame) -> np.ndarray:
    eulers_in_data = all(
        heading in star_df.columns for heading in RELION_EULER_HEADINGS
    )
    if eulers_in_data:
        eulers = star_df[RELION_EULER_HEADINGS].to_numpy()
    else:
        eulers = np.zeros(shape=(len(star_df), 3))
    return eulers


def particle_sources_from_star_df(
    star_df: pd.DataFrame, particle_source_heading: str
) -> np.ndarray:
    if particle_source_heading in star_df.columns:
        particle_source = star_df[particle_source_heading].to_numpy()
    else:
        particle_source = np.full(shape=(len(star_df)), fill_value=np.NAN)
    return particle_source
