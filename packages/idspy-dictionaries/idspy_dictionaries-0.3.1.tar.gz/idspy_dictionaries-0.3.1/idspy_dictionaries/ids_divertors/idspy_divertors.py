#__version__='0.3.1'
#__imas_commit__='dd6854b4d07'
#__imas_version__='3.7.1'
from ..dataclasses_idsschema import IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


@dataclass(slots=True)
class DivertorTargetTwoPointModel(IdsBaseClass):
    """
    Two point model for a given divertor target.

    :ivar t_e_target: Electron temperature at divertor target
    :ivar n_e_target: Electron density at divertor target
    :ivar sol_heat_decay_length: Heat flux decay length in SOL at
        divertor entrance, mapped to the mid-plane, this is the lambda_q
        parameter defined in reference T. Eich et al, Nucl. Fusion 53
        (2013) 093031
    :ivar sol_heat_spreading_length: Heat flux spreading length in SOL
        at equatorial mid-plane, this is the S power spreading parameter
        defined in reference T. Eich et al, Nucl. Fusion 53 (2013)
        093031. Relevant only for attached plasmas.
    :ivar time: Time
    """
    class Meta:
        name = "divertor_target_two_point_model"

    t_e_target: float = field(
        default=9e+40
    )
    n_e_target: float = field(
        default=9e+40
    )
    sol_heat_decay_length: float = field(
        default=9e+40
    )
    sol_heat_spreading_length: float = field(
        default=9e+40
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
class DivertorTargetTile(IdsBaseClass):
    """
    Divertor tile description.

    :ivar name: Name of the tile
    :ivar identifier: Alphanumeric identifier of tile
    :ivar surface_outline: Outline of the tile surface facing the plasma
    :ivar surface_area: Area of the tile surface facing the plasma
    :ivar current_incident: Total current incident on this tile
    :ivar shunt_index: If the tile carries a measurement shunt, index of
        that shunt (in the magnetics IDS shunt array)
    """
    class Meta:
        name = "divertor_target_tile"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    surface_outline: Optional[Rzphi1DStatic] = field(
        default=None
    )
    surface_area: float = field(
        default=9e+40
    )
    current_incident: Optional[SignalFlt1D] = field(
        default=None
    )
    shunt_index: int = field(
        default=999999999
    )


@dataclass(slots=True)
class DivertorTarget(IdsBaseClass):
    """
    Divertor target description.

    :ivar name: Name of the target
    :ivar identifier: Alphanumeric identifier of target
    :ivar heat_flux_steady_limit_max: Maximum steady state heat flux
        allowed on divertor target surface (engineering design limit)
    :ivar temperature_limit_max: Maximum surface target temperature
        allowed to prevent damage (melting, recrystallization,
        sublimation, etc...)
    :ivar t_e_target_sputtering_limit_max: Maximum plasma temperature
        allowed on the divertor target to avoid excessive sputtering
    :ivar power_flux_peak: Peak power flux on the divertor target
        surface
    :ivar flux_expansion: Magnetic flux expansion as defined by Stangeby
        : ratio between the poloidal field at the midplane separatrix
        and the poloidal field at the strike-point see formula attached,
        where u means upstream (midplane separatrix) and t means at
        divertor target (downstream).
    :ivar two_point_model: Description of SOL according to the two point
        model, the downstream point being on this target, for various
        time slices
    :ivar tilt_angle_pol: Angle between field lines projected in
        poloidal plane and target, measured clockwise from the target to
        the projected field lines
    :ivar extension_r: Target length projected on the major radius axis
    :ivar extension_z: Target length projected on the height axis
    :ivar wetted_area: Wetted area of the target, defined by the SOL
        heat flux decay length (lambda_q) mapped to the target using
        flux expansion and spreading factor and the target toroidal
        circumference. In other words, this is the area getting heat
        flux from the maximum value down to one e-fold decay.
    :ivar power_incident_fraction: Power fraction incident on the target
        (normalized to the total power incident on the divertor)
    :ivar power_incident: Total power incident on this target. This
        power is split in the various physical categories listed below
    :ivar power_conducted: Power conducted by the plasma on this
        divertor target
    :ivar power_convected: Power convected by the plasma on this
        divertor target
    :ivar power_radiated: Net radiated power on this divertor target
        (incident - reflected)
    :ivar power_black_body: Black body radiated power emitted from this
        divertor target (emissivity is included)
    :ivar power_neutrals: Net power from neutrals on this divertor
        target (positive means power is deposited on the target)
    :ivar power_recombination_plasma: Power deposited on this divertor
        target due to recombination of plasma ions
    :ivar power_recombination_neutrals: Power deposited on this divertor
        target due to recombination of neutrals into a ground state
        (e.g. molecules)
    :ivar power_currents: Power deposited on this divertor target due to
        electric currents (positive means power is deposited on the
        target)
    :ivar current_incident: Total current incident on this target
    :ivar tile: Set of divertor tiles belonging to this target
    """
    class Meta:
        name = "divertor_target"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    heat_flux_steady_limit_max: float = field(
        default=9e+40
    )
    temperature_limit_max: float = field(
        default=9e+40
    )
    t_e_target_sputtering_limit_max: float = field(
        default=9e+40
    )
    power_flux_peak: Optional[SignalFlt1D] = field(
        default=None
    )
    flux_expansion: Optional[SignalFlt1D] = field(
        default=None
    )
    two_point_model: list[DivertorTargetTwoPointModel] = field(
        default_factory=list
    )
    tilt_angle_pol: Optional[SignalFlt1D] = field(
        default=None
    )
    extension_r: float = field(
        default=9e+40
    )
    extension_z: float = field(
        default=9e+40
    )
    wetted_area: Optional[SignalFlt1D] = field(
        default=None
    )
    power_incident_fraction: Optional[SignalFlt1D] = field(
        default=None
    )
    power_incident: Optional[SignalFlt1D] = field(
        default=None
    )
    power_conducted: Optional[SignalFlt1D] = field(
        default=None
    )
    power_convected: Optional[SignalFlt1D] = field(
        default=None
    )
    power_radiated: Optional[SignalFlt1D] = field(
        default=None
    )
    power_black_body: Optional[SignalFlt1D] = field(
        default=None
    )
    power_neutrals: Optional[SignalFlt1D] = field(
        default=None
    )
    power_recombination_plasma: Optional[SignalFlt1D] = field(
        default=None
    )
    power_recombination_neutrals: Optional[SignalFlt1D] = field(
        default=None
    )
    power_currents: Optional[SignalFlt1D] = field(
        default=None
    )
    current_incident: Optional[SignalFlt1D] = field(
        default=None
    )
    tile: list[DivertorTargetTile] = field(
        default_factory=list,
        metadata={
            "max_occurs": 100,
        }
    )


@dataclass(slots=True)
class Divertor(IdsBaseClass):
    """
    Divertor description.

    :ivar name: Name of the divertor
    :ivar identifier: Alphanumeric identifier of divertor
    :ivar target: Set of divertor targets
    :ivar wetted_area: Wetted area of the divertor (sum over all
        targets)
    :ivar power_incident: Total power incident on the divertor (sum over
        all targets). This power is split in the various physical
        categories listed below
    :ivar power_conducted: Power conducted by the plasma on the divertor
        targets (sum over all targets)
    :ivar power_convected: Power convected by the plasma on the divertor
        targets (sum over all targets)
    :ivar power_radiated: Net radiated power on the divertor targets
        (incident - reflected) (sum over all targets)
    :ivar power_black_body: Black body radiated power emitted from the
        divertor targets (emissivity is included) (sum over all targets)
    :ivar power_neutrals: Net power from neutrals on the divertor
        targets (positive means power is deposited on the target) (sum
        over all targets)
    :ivar power_recombination_plasma: Power deposited on the divertor
        targets due to recombination of plasma ions (sum over all
        targets)
    :ivar power_recombination_neutrals: Power deposited on the divertor
        targets due to recombination of neutrals into a ground state
        (e.g. molecules) (sum over all targets)
    :ivar power_currents: Power deposited on the divertor targets due to
        electric currents (positive means power is deposited on the
        target) (sum over all targets)
    :ivar particle_flux_recycled_total: Total recycled particle flux
        from  the divertor (in equivalent electrons)
    :ivar current_incident: Total current incident on this divertor
    """
    class Meta:
        name = "divertor"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    target: list[DivertorTarget] = field(
        default_factory=list,
        metadata={
            "max_occurs": 6,
        }
    )
    wetted_area: Optional[SignalFlt1D] = field(
        default=None
    )
    power_incident: Optional[SignalFlt1D] = field(
        default=None
    )
    power_conducted: Optional[SignalFlt1D] = field(
        default=None
    )
    power_convected: Optional[SignalFlt1D] = field(
        default=None
    )
    power_radiated: Optional[SignalFlt1D] = field(
        default=None
    )
    power_black_body: Optional[SignalFlt1D] = field(
        default=None
    )
    power_neutrals: Optional[SignalFlt1D] = field(
        default=None
    )
    power_recombination_plasma: Optional[SignalFlt1D] = field(
        default=None
    )
    power_recombination_neutrals: Optional[SignalFlt1D] = field(
        default=None
    )
    power_currents: Optional[SignalFlt1D] = field(
        default=None
    )
    particle_flux_recycled_total: Optional[SignalFlt1D] = field(
        default=None
    )
    current_incident: Optional[SignalFlt1D] = field(
        default=None
    )


@dataclass(slots=True)
class Divertors(IdsBaseClass):
    """
    Description of divertors.

    :ivar ids_properties:
    :ivar midplane: Choice of midplane definition (use the lowest index
        number if more than one value is relevant)
    :ivar divertor: Set of divertors
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "divertors"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    midplane: Optional[IdentifierStatic] = field(
        default=None
    )
    divertor: list[Divertor] = field(
        default_factory=list,
        metadata={
            "max_occurs": 8,
        }
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
