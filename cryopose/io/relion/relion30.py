import pandas as pd

from ..utils import combine_cryoposes_and_raw_data, cryoposes_from_data
from .constants import (
    RELION_30_PARTICLE_SOURCE_HEADING,
    RELION_30_SHIFT_HEADINGS,
    RELION_POSITION_HEADINGS,
)
from .utils import (
    euler_angles_from_star_df,
    particle_sources_from_star_df,
    positions_from_star_df,
)


def star2cryopose(star_data: dict) -> pd.DataFrame:
    """Parse a RELION 3.0 style dataframe into a cryopose dataframe."""
    star_df = list(star_data.values())[0]
    xyz = positions_from_star_df(
        star_df=star_df,
        position_headings=RELION_POSITION_HEADINGS,
        shift_headings=RELION_30_SHIFT_HEADINGS,
    )
    euler_angles = euler_angles_from_star_df(star_df)
    particle_sources = particle_sources_from_star_df(
        star_df=star_df,
        particle_source_heading=RELION_30_PARTICLE_SOURCE_HEADING,
    )

    # assemble cryopose dataframe
    cryoposes = cryoposes_from_data(
        xyz=xyz, euler_angles=euler_angles, particle_sources=particle_sources
    )
    return combine_cryoposes_and_raw_data(cryoposes=cryoposes, raw_df=star_df)
