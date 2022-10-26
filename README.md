# cryotypes

[![License](https://img.shields.io/pypi/l/cryotypes.svg?color=green)](https://github.com/teamtomo/cryotypes/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/cryotypes.svg?color=green)](https://pypi.org/project/cryotypes)
[![Python Version](https://img.shields.io/pypi/pyversions/cryotypes.svg?color=green)](https://python.org)
[![CI](https://github.com/teamtomo/cryotypes/workflows/ci/badge.svg)](https://github.com/alisterburt/cryotypes/actions)
[![codecov](https://codecov.io/gh/teamtomo/cryotypes/branch/master/graph/badge.svg)](https://codecov.io/gh/teamtomo/cryotypes)

`cryotypes` defines a set of super-simple, extensible data structures for the fundamental types of cryoEM data and their relative metadata:
- `PoseSet`: a set of particle poses, compatible with 2D and 3D data
- `ProjectionModel`: a set of parameters for a projection model (tilt-series alignments)
- `Tomogram`: a 3D image
- `Micrograph`: a 2D image

Each cryotype defines an `experiment_id` attribute which is intended as a unique identifier for individual experiments. This can be used, for example, to match particles to the correct tilt series and tomogram.


## `PoseSet`
A `PoseSet` is a [pandas `DataFrame`](https://pandas.pydata.org/docs/) with specific column headings for particle positions and orientations, experiment identifiers and pixel/voxel spacing. This data-structure can be used for both 2D and 3D particle poses.

### DataFrame column headings
| Heading         | Python name   | Semantics                                            |
|:----------------|:--------------|:-----------------------------------------------------|
| `x`             | POSITION_X    | particle position in x-dimension                     |
| `y`             | POSITION_Y    | particle position in y-dimension                     |
| `z`             | POSITION_Z    | particle position in z-dimension                     |
| `dx`            | SHIFT_X       | particle shift in x-dimension                        |
| `dy`            | SHIFT_Y       | particle shift in y-dimension                        |
| `dz`            | SHIFT_Z       | particle shift in z-dimension                        |
| `orientation`   | ORIENTATION   | particle orientation                                 |
| `experiment_id` | EXPERIMENT_ID | experimental identifier for micrograph/tilt-series   |
| `pixel_spacing` | PIXEL_SPACING | isotropic pixel/voxel spacing for particle positions |

The labels can be conveniently accessed from Python should you need them.

```python
from cryotypes import PoseSetDataLabels as CPDL

pose_dataframe[PSDL.POSITION_X] = xyz[:, 0]
```

### Positions
Particle positions are coordinates in 2D or 3D images. The center of the first pixel is taken to be the origin `(0, 0)` or `(0, 0, 0)` and the units of particle positions are pixels.

### Shifts
Particle shifts are in image pixels and are additive to positions, such that `POSITION + SHIFT` is the position of the particle in the tomogram.

### Orientations
Particle orientations are stored as
[`scipy.spatial.transform.Rotation`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.html) objects.
These transformations should rotate the basis vectors of a reference such that they are correctly oriented in a tomogram.

## `ProjectionModel`
A `ProjectionModel` is a [pandas `DataFrame`](https://pandas.pydata.org/docs/) with specific column 
headings for the parameters of a projection model. Together, this information constitues a 'tilt-series alignment'.

| Heading         | Python name   | Semantics                                  |
|:----------------|:--------------|:-------------------------------------------|
| `rotation_x`    | ROTATION_X    | tomogram rotation around x-axis            |
| `rotation_y`    | ROTATION_Y    | tomogram rotation around y-axis            |
| `rotation_z`    | ROTATION_Z    | tomogram rotation around z-axis            |
| `dx`            | SHIFT_X       | particle shift in x-dimension              |
| `dy`            | SHIFT_Y       | particle shift in y-dimension              |
| `experiment_id` | EXPERIMENT_ID | identifier for micrograph/tilt-series      |
| `pixel_spacing` | PIXEL_SPACING | isotropic pixel/voxel spacing for shifts   |
| `source`        | SOURCE        | reference to the file from which data came |

A utility function is also provided for generating projection matrices from these data.

```python
from cryotypes.projectionmodel import projection_model_to_projection_matrices

projection_matrices = projection_model_to_projection_matrices(
    df=projection_model,  # ProjectionModel dataframe
    tilt_image_center=(1919, 1355),  # tilt-image rotation center (xy)
    tomogram_dimensions=(3838, 3710, 2000)  # dimensions of tomogram (xyz)
)
```

**Note:** these projection matrices are only valid for positions in a tomogram of the dimensions
provided in this function and must be recalculated for different tomogram dimensions.

## `Tomogram`
A `Tomogram` is an object that follows a specific [python `Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol) for tomogram data. The protocol specifies the following attributes:

- `data`: an array-like 3D image (`numpy`, `dask`, ...)
- `experiment_id`: experimental identifier
- `pixel_spacing`: isotropic pixel/voxel spacing
