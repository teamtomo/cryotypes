# cryopose

[![License](https://img.shields.io/pypi/l/cryopose.svg?color=green)](https://github.com/teamtomo/cryopose/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/cryopose.svg?color=green)](https://pypi.org/project/cryopose)
[![Python Version](https://img.shields.io/pypi/pyversions/cryopose.svg?color=green)](https://python.org)
[![CI](https://github.com/teamtomo/cryopose/workflows/ci/badge.svg)](https://github.com/alisterburt/cryopose/actions)
[![codecov](https://codecov.io/gh/teamtomo/cryopose/branch/master/graph/badge.svg)](https://codecov.io/gh/teamtomo/cryopose)

`cryopose` defines a super-simple, extensible data structure for sets of particle poses from cryo-EM software.

A `cryopose` dataframe is a [pandas `DataFrame`](https://pandas.pydata.org/docs/) with specific column headings
for particle positions and orientations, experimental identifiers and pixel/voxel spacing.

This data-structure can be used for both 2D and 3D particle poses and is easily passed between
Python packages for file input/output and analysis.

## DataFrame column headings

The following headings are defined at in `_data_labels.py`.

| Heading         | Python name   | Semantics                                            |
|:----------------|:--------------|:-----------------------------------------------------|
| `x`             | POSITION_X    | particle position in x-dimension                     |
| `y`             | POSITION_Y    | particle position in y-dimension                     |
| `z`             | POSITION_Z    | particle position in z-dimension                     |
| `orientation`   | ORIENTATION   | particle orientation                                 |
| `experiment_id` | EXPERIMENT_ID | experimental identifier for micrograph/tilt-series   |
| `pixel_spacing` | PIXEL_SPACING | isotropic pixel/voxel spacing for particle positions |

The labels can be conveniently accessed from Python should you need them.

```python
from cryopose import CryoPoseDataLabels as CPDL

df[CPDL.POSITION_X] = xyz[:, 0]
```

## Ambiguities

This section aims to deal with ambiguities in the way these metadata are defined.

### Positions
Particle positions are coordinates in 2D or 3D images. The center of the first pixel is taken to be the origin `(0, 0)` or `(0, 0, 0)` and the units of particle positions are pixels.

### Orientations
Particle orientations are stored as
[`scipy.spatial.transform.Rotation`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.html) objects.
These transformations should rotate the basis vectors of a reference such that they are correctly oriented in a tomogram.
