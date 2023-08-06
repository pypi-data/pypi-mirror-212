#__version__='0.3.1'
#__imas_commit__='dd6854b4d07'
#__imas_version__='3.7.1'
from ..dataclasses_idsschema import IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


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
class PhysicalQuantityFlt1DTime1(IdsBaseClass):
    """Similar to a signal (FLT_1D) but with time base one level above (NB : since this is described in the utilities section, the timebase must be directly below the closest AoS)

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
        name = "physical_quantity_flt_1d_time_1"

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
            default="FLT_1D"
        )


@dataclass(slots=True)
class PsiNormalization(IdsBaseClass):
    """
    Quantities used to normalize psi, as a function of time.

    :ivar psi_magnetic_axis: Value of the poloidal magnetic flux at the
        magnetic axis
    :ivar psi_boundary: Value of the poloidal magnetic flux at the
        plasma boundary
    :ivar time: Time for the R,Z,phi coordinates
    """
    class Meta:
        name = "psi_normalization"

    psi_magnetic_axis: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    psi_boundary: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    time: Optional[str] = field(
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
class Rzphirhopsitheta1DDynamicAos1CommonTime1(IdsBaseClass):
    """
    Structure for list of R, Z, Phi, rho_tor_norm, psi, theta positions (1D,
    dynamic within a type 1 array of structures, assuming a common time array one
    level above.

    :ivar r: Major radius
    :ivar z: Height
    :ivar phi: Toroidal angle  (oriented counter-clockwise when viewing
        from above)
    :ivar psi: Poloidal flux
    :ivar rho_tor_norm: Normalised toroidal flux coordinate
    :ivar theta: Poloidal angle (oriented clockwise when viewing the
        poloidal cross section on the right hand side of the tokamak
        axis of symmetry, with the origin placed on the plasma magnetic
        axis)
    """
    class Meta:
        name = "rzphirhopsitheta1d_dynamic_aos1_common_time_1"

    r: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    z: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    phi: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    psi: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    rho_tor_norm: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    theta: Optional[ndarray[(int,), float]] = field(
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
class SignalFlt1DValidityPosition(IdsBaseClass):
    """
    Signal (FLT_1D) with its time base and validity flags and rho_tor_norm
    position.

    :ivar rho_tor_norm: Normalised toroidal flux coordinate of the
        measurement
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
        name = "signal_flt_1d_validity_position"

    rho_tor_norm: Optional[ndarray[(int,), float]] = field(
        default=None
    )
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
class SignalFlt2D(IdsBaseClass):
    """
    Signal (FLT_2D) with its time base.

    :ivar time: Time
    """
    class Meta:
        name = "signal_flt_2d"

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
            default="FLT_2D"
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
class EceChannelBeamPhase(IdsBaseClass):
    """
    Phase ellipse characteristics.

    :ivar curvature: Inverse curvature radii for the phase ellipse,
        positive/negative for divergent/convergent beams
    :ivar angle: Rotation angle for the phase ellipse
    """
    class Meta:
        name = "ece_channel_beam_phase"

    curvature: Optional[SignalFlt2D] = field(
        default=None
    )
    angle: Optional[SignalFlt1D] = field(
        default=None
    )


@dataclass(slots=True)
class EceChannelBeamSpot(IdsBaseClass):
    """
    Spot ellipse characteristics.

    :ivar size: Size of the spot ellipse
    :ivar angle: Rotation angle for the spot ellipse
    """
    class Meta:
        name = "ece_channel_beam_spot"

    size: Optional[SignalFlt2D] = field(
        default=None
    )
    angle: Optional[SignalFlt1D] = field(
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
class Polarizer(IdsBaseClass):
    """
    Generic description of a polarizer (extension of the detector_aperture complex
    type)

    :ivar centre: If geometry_type=2, coordinates of the centre of the
        circle. If geometry_type=1 or 3, coordinates of the origin of
        the local coordinate system (X1,X2,X3) describing the plane
        polarizer. This origin is located within the polarizer area.
        Note that there is some flexibility here and the data provider
        should choose the most convenient coordinate system for the
        object, respecting the definitions of (X1,X2,X3) indicated
        below.
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
        the height axis. The X3 axis is normal to the polarizer plane
        and oriented towards the plasma.
    :ivar polarization_angle: Alignment angle of the polarizer in the
        (x1,x2) plane. Electric fields parallel to the polarizer angle
        will be reflected. The angle is defined with respect to the x1
        unit vector, positive in the counter-clockwise direction when
        looking towards the plasma
    """
    class Meta:
        name = "polarizer"

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
    polarization_angle: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class EceChannelBeam(IdsBaseClass):
    """
    Beam characteristics.

    :ivar spot: Spot ellipse characteristics
    :ivar phase: Phase ellipse characteristics
    """
    class Meta:
        name = "ece_channel_beam"

    spot: Optional[EceChannelBeamSpot] = field(
        default=None
    )
    phase: Optional[EceChannelBeamPhase] = field(
        default=None
    )


@dataclass(slots=True)
class EceChannel(IdsBaseClass):
    """
    Charge exchange channel.

    :ivar name: Name of the channel
    :ivar identifier: ID of the channel
    :ivar frequency: Frequency of the channel
    :ivar harmonic: Harmonic detected by the channel. 1 corresponds to
        the "O1" mode, while 2 corresponds to the "X2" mode.
    :ivar if_bandwidth: Full-width of the Intermediate Frequency (IF)
        bandpass filter
    :ivar position: Position of the measurements (taking into account
        the suprathermal shift)
    :ivar delta_position_suprathermal: Simple estimate of the difference
        in position induced by the presence of suprathermal electrons.
        Position without corrections = position -
        delta_position_suprathermal
    :ivar t_e: Electron temperature
    :ivar t_e_voltage: Raw voltage measured on each channel, from which
        the calibrated temperature data is then derived
    :ivar optical_depth: Optical depth of the plasma at the position of
        the measurement. This parameter is a proxy for the local / non-
        local character of the ECE emission. It must be greater than 1
        to guarantee that the measurement is dominated by local ECE
        emission (non-local otherwise)
    :ivar time: Timebase for the processed dynamic data of this channel
        (outside of the beam structure)
    :ivar beam: ECE Gaussian optics parameters taken at the
        line_of_sight/first_point position (for synthetic modelling of
        the ECE emission)
    """
    class Meta:
        name = "ece_channel"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    frequency: Optional[PhysicalQuantityFlt1DTime1] = field(
        default=None
    )
    harmonic: Optional[PhysicalQuantityFlt1DTime1] = field(
        default=None
    )
    if_bandwidth: float = field(
        default=9e+40
    )
    position: Optional[Rzphirhopsitheta1DDynamicAos1CommonTime1] = field(
        default=None
    )
    delta_position_suprathermal: Optional[Rzphirhopsitheta1DDynamicAos1CommonTime1] = field(
        default=None
    )
    t_e: Optional[PhysicalQuantityFlt1DTime1] = field(
        default=None
    )
    t_e_voltage: Optional[SignalFlt1DValidity] = field(
        default=None
    )
    optical_depth: Optional[PhysicalQuantityFlt1DTime1] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
    beam: Optional[EceChannelBeam] = field(
        default=None
    )


@dataclass(slots=True)
class Ece(IdsBaseClass):
    """
    Electron cyclotron emission diagnostic.

    :ivar ids_properties:
    :ivar line_of_sight: Description of the line of sight of the
        diagnostic (valid for all channels), defined by two points. By
        convention, the first point is the closest to the diagnostic
    :ivar t_e_central: Electron temperature from the closest channel to
        the magnetic axis, together with its radial location
    :ivar channel: Set of channels (frequency)
    :ivar polarizer: Set of polarizers placed in front of the diagnostic
        (if any). Polarizers are assumed to be orthogonal to the line of
        sight, so that the x3 unit vector is aligned with the line of
        sight
    :ivar psi_normalization: Quantities to use to normalize psi, as a
        function of time
    :ivar latency: Upper bound of the delay between physical information
        received by the detector and data available on the real-time
        (RT) network.
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "ece"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    line_of_sight: Optional[LineOfSight2Points] = field(
        default=None
    )
    t_e_central: Optional[SignalFlt1DValidityPosition] = field(
        default=None
    )
    channel: list[EceChannel] = field(
        default_factory=list,
        metadata={
            "max_occurs": 100,
        }
    )
    polarizer: list[Polarizer] = field(
        default_factory=list,
        metadata={
            "max_occurs": 3,
        }
    )
    psi_normalization: Optional[PsiNormalization] = field(
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
