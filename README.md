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

## DataFrame Column headings

| Heading         | Python name             | Semantics                                            |
|:----------------|:------------------------|:-----------------------------------------------------|
| `x`             | CRYOPOSE_POSITION_X     | particle position in x-dimension                     |
| `y`             | CRYOPOSE_POSITION_Y     | particle position in y-dimension                     |
| `z`             | CRYOPOSE_POSITION_Z     | particle position in z-dimension                     |
| `orientation`   | CRYOPOSE_ORIENTATION    | particle orientation                                 |
| `experiment_id` | CRYOPOSE_EXPERIMENT_ID  | experimental identifier for micrograph/tilt-series   |
| `pixel_spacing` | CRYOPOSE_PIXEL_SPACING  | isotropic pixel/voxel spacing for particle positions |

## Ambiguities

This section aims to deal with ambiguities in the way these metadata are defined.

### Positions
Particle positions are coordinates in 2D or 3D images. The center of the first pixel is taken to be the origin `(0, 0)` or `(0, 0, 0)`.

### Orientations
Particle orientations are
