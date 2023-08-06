#__version__='0.3.1'
#__imas_commit__='dd6854b4d07'
#__imas_version__='3.7.1'
from ..dataclasses_idsschema import IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


@dataclass(slots=True)
class CameraVisibleFrame(IdsBaseClass):
    """
    Frame of a camera.

    :ivar image_raw: Raw image (unprocessed) (digital levels). First
        dimension : line index (horizontal axis). Second dimension:
        column index (vertical axis).
    :ivar radiance: Radiance image. First dimension : line index
        (horizontal axis). Second dimension: column index (vertical
        axis).
    :ivar time: Time
    """
    class Meta:
        name = "camera_visible_frame"

    image_raw: Optional[ndarray[(int, int), int]] = field(
        default=None
    )
    radiance: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class CameraVisibleGeometryMatrixInterpolated(IdsBaseClass):
    """
    Interpolated geometry matrix.

    :ivar r: Major radius of interpolation knots
    :ivar z: Height of interpolation knots
    :ivar phi: Toroidal angle (oriented counter-clockwise when viewing
        from above) of interpolation knots
    """
    class Meta:
        name = "camera_visible_geometry_matrix_interpolated"

    r: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    z: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    phi: Optional[ndarray[(int,), float]] = field(
        default=None
    )

    @dataclass(slots=True)
    class Data(IdsBaseClass):
        """
        :ivar class_of: Class of Data Item
        """
        class_of: str = field(
            init=False,
            default="FLT_3D"
        )


@dataclass(slots=True)
class CameraVisibleGeometryMatrixStep2(IdsBaseClass):
    """
    Geometry matrix of the detector.

    :ivar voxel_indices: List of voxel indices (defined in the voxel
        map) used in the sparse data array
    :ivar pixel_indices: List of pixel indices used in the sparse data
        array. The first dimension refers to the data array index. The
        second dimension lists the line index (horizontal axis) in first
        position, then the column index (vertical axis).
    """
    class Meta:
        name = "camera_visible_geometry_matrix_step2"

    voxel_indices: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    pixel_indices: Optional[ndarray[(int, int), int]] = field(
        default=None
    )

    @dataclass(slots=True)
    class Data(IdsBaseClass):
        """
        :ivar class_of: Class of Data Item
        """
        class_of: str = field(
            init=False,
            default="FLT_1D"
        )


@dataclass(slots=True)
class IdentifierStatic(IdsBaseClass):
    """Standard type for identifiers (static).

    The three fields: name, index and description are all
    representations of the same information. Associated with each
    application of this identifier-type, there should be a translation
    table defining the three fields for all objects to be identified.

    :ivar name: Short string identifier
    :ivar index: Integer identifier (enumeration index within a list).
        Private identifier values must be indicated by a negative index.
    :ivar description: Verbose description
    """
    class Meta:
        name = "identifier_static"

    name: str = field(
        default=""
    )
    index: int = field(
        default=999999999
    )
    description: str = field(
        default=""
    )


@dataclass(slots=True)
class IdsProperties(IdsBaseClass):
    """Interface Data Structure properties.

    This element identifies the node above as an IDS

    :ivar comment: Any comment describing the content of this IDS
    :ivar homogeneous_time: This node must be filled (with 0, 1, or 2)
        for the IDS to be valid. If 1, the time of this IDS is
        homogeneous, i.e. the time values for this IDS are stored in the
        time node just below the root of this IDS. If 0, the time values
        are stored in the various time fields at lower levels in the
        tree. In the case only constant or static nodes are filled
        within the IDS, homogeneous_time must be set to 2
    :ivar provider: Name of the person in charge of producing this data
    :ivar creation_date: Date at which this data has been produced
    """
    class Meta:
        name = "ids_properties"

    comment: str = field(
        default=""
    )
    homogeneous_time: int = field(
        default=999999999
    )
    provider: str = field(
        default=""
    )
    creation_date: str = field(
        default=""
    )


@dataclass(slots=True)
class Library(IdsBaseClass):
    """
    Library used by the code that has produced this IDS.

    :ivar name: Name of software
    :ivar commit: Unique commit reference of software
    :ivar version: Unique version (tag) of software
    :ivar repository: URL of software repository
    :ivar parameters: List of the code specific parameters in XML format
    """
    class Meta:
        name = "library"

    name: str = field(
        default=""
    )
    commit: str = field(
        default=""
    )
    version: str = field(
        default=""
    )
    repository: str = field(
        default=""
    )
    parameters: str = field(
        default=""
    )


@dataclass(slots=True)
class Rzphi0DStatic(IdsBaseClass):
    """
    Structure for R, Z, Phi positions (0D, static)

    :ivar r: Major radius
    :ivar z: Height
    :ivar phi: Toroidal angle (oriented counter-clockwise when viewing
        from above)
    """
    class Meta:
        name = "rzphi0d_static"

    r: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )
    phi: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class X1X21DStatic(IdsBaseClass):
    """
    Structure for list of X1, X2 positions (1D, static)

    :ivar x1: Positions along x1 axis
    :ivar x2: Positions along x2 axis
    """
    class Meta:
        name = "x1x21d_static"

    x1: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    x2: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class Xyz0DStatic(IdsBaseClass):
    """
    Structure for list of X, Y, Z components (0D, static)

    :ivar x: Component along X axis
    :ivar y: Component along Y axis
    :ivar z: Component along Z axis
    """
    class Meta:
        name = "xyz0d_static"

    x: float = field(
        default=9e+40
    )
    y: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class Code(IdsBaseClass):
    """
    Generic decription of the code-specific parameters for the code that has
    produced this IDS.

    :ivar name: Name of software generating IDS
    :ivar commit: Unique commit reference of software
    :ivar version: Unique version (tag) of software
    :ivar repository: URL of software repository
    :ivar parameters: List of the code specific parameters in XML format
    :ivar output_flag: Output flag : 0 means the run is successful,
        other values mean some difficulty has been encountered, the
        exact meaning is then code specific. Negative values mean the
        result shall not be used.
    :ivar library: List of external libraries used by the code that has
        produced this IDS
    """
    class Meta:
        name = "code"

    name: str = field(
        default=""
    )
    commit: str = field(
        default=""
    )
    version: str = field(
        default=""
    )
    repository: str = field(
        default=""
    )
    parameters: str = field(
        default=""
    )
    output_flag: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    library: list[Library] = field(
        default_factory=list,
        metadata={
            "max_occurs": 10,
        }
    )


@dataclass(slots=True)
class DetectorAperture(IdsBaseClass):
    """
    Generic description of a plane detector or collimating aperture.

    :ivar geometry_type: Type of geometry used to describe the surface
        of the detector or aperture (1:'outline', 2:'circular',
        3:'rectangle'). In case of 'outline', the surface is described
        by an outline of point in a local coordinate system defined by a
        centre and three unit vectors X1, X2, X3. Note that there is
        some flexibility here and the data provider should choose the
        most convenient coordinate system for the object, respecting the
        definitions of (X1,X2,X3) indicated below. In case of
        'circular', the surface is a circle defined by its centre,
        radius, and normal vector oriented towards the plasma X3.  In
        case of 'rectangle', the surface is a rectangle defined by its
        centre, widths in the X1 and X2 directions, and normal vector
        oriented towards the plasma X3.
    :ivar centre: If geometry_type=2, coordinates of the centre of the
        circle. If geometry_type=1 or 3, coordinates of the origin of
        the local coordinate system (X1,X2,X3) describing the plane
        detector/aperture. This origin is located within the
        detector/aperture area.
    :ivar radius: Radius of the circle, used only if geometry_type = 2
    :ivar x1_unit_vector: Components of the X1 direction unit vector in
        the (X,Y,Z) coordinate system, where X is the major radius axis
        for phi = 0, Y is the major radius axis for phi = pi/2, and Z is
        the height axis. The X1 vector is more horizontal than X2 (has a
        smaller abs(Z) component) and oriented in the positive phi
        direction (counter-clockwise when viewing from above).
    :ivar x2_unit_vector: Components of the X2 direction unit vector in
        the (X,Y,Z) coordinate system, where X is the major radius axis
        for phi = 0, Y is the major radius axis for phi = pi/2, and Z is
        the height axis. The X2 axis is orthonormal so that uX2 = uX3 x
        uX1.
    :ivar x3_unit_vector: Components of the X3 direction unit vector in
        the (X,Y,Z) coordinate system, where X is the major radius axis
        for phi = 0, Y is the major radius axis for phi = pi/2, and Z is
        the height axis. The X3 axis is normal to the detector/aperture
        plane and oriented towards the plasma.
    :ivar x1_width: Full width of the aperture in the X1 direction, used
        only if geometry_type = 3
    :ivar x2_width: Full width of the aperture in the X2 direction, used
        only if geometry_type = 3
    :ivar outline: Irregular outline of the detector/aperture in the
        (X1, X2) coordinate system. Do NOT repeat the first point.
    :ivar surface: Surface of the detector/aperture, derived from the
        above geometric data
    """
    class Meta:
        name = "detector_aperture"

    geometry_type: int = field(
        default=999999999
    )
    centre: Optional[Rzphi0DStatic] = field(
        default=None
    )
    radius: float = field(
        default=9e+40
    )
    x1_unit_vector: Optional[Xyz0DStatic] = field(
        default=None
    )
    x2_unit_vector: Optional[Xyz0DStatic] = field(
        default=None
    )
    x3_unit_vector: Optional[Xyz0DStatic] = field(
        default=None
    )
    x1_width: float = field(
        default=9e+40
    )
    x2_width: float = field(
        default=9e+40
    )
    outline: Optional[X1X21DStatic] = field(
        default=None
    )
    surface: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class GeometryMatrixEmission(IdsBaseClass):
    """
    Emission grid for the geometry matrix of a detector.

    :ivar grid_type: Grid type
    :ivar dim1: First dimension values
    :ivar dim2: Second dimension values
    :ivar dim3: Third dimension values
    """
    class Meta:
        name = "geometry_matrix_emission"

    grid_type: Optional[IdentifierStatic] = field(
        default=None
    )
    dim1: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    dim2: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    dim3: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class CameraVisibleGeometryMatrix(IdsBaseClass):
    """
    Geometry matrix of the camera.

    :ivar with_reflections: Geometry matrix with reflections
    :ivar without_reflections: Geometry matrix without reflections
    :ivar interpolated: Interpolated geometry matrix for reflected light
    :ivar voxel_map: Voxel map for geometry matrix. The cells with same
        number are merged in the computation into a single emission
        source meta-cell (the voxel). Cells with number -1 are excluded.
        Voxel count starts from 0.
    :ivar voxels_n: Number of voxels defined in the voxel_map.
    :ivar emission_grid: Grid defining the light emission cells
    """
    class Meta:
        name = "camera_visible_geometry_matrix"

    with_reflections: Optional[CameraVisibleGeometryMatrixStep2] = field(
        default=None
    )
    without_reflections: Optional[CameraVisibleGeometryMatrixStep2] = field(
        default=None
    )
    interpolated: Optional[CameraVisibleGeometryMatrixInterpolated] = field(
        default=None
    )
    voxel_map: Optional[ndarray[(int, int, int), int]] = field(
        default=None
    )
    voxels_n: int = field(
        default=999999999
    )
    emission_grid: Optional[GeometryMatrixEmission] = field(
        default=None
    )


@dataclass(slots=True)
class CameraVisibleDetector(IdsBaseClass):
    """
    Detector for a visible camera.

    :ivar pixel_to_alpha: Alpha angle of each pixel in the horizontal
        axis
    :ivar pixel_to_beta: Beta angle of each pixel in the vertical axis
    :ivar wavelength_lower: Lower bound of the detector wavelength range
    :ivar wavelength_upper: Upper bound of the detector wavelength range
    :ivar counts_to_radiance: Counts to radiance factor, for each pixel
        of the detector. Includes both the transmission losses in the
        relay optics and the quantum efficiency of the camera itself,
        integrated over the wavelength range
    :ivar exposure_time: Exposure time
    :ivar noise: Detector noise (e.g. read-out noise) (rms counts per
        second exposure time)
    :ivar columns_n: Number of pixel columns in the horizontal direction
    :ivar lines_n: Number of pixel lines in the vertical direction
    :ivar frame: Set of frames
    :ivar geometry_matrix: Description of geometry matrix (ray transfer
        matrix)
    """
    class Meta:
        name = "camera_visible_detector"

    pixel_to_alpha: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pixel_to_beta: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    wavelength_lower: float = field(
        default=9e+40
    )
    wavelength_upper: float = field(
        default=9e+40
    )
    counts_to_radiance: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    exposure_time: float = field(
        default=9e+40
    )
    noise: float = field(
        default=9e+40
    )
    columns_n: int = field(
        default=999999999
    )
    lines_n: int = field(
        default=999999999
    )
    frame: list[CameraVisibleFrame] = field(
        default_factory=list
    )
    geometry_matrix: Optional[CameraVisibleGeometryMatrix] = field(
        default=None
    )


@dataclass(slots=True)
class CameraVisibleChannel(IdsBaseClass):
    """
    Channel of a camera.

    :ivar name: Name of the channel
    :ivar aperture: Description of apertures between plasma and the
        detectors (position, outline shape and orientation)
    :ivar viewing_angle_alpha_bounds: Minimum and maximum values of
        alpha angle of the field of view, where alpha is the agle
        between the axis X3 and projection of the chord of view  on the
        plane X1X3 counted clockwise from the top view of X2 axis. X1,
        X2, X3 are the ones of the first aperture (i.e. the closest to
        the plasma).
    :ivar viewing_angle_beta_bounds: Minimum and maximum values of beta
        angle of the field of view, where beta is the angle between the
        axis X3 and projection of the chord of view on the plane X2X3
        counted clockwise from the top view of X1 axis. X1, X2, X3 are
        the ones of the first aperture (i.e. the closest to the plasma).
    :ivar detector: Set of detectors
    """
    class Meta:
        name = "camera_visible_channel"

    name: str = field(
        default=""
    )
    aperture: list[DetectorAperture] = field(
        default_factory=list,
        metadata={
            "max_occurs": 3,
        }
    )
    viewing_angle_alpha_bounds: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    viewing_angle_beta_bounds: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    detector: list[CameraVisibleDetector] = field(
        default_factory=list,
        metadata={
            "max_occurs": 10,
        }
    )


@dataclass(slots=True)
class CameraVisible(IdsBaseClass):
    """
    Camera in the visible light range.

    :ivar ids_properties:
    :ivar name: Name of the camera
    :ivar channel: Set of channels (a front aperture, possibly followed
        by others, viewing the plasma recorded by one or more detectors
        e.g. for different wavelength ranges)
    :ivar latency: Upper bound of the delay between physical information
        received by the detector and data available on the real-time
        (RT) network.
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "camera_visible"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    name: str = field(
        default=""
    )
    channel: list[CameraVisibleChannel] = field(
        default_factory=list,
        metadata={
            "max_occurs": 20,
        }
    )
    latency: float = field(
        default=9e+40
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
