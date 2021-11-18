import pandas as pd

from ..utils import cryoposes_from_data
from .constants import (
    RELION_31_PARTICLE_SOURCE_HEADING,
    RELION_31_PIXEL_SIZE_HEADING,
    RELION_31_SHIFT_HEADINGS,
    RELION_POSITION_HEADINGS,
)
from .utils import (
    euler_angles_from_star_df,
    particle_sources_from_star_df,
    positions_from_star_df,
)


def star2cryopose(star_data: dict) -> pd.DataFrame:
    """Parse a RELION 3.1 style dataframe into a cryopose dataframe."""
    star_df = star_data["particles"].merge(star_data["optics"])

    xyz = positions_from_star_df(
        star_df=star_df,
        position_headings=RELION_POSITION_HEADINGS,
        shift_headings=RELION_31_SHIFT_HEADINGS,
        rescale_shifts=True,
        pixel_size_heading=RELION_31_PIXEL_SIZE_HEADING,
    )
    euler_angles = euler_angles_from_star_df(star_df=star_df)
    particle_sources = particle_sources_from_star_df(
        star_df=star_df, particle_source_heading=RELION_31_PARTICLE_SOURCE_HEADING
    )

    cryoposes = cryoposes_from_data(
        xyz=xyz, euler_angles=euler_angles, particle_sources=particle_sources
    )
    return cryoposes
