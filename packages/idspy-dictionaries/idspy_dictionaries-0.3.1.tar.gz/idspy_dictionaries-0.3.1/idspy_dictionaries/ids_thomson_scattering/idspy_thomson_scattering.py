#__version__='0.3.1'
#__imas_commit__='dd6854b4d07'
#__imas_version__='3.7.1'
from ..dataclasses_idsschema import IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


@dataclass(slots=True)
class DataEntry(IdsBaseClass):
    """
    Definition of a data entry.

    :ivar user: Username
    :ivar machine: Name of the experimental device to which this data is
        related
    :ivar pulse_type: Type of the data entry, e.g. "pulse",
        "simulation", ...
    :ivar pulse: Pulse number
    :ivar run: Run number
    """
    class Meta:
        name = "data_entry"

    user: str = field(
        default=""
    )
    machine: str = field(
        default=""
    )
    pulse_type: str = field(
        default=""
    )
    pulse: int = field(
        default=999999999
    )
    run: int = field(
        default=999999999
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
class Rzphi1DDynamicAos1CommonTime(IdsBaseClass):
    """
    Structure for R, Z, Phi positions (1D, dynamic within a type 1 array of
    structure and with a common time base at the same level)

    :ivar r: Major radius
    :ivar z: Height
    :ivar phi: Toroidal angle
    :ivar time: Time for the R,Z,phi coordinates
    """
    class Meta:
        name = "rzphi1d_dynamic_aos1_common_time"

    r: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    z: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    phi: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    time: Optional[str] = field(
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
class IdsIdentification(IdsBaseClass):
    """
    Identifier of an IDS.

    :ivar name: IDS name
    :ivar occurrence: IDS occurrence
    :ivar data_entry: Data entry to which this IDS belongs
    """
    class Meta:
        name = "ids_identification"

    name: str = field(
        default=""
    )
    occurrence: int = field(
        default=999999999
    )
    data_entry: Optional[DataEntry] = field(
        default=None
    )


@dataclass(slots=True)
class ThomsonScatteringChannel(IdsBaseClass):
    """
    Thomson scattering channel.

    :ivar name: Name of the channel
    :ivar identifier: ID of the channel
    :ivar position: Average position of the measurements (intersection
        between laser beam and line of sight)
    :ivar delta_position: Incremental variation of the position of the
        measurements, due to e.g. different lasers not intersecting the
        line of sight at the same position. The actual position is then
        the static position + delta_position
    :ivar distance_separatrix_midplane: Distance between the measurement
        position and the separatrix, mapped along flux surfaces to the
        outboard midplane, in the major radius direction. Positive value
        means the measurement is outside of the separatrix.
    :ivar t_e: Electron temperature
    :ivar n_e: Electron density
    """
    class Meta:
        name = "thomson_scattering_channel"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    position: Optional[Rzphi0DStatic] = field(
        default=None
    )
    delta_position: Optional[Rzphi1DDynamicAos1CommonTime] = field(
        default=None
    )
    distance_separatrix_midplane: Optional[SignalFlt1D] = field(
        default=None
    )
    t_e: Optional[SignalFlt1D] = field(
        default=None
    )
    n_e: Optional[SignalFlt1D] = field(
        default=None
    )


@dataclass(slots=True)
class ThomsonScattering(IdsBaseClass):
    """
    Thomson scattering diagnostic.

    :ivar ids_properties:
    :ivar equilibrium_id: ID of the IDS equilibrium used to map
        measurements - we may decide that this is superseeded when the
        systematic documentation of input provenance is adopted
    :ivar midplane: Choice of midplane definition for the mapping of
        measurements on an equilibrium
    :ivar channel: Set of channels (lines-of-sight)
    :ivar latency: Upper bound of the delay between physical information
        received by the detector and data available on the real-time
        (RT) network.
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "thomson_scattering"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    equilibrium_id: Optional[IdsIdentification] = field(
        default=None
    )
    midplane: Optional[IdentifierStatic] = field(
        default=None
    )
    channel: list[ThomsonScatteringChannel] = field(
        default_factory=list,
        metadata={
            "max_occurs": 150,
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
