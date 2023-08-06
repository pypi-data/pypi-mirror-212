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
class MagneticsBpolProbeNonLinear(IdsBaseClass):
    """
    Non-linear response of the probe.

    :ivar b_field_linear: Array of magnetic field values (corresponding
        to the assumption of a linear relation between magnetic field
        and probe coil current), for each of which the probe non-linear
        response is given in ../b_field_non_linear
    :ivar b_field_non_linear: Magnetic field value taking into account
        the non-linear response of the probe
    """
    class Meta:
        name = "magnetics_bpol_probe_non_linear"

    b_field_linear: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    b_field_non_linear: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class MagneticsMethodDistinct(IdsBaseClass):
    """
    Processed quantities derived from the magnetic measurements, using various
    methods.

    :ivar method_name: Name of the calculation method
    :ivar time: Time
    """
    class Meta:
        name = "magnetics_method_distinct"

    method_name: str = field(
        default=""
    )
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
class SignalFlt1DValidity(IdsBaseClass):
    """
    Signal (FLT_1D) with its time base and validity flags.

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
    :ivar time: Time
    """
    class Meta:
        name = "signal_flt_1d_validity"

    validity_timed: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    validity: int = field(
        default=999999999
    )
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
class LineOfSight2PointsRz(IdsBaseClass):
    """
    Generic description of a line of sight, defined by two points, in R and Z only.

    :ivar first_point: Position of the first point
    :ivar second_point: Position of the second point
    """
    class Meta:
        name = "line_of_sight_2points_rz"

    first_point: Optional[Rz0DStatic] = field(
        default=None
    )
    second_point: Optional[Rz0DStatic] = field(
        default=None
    )


@dataclass(slots=True)
class MagneticsBpolProbe(IdsBaseClass):
    """
    Poloidal field probes.

    :ivar name: Name of the probe
    :ivar identifier: ID of the probe
    :ivar type: Probe type
    :ivar position: R, Z, Phi position of the coil centre
    :ivar poloidal_angle: Angle of the sensor normal vector (vector
        parallel to the the axis of the coil, n on the diagram) with
        respect to horizontal plane (clockwise theta-like angle). Zero
        if sensor normal vector fully in the horizontal plane and
        oriented towards increasing major radius. Values in [0 , 2Pi]
    :ivar toroidal_angle: Angle of the projection of the sensor normal
        vector (n) in the horizontal plane with the increasing R
        direction (i.e. grad(R)) (angle is counter-clockwise from above
        as in cocos=11 phi-like angle). Values should be taken modulo pi
        with values within (-pi/2,pi/2]. Zero if projected sensor normal
        is parallel to grad(R), pi/2 if it is parallel to grad(phi).
    :ivar indices_differential: Indices (from the bpol_probe array of
        structure) of the two probes used to build the field difference
        field(second index) - field(first index). Use only if
        ../type/index = 6, leave empty otherwise
    :ivar bandwidth_3db: 3dB bandwith (first index : lower frequency
        bound, second index : upper frequency bound)
    :ivar area: Area of each turn of the sensor; becomes effective area
        when multiplied by the turns
    :ivar length: Length of the sensor along it's normal vector (n)
    :ivar turns: Turns in the coil, including sign
    :ivar field_value: Magnetic field component in direction of sensor
        normal axis (n) averaged over sensor volume defined by area and
        length, where n =
        cos(poloidal_angle)*cos(toroidal_angle)*grad(R) -
        sin(poloidal_angle)*grad(Z) +
        cos(poloidal_angle)*sin(toroidal_angle)*grad(Phi)/norm(grad(Phi))
    :ivar voltage: Voltage on the coil terminals
    :ivar non_linear_response: Non-linear response of the probe
        (typically in case of a Hall probe)
    """
    class Meta:
        name = "magnetics_bpol_probe"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    type: Optional[IdentifierStatic] = field(
        default=None
    )
    position: Optional[Rzphi0DStatic] = field(
        default=None
    )
    poloidal_angle: float = field(
        default=9e+40
    )
    toroidal_angle: float = field(
        default=9e+40
    )
    indices_differential: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    bandwidth_3db: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    area: float = field(
        default=9e+40
    )
    length: float = field(
        default=9e+40
    )
    turns: int = field(
        default=999999999
    )
    field_value: Optional[SignalFlt1DValidity] = field(
        default=None
    )
    voltage: Optional[SignalFlt1DValidity] = field(
        default=None
    )
    non_linear_response: Optional[MagneticsBpolProbeNonLinear] = field(
        default=None
    )


@dataclass(slots=True)
class MagneticsFluxLoop(IdsBaseClass):
    """
    Flux loops.

    :ivar name: Name of the flux loop
    :ivar identifier: ID of the flux loop
    :ivar type: Flux loop type
    :ivar position: List of (R,Z,phi) points defining the position of
        the loop (see data structure documentation FLUXLOOPposition.pdf)
    :ivar indices_differential: Indices (from the flux_loop array of
        structure) of the two flux loops used to build the flux
        difference flux(second index) - flux(first index). Use only if
        ../type/index = 6, leave empty otherwise
    :ivar area: Effective area (ratio between flux and average magnetic
        field over the loop)
    :ivar gm9: Integral of 1/R over the loop area (ratio between flux
        and magnetic rigidity R0.B0). Use only if ../type/index = 3 to
        6, leave empty otherwise.
    :ivar flux: Measured magnetic flux over loop in which Z component of
        normal to loop is directed downwards (negative grad Z direction)
    :ivar voltage: Measured voltage between the loop terminals
    """
    class Meta:
        name = "magnetics_flux_loop"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    type: Optional[IdentifierStatic] = field(
        default=None
    )
    position: list[Rzphi0DStatic] = field(
        default_factory=list,
        metadata={
            "max_occurs": 10,
        }
    )
    indices_differential: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    area: float = field(
        default=9e+40
    )
    gm9: float = field(
        default=9e+40
    )
    flux: Optional[SignalFlt1DValidity] = field(
        default=None
    )
    voltage: Optional[SignalFlt1DValidity] = field(
        default=None
    )


@dataclass(slots=True)
class MagneticsMethod(IdsBaseClass):
    """
    Processed quantities derived from the magnetic measurements, using various
    methods.

    :ivar name: Name of the data processing method
    :ivar ip: Plasma current. Positive sign means anti-clockwise when
        viewed from above.
    """
    class Meta:
        name = "magnetics_method"

    name: str = field(
        default=""
    )
    ip: Optional[SignalFlt1D] = field(
        default=None
    )


@dataclass(slots=True)
class MagneticsRogowski(IdsBaseClass):
    """
    Rogowski coil.

    :ivar name: Name of the coil
    :ivar identifier: ID of the coil
    :ivar measured_quantity: Quantity measured by the sensor
    :ivar position: List of (R,Z,phi) points defining the position of
        the coil guiding centre
    :ivar indices_compound: Indices (from the rogowski_coil array of
        structure) of the partial Rogoswkis used to build the coumpound
        signal (sum of the partial Rogoswki signals) Use only if
        ../measure_quantity/index = 5, leave empty otherwise
    :ivar area: Effective area of the loop wrapped around the guiding
        centre. In case of multiple layers, sum of the areas of each
        layer
    :ivar turns_per_metre: Number of turns per unit length. In case of
        multiple layers, turns are counted for a single layer
    :ivar current: Measured current inside the Rogowski coil contour.
        The normal direction to the Rogowski coil is defined by the
        order of points in the list of guiding centre positions. The
        current is positive when oriented in the same direction as the
        normal.
    """
    class Meta:
        name = "magnetics_rogowski"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    measured_quantity: Optional[IdentifierStatic] = field(
        default=None
    )
    position: list[Rzphi0DStatic] = field(
        default_factory=list,
        metadata={
            "max_occurs": 100,
        }
    )
    indices_compound: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    area: float = field(
        default=9e+40
    )
    turns_per_metre: float = field(
        default=9e+40
    )
    current: Optional[SignalFlt1DValidity] = field(
        default=None
    )


@dataclass(slots=True)
class MagneticsShunt(IdsBaseClass):
    """
    Shunt for current measurement (often located in the divertor structure)

    :ivar name: Name of the shunt
    :ivar identifier: Alphanumeric identifier of the shunt
    :ivar position: Position of shunt terminals
    :ivar resistance: Shunt resistance
    :ivar voltage: Voltage on the shunt terminals (Vfirst_point-
        Vsecond_point)
    :ivar divertor_index: If the shunt is located on a given divertor,
        index of that divertor in the divertors IDS
    :ivar target_index: If the shunt is located on a divertor target,
        index of that target in the divertors IDS
    :ivar tile_index: If the shunt is located on a divertor tile, index
        of that tile in the divertors IDS
    """
    class Meta:
        name = "magnetics_shunt"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    position: Optional[LineOfSight2PointsRz] = field(
        default=None
    )
    resistance: float = field(
        default=9e+40
    )
    voltage: Optional[SignalFlt1DValidity] = field(
        default=None
    )
    divertor_index: int = field(
        default=999999999
    )
    target_index: int = field(
        default=999999999
    )
    tile_index: int = field(
        default=999999999
    )


@dataclass(slots=True)
class Magnetics(IdsBaseClass):
    """
    Magnetic diagnostics for equilibrium identification and plasma shape control.

    :ivar ids_properties:
    :ivar flux_loop: Flux loops; partial flux loops can be described
    :ivar bpol_probe: Poloidal field probes
    :ivar b_field_pol_probe: Poloidal field probes
    :ivar b_field_tor_probe: Toroidal field probes
    :ivar rogowski_coil: Set of Rogowski coils
    :ivar shunt: Set of shunt resistances through which currents in the
        divertor structure are measured. Shunts are modelled as
        piecewise straight line segments in the poloidal plane.
    :ivar method: A method generating processed quantities derived from
        the magnetic measurements
    :ivar ip: Plasma current. Positive sign means anti-clockwise when
        viewed from above. The array of structure corresponds to a set
        of calculation methods (starting with the generally recommended
        method).
    :ivar diamagnetic_flux: Diamagnetic flux. The array of structure
        corresponds to a set of calculation methods (starting with the
        generally recommended method).
    :ivar latency: Upper bound of the delay between physical information
        received by the detector and data available on the real-time
        (RT) network.
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "magnetics"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    flux_loop: list[MagneticsFluxLoop] = field(
        default_factory=list,
        metadata={
            "max_occurs": 200,
        }
    )
    bpol_probe: list[MagneticsBpolProbe] = field(
        default_factory=list,
        metadata={
            "max_occurs": 200,
        }
    )
    b_field_pol_probe: list[MagneticsBpolProbe] = field(
        default_factory=list,
        metadata={
            "max_occurs": 200,
        }
    )
    b_field_tor_probe: list[MagneticsBpolProbe] = field(
        default_factory=list,
        metadata={
            "max_occurs": 20,
        }
    )
    rogowski_coil: list[MagneticsRogowski] = field(
        default_factory=list,
        metadata={
            "max_occurs": 20,
        }
    )
    shunt: list[MagneticsShunt] = field(
        default_factory=list,
        metadata={
            "max_occurs": 50,
        }
    )
    method: list[MagneticsMethod] = field(
        default_factory=list,
        metadata={
            "max_occurs": 10,
        }
    )
    ip: list[MagneticsMethodDistinct] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    diamagnetic_flux: list[MagneticsMethodDistinct] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
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
