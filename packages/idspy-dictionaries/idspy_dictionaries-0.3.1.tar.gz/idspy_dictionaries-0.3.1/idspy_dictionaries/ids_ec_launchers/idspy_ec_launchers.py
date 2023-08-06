#__version__='0.3.1'
#__imas_commit__='dd6854b4d07'
#__imas_version__='3.7.1'
from ..dataclasses_idsschema import IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


@dataclass(slots=True)
class EcLaunchersBeamPhase(IdsBaseClass):
    """
    Phase ellipse characteristics.

    :ivar curvature: Inverse curvature radii for the phase ellipse,
        positive/negative for divergent/convergent beams
    :ivar angle: Rotation angle for the phase ellipse
    """
    class Meta:
        name = "ec_launchers_beam_phase"

    curvature: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    angle: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class EcLaunchersBeamSpot(IdsBaseClass):
    """
    Spot ellipse characteristics.

    :ivar size: Size of the spot ellipse
    :ivar angle: Rotation angle for the spot ellipse
    """
    class Meta:
        name = "ec_launchers_beam_spot"

    size: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    angle: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class EcLaunchersLaunchingPosition(IdsBaseClass):
    """
    Structure for R, Z, Phi positions and min max values of R (1D, dynamic within a
    type 1 array of structure and with a common time base at the same level)

    :ivar r: Major radius
    :ivar r_limit_min: Major radius lower limit for the system
    :ivar r_limit_max: Major radius upper limit for the system
    :ivar z: Height
    :ivar phi: Toroidal angle
    """
    class Meta:
        name = "ec_launchers_launching_position"

    r: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    r_limit_min: float = field(
        default=9e+40
    )
    r_limit_max: float = field(
        default=9e+40
    )
    z: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    phi: Optional[ndarray[(int,), float]] = field(
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
class EcLaunchersBeam(IdsBaseClass):
    """
    Electron Cyclotron beam.

    :ivar name: Beam name
    :ivar identifier: Beam identifier
    :ivar frequency: Frequency
    :ivar power_launched: Beam power launched into the vacuum vessel
    :ivar mode: Identifier for the main plasma wave mode excited by the
        EC beam. For the ordinary mode (O-mode), mode=1. For the
        extraordinary mode (X-mode), mode=-1
    :ivar launching_position: Launching position of the beam
    :ivar steering_angle_pol: Steering angle of the EC beam in the R,Z
        plane (from the -R axis towards the -Z axis),
        angle_pol=atan2(-k_Z,-k_R), where k_Z and k_R are the Z and R
        components of the mean wave vector in the EC beam
    :ivar steering_angle_tor: Steering angle of the EC beam away from
        the poloidal plane that is increasing towards the positive phi
        axis, angle_tor=arcsin(k_phi/k), where k_phi is the component of
        the wave vector in the phi direction and k is the length of the
        wave vector. Here the term wave vector refers to the mean wave
        vector in the EC beam
    :ivar spot: Spot ellipse characteristics
    :ivar phase: Phase ellipse characteristics
    :ivar time: Time base used for position, angle, spot and phase
        quantities
    """
    class Meta:
        name = "ec_launchers_beam"

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
    mode: int = field(
        default=999999999
    )
    launching_position: Optional[EcLaunchersLaunchingPosition] = field(
        default=None
    )
    steering_angle_pol: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    steering_angle_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    spot: Optional[EcLaunchersBeamSpot] = field(
        default=None
    )
    phase: Optional[EcLaunchersBeamPhase] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )


@dataclass(slots=True)
class EcLaunchers(IdsBaseClass):
    """
    Launchers for heating and current drive in the electron cyclotron (EC)
    frequencies.

    :ivar ids_properties:
    :ivar beam: Set of Electron Cyclotron beams
    :ivar latency: Upper bound of the delay between input command
        received from the RT network and actuator starting to react.
        Applies globally to the system described by this IDS unless
        specific latencies (e.g. channel-specific or antenna-specific)
        are provided at a deeper level in the IDS structure.
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "ec_launchers"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    beam: list[EcLaunchersBeam] = field(
        default_factory=list,
        metadata={
            "max_occurs": 100,
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
