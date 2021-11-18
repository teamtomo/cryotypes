import relion30
import relion31
import starfile

from ...typing_utils import PathLike


def read(star_file: PathLike):
    data = starfile.read(star_file, always_dict=True)
    if len(data) == 1:
        # star file contains one data block, only happens in RELION 3.0
        return relion30.star2cryopose(star_data=data)
    elif all([block in data.keys() for block in ("optics", "data")]):
        # star file contains optics and data blocks, likely RELION 3.1
        return relion31.star2cryopose(star_data=data)
