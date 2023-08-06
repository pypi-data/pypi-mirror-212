#__version__='0.3.1'
#__imas_commit__='dd6854b4d07'
#__imas_version__='3.7.1'
from ..dataclasses_idsschema import IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


@dataclass(slots=True)
class Identifier(IdsBaseClass):
    """Standard type for identifiers (constant).

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
        name = "identifier"

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
class SignalInt1D(IdsBaseClass):
    """
    Signal (INT_1D) with its time base.

    :ivar time: Time
    """
    class Meta:
        name = "signal_int_1d"

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
            default="INT_1D"
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
class LineOfSight3Points(IdsBaseClass):
    """
    Generic description of a line of sight, defined by two points (one way) and an
    optional third point to indicate the direction of reflection if the second
    point is e.g. the position of a mirror reflecting the line-of-sight.

    :ivar first_point: Position of the first point
    :ivar second_point: Position of the second point
    :ivar third_point: Position of the third point
    """
    class Meta:
        name = "line_of_sight_3points"

    first_point: Optional[Rzphi0DStatic] = field(
        default=None
    )
    second_point: Optional[Rzphi0DStatic] = field(
        default=None
    )
    third_point: Optional[Rzphi0DStatic] = field(
        default=None
    )


@dataclass(slots=True)
class PulseScheduleEvent(IdsBaseClass):
    """
    Event.

    :ivar type: Type of this event
    :ivar identifier: Unique identifier of this event provided by the
        scheduling / event handler
    :ivar time_stamp: Time stamp of this event
    :ivar duration: Duration of this event
    :ivar acquisition_strategy: Acquisition strategy related to this
        event: index = 1 : on-trigger; index = 2 : pre-trigger; index =
        3 : post-trigger
    :ivar acquisition_state: Acquisition state of the related system :
        index = 1 : armed; index = 2 : on; index = 3 : off; index = 4 :
        closed
    :ivar provider: System having generated this event
    :ivar listeners: Systems listening to this event
    """
    class Meta:
        name = "pulse_schedule_event"

    type: Optional[Identifier] = field(
        default=None
    )
    identifier: str = field(
        default=""
    )
    time_stamp: float = field(
        default=9e+40
    )
    duration: float = field(
        default=9e+40
    )
    acquisition_strategy: Optional[Identifier] = field(
        default=None
    )
    acquisition_state: Optional[Identifier] = field(
        default=None
    )
    provider: str = field(
        default=""
    )
    listeners: Optional[list[str]] = field(
        default=None
    )


@dataclass(slots=True)
class PulseScheduleReference(IdsBaseClass):
    """General structure for pulse schedule reference.

    NB: we propose to use the automatically generated reference/data_error_upper and reference/data_error_lower nodes to describe the upper of lower bound of the envelope of the waveform, since they almost have the same meaning and are already set on the same time base as reference/data.

    :ivar reference_name: Reference name (e.g. in the native pulse
        schedule system of the device)
    :ivar reference: Reference waveform. Caution : error bars of the
        reference/data node are not used in the usual sense, instead
        they are used to describe the control envelope, with a meaning
        depending on the chosen envelope_type option.
    :ivar reference_type: Reference type:  0:relative (don't use for the
        moment, to be defined later when segments are introduced in the
        IDS structure); 1: absolute: the reference time trace is
        provided in the reference/data node
    :ivar envelope_type: Envelope type:  0:relative: means that the
        envelope upper and lower bound values are defined respectively
        as reference.data * reference.data_error_upper and
        reference.data * reference.data_error_lower. 1: absolute: the
        envelope upper and lower bound values are given respectively by
        reference/data_error_upper and reference/data_error_lower. Lower
        are upper are taken in the strict mathematical sense, without
        considering absolute values of the data
    """
    class Meta:
        name = "pulse_schedule_reference"

    reference_name: str = field(
        default=""
    )
    reference: Optional[SignalFlt1D] = field(
        default=None
    )
    reference_type: int = field(
        default=999999999
    )
    envelope_type: int = field(
        default=999999999
    )


@dataclass(slots=True)
class PulseScheduleDensityControlIon(IdsBaseClass):
    """
    References for ion species.

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge
    :ivar label: String identifying ion (e.g. H, D, T, He, C, D2, ...)
    :ivar n_i_volume_average: Volume averaged ion density (average over
        the plasma volume up to the LCFS)
    """
    class Meta:
        name = "pulse_schedule_density_control_ion"

    element: list[PlasmaCompositionNeutralElementConstant] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    z_ion: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    n_i_volume_average: Optional[PulseScheduleReference] = field(
        default=None
    )


@dataclass(slots=True)
class PulseScheduleDensityControlValve(IdsBaseClass):
    """
    Gas injection valve.

    :ivar name: Name of the valve
    :ivar identifier: Identifier of the valve
    :ivar flow_rate: Flow rate of the valve
    :ivar species: Species injected by the valve (may be more than one
        in case the valve injects a gas mixture)
    """
    class Meta:
        name = "pulse_schedule_density_control_valve"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    flow_rate: Optional[PulseScheduleReference] = field(
        default=None
    )
    species: list[GasMixtureConstant] = field(
        default_factory=list,
        metadata={
            "max_occurs": 3,
        }
    )


@dataclass(slots=True)
class PulseScheduleEcAntenna(IdsBaseClass):
    """
    EC antenna.

    :ivar name: Name of the launcher
    :ivar identifier: Identifier of the launcher
    :ivar power: Power launched from this launcher into the vacuum
        vessel
    :ivar frequency: Frequency
    :ivar deposition_rho_tor_norm: Normalised toroidal flux coordinate
        at which the main deposition should occur
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
    """
    class Meta:
        name = "pulse_schedule_ec_antenna"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    power: Optional[PulseScheduleReference] = field(
        default=None
    )
    frequency: Optional[PulseScheduleReference] = field(
        default=None
    )
    deposition_rho_tor_norm: Optional[PulseScheduleReference] = field(
        default=None
    )
    steering_angle_pol: Optional[PulseScheduleReference] = field(
        default=None
    )
    steering_angle_tor: Optional[PulseScheduleReference] = field(
        default=None
    )


@dataclass(slots=True)
class PulseScheduleFluxControl(IdsBaseClass):
    """
    Flux control references.

    :ivar i_plasma: Plasma current
    :ivar loop_voltage: Loop voltage
    :ivar li_3: Internal inductance
    :ivar beta_normal: Normalised toroidal beta, defined as 100 *
        beta_tor * a[m] * B0 [T] / ip [MA]
    :ivar mode: Control mode (operation mode and/or settings used by the
        controller)
    """
    class Meta:
        name = "pulse_schedule_flux_control"

    i_plasma: Optional[PulseScheduleReference] = field(
        default=None
    )
    loop_voltage: Optional[PulseScheduleReference] = field(
        default=None
    )
    li_3: Optional[PulseScheduleReference] = field(
        default=None
    )
    beta_normal: Optional[PulseScheduleReference] = field(
        default=None
    )
    mode: Optional[SignalInt1D] = field(
        default=None
    )


@dataclass(slots=True)
class PulseScheduleGap(IdsBaseClass):
    """
    Gap for describing the plasma boundary.

    :ivar name: Name of the gap
    :ivar identifier: Identifier of the gap
    :ivar r: Major radius of the reference point
    :ivar z: Height of the reference point
    :ivar angle: Angle between the direction in which the gap is
        measured (in the poloidal cross-section) and the horizontal
        axis.
    :ivar value: Value of the gap, i.e. distance between the reference
        point and the separatrix along the gap direction
    """
    class Meta:
        name = "pulse_schedule_gap"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    r: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )
    angle: float = field(
        default=9e+40
    )
    value: Optional[PulseScheduleReference] = field(
        default=None
    )


@dataclass(slots=True)
class PulseScheduleIcAntenna(IdsBaseClass):
    """
    IC antenna.

    :ivar name: Name of the antenna
    :ivar identifier: Identifier of the antenna
    :ivar power_type: Type of power used in the sibling power node
        (defining which power is referred to in this pulse_schedule).
        Index = 1: power_launched, 2: power_forward (see definitions in
        the ic_antennas  IDS)
    :ivar power: Power
    :ivar phase: Phase
    :ivar frequency: Frequency
    """
    class Meta:
        name = "pulse_schedule_ic_antenna"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    power_type: Optional[IdentifierStatic] = field(
        default=None
    )
    power: Optional[PulseScheduleReference] = field(
        default=None
    )
    phase: Optional[PulseScheduleReference] = field(
        default=None
    )
    frequency: Optional[PulseScheduleReference] = field(
        default=None
    )


@dataclass(slots=True)
class PulseScheduleLhAntenna(IdsBaseClass):
    """
    LH antenna.

    :ivar name: Name of the antenna
    :ivar identifier: Identifier of the antenna
    :ivar power_type: Type of power used in the sibling power node
        (defining which power is referred to in this pulse_schedule).
        Index = 1: power_launched, 2: power_forward (see definitions in
        the lh_antennas  IDS)
    :ivar power: Power
    :ivar phase: Phasing between neighbour waveguides (in the toroidal
        direction)
    :ivar n_parallel: Main parallel refractive index of the injected
        wave power spectrum
    :ivar frequency: Frequency
    """
    class Meta:
        name = "pulse_schedule_lh_antenna"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    power_type: Optional[IdentifierStatic] = field(
        default=None
    )
    power: Optional[PulseScheduleReference] = field(
        default=None
    )
    phase: Optional[PulseScheduleReference] = field(
        default=None
    )
    n_parallel: Optional[PulseScheduleReference] = field(
        default=None
    )
    frequency: Optional[PulseScheduleReference] = field(
        default=None
    )


@dataclass(slots=True)
class PulseScheduleNbiUnit(IdsBaseClass):
    """
    NBI unit.

    :ivar name: Name of the NBI unit
    :ivar identifier: Identifier of the NBI unit
    :ivar species: Species injected by the NBI unit (may be more than
        one in case the unit injects a gas mixture)
    :ivar power: Power launched from this unit into the vacuum vessel
    :ivar energy: Full energy of the injected species (acceleration of a
        single atom)
    """
    class Meta:
        name = "pulse_schedule_nbi_unit"

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
    power: Optional[PulseScheduleReference] = field(
        default=None
    )
    energy: Optional[PulseScheduleReference] = field(
        default=None
    )


@dataclass(slots=True)
class PulseScheduleOutline(IdsBaseClass):
    """
    RZ outline.

    :ivar r: Major radius
    :ivar z: Height
    """
    class Meta:
        name = "pulse_schedule_outline"

    r: Optional[PulseScheduleReference] = field(
        default=None
    )
    z: Optional[PulseScheduleReference] = field(
        default=None
    )


@dataclass(slots=True)
class PulseSchedulePfActiveCoil(IdsBaseClass):
    """
    PF coil.

    :ivar name: Name of the coil
    :ivar identifier: Identifier of the coil
    :ivar current: Current fed in the coil (for 1 turn, to be multiplied
        by the number of turns to obtain the generated magnetic field),
        positive when flowing from side 1 to side 2 of the coil (inside
        the coil), this numbering being made consistently with the
        convention that the current is counter-clockwise when seen from
        above.
    :ivar resistance_additional: Additional resistance due to e.g.
        dynamically switchable resistors
    """
    class Meta:
        name = "pulse_schedule_pf_active_coil"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    current: Optional[PulseScheduleReference] = field(
        default=None
    )
    resistance_additional: Optional[PulseScheduleReference] = field(
        default=None
    )


@dataclass(slots=True)
class PulseSchedulePfActiveSupply(IdsBaseClass):
    """
    PF supply.

    :ivar name: Name of the supply
    :ivar identifier: Identifier of the supply
    :ivar voltage: Voltage at the supply output (Vside1-Vside2)
    """
    class Meta:
        name = "pulse_schedule_pf_active_supply"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    voltage: Optional[PulseScheduleReference] = field(
        default=None
    )


@dataclass(slots=True)
class PulseScheduleRz(IdsBaseClass):
    """
    R,Z position.

    :ivar r: Major radius
    :ivar z: Height
    """
    class Meta:
        name = "pulse_schedule_rz"

    r: Optional[PulseScheduleReference] = field(
        default=None
    )
    z: Optional[PulseScheduleReference] = field(
        default=None
    )


@dataclass(slots=True)
class PulseScheduleTf(IdsBaseClass):
    """
    Toroidal field references.

    :ivar b_field_tor_vacuum_r: Vacuum field times major radius in the
        toroidal field magnet. Positive sign means anti-clockwise when
        viewed from above
    :ivar mode: Control mode (operation mode and/or settings used by the
        controller)
    """
    class Meta:
        name = "pulse_schedule_tf"

    b_field_tor_vacuum_r: Optional[PulseScheduleReference] = field(
        default=None
    )
    mode: Optional[SignalInt1D] = field(
        default=None
    )


@dataclass(slots=True)
class PulseScheduleDensityControl(IdsBaseClass):
    """
    Gas injection system.

    :ivar valve: Set of injection valves. Time-dependent
    :ivar n_e_line: Line integrated electron density
    :ivar n_e_line_method: Method for n_e_line calculation : Index = 1:
        integral over a line of sight in the whole vacuum chamber, 2 :
        integral over a line of sight within the LCFS, 3 : integral of a
        1D core profile over rho_tor_norm up to the LCFS
    :ivar n_e_line_of_sight: Description of the line of sight for
        calculating n_e, defined by two points when the beam is not
        reflected, a third point is added to define the reflected beam
        path
    :ivar n_e_volume_average: Volume averaged electron density (average
        over the plasma volume up to the LCFS)
    :ivar zeff: Line averaged effective charge
    :ivar zeff_method: Method for zeff calculation : Index = 1: average
        over a line of sight in the whole vacuum chamber, 2 : average
        over a line of sight within the LCFS, 3 : average of a 1D core
        profile over rho_tor_norm up to the LCFS
    :ivar zeff_line_of_sight: Description of the line of sight for
        calculating zeff, defined by two points when the beam is not
        reflected, a third point is added to define the reflected beam
        path
    :ivar n_t_over_n_d: Average ratio of tritium over deuterium density
    :ivar n_h_over_n_d: Average ratio of hydrogen over deuterium density
    :ivar mode: Control mode (operation mode and/or settings used by the
        controller)
    :ivar ion: Quantities related to the different ion species, in the
        sense of isonuclear or isomolecular sequences
    """
    class Meta:
        name = "pulse_schedule_density_control"

    valve: list[PulseScheduleDensityControlValve] = field(
        default_factory=list,
        metadata={
            "max_occurs": 20,
        }
    )
    n_e_line: Optional[PulseScheduleReference] = field(
        default=None
    )
    n_e_line_method: Optional[IdentifierStatic] = field(
        default=None
    )
    n_e_line_of_sight: Optional[LineOfSight3Points] = field(
        default=None
    )
    n_e_volume_average: Optional[PulseScheduleReference] = field(
        default=None
    )
    zeff: Optional[PulseScheduleReference] = field(
        default=None
    )
    zeff_method: Optional[IdentifierStatic] = field(
        default=None
    )
    zeff_line_of_sight: Optional[LineOfSight3Points] = field(
        default=None
    )
    n_t_over_n_d: Optional[PulseScheduleReference] = field(
        default=None
    )
    n_h_over_n_d: Optional[PulseScheduleReference] = field(
        default=None
    )
    mode: Optional[SignalInt1D] = field(
        default=None
    )
    ion: list[PulseScheduleDensityControlIon] = field(
        default_factory=list,
        metadata={
            "max_occurs": 20,
        }
    )


@dataclass(slots=True)
class PulseScheduleEc(IdsBaseClass):
    """
    Electron cyclotron heating and current drive system.

    :ivar launcher: Set of ECRH launchers
    :ivar mode: Control mode (operation mode and/or settings used by the
        controller)
    :ivar power: Total EC power (sum over the launchers)
    """
    class Meta:
        name = "pulse_schedule_ec"

    launcher: list[PulseScheduleEcAntenna] = field(
        default_factory=list,
        metadata={
            "max_occurs": 10,
        }
    )
    mode: Optional[SignalInt1D] = field(
        default=None
    )
    power: Optional[PulseScheduleReference] = field(
        default=None
    )


@dataclass(slots=True)
class PulseScheduleIc(IdsBaseClass):
    """
    Ion cyclotron heating and current drive system.

    :ivar antenna: Set of ICRH antennas
    :ivar mode: Control mode (operation mode and/or settings used by the
        controller)
    """
    class Meta:
        name = "pulse_schedule_ic"

    antenna: list[PulseScheduleIcAntenna] = field(
        default_factory=list,
        metadata={
            "max_occurs": 3,
        }
    )
    mode: Optional[SignalInt1D] = field(
        default=None
    )


@dataclass(slots=True)
class PulseScheduleLh(IdsBaseClass):
    """
    Lower hybrid heating and current drive system.

    :ivar antenna: Set of LH antennas
    :ivar mode: Control mode (operation mode and/or settings used by the
        controller)
    """
    class Meta:
        name = "pulse_schedule_lh"

    antenna: list[PulseScheduleLhAntenna] = field(
        default_factory=list,
        metadata={
            "max_occurs": 3,
        }
    )
    mode: Optional[SignalInt1D] = field(
        default=None
    )


@dataclass(slots=True)
class PulseScheduleNbi(IdsBaseClass):
    """
    Neutral beam heating and current drive system.

    :ivar unit: Set of NBI units
    :ivar mode: Control mode (operation mode and/or settings used by the
        controller)
    :ivar power: Total NBI power (sum over the units)
    """
    class Meta:
        name = "pulse_schedule_nbi"

    unit: list[PulseScheduleNbiUnit] = field(
        default_factory=list,
        metadata={
            "max_occurs": 36,
        }
    )
    mode: Optional[SignalInt1D] = field(
        default=None
    )
    power: Optional[PulseScheduleReference] = field(
        default=None
    )


@dataclass(slots=True)
class PulseSchedulePfActive(IdsBaseClass):
    """
    PF coils references.

    :ivar coil: Set of poloidal field coils
    :ivar supply: Set of PF power supplies
    :ivar mode: Control mode (operation mode and/or settings used by the
        controller)
    """
    class Meta:
        name = "pulse_schedule_pf_active"

    coil: list[PulseSchedulePfActiveCoil] = field(
        default_factory=list,
        metadata={
            "max_occurs": 32,
        }
    )
    supply: list[PulseSchedulePfActiveSupply] = field(
        default_factory=list,
        metadata={
            "max_occurs": 32,
        }
    )
    mode: Optional[SignalInt1D] = field(
        default=None
    )


@dataclass(slots=True)
class PulseSchedulePosition(IdsBaseClass):
    """
    Flux control references.

    :ivar magnetic_axis: Magnetic axis position
    :ivar geometric_axis: RZ position of the geometric axis (defined as
        (Rmin+Rmax) / 2 and (Zmin+Zmax) / 2 of the boundary)
    :ivar minor_radius: Minor radius of the plasma boundary (defined as
        (Rmax-Rmin) / 2 of the boundary)
    :ivar elongation: Elongation of the plasma boundary
    :ivar elongation_upper: Elongation (upper half w.r.t. geometric
        axis) of the plasma boundary
    :ivar elongation_lower: Elongation (lower half w.r.t. geometric
        axis) of the plasma boundary
    :ivar triangularity: Triangularity of the plasma boundary
    :ivar triangularity_upper: Upper triangularity of the plasma
        boundary
    :ivar triangularity_lower: Lower triangularity of the plasma
        boundary
    :ivar x_point: Array of X-points, for each of them the RZ position
        is given
    :ivar strike_point: Array of strike points, for each of them the RZ
        position is given
    :ivar active_limiter_point: RZ position of the active limiter point
        (point of the plasma boundary in contact with the limiter)
    :ivar boundary_outline: Set of (R,Z) points defining the outline of
        the plasma boundary
    :ivar gap: Set of gaps, defined by a reference point and a
        direction.
    :ivar mode: Control mode (operation mode and/or settings used by the
        controller)
    """
    class Meta:
        name = "pulse_schedule_position"

    magnetic_axis: Optional[PulseScheduleRz] = field(
        default=None
    )
    geometric_axis: Optional[PulseScheduleRz] = field(
        default=None
    )
    minor_radius: Optional[PulseScheduleReference] = field(
        default=None
    )
    elongation: Optional[PulseScheduleReference] = field(
        default=None
    )
    elongation_upper: Optional[PulseScheduleReference] = field(
        default=None
    )
    elongation_lower: Optional[PulseScheduleReference] = field(
        default=None
    )
    triangularity: Optional[PulseScheduleReference] = field(
        default=None
    )
    triangularity_upper: Optional[PulseScheduleReference] = field(
        default=None
    )
    triangularity_lower: Optional[PulseScheduleReference] = field(
        default=None
    )
    x_point: list[PulseScheduleRz] = field(
        default_factory=list,
        metadata={
            "max_occurs": 2,
        }
    )
    strike_point: list[PulseScheduleRz] = field(
        default_factory=list,
        metadata={
            "max_occurs": 4,
        }
    )
    active_limiter_point: Optional[PulseScheduleRz] = field(
        default=None
    )
    boundary_outline: list[PulseScheduleOutline] = field(
        default_factory=list,
        metadata={
            "max_occurs": 301,
        }
    )
    gap: list[PulseScheduleGap] = field(
        default_factory=list,
        metadata={
            "max_occurs": 51,
        }
    )
    mode: Optional[SignalInt1D] = field(
        default=None
    )


@dataclass(slots=True)
class PulseSchedule(IdsBaseClass):
    """Description of Pulse Schedule, described by subsystems waveform references
    and an enveloppe around them.

    The controllers, pulse schedule and SDN are defined in separate
    IDSs. All names and identifiers of subsystems appearing in the
    pulse_schedule must be identical to those used in the IDSs
    describing the related subsystems.

    :ivar ids_properties:
    :ivar ic: Ion cyclotron heating and current drive system
    :ivar ec: Electron cyclotron heating and current drive system
    :ivar lh: Lower Hybrid heating and current drive system
    :ivar nbi: Neutral beam heating and current drive system
    :ivar density_control: Gas injection system and density control
        references
    :ivar event: List of events, either predefined triggers  or events
        recorded during the pulse
    :ivar flux_control: Magnetic flux control references
    :ivar pf_active: Poloidal field coil references
    :ivar position_control: Plasma position and shape control references
    :ivar tf: Toroidal field references
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "pulse_schedule"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    ic: Optional[PulseScheduleIc] = field(
        default=None
    )
    ec: Optional[PulseScheduleEc] = field(
        default=None
    )
    lh: Optional[PulseScheduleLh] = field(
        default=None
    )
    nbi: Optional[PulseScheduleNbi] = field(
        default=None
    )
    density_control: Optional[PulseScheduleDensityControl] = field(
        default=None
    )
    event: list[PulseScheduleEvent] = field(
        default_factory=list,
        metadata={
            "max_occurs": 130,
        }
    )
    flux_control: Optional[PulseScheduleFluxControl] = field(
        default=None
    )
    pf_active: Optional[PulseSchedulePfActive] = field(
        default=None
    )
    position_control: Optional[PulseSchedulePosition] = field(
        default=None
    )
    tf: Optional[PulseScheduleTf] = field(
        default=None
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
