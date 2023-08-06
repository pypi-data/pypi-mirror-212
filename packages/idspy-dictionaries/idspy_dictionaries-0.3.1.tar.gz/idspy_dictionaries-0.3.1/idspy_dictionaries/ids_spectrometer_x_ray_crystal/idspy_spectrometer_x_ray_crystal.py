#__version__='0.3.1'
#__imas_commit__='dd6854b4d07'
#__imas_version__='3.7.1'
from ..dataclasses_idsschema import IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


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
class Rzphi1DStatic(IdsBaseClass):
    """
    Structure for list of R, Z, Phi positions (1D, static)

    :ivar r: Major radius
    :ivar z: Height
    :ivar phi: Toroidal angle (oriented counter-clockwise when viewing
        from above)
    """
    class Meta:
        name = "rzphi1d_static"

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
class Rzphi2DStatic(IdsBaseClass):
    """
    Structure for list of R, Z, Phi positions (2D, static)

    :ivar r: Major radius
    :ivar z: Height
    :ivar phi: Toroidal angle (oriented counter-clockwise when viewing
        from above)
    """
    class Meta:
        name = "rzphi2d_static"

    r: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    z: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    phi: Optional[ndarray[(int,int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class SpectrometerXRayCrystalFlt2DTime1(IdsBaseClass):
    """
    Similar to a signal (FLT_2D) but with time base one level above.

    :ivar validity_timed: Indicator of the validity of the data for each
        time slice. 0: valid from automated processing, 1: valid and
        certified by the diagnostic RO; - 1 means problem identified in
        the data processing (request verification by the diagnostic RO),
        -2: invalid data, should not be used (values lower than -2 have
        a code-specific meaning detailing the origin of their
        invalidity)
    :ivar validity: Indicator of the validity of the data for the whole
        acquisition period. 0: valid from automated processing, 1: valid
        and certified by the diagnostic RO; - 1 means problem identified
        in the data processing (request verification by the diagnostic
        RO), -2: invalid data, should not be used (values lower than -2
        have a code-specific meaning detailing the origin of their
        invalidity)
    """
    class Meta:
        name = "spectrometer_x_ray_crystal_flt_2d_time_1"

    validity_timed: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    validity: int = field(
        default=999999999
    )

    @dataclass(slots=True)
    class Data(IdsBaseClass):
        """
        :ivar class_of: Class of Data Item
        """
        class_of: str = field(
            init=False,
            default="FLT_2D"
        )


@dataclass(slots=True)
class SpectrometerXRayCrystalFrame(IdsBaseClass):
    """
    Frame of a camera.

    :ivar counts_n: Number of counts detected on each pixel of the frame
        during one exposure time
    :ivar counts_bin_n: Number of counts detected on each pixel/bin of
        the binned frame during one exposure time
    :ivar time: Time
    """
    class Meta:
        name = "spectrometer_x_ray_crystal_frame"

    counts_n: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    counts_bin_n: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    time: Optional[float] = field(
        default=None
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
class CurvedObject(IdsBaseClass):
    """
    Generic description of a small plane or curved object (crystal, reflector,
    ...), using a generalization of the detector_aperture complexType.

    :ivar identifier: ID of the object
    :ivar geometry_type: Geometry of the object contour. Note that there
        is some flexibility in the choice of the local coordinate system
        (X1,X2,X3). The data provider should choose the most convenient
        coordinate system for the object, respecting the definitions of
        (X1,X2,X3) indicated below.
    :ivar curvature_type: Curvature of the object.
    :ivar material: Material of the object
    :ivar centre: Coordinates of the origin of the local coordinate
        system (X1,X2,X3) describing the object. This origin is located
        within the object area and should be the middle point of the
        object surface. If geometry_type=2, it's the centre of the
        circular object. If geometry_type=3, it's the centre of the
        rectangular object.
    :ivar radius: Radius of the circle, used only if geometry_type/index
        = 2
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
        the height axis. The X3 axis is normal to the object surface and
        oriented towards the plasma.
    :ivar x1_width: Full width of the object in the X1 direction, used
        only if geometry_type/index = 3
    :ivar x2_width: Full width of the object in the X2 direction, used
        only if geometry_type/index = 3
    :ivar outline: Irregular outline of the object in the (X1, X2)
        coordinate system, used only if geometry_type/index=1. Do NOT
        repeat the first point.
    :ivar x1_curvature: Radius of curvature in the X1 direction, to be
        filled only for curvature_type/index = 2, 4 or 5
    :ivar x2_curvature: Radius of curvature in the X2 direction, to be
        filled only for curvature_type/index = 3 or 5
    :ivar surface: Surface of the object, derived from the above
        geometric data
    """
    class Meta:
        name = "curved_object"

    identifier: str = field(
        default=""
    )
    geometry_type: Optional[IdentifierStatic] = field(
        default=None
    )
    curvature_type: Optional[IdentifierStatic] = field(
        default=None
    )
    material: Optional[IdentifierStatic] = field(
        default=None
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
    x1_curvature: float = field(
        default=9e+40
    )
    x2_curvature: float = field(
        default=9e+40
    )
    surface: float = field(
        default=9e+40
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
class FilterWindow(IdsBaseClass):
    """
    Characteristics of the filter window (largely derived from curved_object), with
    some filter specific additions.

    :ivar identifier: ID of the filter
    :ivar geometry_type: Geometry of the filter contour. Note that there
        is some flexibility in the choice of the local coordinate system
        (X1,X2,X3). The data provider should choose the most convenient
        coordinate system for the filter, respecting the definitions of
        (X1,X2,X3) indicated below.
    :ivar curvature_type: Curvature of the filter.
    :ivar centre: Coordinates of the origin of the local coordinate
        system (X1,X2,X3) describing the filter. This origin is located
        within the filter area and should be the middle point of the
        filter surface. If geometry_type=2, it's the centre of the
        circular filter. If geometry_type=3, it's the centre of the
        rectangular filter.
    :ivar radius: Radius of the circle, used only if geometry_type/index
        = 2
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
        the height axis. The X3 axis is normal to the filter surface and
        oriented towards the plasma.
    :ivar x1_width: Full width of the filter in the X1 direction, used
        only if geometry_type/index = 3
    :ivar x2_width: Full width of the filter in the X2 direction, used
        only if geometry_type/index = 3
    :ivar outline: Irregular outline of the filter in the (X1, X2)
        coordinate system, used only if geometry_type/index=1. Do NOT
        repeat the first point.
    :ivar x1_curvature: Radius of curvature in the X1 direction, to be
        filled only for curvature_type/index = 2, 4 or 5
    :ivar x2_curvature: Radius of curvature in the X2 direction, to be
        filled only for curvature_type/index = 3 or 5
    :ivar surface: Surface of the filter, derived from the above
        geometric data
    :ivar material: Material of the filter window
    :ivar thickness: Thickness of the filter window
    :ivar wavelength_lower: Lower bound of the filter wavelength range
    :ivar wavelength_upper: Upper bound of the filter wavelength range
    :ivar wavelengths: Array of wavelength values
    :ivar photon_absorption: Probability of absorbing a photon passing
        through the filter as a function of its wavelength
    """
    class Meta:
        name = "filter_window"

    identifier: str = field(
        default=""
    )
    geometry_type: Optional[IdentifierStatic] = field(
        default=None
    )
    curvature_type: Optional[IdentifierStatic] = field(
        default=None
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
    x1_curvature: float = field(
        default=9e+40
    )
    x2_curvature: float = field(
        default=9e+40
    )
    surface: float = field(
        default=9e+40
    )
    material: Optional[IdentifierStatic] = field(
        default=None
    )
    thickness: float = field(
        default=9e+40
    )
    wavelength_lower: float = field(
        default=9e+40
    )
    wavelength_upper: float = field(
        default=9e+40
    )
    wavelengths: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    photon_absorption: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class LineOfSight2Points(IdsBaseClass):
    """
    Generic description of a line of sight, defined by two points.

    :ivar first_point: Position of the first point
    :ivar second_point: Position of the second point
    """
    class Meta:
        name = "line_of_sight_2points"

    first_point: Optional[Rzphi0DStatic] = field(
        default=None
    )
    second_point: Optional[Rzphi0DStatic] = field(
        default=None
    )


@dataclass(slots=True)
class LineOfSight2PointsRzphi2D(IdsBaseClass):
    """
    Generic description of a line of sight, defined by two points.

    :ivar first_point: Position of the first point
    :ivar second_point: Position of the second point
    """
    class Meta:
        name = "line_of_sight_2points_rzphi_2d"

    first_point: Optional[Rzphi2DStatic] = field(
        default=None
    )
    second_point: Optional[Rzphi2DStatic] = field(
        default=None
    )


@dataclass(slots=True)
class SpectrometerXRayCrystalCrystal(IdsBaseClass):
    """
    Characteristics of the crystal used, extension of the generic description of a
    small plane or curved object (crystal, reflector, ...)

    :ivar identifier: ID of the object
    :ivar geometry_type: Geometry of the object contour. Note that there
        is some flexibility in the choice of the local coordinate system
        (X1,X2,X3). The data provider should choose the most convenient
        coordinate system for the object, respecting the definitions of
        (X1,X2,X3) indicated below.
    :ivar curvature_type: Curvature of the object.
    :ivar material: Material of the object
    :ivar centre: Coordinates of the origin of the local coordinate
        system (X1,X2,X3) describing the object. This origin is located
        within the object area and should be the middle point of the
        object surface. If geometry_type=2, it's the centre of the
        circular object. If geometry_type=3, it's the centre of the
        rectangular object.
    :ivar radius: Radius of the circle, used only if geometry_type/index
        = 2
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
        the height axis. The X3 axis is normal to the object surface and
        oriented towards the plasma.
    :ivar x1_width: Full width of the object in the X1 direction, used
        only if geometry_type/index = 3
    :ivar x2_width: Full width of the object in the X2 direction, used
        only if geometry_type/index = 3
    :ivar outline: Irregular outline of the object in the (X1, X2)
        coordinate system, used only if geometry_type/index=1. Do NOT
        repeat the first point.
    :ivar x1_curvature: Radius of curvature in the X1 direction, to be
        filled only for curvature_type/index = 2, 4 or 5
    :ivar x2_curvature: Radius of curvature in the X2 direction, to be
        filled only for curvature_type/index = 3 or 5
    :ivar surface: Surface of the object, derived from the above
        geometric data
    :ivar wavelength_bragg: Bragg wavelength of the crystal
    :ivar angle_bragg: Bragg angle of the crystal
    :ivar thickness: Thickness of the crystal
    :ivar cut: Miller indices characterizing the cut of the crystal (can
        be of length 3 or 4)
    :ivar mesh_type: Crystal mesh type
    """
    class Meta:
        name = "spectrometer_x_ray_crystal_crystal"

    identifier: str = field(
        default=""
    )
    geometry_type: Optional[IdentifierStatic] = field(
        default=None
    )
    curvature_type: Optional[IdentifierStatic] = field(
        default=None
    )
    material: Optional[IdentifierStatic] = field(
        default=None
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
    x1_curvature: float = field(
        default=9e+40
    )
    x2_curvature: float = field(
        default=9e+40
    )
    surface: float = field(
        default=9e+40
    )
    wavelength_bragg: float = field(
        default=9e+40
    )
    angle_bragg: float = field(
        default=9e+40
    )
    thickness: float = field(
        default=9e+40
    )
    cut: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    mesh_type: Optional[IdentifierStatic] = field(
        default=None
    )


@dataclass(slots=True)
class SpectrometerXRayCrystalInstrumentFunction(IdsBaseClass):
    """
    Instrument function.

    :ivar wavelengths: Array of wavelengths on which the instrument
        function is defined
    :ivar values: Explicit instrument function values for the detector.
        When multiplied by the line-integrated emission spectrum in
        photons/second/sr/m/m^2 received on a pixel of the detector,
        gives the detector pixel output in counts/seconds.
    :ivar type: Instrument function type
    :ivar intensity: Scaling factor for the instrument function such
        that convolving the instrument function with an emission
        spectrum gives the counts per second on the detector
    :ivar centre: Centre (in terms of absolute wavelength) of instrument
        function
    :ivar sigma: Standard deviation of Gaussian instrument function
    :ivar scale: Scale of Lorentzian instrument function (full width at
        half height)
    """
    class Meta:
        name = "spectrometer_x_ray_crystal_instrument_function"

    wavelengths: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    values: Optional[ndarray[(int,int, int), float]] = field(
        default=None
    )
    type: Optional[IdentifierStatic] = field(
        default=None
    )
    intensity: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    centre: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    sigma: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    scale: Optional[ndarray[(int,int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class SpectrometerXRayCrystalProxy(IdsBaseClass):
    """
    X-ray crystal spectrometer profile proxy.

    :ivar lines_of_sight_second_point: For each profile point, a line of
        sight is defined by a first point given by the centre of the
        crystal and a second point described here.
    :ivar lines_of_sight_rho_tor_norm: Shortest distance in rho_tor_norm
        between lines of sight and magnetic axis, signed with following
        convention : positive (resp. negative) means the point of
        shortest distance is above (resp. below) the magnetic axis
    :ivar t_i: Ion temperature (estimated from a spectral fit directly
        on the output line-integrated signal, without tomographic
        inversion)
    :ivar t_e: Electron temperature (estimated from a spectral fit
        directly on the output line-integrated signal, without
        tomographic inversion)
    :ivar velocity_tor: Toroidal velocity (estimated from a spectral fit
        directly on the output line-integrated signal, without
        tomographic inversion)
    :ivar time: Timebase for the dynamic nodes of this probe located at
        this level of the IDS structure
    """
    class Meta:
        name = "spectrometer_x_ray_crystal_proxy"

    lines_of_sight_second_point: Optional[Rzphi1DStatic] = field(
        default=None
    )
    lines_of_sight_rho_tor_norm: Optional[SpectrometerXRayCrystalFlt2DTime1] = field(
        default=None
    )
    t_i: Optional[SpectrometerXRayCrystalFlt2DTime1] = field(
        default=None
    )
    t_e: Optional[SpectrometerXRayCrystalFlt2DTime1] = field(
        default=None
    )
    velocity_tor: Optional[SpectrometerXRayCrystalFlt2DTime1] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )


@dataclass(slots=True)
class CameraGeometry(IdsBaseClass):
    """Camera geometry.

    The orientation of the camera is described as follows : pixels are aligned along x1 and x2 unit vectors while x3 is normal to the detector plane.

    :ivar identifier: ID of the camera
    :ivar pixel_dimensions: Pixel dimension in each direction (x1, x2)
    :ivar pixels_n: Number of pixels in each direction (x1, x2)
    :ivar pixel_position: Position of the centre of each pixel. First
        dimension : line index (x1 axis). Second dimension: column index
        (x2 axis).
    :ivar camera_dimensions: Total camera dimension in each direction
        (x1, x2)
    :ivar centre: Position of the camera centre
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
        the height axis. The X3 axis is normal to the camera plane and
        oriented towards the plasma.
    :ivar line_of_sight: Description of the line of sight for each
        pixel, given by 2 points. For each coordinate : first dimension
        : line index (x1 axis); second dimension: column index (x2
        axis).
    """
    class Meta:
        name = "camera_geometry"

    identifier: str = field(
        default=""
    )
    pixel_dimensions: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pixels_n: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    pixel_position: Optional[Rzphi2DStatic] = field(
        default=None
    )
    camera_dimensions: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    centre: Optional[Rzphi0DStatic] = field(
        default=None
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
    line_of_sight: Optional[LineOfSight2PointsRzphi2D] = field(
        default=None
    )


@dataclass(slots=True)
class SpectrometerXRayCrystalBin(IdsBaseClass):
    """
    Binning scheme (binning done in the vertical direction)

    :ivar z_pixel_range: Vertical pixel index range indicating the
        corresponding binned detector area
    :ivar wavelength: Wavelength of incoming photons on each horizontal
        pixel of this bin.
    :ivar line_of_sight: Description of the line of sight from the
        crystal to the plasma for this bin, defined by two points
    """
    class Meta:
        name = "spectrometer_x_ray_crystal_bin"

    z_pixel_range: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    wavelength: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    line_of_sight: Optional[LineOfSight2Points] = field(
        default=None
    )


@dataclass(slots=True)
class SpectrometerXRayCrystalChannel(IdsBaseClass):
    """
    X-crystal spectrometer channel.

    :ivar exposure_time: Exposure time of the measurement
    :ivar energy_bound_lower: Lower energy bound for the photon
        detection, for each pixel (horizontal, vertical)
    :ivar energy_bound_upper: Upper energy bound for the photon
        detection, for each pixel (horizontal, vertical)
    :ivar aperture: Collimating aperture
    :ivar reflector: Set of reflectors (optional) reflecting the light
        coming from the plasma towards the crystal. If empty, means that
        the plasma light directly arrives on the crystal.
    :ivar crystal: Characteristics of the crystal used
    :ivar filter_window: Set of filter windows
    :ivar camera: Characteristics of the camera used
    :ivar z_frames: Height of the observed zone at the focal plane in
        the plasma, corresponding to the vertical dimension of the frame
    :ivar wavelength_frames: Wavelength of incoming photons on each
        pixel of the frames, mainly varying accross the horizontal
        dimension of the frame. However a 2D map of the wavelength is
        given since it is not constant vertically due to the elliptical
        curvature of the photon iso-surfaces
    :ivar bin: Set of bins (binning in the vertical dimension) defined
        to increase the signal to noise ratio of the spectra
    :ivar frame: Set of frames
    :ivar energies: Array of energy values for tabulation of the
        detection efficiency
    :ivar detection_efficiency: Probability of detection of a photon
        impacting the detector as a function of its energy
    :ivar profiles_line_integrated: Profiles proxies are given in the
        vertical direction of the detector. They are estimated directly
        from the camera, without tomographic inversion. Binning is
        allowed so the number of profile points may be lower than the
        length of z_frames. Physical quantities deduced from the
        measured spectra are given for each profile point. They
        correspond to the spectra integrated along lines of sight,
        defined by a first point given by the centre of the crystal and
        a second point (depending on the profile point) described below.
    :ivar instrument_function: Instrument function, i.e. response of the
        detector to a monochromatic emission passing through the
        spectrometer. The resulting image on the detector will be a 2-D
        distribution of pixel values, for each wavelength. It can be
        given as explicit values for each detector pixel (values node)
        or as a parametric function of wavelength (described by the
        other nodes)
    """
    class Meta:
        name = "spectrometer_x_ray_crystal_channel"

    exposure_time: float = field(
        default=9e+40
    )
    energy_bound_lower: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    energy_bound_upper: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    aperture: Optional[DetectorAperture] = field(
        default=None
    )
    reflector: list[CurvedObject] = field(
        default_factory=list,
        metadata={
            "max_occurs": 10,
        }
    )
    crystal: Optional[SpectrometerXRayCrystalCrystal] = field(
        default=None
    )
    filter_window: list[FilterWindow] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    camera: Optional[CameraGeometry] = field(
        default=None
    )
    z_frames: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    wavelength_frames: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    bin: list[SpectrometerXRayCrystalBin] = field(
        default_factory=list,
        metadata={
            "max_occurs": 100,
        }
    )
    frame: list[SpectrometerXRayCrystalFrame] = field(
        default_factory=list
    )
    energies: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    detection_efficiency: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    profiles_line_integrated: Optional[SpectrometerXRayCrystalProxy] = field(
        default=None
    )
    instrument_function: Optional[SpectrometerXRayCrystalInstrumentFunction] = field(
        default=None
    )


@dataclass(slots=True)
class SpectrometerXRayCrystal(IdsBaseClass):
    """
    X-crystal spectrometer diagnostic.

    :ivar ids_properties:
    :ivar channel: Measurement channel, composed of a camera, a crystal,
        and (optional) a set of reflectors. The light coming from the
        plasma passes through the (optional) set of reflectors, then the
        crystal and arrives at the camera
    :ivar latency: Upper bound of the delay between physical information
        received by the detector and data available on the real-time
        (RT) network.
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "spectrometer_x_ray_crystal"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    channel: list[SpectrometerXRayCrystalChannel] = field(
        default_factory=list,
        metadata={
            "max_occurs": 30,
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
