#__version__='0.3.1'
#__imas_commit__='dd6854b4d07'
#__imas_version__='3.7.1'
from ..dataclasses_idsschema import IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


@dataclass(slots=True)
class GasInjectionValveResponse(IdsBaseClass):
    """
    Gas injection valve response curve.

    :ivar voltage: Voltage applied to open the valve
    :ivar flow_rate: Flow rate at the exit of the valve
    """
    class Meta:
        name = "gas_injection_valve_response"

    voltage: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    flow_rate: Optional[ndarray[(int,), float]] = field(
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
class PlasmaCompositionNeutralElementConstant(IdsBaseClass):
    """
    Element entering in the composition of the neutral atom or molecule (constant)

    :ivar a: Mass of atom
    :ivar z_n: Nuclear charge
    :ivar atoms_n: Number of atoms of this element in the molecule
    :ivar multiplicity: Multiplicity of the atom
    """
    class Meta:
        name = "plasma_composition_neutral_element_constant"

    a: float = field(
        default=9e+40
    )
    z_n: float = field(
        default=9e+40
    )
    atoms_n: int = field(
        default=999999999
    )
    multiplicity: float = field(
        default=9e+40
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
class GasMixtureConstant(IdsBaseClass):
    """
    Description of a neutral species within a gas mixture (constant)

    :ivar element: List of elements forming the atom or molecule
    :ivar label: String identifying neutral (e.g. H, D, T, He, C, ...)
    :ivar fraction: Relative fraction of this species (in molecules) in
        the gas mixture
    """
    class Meta:
        name = "gas_mixture_constant"

    element: list[PlasmaCompositionNeutralElementConstant] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    label: str = field(
        default=""
    )
    fraction: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class GasInjectionPipe(IdsBaseClass):
    """
    Gas injection pipe.

    :ivar name: Name of the injection pipe
    :ivar identifier: ID of the injection pipe
    :ivar species: Species injected by the pipe (may be more than one in
        case the valve injects a gas mixture)
    :ivar length: Pipe length
    :ivar exit_position: Exit position of the pipe in the vaccum vessel
    :ivar second_point: Second point indicating (combined with the
        exit_position) the direction of the gas injection towards the
        plasma
    :ivar flow_rate: Flow rate at the exit of the pipe
    :ivar valve_indices: Indices (from the ../../valve array of
        structure) of the valve(s) that are feeding this pipe
    """
    class Meta:
        name = "gas_injection_pipe"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    species: list[GasMixtureConstant] = field(
        default_factory=list,
        metadata={
            "max_occurs": 3,
        }
    )
    length: float = field(
        default=9e+40
    )
    exit_position: Optional[Rzphi0DStatic] = field(
        default=None
    )
    second_point: Optional[Rzphi0DStatic] = field(
        default=None
    )
    flow_rate: Optional[SignalFlt1D] = field(
        default=None
    )
    valve_indices: Optional[ndarray[(int,), int]] = field(
        default=None
    )


@dataclass(slots=True)
class GasInjectionPipeValve(IdsBaseClass):
    """
    Gas injection valve.

    :ivar name: Name of the valve
    :ivar identifier: ID of the valve
    :ivar species: Species injected by the valve (may be more than one
        in case the valve injects a gas mixture)
    :ivar flow_rate_min: Minimum flow rate of the valve
    :ivar flow_rate_max: Maximum flow rate of the valve
    :ivar flow_rate: Flow rate at the exit of the valve
    :ivar electron_rate: Number of electrons injected per second
    :ivar pipe_indices: Indices (from the ../../pipe array of structure)
        of the pipe(s) that are fed by this valve
    :ivar voltage: Voltage applied to open the valve (raw data used to
        compute the gas flow rate)
    :ivar response_curve: Response curve of the valve, i.e. gas flow
        rate obtained as a function of the applied voltage.
    """
    class Meta:
        name = "gas_injection_pipe_valve"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    species: list[GasMixtureConstant] = field(
        default_factory=list,
        metadata={
            "max_occurs": 3,
        }
    )
    flow_rate_min: float = field(
        default=9e+40
    )
    flow_rate_max: float = field(
        default=9e+40
    )
    flow_rate: Optional[SignalFlt1D] = field(
        default=None
    )
    electron_rate: Optional[SignalFlt1D] = field(
        default=None
    )
    pipe_indices: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    voltage: Optional[SignalFlt1D] = field(
        default=None
    )
    response_curve: Optional[GasInjectionValveResponse] = field(
        default=None
    )


@dataclass(slots=True)
class GasInjection(IdsBaseClass):
    """
    Gas injection by a system of pipes and valves.

    :ivar ids_properties:
    :ivar pipe: Set of gas injection pipes
    :ivar valve: Set of valves connecting a gas bottle to pipes
    :ivar latency: Upper bound of the delay between input command
        received from the RT network and actuator starting to react.
        Applies globally to the system described by this IDS unless
        specific latencies (e.g. channel-specific or antenna-specific)
        are provided at a deeper level in the IDS structure.
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "gas_injection"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    pipe: list[GasInjectionPipe] = field(
        default_factory=list,
        metadata={
            "max_occurs": 20,
        }
    )
    valve: list[GasInjectionPipeValve] = field(
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
