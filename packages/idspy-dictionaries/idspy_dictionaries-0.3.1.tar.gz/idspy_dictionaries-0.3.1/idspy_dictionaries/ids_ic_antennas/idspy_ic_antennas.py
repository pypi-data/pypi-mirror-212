#__version__='0.3.1'
#__imas_commit__='dd6854b4d07'
#__imas_version__='3.7.1'
from ..dataclasses_idsschema import IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


@dataclass(slots=True)
class AnnulusStatic(IdsBaseClass):
    """
    Annulus description (2D object)

    :ivar r: Centre major radius
    :ivar z: Centre height
    :ivar radius_inner: Inner radius
    :ivar radius_outer: Outer radius
    """
    class Meta:
        name = "annulus_static"

    r: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )
    radius_inner: float = field(
        default=9e+40
    )
    radius_outer: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class ArcsOfCircleStatic(IdsBaseClass):
    """
    Arcs of circle description of a 2D contour.

    :ivar r: Major radii of the start point of each arc of circle
    :ivar z: Height of the start point of each arc of circle
    :ivar curvature_radii: Curvature radius of each arc of circle
    """
    class Meta:
        name = "arcs_of_circle_static"

    r: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    z: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    curvature_radii: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class IcAntennasSurfaceCurrent(IdsBaseClass):
    """
    Description of the IC surface current on the antenna straps and on passive
    components.

    :ivar m_pol: Poloidal mode numbers, used to describe the spectrum of
        the antenna current. The poloidal angle is defined from the
        reference point; the angle at a point (R,Z) is given by
        atan((Z-Zref)/(R-Rref)), where Rref=reference_point/r and
        Zref=reference_point/z
    :ivar n_tor: Toroidal mode numbers, used to describe the spectrum of
        the antenna current
    :ivar spectrum: Spectrum of the total surface current on the antenna
        strap and passive components expressed in poloidal and toroidal
        modes
    :ivar time: Time
    """
    class Meta:
        name = "ic_antennas_surface_current"

    m_pol: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    n_tor: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    spectrum: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    time: Optional[float] = field(
        default=None
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
class ObliqueStatic(IdsBaseClass):
    """
    Description of a 2D parallelogram.

    :ivar r: Major radius of the reference point (from which the alpha
        and beta angles are defined, marked by a + on the diagram)
    :ivar z: Height of the reference point (from which the alpha and
        beta angles are defined, marked by a + on the diagram)
    :ivar length_alpha: Length of the parallelogram side inclined with
        angle alpha with respect to the major radius axis
    :ivar length_beta: Length of the parallelogram side inclined with
        angle beta with respect to the height axis
    :ivar alpha: Inclination of first angle measured counter-clockwise
        from horizontal outwardly directed radial vector (grad R).
    :ivar beta: Inclination of second angle measured counter-clockwise
        from vertically upwards directed vector (grad Z). If both alpha
        and beta are zero (rectangle) then the simpler rectangular
        elements description should be used.
    """
    class Meta:
        name = "oblique_static"

    r: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )
    length_alpha: float = field(
        default=9e+40
    )
    length_beta: float = field(
        default=9e+40
    )
    alpha: float = field(
        default=9e+40
    )
    beta: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class RectangleStatic(IdsBaseClass):
    """
    Rectangular description of a 2D object.

    :ivar r: Geometric centre R
    :ivar z: Geometric centre Z
    :ivar width: Horizontal full width
    :ivar height: Vertical full height
    """
    class Meta:
        name = "rectangle_static"

    r: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )
    width: float = field(
        default=9e+40
    )
    height: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class Rz0DConstant(IdsBaseClass):
    """
    Structure for a single R, Z position (0D, constant)

    :ivar r: Major radius
    :ivar z: Height
    """
    class Meta:
        name = "rz0d_constant"

    r: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class Rz0DStatic(IdsBaseClass):
    """
    Structure for a single R, Z position (0D, static)

    :ivar r: Major radius
    :ivar z: Height
    """
    class Meta:
        name = "rz0d_static"

    r: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class Rz1DStatic(IdsBaseClass):
    """
    Structure for list of R, Z positions (1D, constant)

    :ivar r: Major radius
    :ivar z: Height
    """
    class Meta:
        name = "rz1d_static"

    r: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    z: Optional[ndarray[(int,), float]] = field(
        default=None
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
class SignalFlt1D(IdsBaseClass):
    """
    Signal (FLT_1D) with its time base.

    :ivar time: Time
    """
    class Meta:
        name = "signal_flt_1d"

    time: Optional[str] = field(
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
class SignalFlt1DUnitsLevel2(IdsBaseClass):
    """
    Signal (FLT_1D) with its time base, data units 2 levels above.

    :ivar time: Time
    """
    class Meta:
        name = "signal_flt_1d_units_level_2"

    time: Optional[str] = field(
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
class IcAntennasMatchingElement(IdsBaseClass):
    """
    Matching element.

    :ivar name: Name
    :ivar type: Type of the matching element. Index = 1 : capacitor
        (fill capacitance); Index = 2 : stub (fill phase)
    :ivar capacitance: Capacitance of the macthing element
    :ivar phase: Phase delay induced by the stub
    """
    class Meta:
        name = "ic_antennas_matching_element"

    name: str = field(
        default=""
    )
    type: Optional[IdentifierStatic] = field(
        default=None
    )
    capacitance: Optional[SignalFlt1D] = field(
        default=None
    )
    phase: Optional[SignalFlt1D] = field(
        default=None
    )


@dataclass(slots=True)
class IcAntennasMeasurement(IdsBaseClass):
    """
    Voltage or current measurement.

    :ivar name: Name
    :ivar identifier: Identifier
    :ivar position: Position of the measurement
    :ivar amplitude: Amplitude of the measurement
    :ivar phase: Phase of the measurement
    """
    class Meta:
        name = "ic_antennas_measurement"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    position: Optional[Rzphi0DStatic] = field(
        default=None
    )
    amplitude: Optional[SignalFlt1DUnitsLevel2] = field(
        default=None
    )
    phase: Optional[SignalFlt1D] = field(
        default=None
    )


@dataclass(slots=True)
class ThickLineStatic(IdsBaseClass):
    """
    2D contour approximated by two points and a thickness (in the direction
    perpendicular to the segment) in the poloidal cross-section.

    :ivar first_point: Position of the first point
    :ivar second_point: Position of the second point
    :ivar thickness: Thickness
    """
    class Meta:
        name = "thick_line_static"

    first_point: Optional[Rz0DStatic] = field(
        default=None
    )
    second_point: Optional[Rz0DStatic] = field(
        default=None
    )
    thickness: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class Outline2DGeometryStatic(IdsBaseClass):
    """
    Description of 2D geometry.

    :ivar geometry_type: Type used to describe the element shape
        (1:'outline', 2:'rectangle', 3:'oblique', 4:'arcs of circle, 5:
        'annulus', 6 : 'thick line')
    :ivar outline: Irregular outline of the element. Do NOT repeat the
        first point.
    :ivar rectangle: Rectangular description of the element
    :ivar oblique: Parallelogram description of the element
    :ivar arcs_of_circle: Description of the element contour by a set of
        arcs of circle. For each of these, the position of the start
        point is given together with the curvature radius. The end point
        is given by the start point of the next arc of circle.
    :ivar annulus: The element is an annulus of centre R, Z, with inner
        radius radius_inner and outer radius radius_outer
    :ivar thick_line: The element is approximated by a rectangle defined
        by a central segment and a thickness in the direction
        perpendicular to the segment
    """
    class Meta:
        name = "outline_2d_geometry_static"

    geometry_type: int = field(
        default=999999999
    )
    outline: Optional[Rz1DStatic] = field(
        default=None
    )
    rectangle: Optional[RectangleStatic] = field(
        default=None
    )
    oblique: Optional[ObliqueStatic] = field(
        default=None
    )
    arcs_of_circle: Optional[ArcsOfCircleStatic] = field(
        default=None
    )
    annulus: Optional[AnnulusStatic] = field(
        default=None
    )
    thick_line: Optional[ThickLineStatic] = field(
        default=None
    )


@dataclass(slots=True)
class IcAntennasStrap(IdsBaseClass):
    """
    Properties of IC antenna strap.

    :ivar outline: Strap outline
    :ivar width_tor: Width of strap in the toroidal direction
    :ivar distance_to_conductor: Distance to conducting wall or other
        conductor behind the antenna strap
    :ivar geometry: Cross-sectional shape of the strap
    :ivar current: Root mean square current flowing along the strap
    :ivar phase: Phase of the strap current
    """
    class Meta:
        name = "ic_antennas_strap"

    outline: Optional[Rzphi1DStatic] = field(
        default=None
    )
    width_tor: float = field(
        default=9e+40
    )
    distance_to_conductor: float = field(
        default=9e+40
    )
    geometry: Optional[Outline2DGeometryStatic] = field(
        default=None
    )
    current: Optional[SignalFlt1D] = field(
        default=None
    )
    phase: Optional[SignalFlt1D] = field(
        default=None
    )


@dataclass(slots=True)
class IcAntennasAntennaModule(IdsBaseClass):
    """
    Module of an IC antenna.

    :ivar name: Name of the module
    :ivar identifier: Identifier of the module
    :ivar frequency: Frequency
    :ivar power_launched: Power launched from this module into the
        vacuum vessel
    :ivar power_forward: Forward power arriving to the back of the
        module
    :ivar power_reflected: Reflected power
    :ivar reflection_coefficient: Power reflection coefficient
    :ivar phase_forward: Phase of the forward power with respect to the
        first module
    :ivar phase_reflected: Phase of the reflected power with respect to
        the forward power of this module
    :ivar voltage: Set of voltage measurements
    :ivar current: Set of current measurements
    :ivar pressure: Set of pressure measurements
    :ivar matching_element: Set of matching elements
    :ivar strap: Set of IC antenna straps
    """
    class Meta:
        name = "ic_antennas_antenna_module"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    frequency: Optional[SignalFlt1D] = field(
        default=None
    )
    power_launched: Optional[SignalFlt1D] = field(
        default=None
    )
    power_forward: Optional[SignalFlt1D] = field(
        default=None
    )
    power_reflected: Optional[SignalFlt1D] = field(
        default=None
    )
    reflection_coefficient: Optional[SignalFlt1D] = field(
        default=None
    )
    phase_forward: Optional[SignalFlt1D] = field(
        default=None
    )
    phase_reflected: Optional[SignalFlt1D] = field(
        default=None
    )
    voltage: list[IcAntennasMeasurement] = field(
        default_factory=list,
        metadata={
            "max_occurs": 10,
        }
    )
    current: list[IcAntennasMeasurement] = field(
        default_factory=list,
        metadata={
            "max_occurs": 10,
        }
    )
    pressure: list[IcAntennasMeasurement] = field(
        default_factory=list,
        metadata={
            "max_occurs": 10,
        }
    )
    matching_element: list[IcAntennasMatchingElement] = field(
        default_factory=list,
        metadata={
            "max_occurs": 10,
        }
    )
    strap: list[IcAntennasStrap] = field(
        default_factory=list,
        metadata={
            "max_occurs": 10,
        }
    )


@dataclass(slots=True)
class IcAntennasAntenna(IdsBaseClass):
    """
    Ion Cyclotron Antenna.

    :ivar name: Name of the antenna (unique within the set of all
        antennas of the experiment)
    :ivar identifier: Identifier of the antenna (unique within the set
        of all antennas of the experiment)
    :ivar frequency: Frequency (average over modules)
    :ivar power_launched: Power launched from this antenna into the
        vacuum vessel
    :ivar power_forward: Forward power arriving to the back of the
        antenna
    :ivar power_reflected: Reflected power
    :ivar module: Set of antenna modules (each module is fed by a single
        transmission line)
    :ivar surface_current: Description of the IC surface current on the
        antenna straps and on passive components, for every time slice
    """
    class Meta:
        name = "ic_antennas_antenna"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    frequency: Optional[SignalFlt1D] = field(
        default=None
    )
    power_launched: Optional[SignalFlt1D] = field(
        default=None
    )
    power_forward: Optional[SignalFlt1D] = field(
        default=None
    )
    power_reflected: Optional[SignalFlt1D] = field(
        default=None
    )
    module: list[IcAntennasAntennaModule] = field(
        default_factory=list,
        metadata={
            "max_occurs": 8,
        }
    )
    surface_current: list[IcAntennasSurfaceCurrent] = field(
        default_factory=list
    )


@dataclass(slots=True)
class IcAntennas(IdsBaseClass):
    """
    Antenna systems for heating and current drive in the ion cyclotron (IC)
    frequencies.

    :ivar ids_properties:
    :ivar reference_point: Reference point used to define the poloidal
        angle, e.g. the geometrical centre of the vacuum vessel. Used to
        define the poloidal mode numbers under antenna/surface_current
    :ivar antenna: Set of Ion Cyclotron antennas
    :ivar power_launched: Power launched into the vacuum vessel by the
        whole ICRH system (sum over antennas)
    :ivar latency: Upper bound of the delay between input command
        received from the RT network and actuator starting to react.
        Applies globally to the system described by this IDS unless
        specific latencies (e.g. channel-specific or antenna-specific)
        are provided at a deeper level in the IDS structure.
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "ic_antennas"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    reference_point: Optional[Rz0DConstant] = field(
        default=None
    )
    antenna: list[IcAntennasAntenna] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    power_launched: Optional[SignalFlt1D] = field(
        default=None
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
