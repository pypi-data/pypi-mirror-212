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
class NbiUnitBeamletsGroupDivergence(IdsBaseClass):
    """
    Describes a divergence component of a group of beamlets.

    :ivar particles_fraction: Fraction of injected particles in the
        component
    :ivar vertical: The vertical beamlet divergence of the component.
        Here the divergence is defined for Gaussian beams as the angel
        where the beam density is reduced by a factor 1/e compared to
        the maximum density. For non-Gaussian beams the divergence is
        sqrt(2)*mean((x-mean(x))**2), where x is the angle and the mean
        should be performed over the beam density, P(x):
        mean(y)=int(y*P(x)*dx).
    :ivar horizontal: The horiztonal beamlet divergence of the
        component. Here the divergence is defined for Gaussian beams as
        the angel where the beam density is reduced by a factor 1/e
        compared to the maximum density. For non-Gaussian beams the
        divergence is sqrt(2)*mean((x-mean(x))**2), where x is the angle
        and the mean should be performed over the beam density, P(x):
        mean(y)=int(y*P(x)*dx).
    """
    class Meta:
        name = "nbi_unit_beamlets_group_divergence"

    particles_fraction: float = field(
        default=9e+40
    )
    vertical: float = field(
        default=9e+40
    )
    horizontal: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class NbiUnitBeamletsGroupFocus(IdsBaseClass):
    """
    Describes of a group of beamlets is focused.

    :ivar focal_length_horizontal: Horizontal focal length along the
        beam line, i.e. the point along the centre of the beamlet-group
        where the beamlet-group has its minimum horizontal width
    :ivar focal_length_vertical: Vertical focal length along the beam
        line, i.e. the point along the centre of the beamlet-group where
        the beamlet-group has its minimum vertical width
    :ivar width_min_horizontal: The horizontal width of the beamlets
        group at the at the horizontal focal point
    :ivar width_min_vertical: The vertical width of the beamlets group
        at the at the vertical focal point
    """
    class Meta:
        name = "nbi_unit_beamlets_group_focus"

    focal_length_horizontal: float = field(
        default=9e+40
    )
    focal_length_vertical: float = field(
        default=9e+40
    )
    width_min_horizontal: float = field(
        default=9e+40
    )
    width_min_vertical: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class PlasmaCompositionSpecies(IdsBaseClass):
    """
    Description of simple species (elements) without declaration of their
    ionisation state.

    :ivar a: Mass of atom
    :ivar z_n: Nuclear charge
    :ivar label: String identifying the species (e.g. H, D, T, ...)
    """
    class Meta:
        name = "plasma_composition_species"

    a: float = field(
        default=9e+40
    )
    z_n: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )


@dataclass(slots=True)
class Rzphi0DDynamicAos3(IdsBaseClass):
    """
    Structure for R, Z, Phi positions (0D, dynamic within a type 3 array of
    structures (index on time))

    :ivar r: Major radius
    :ivar z: Height
    :ivar phi: Toroidal angle (oriented counter-clockwise when viewing
        from above)
    """
    class Meta:
        name = "rzphi0d_dynamic_aos3"

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
class NbiUnitBeamletsGroupBeamlets(IdsBaseClass):
    """
    Detailed information on beamlets.

    :ivar positions: Position of each beamlet
    :ivar tangency_radii: Tangency radius (major radius where the
        central line of a beamlet is tangent to a circle around the
        torus), for each beamlet
    :ivar angles: Angle of inclination between a line at the centre of a
        beamlet and the horizontal plane, for each beamlet
    :ivar power_fractions: Fraction of power of a unit injected by each
        beamlet
    """
    class Meta:
        name = "nbi_unit_beamlets_group_beamlets"

    positions: Optional[Rzphi1DStatic] = field(
        default=None
    )
    tangency_radii: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    angles: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_fractions: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class NbiUnitBeamletsGroupTilting(IdsBaseClass):
    """
    Variation of position, tangency radius and angle in case of dynamic beam
    tilting, for a given time slice.

    :ivar delta_position: Variation of the position of the beamlet group
        centre
    :ivar delta_tangency_radius: Variation of the tangency radius (major
        radius where the central line of a NBI unit is tangent to a
        circle around the torus)
    :ivar delta_angle: Variation of the angle of inclination between a
        beamlet at the centre of the injection unit surface and the
        horiontal plane
    :ivar time: Time
    """
    class Meta:
        name = "nbi_unit_beamlets_group_tilting"

    delta_position: Optional[Rzphi0DDynamicAos3] = field(
        default=None
    )
    delta_tangency_radius: float = field(
        default=9e+40
    )
    delta_angle: float = field(
        default=9e+40
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class NbiUnitBeamletsGroup(IdsBaseClass):
    """
    Group of beamlets.

    :ivar position: R, Z, Phi position of the beamlet group centre
    :ivar tangency_radius: Tangency radius (major radius where the
        central line of a NBI unit is tangent to a circle around the
        torus)
    :ivar angle: Angle of inclination between a beamlet at the centre of
        the injection unit surface and the horiontal plane
    :ivar tilting: In case of dynamic beam tilting (i.e. during the
        pulse), e.g. for some Beam Emission Spectroscopy use cases,
        variations of position, tangency radius and angle with respect
        to their static value, for various time slices
    :ivar direction: Direction of the beam seen from above the torus: -1
        = clockwise; 1 = counter clockwise
    :ivar width_horizontal: Horizontal width of the beam group at the
        injection unit surface (or grounded grid)
    :ivar width_vertical: Vertical width of the beam group at the
        injection unit surface (or grounded grid)
    :ivar focus: Describes how the beamlet group is focused
    :ivar divergence_component: Detailed information on beamlet
        divergence. Divergence is described as a superposition of
        Gaussian components with amplitide "particles_fraction" and
        vertical/horizontal divergence. Note that for positive ion NBI
        the divergence is well described by a single Gaussian
    :ivar beamlets: Detailed information on beamlets
    """
    class Meta:
        name = "nbi_unit_beamlets_group"

    position: Optional[Rzphi0DStatic] = field(
        default=None
    )
    tangency_radius: float = field(
        default=9e+40
    )
    angle: float = field(
        default=9e+40
    )
    tilting: list[NbiUnitBeamletsGroupTilting] = field(
        default_factory=list
    )
    direction: int = field(
        default=999999999
    )
    width_horizontal: float = field(
        default=9e+40
    )
    width_vertical: float = field(
        default=9e+40
    )
    focus: Optional[NbiUnitBeamletsGroupFocus] = field(
        default=None
    )
    divergence_component: list[NbiUnitBeamletsGroupDivergence] = field(
        default_factory=list,
        metadata={
            "max_occurs": 3,
        }
    )
    beamlets: Optional[NbiUnitBeamletsGroupBeamlets] = field(
        default=None
    )


@dataclass(slots=True)
class NbiUnit(IdsBaseClass):
    """
    NBI unit.

    :ivar name: Name of the NBI unit
    :ivar identifier: ID of the NBI unit
    :ivar species: Injected species
    :ivar power_launched: Power launched from this unit into the vacuum
        vessel
    :ivar energy: Full energy of the injected species (acceleration of a
        single atom)
    :ivar beam_current_fraction: Fractions of beam current distributed
        among the different energies, the first index corresponds to the
        fast neutrals energy (1:full, 2: half, 3: one third)
    :ivar beam_power_fraction: Fractions of beam power distributed among
        the different energies, the first index corresponds to the fast
        neutrals energy (1:full, 2: half, 3: one third)
    :ivar beamlets_group: Group of beamlets with common vertical and
        horizontal focal point. If there are no common focal points,
        then select small groups of beamlets such that a focal point
        description of the beamlets group provides a fair description
    :ivar source: Description of the surface of the ion source from
        which the beam is extracted
    :ivar aperture: Description of a set of collimating apertures
        through which the beam is launched
    """
    class Meta:
        name = "nbi_unit"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    species: Optional[PlasmaCompositionSpecies] = field(
        default=None
    )
    power_launched: Optional[SignalFlt1D] = field(
        default=None
    )
    energy: Optional[SignalFlt1D] = field(
        default=None
    )
    beam_current_fraction: Optional[SignalFlt2D] = field(
        default=None
    )
    beam_power_fraction: Optional[SignalFlt2D] = field(
        default=None
    )
    beamlets_group: list[NbiUnitBeamletsGroup] = field(
        default_factory=list,
        metadata={
            "max_occurs": 16,
        }
    )
    source: Optional[DetectorAperture] = field(
        default=None
    )
    aperture: list[DetectorAperture] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )


@dataclass(slots=True)
class Nbi(IdsBaseClass):
    """
    Neutral Beam Injection systems and description of the fast neutrals that arrive
    into the torus.

    :ivar ids_properties:
    :ivar unit: The NBI system is described as a set of units of which
        the power can be controlled individually.
    :ivar latency: Upper bound of the delay between input command
        received from the RT network and actuator starting to react.
        Applies globally to the system described by this IDS unless
        specific latencies (e.g. channel-specific or antenna-specific)
        are provided at a deeper level in the IDS structure.
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "nbi"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    unit: list[NbiUnit] = field(
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
