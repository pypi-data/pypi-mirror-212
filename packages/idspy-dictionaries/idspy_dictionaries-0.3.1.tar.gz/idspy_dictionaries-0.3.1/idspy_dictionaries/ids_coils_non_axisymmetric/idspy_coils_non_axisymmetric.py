#__version__='0.3.1'
#__imas_commit__='dd6854b4d07'
#__imas_version__='3.7.1'
from ..dataclasses_idsschema import IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


@dataclass(slots=True)
class DeltaRzphi1DStatic(IdsBaseClass):
    """
    Structure for R, Z, Phi relative positions (1D, static)

    :ivar delta_r: Major radii (relative to a reference point)
    :ivar delta_z: Heights (relative to a reference point)
    :ivar delta_phi: Toroidal angles (relative to a reference point)
    """
    class Meta:
        name = "delta_rzphi1d_static"

    delta_r: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    delta_z: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    delta_phi: Optional[ndarray[(int,), float]] = field(
        default=None
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
class CoilConductorElements(IdsBaseClass):
    """
    Elements descibring the conductor contour.

    :ivar names: Name or description of every element
    :ivar types: Type of every element: 1: line segment, its ends are
        given by the start and end points; index = 2: arc of a circle;
        index = 3: full circle
    :ivar start_points: Position of the start point of every element
    :ivar intermediate_points: Position of an intermediate point along
        the arc of circle, for every element, providing the orientation
        of the element (must define with the corresponding start point
        an aperture angle strictly inferior to PI). Meaningful only if
        type/index = 2, fill with default/empty value otherwise
    :ivar end_points: Position of the end point of every element.
        Meaningful only if type/index = 1 or 2, fill with default/empty
        value otherwise
    :ivar centres: Position of the centre of the arc of a circle of
        every element (meaningful only if type/index = 2 or 3, fill with
        default/empty value otherwise)
    """
    class Meta:
        name = "coil_conductor_elements"

    names: Optional[list[str]] = field(
        default=None
    )
    types: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    start_points: Optional[Rzphi1DStatic] = field(
        default=None
    )
    intermediate_points: Optional[Rzphi1DStatic] = field(
        default=None
    )
    end_points: Optional[Rzphi1DStatic] = field(
        default=None
    )
    centres: Optional[Rzphi1DStatic] = field(
        default=None
    )


@dataclass(slots=True)
class CoilConductor(IdsBaseClass):
    """
    Description of a conductor.

    :ivar elements: Set of geometrical elements (line segments and/or
        arcs of a circle) describing the contour of the conductor centre
    :ivar cross_section: The cross-section perpendicular to the
        conductor contour is described by a series of contour points,
        given by their relative position with respect to the start point
        of the first element. This cross-section is assumed constant for
        all elements.
    :ivar resistance: conductor resistance
    :ivar current: Current in the conductor (positive when it flows from
        the first to the last element)
    :ivar voltage: Voltage on the conductor terminals
    """
    class Meta:
        name = "coil_conductor"

    elements: Optional[CoilConductorElements] = field(
        default=None
    )
    cross_section: Optional[DeltaRzphi1DStatic] = field(
        default=None
    )
    resistance: float = field(
        default=9e+40
    )
    current: Optional[SignalFlt1D] = field(
        default=None
    )
    voltage: Optional[SignalFlt1D] = field(
        default=None
    )


@dataclass(slots=True)
class Coil(IdsBaseClass):
    """
    Description of a given coil.

    :ivar name: Name of the coil
    :ivar identifier: Alphanumeric identifier of coil
    :ivar conductor: Set of conductors inside the coil. The structure
        can be used with size 1 for a simplified description as a single
        conductor. A conductor is composed of several elements, serially
        connected, i.e. transporting the same current.
    :ivar turns: Number of total turns in the coil. May be a fraction
        when describing the coil connections.
    :ivar resistance: Coil resistance
    :ivar current: Current in one turn of the coil (to be multiplied by
        the number of turns to calculate the magnetic field generated).
        Sign convention : a positive current generates a positive radial
        magnetic field
    :ivar voltage: Voltage on the coil terminals. Sign convention : a
        positive power supply voltage (and power supply current)
        generates a positive radial magnetic field
    """
    class Meta:
        name = "coil"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    conductor: list[CoilConductor] = field(
        default_factory=list,
        metadata={
            "max_occurs": 20,
        }
    )
    turns: float = field(
        default=9e+40
    )
    resistance: float = field(
        default=9e+40
    )
    current: Optional[SignalFlt1D] = field(
        default=None
    )
    voltage: Optional[SignalFlt1D] = field(
        default=None
    )


@dataclass(slots=True)
class CoilsNonAxisymmetric(IdsBaseClass):
    """
    Non axisymmetric active coils system (e.g. ELM control coils, error field
    correction coils, ...)

    :ivar ids_properties:
    :ivar coil: Set of coils
    :ivar latency: Upper bound of the delay between input command
        received from the RT network and actuator starting to react.
        Applies globally to the system described by this IDS unless
        specific latencies (e.g. channel-specific or antenna-specific)
        are provided at a deeper level in the IDS structure.
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "coils_non_axisymmetric"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    coil: list[Coil] = field(
        default_factory=list,
        metadata={
            "max_occurs": 32,
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
