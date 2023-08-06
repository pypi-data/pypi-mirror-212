#__version__='0.3.1'
#__imas_commit__='dd6854b4d07'
#__imas_version__='3.7.1'
from ..dataclasses_idsschema import IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


@dataclass(slots=True)
class EntryTag(IdsBaseClass):
    """
    Tag qualifying an entry or a list of entries.

    :ivar name: Name of the tag
    :ivar comment: Any comment describing the content of the tagged list
        of entries
    """
    class Meta:
        name = "entry_tag"

    name: str = field(
        default=""
    )
    comment: str = field(
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
class SummaryConstantFlt0D(IdsBaseClass):
    """
    Summary constant FLT_0D + source information.

    :ivar value: Value
    :ivar source: Source of the data (any comment describing the origin
        of the data : code, path to diagnostic signals, processing
        method, ...)
    """
    class Meta:
        name = "summary_constant_flt_0d"

    value: float = field(
        default=9e+40
    )
    source: str = field(
        default=""
    )


@dataclass(slots=True)
class SummaryConstantFlt0D2(IdsBaseClass):
    """
    Summary constant FLT_0D + source information, units as parent level 2.

    :ivar value: Value
    :ivar source: Source of the data (any comment describing the origin
        of the data : code, path to diagnostic signals, processing
        method, ...)
    """
    class Meta:
        name = "summary_constant_flt_0d_2"

    value: float = field(
        default=9e+40
    )
    source: str = field(
        default=""
    )


@dataclass(slots=True)
class SummaryConstantInt0D(IdsBaseClass):
    """
    Summary constant INT_0D + source information.

    :ivar value: Value
    :ivar source: Source of the data (any comment describing the origin
        of the data : code, path to diagnostic signals, processing
        method, ...)
    """
    class Meta:
        name = "summary_constant_int_0d"

    value: int = field(
        default=999999999
    )
    source: str = field(
        default=""
    )


@dataclass(slots=True)
class SummaryConstantStr0D(IdsBaseClass):
    """
    Summary constant STR_0D + source information.

    :ivar value: Value
    :ivar source: Source of the data (any comment describing the origin
        of the data : code, path to diagnostic signals, processing
        method, ...)
    """
    class Meta:
        name = "summary_constant_str_0d"

    value: str = field(
        default=""
    )
    source: str = field(
        default=""
    )


@dataclass(slots=True)
class SummaryDynamicFlt1DRoot(IdsBaseClass):
    """
    Summary dynamic FLT_1D + source information, time at the root of the IDS.

    :ivar value: Value
    :ivar source: Source of the data (any comment describing the origin
        of the data : code, path to diagnostic signals, processing
        method, ...)
    """
    class Meta:
        name = "summary_dynamic_flt_1d_root"

    value: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    source: str = field(
        default=""
    )


@dataclass(slots=True)
class SummaryDynamicFlt1DRootParent2(IdsBaseClass):
    """
    Summary dynamic FLT_1D + source information, time at the root of the IDS and
    units as parent level 2.

    :ivar value: Value
    :ivar source: Source of the data (any comment describing the origin
        of the data : code, path to diagnostic signals, processing
        method, ...)
    """
    class Meta:
        name = "summary_dynamic_flt_1d_root_parent_2"

    value: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    source: str = field(
        default=""
    )


@dataclass(slots=True)
class SummaryDynamicFlt2DFraction2(IdsBaseClass):
    """
    Summary dynamic FL2_1D + source information, time at the root of the IDS, first
    dimension 1...3 (beam fractions)

    :ivar value: Value
    :ivar source: Source of the data (any comment describing the origin
        of the data : code, path to diagnostic signals, processing
        method, ...)
    """
    class Meta:
        name = "summary_dynamic_flt_2d_fraction_2"

    value: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    source: str = field(
        default=""
    )


@dataclass(slots=True)
class SummaryDynamicInt1DRoot(IdsBaseClass):
    """
    Summary dynamic INT_1D + source information, time at the root of the IDS.

    :ivar value: Value
    :ivar source: Source of the data (any comment describing the origin
        of the data : code, path to diagnostic signals, processing
        method, ...)
    """
    class Meta:
        name = "summary_dynamic_int_1d_root"

    value: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    source: str = field(
        default=""
    )


@dataclass(slots=True)
class SummaryLocalPosition(IdsBaseClass):
    """
    Radial position at which physics quantities are evaluated.

    :ivar rho_tor_norm: Normalised toroidal flux coordinate. The
        normalizing value for rho_tor_norm, is the toroidal flux
        coordinate at the equilibrium boundary (LCFS or 99.x % of the
        LCFS in case of a fixed boundary equilibium calculation, see
        time_slice/boundary/b_flux_pol_norm in the equilibrium IDS)
    :ivar rho_tor: Toroidal flux coordinate. rho_tor =
        sqrt(b_flux_tor/(pi*b0)) ~ sqrt(pi*r^2*b0/(pi*b0)) ~ r [m]. The
        toroidal field used in its definition is indicated under
        global_quantities/b0
    :ivar psi: Poloidal magnetic flux
    """
    class Meta:
        name = "summary_local_position"

    rho_tor_norm: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    rho_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    psi: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryLocalPositionRZ(IdsBaseClass):
    """
    Radial position at which physics quantities are evaluated, including an R,Z
    position.

    :ivar rho_tor_norm: Normalised toroidal flux coordinate. The
        normalizing value for rho_tor_norm, is the toroidal flux
        coordinate at the equilibrium boundary (LCFS or 99.x % of the
        LCFS in case of a fixed boundary equilibium calculation, see
        time_slice/boundary/b_flux_pol_norm in the equilibrium IDS)
    :ivar rho_tor: Toroidal flux coordinate. rho_tor =
        sqrt(b_flux_tor/(pi*b0)) ~ sqrt(pi*r^2*b0/(pi*b0)) ~ r [m]. The
        toroidal field used in its definition is indicated under
        global_quantities/b0
    :ivar psi: Poloidal magnetic flux
    :ivar r: Major radius
    :ivar z: Height
    """
    class Meta:
        name = "summary_local_position_r_z"

    rho_tor_norm: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    rho_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    psi: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    r: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    z: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryRz1DDynamic(IdsBaseClass):
    """
    Structure for R, Z positions (1D, dynamic) + source information.

    :ivar r: Major radius
    :ivar z: Height
    :ivar source: Source of the data (any comment describing the origin
        of the data : code, path to diagnostic signals, processing
        method, ...)
    """
    class Meta:
        name = "summary_rz1d_dynamic"

    r: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    z: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    source: str = field(
        default=""
    )


@dataclass(slots=True)
class SummaryStaticFlt0D(IdsBaseClass):
    """
    Summary static FLT_0D + source information.

    :ivar value: Value
    :ivar source: Source of the data (any comment describing the origin
        of the data : code, path to diagnostic signals, processing
        method, ...)
    """
    class Meta:
        name = "summary_static_flt_0d"

    value: float = field(
        default=9e+40
    )
    source: str = field(
        default=""
    )


@dataclass(slots=True)
class SummaryStaticInt0D(IdsBaseClass):
    """
    Summary static INT_0D + source information.

    :ivar value: Value
    :ivar source: Source of the data (any comment describing the origin
        of the data : code, path to diagnostic signals, processing
        method, ...)
    """
    class Meta:
        name = "summary_static_int_0d"

    value: int = field(
        default=999999999
    )
    source: str = field(
        default=""
    )


@dataclass(slots=True)
class SummaryStaticStr0D(IdsBaseClass):
    """
    Summary static STR_0D + source information.

    :ivar value: Value
    :ivar source: Source of the data (any comment describing the origin
        of the data : code, path to diagnostic signals, processing
        method, ...)
    """
    class Meta:
        name = "summary_static_str_0d"

    value: str = field(
        default=""
    )
    source: str = field(
        default=""
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
class SummaryBoundary(IdsBaseClass):
    """
    Geometry of the plasma boundary.

    :ivar type: 0 (limiter), 1 (diverted), 11 (LSN), 12 (USN), 13 (DN),
        14 (snowflake)
    :ivar geometric_axis_r: R position of the geometric axis (defined as
        (Rmax+Rmin) / 2 of the boundary)
    :ivar geometric_axis_z: Z position of the geometric axis (defined as
        (Zmax+Zmin) / 2 of the boundary)
    :ivar magnetic_axis_r: R position of the magnetic axis
    :ivar magnetic_axis_z: Z position of the magnetic axis
    :ivar minor_radius: Minor radius of the plasma boundary (defined as
        (Rmax-Rmin) / 2 of the boundary)
    :ivar elongation: Elongation of the plasma boundary
    :ivar triangularity_upper: Upper triangularity of the plasma
        boundary
    :ivar triangularity_lower: Lower triangularity of the plasma
        boundary
    :ivar strike_point_inner_r: R position of the inner strike point
    :ivar strike_point_inner_z: Z position of the inner strike point
    :ivar strike_point_outer_r: R position of the outer strike point
    :ivar strike_point_outer_z: Z position of the outer strike point
    :ivar strike_point_configuration: String describing the
        configuration of the strike points (constant, may need to become
        dynamic when available)
    :ivar gap_limiter_wall: Distance between the separatrix and the
        nearest limiter or wall element
    :ivar distance_inner_outer_separatrices: Distance between the inner
        and outer separatrices, in the major radius direction, at the
        plasma outboard and at the height corresponding to the maximum R
        for the inner separatrix.
    :ivar x_point_main: RZ position of the main X-point
    """
    class Meta:
        name = "summary_boundary"

    type: Optional[SummaryDynamicInt1DRoot] = field(
        default=None
    )
    geometric_axis_r: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    geometric_axis_z: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    magnetic_axis_r: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    magnetic_axis_z: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    minor_radius: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    elongation: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    triangularity_upper: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    triangularity_lower: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    strike_point_inner_r: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    strike_point_inner_z: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    strike_point_outer_r: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    strike_point_outer_z: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    strike_point_configuration: Optional[SummaryConstantStr0D] = field(
        default=None
    )
    gap_limiter_wall: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    distance_inner_outer_separatrices: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    x_point_main: Optional[SummaryRz1DDynamic] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryDisruption(IdsBaseClass):
    """
    Disruption related parameters.

    :ivar time: Time of the disruption
    :ivar time_radiated_power_max: Time of maximum radiated power,
        relative to the time of the disruption
    :ivar time_half_ip: Time at which the plasma current has fallen to
        half of the initial current at the start of the disruption,
        relative to the time of the disruption
    :ivar vertical_displacement: Direction of the plasma vertical
        displacement just before the disruption 1 (upwards) / 0 (no
        displacement)/ -1 (downwards)
    :ivar mitigation_valve: Flag indicating whether any disruption
        mitigation valve has been used (1) or none (0)
    """
    class Meta:
        name = "summary_disruption"

    time: Optional[SummaryConstantFlt0D] = field(
        default=None
    )
    time_radiated_power_max: Optional[SummaryConstantFlt0D] = field(
        default=None
    )
    time_half_ip: Optional[SummaryConstantFlt0D] = field(
        default=None
    )
    vertical_displacement: Optional[SummaryConstantInt0D] = field(
        default=None
    )
    mitigation_valve: Optional[SummaryConstantInt0D] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryElms(IdsBaseClass):
    """
    Edge Localized Modes related quantities.

    :ivar frequency: ELMs frequency
    :ivar type: ELMs type (I, II, III, ...)
    """
    class Meta:
        name = "summary_elms"

    frequency: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    type: Optional[SummaryDynamicInt1DRoot] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryGasInjection(IdsBaseClass):
    """
    List of ion species and other gas injection related quantities.

    :ivar total: Total gas injection rate (sum over species)
    :ivar midplane: Gas injection rate from all valves located near the
        equatorial midplane
    :ivar top: Gas injection rate from all valves located near the top
        of the vaccuum chamber
    :ivar bottom: Gas injection rate from all valves located near near
        the bottom of the vaccuum chamber
    :ivar hydrogen: Hydrogen
    :ivar deuterium: Deuterium
    :ivar tritium: Tritium
    :ivar helium_3: Helium isotope with 3 nucleons
    :ivar helium_4: Helium isotope with 4 nucleons
    :ivar impurity_seeding: Flag set to 1 if any gas other than H, D, T,
        He is puffed during the pulse, 0 otherwise
    :ivar beryllium: Beryllium
    :ivar lithium: Lithium
    :ivar carbon: Carbon
    :ivar oxygen: Oxygen
    :ivar nitrogen: Nitrogen
    :ivar neon: Neon
    :ivar argon: Argon
    :ivar xenon: Xenon
    :ivar krypton: Krypton
    :ivar methane: Methane (CH4)
    :ivar methane_carbon_13: Methane (CH4 with carbon 13)
    :ivar methane_deuterated: Deuterated methane (CD4)
    :ivar silane: Silane (SiH4)
    :ivar ethylene: Ethylene (C2H4)
    :ivar ethane: Ethane (C2H6)
    :ivar propane: Propane (C3H8)
    :ivar ammonia: Ammonia (NH3)
    :ivar ammonia_deuterated: Deuterated ammonia (ND3)
    """
    class Meta:
        name = "summary_gas_injection"

    total: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    midplane: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    top: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    bottom: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    hydrogen: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    deuterium: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    tritium: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    helium_3: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    helium_4: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    impurity_seeding: Optional[SummaryConstantInt0D] = field(
        default=None
    )
    beryllium: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    lithium: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    carbon: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    oxygen: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    nitrogen: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    neon: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    argon: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    xenon: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    krypton: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    methane: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    methane_carbon_13: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    methane_deuterated: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    silane: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    ethylene: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    ethane: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    propane: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    ammonia: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    ammonia_deuterated: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryGasInjectionAccumulated(IdsBaseClass):
    """
    List of accumulated ion species and other related quantities within volume
    enclosed by first wall contour.

    :ivar total: Total accumulated injected gas (sum over species)
    :ivar midplane: Accumulated gas injected from all valves located
        near the equatorial midplane
    :ivar top: Accumulated gas injected from all valves located near the
        top of the vacuum chamber
    :ivar bottom: Accumulated gas injected from all valves located near
        near the bottom of the vacuum chamber
    :ivar hydrogen: Hydrogen
    :ivar deuterium: Deuterium
    :ivar tritium: Tritium
    :ivar helium_3: Helium isotope with 3 nucleons
    :ivar helium_4: Helium isotope with 4 nucleons
    :ivar impurity_seeding: Flag set to 1 if any gas other than H, D, T,
        He is puffed during the pulse, 0 otherwise
    :ivar beryllium: Beryllium
    :ivar lithium: Lithium
    :ivar carbon: Carbon
    :ivar oxygen: Oxygen
    :ivar nitrogen: Nitrogen
    :ivar neon: Neon
    :ivar argon: Argon
    :ivar xenon: Xenon
    :ivar krypton: Krypton
    :ivar methane: Methane (CH4)
    :ivar methane_carbon_13: Methane (CH4 with carbon 13)
    :ivar methane_deuterated: Deuterated methane (CD4)
    :ivar silane: Silane (SiH4)
    :ivar ethylene: Ethylene (C2H4)
    :ivar ethane: Ethane (C2H6)
    :ivar propane: Propane (C3H8)
    :ivar ammonia: Ammonia (NH3)
    :ivar ammonia_deuterated: Deuterated ammonia (ND3)
    """
    class Meta:
        name = "summary_gas_injection_accumulated"

    total: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    midplane: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    top: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    bottom: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    hydrogen: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    deuterium: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    tritium: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    helium_3: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    helium_4: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    impurity_seeding: Optional[SummaryConstantInt0D] = field(
        default=None
    )
    beryllium: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    lithium: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    carbon: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    oxygen: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    nitrogen: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    neon: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    argon: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    xenon: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    krypton: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    methane: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    methane_carbon_13: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    methane_deuterated: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    silane: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    ethylene: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    ethane: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    propane: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    ammonia: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    ammonia_deuterated: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryGasInjectionPrefill(IdsBaseClass):
    """
    List of accumulated ion species during the prefill (constant)

    :ivar total: Total accumulated injected gas (sum over species)
    :ivar midplane: Accumulated gas injected from all valves located
        near the equatorial midplane
    :ivar top: Accumulated gas injected from all valves located near the
        top of the vacuum chamber
    :ivar bottom: Accumulated gas injected from all valves located near
        near the bottom of the vacuum chamber
    :ivar hydrogen: Hydrogen
    :ivar deuterium: Deuterium
    :ivar tritium: Tritium
    :ivar helium_3: Helium isotope with 3 nucleons
    :ivar helium_4: Helium isotope with 4 nucleons
    :ivar impurity_seeding: Flag set to 1 if any gas other than H, D, T,
        He is puffed during the prefill, 0 otherwise
    :ivar beryllium: Beryllium
    :ivar lithium: Lithium
    :ivar carbon: Carbon
    :ivar oxygen: Oxygen
    :ivar nitrogen: Nitrogen
    :ivar neon: Neon
    :ivar argon: Argon
    :ivar xenon: Xenon
    :ivar krypton: Krypton
    :ivar methane: Methane (CH4)
    :ivar methane_carbon_13: Methane (CH4 with carbon 13)
    :ivar methane_deuterated: Deuterated methane (CD4)
    :ivar silane: Silane (SiH4)
    :ivar ethylene: Ethylene (C2H4)
    :ivar ethane: Ethane (C2H6)
    :ivar propane: Propane (C3H8)
    :ivar ammonia: Ammonia (NH3)
    :ivar ammonia_deuterated: Deuterated ammonia (ND3)
    """
    class Meta:
        name = "summary_gas_injection_prefill"

    total: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    midplane: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    top: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    bottom: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    hydrogen: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    deuterium: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    tritium: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    helium_3: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    helium_4: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    impurity_seeding: Optional[SummaryConstantInt0D] = field(
        default=None
    )
    beryllium: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    lithium: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    carbon: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    oxygen: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    nitrogen: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    neon: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    argon: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    xenon: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    krypton: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    methane: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    methane_carbon_13: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    methane_deuterated: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    silane: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    ethylene: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    ethane: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    propane: Optional[SummaryConstantFlt0D] = field(
        default=None
    )
    ammonia: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )
    ammonia_deuterated: Optional[SummaryConstantFlt0D2] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryGlobalQuantities(IdsBaseClass):
    """
    Various global quantities calculated from the fields solved in the transport
    equations and from the Derived Profiles.

    :ivar ip: Total plasma current (toroidal component). Positive sign
        means anti-clockwise when viewed from above.
    :ivar current_non_inductive: Total non-inductive current (toroidal
        component). Positive sign means anti-clockwise when viewed from
        above.
    :ivar current_bootstrap: Bootstrap current (toroidal component).
        Positive sign means anti-clockwise when viewed from above.
    :ivar current_ohm: Ohmic current (toroidal component). Positive sign
        means anti-clockwise when viewed from above.
    :ivar current_alignment: Figure of merit of the alignment of the
        current profile sources, defined in the following reference:
        http://iopscience.iop.org/article/10.1088/0029-5515/43/7/318
    :ivar v_loop: LCFS loop voltage (positive value drives positive
        ohmic current that flows anti-clockwise when viewed from above)
    :ivar li: Internal inductance. The li_3 definition is used, i.e.
        li_3 = 2/R0/mu0^2/Ip^2 * int(Bp^2 dV).
    :ivar li_mhd: Internal inductance as determined by an equilibrium
        reconstruction code. Use this only when the li node above is
        used for another estimation method and there is a need to store
        a second value of li (determined by an equilibrium
        reconstruction code). The li_3 definition is used, i.e. li_3 =
        2/R0/mu0^2/Ip^2 * int(Bp^2 dV).
    :ivar beta_tor: Toroidal beta, defined as the volume-averaged total
        perpendicular pressure divided by (B0^2/(2*mu0)), i.e.
        beta_toroidal = 2 mu0 int(p dV) / V / B0^2
    :ivar beta_tor_mhd: Toroidal beta, using the pressure determined by
        an equilibrium reconstruction code
    :ivar beta_tor_norm: Normalised toroidal beta, defined as 100 *
        beta_tor * a[m] * B0 [T] / ip [MA]
    :ivar beta_tor_norm_mhd: Normalised toroidal beta, using the
        pressure determined by an equilibrium reconstruction code
    :ivar beta_tor_thermal_norm: Normalised toroidal beta from thermal
        pressure only, defined as 100 * beta_tor_thermal * a[m] * B0 [T]
        / ip [MA]
    :ivar beta_pol: Poloidal beta. Defined as betap = 4 int(p dV) / [R_0
        * mu_0 * Ip^2]
    :ivar beta_pol_mhd: Poloidal beta estimated from the pressure
        determined by an equilibrium reconstruction code. Defined as
        betap = 4 int(p dV) / [R_0 * mu_0 * Ip^2]
    :ivar energy_diamagnetic: Plasma diamagnetic energy content = 3/2 *
        integral over the plasma volume of the total perpendicular
        pressure
    :ivar denergy_diamagnetic_dt: Time derivative of the diamagnetic
        plasma energy content
    :ivar energy_total: Plasma energy content = 3/2 * integral over the
        plasma volume of the total kinetic pressure
    :ivar energy_mhd: Plasma energy content = 3/2 * integral over the
        plasma volume of the total kinetic pressure (pressure determined
        by an equilibrium reconstruction code)
    :ivar energy_thermal: Thermal plasma energy content = 3/2 * integral
        over the plasma volume of the thermal pressure
    :ivar energy_ion_total_thermal: Thermal ion plasma energy content
        (sum over the ion species) = 3/2 * integral over the plasma
        volume of the thermal ion pressure
    :ivar energy_electrons_thermal: Thermal electron plasma energy
        content = 3/2 * integral over the plasma volume of the thermal
        electron pressure
    :ivar denergy_thermal_dt: Time derivative of the thermal plasma
        energy content
    :ivar energy_b_field_pol: Poloidal magnetic plasma energy content =
        1/(2.mu0) * integral over the plasma volume of b_field_pol^2
    :ivar energy_fast_perpendicular: Fast particles perpendicular energy
        content = 3/2 * integral over the plasma volume of the fast
        perpendicular pressure
    :ivar energy_fast_parallel: Fast particles parallel energy content =
        3/2 * integral over the plasma volume of the fast parallel
        pressure
    :ivar volume: Volume of the confined plasma
    :ivar h_mode: H-mode flag: 0 when the plasma is in L-mode and 1 when
        in H-mode
    :ivar r0: Reference major radius where the vacuum toroidal magnetic
        field is given (usually a fixed position such as the middle of
        the vessel at the equatorial midplane)
    :ivar b0: Vacuum toroidal field at R0. Positive sign means anti-
        clockwise when viewed from above. The product R0B0 must be
        consistent with the b_tor_vacuum_r field of the tf IDS.
    :ivar fusion_gain: Fusion gain : ratio of the power provided by
        fusion reactions to the auxiliary power needed to heat the
        plasma. Often noted as Q in the litterature.
    :ivar h_98: Energy confinement time enhancement factor over the
        IPB98(y,2) scaling
    :ivar tau_energy: Energy confinement time
    :ivar tau_helium: Helium confinement time
    :ivar tau_resistive: Current diffusion characteristic time
    :ivar tau_energy_98: Energy confinement time estimated from the
        IPB98(y,2) scaling
    :ivar ratio_tau_helium_fuel: Ratio of Helium confinement time to
        fuel confinement time
    :ivar resistance: Plasma electric resistance
    :ivar q_95: q at the 95% poloidal flux surface (IMAS uses COCOS=11:
        only positive when toroidal current and magnetic field are in
        same direction)
    :ivar power_ohm: Ohmic power
    :ivar power_steady: Total power coupled to the plasma minus dW/dt
        (correcting from transient energy content)
    :ivar power_radiated: Total radiated power
    :ivar power_radiated_inside_lcfs: Radiated power from the plasma
        inside the Last Closed Flux Surface
    :ivar power_radiated_outside_lcfs: Radiated power from the plasma
        outside the Last Closed Flux Surface
    :ivar power_line: Radiated power from line radiation
    :ivar power_bremsstrahlung: Radiated power from Bremsstrahlung
    :ivar power_synchrotron: Radiated power from synchrotron radiation
    :ivar power_loss: Power through separatrix
    :ivar greenwald_fraction: Greenwald fraction =line_average/n_e/value
        divided by (global_quantities/ip/value *1e6 * pi *
        minor_radius^2)
    :ivar fusion_fluence: Fusion fluence : power provided by fusion
        reactions, integrated over time since the beginning of the pulse
    :ivar psi_external_average: Average (over the plasma poloidal cross
        section) plasma poloidal magnetic flux produced by all toroidal
        loops (active coils and passive loops) but the plasma, given by
        the following formula : int(psi_loops.j_tor.dS) / Ip
    """
    class Meta:
        name = "summary_global_quantities"

    ip: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    current_non_inductive: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    current_bootstrap: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    current_ohm: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    current_alignment: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    v_loop: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    li: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    li_mhd: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    beta_tor: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    beta_tor_mhd: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    beta_tor_norm: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    beta_tor_norm_mhd: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    beta_tor_thermal_norm: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    beta_pol: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    beta_pol_mhd: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    energy_diamagnetic: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    denergy_diamagnetic_dt: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    energy_total: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    energy_mhd: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    energy_thermal: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    energy_ion_total_thermal: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    energy_electrons_thermal: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    denergy_thermal_dt: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    energy_b_field_pol: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    energy_fast_perpendicular: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    energy_fast_parallel: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    volume: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    h_mode: Optional[SummaryDynamicInt1DRoot] = field(
        default=None
    )
    r0: Optional[SummaryConstantFlt0D] = field(
        default=None
    )
    b0: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    fusion_gain: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    h_98: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    tau_energy: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    tau_helium: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    tau_resistive: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    tau_energy_98: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    ratio_tau_helium_fuel: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    resistance: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    q_95: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power_ohm: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power_steady: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power_radiated: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power_radiated_inside_lcfs: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power_radiated_outside_lcfs: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power_line: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power_bremsstrahlung: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power_synchrotron: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power_loss: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    greenwald_fraction: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    fusion_fluence: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    psi_external_average: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryHCdEc(IdsBaseClass):
    """
    ECRH/CD related parameters.

    :ivar frequency: ECRH frequency
    :ivar position: Position of the maximum of the ECRH power
        deposition, in rho_tor_norm
    :ivar polarisation: Polarisation of the ECRH waves (0 = O mode, 1 =
        X mode)
    :ivar harmonic: Harmonic number of the absorbed ECRH waves
    :ivar angle_tor: Toroidal angle of ECRH at resonance
    :ivar angle_pol: Poloidal angle of ECRH at resonance
    :ivar power: Electron cyclotron heating power coupled to the plasma
        from this launcher
    :ivar power_launched: Electron cyclotron heating power launched into
        the vacuum vessel from this launcher
    :ivar current: Parallel current driven by EC waves
    :ivar energy_fast: Fast particle energy content driven by EC waves
    """
    class Meta:
        name = "summary_h_cd_ec"

    frequency: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    position: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    polarisation: Optional[SummaryDynamicInt1DRoot] = field(
        default=None
    )
    harmonic: Optional[SummaryDynamicInt1DRoot] = field(
        default=None
    )
    angle_tor: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    angle_pol: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power_launched: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    current: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    energy_fast: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryHCdIc(IdsBaseClass):
    """
    ICRH related parameters.

    :ivar frequency: ICRH frequency
    :ivar position: Position of the maximum of the ICRH power
        deposition, in rho_tor_norm
    :ivar n_tor: Main toroidal mode number of IC waves
    :ivar k_perpendicular: Main perpendicular wave number of IC waves
    :ivar e_field_plus_minus_ratio: Average E+/E- power ratio of IC
        waves
    :ivar harmonic: Harmonic number of the absorbed ICRH waves
    :ivar phase: Phase between straps
    :ivar power: IC heating power coupled to the plasma from this
        launcher
    :ivar power_launched: IC heating power launched into the vacuum
        vessel from this launcher
    :ivar current: Parallel current driven by IC waves
    :ivar energy_fast: Fast particle energy content driven by IC waves
    """
    class Meta:
        name = "summary_h_cd_ic"

    frequency: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    position: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    n_tor: Optional[SummaryDynamicInt1DRoot] = field(
        default=None
    )
    k_perpendicular: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    e_field_plus_minus_ratio: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    harmonic: Optional[SummaryDynamicInt1DRoot] = field(
        default=None
    )
    phase: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power_launched: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    current: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    energy_fast: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryHCdLh(IdsBaseClass):
    """
    LHCD related parameters.

    :ivar frequency: LH wave frequency
    :ivar position: Position of the maximum of the LH power deposition,
        in rho_tor_norm
    :ivar n_parallel: Main parallel refractive index of LH waves at
        launch
    :ivar power: LH heating power coupled to the plasma from this
        launcher
    :ivar power_launched: LH heating power launched into the vacuum
        vessel from this launcher
    :ivar current: Parallel current driven by LH waves
    :ivar energy_fast: Fast particle energy content driven by LH waves
    """
    class Meta:
        name = "summary_h_cd_lh"

    frequency: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    position: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    n_parallel: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power_launched: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    current: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    energy_fast: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryKicks(IdsBaseClass):
    """
    Vertical kicks.

    :ivar occurrence: Flag set to 1 if vertical kicks of the plasma
        position are used during the pulse, 0 otherwise
    """
    class Meta:
        name = "summary_kicks"

    occurrence: Optional[SummaryConstantInt0D] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryLimiter(IdsBaseClass):
    """
    Limiter characteristics.

    :ivar material: Limiter material
    """
    class Meta:
        name = "summary_limiter"

    material: Optional[IdentifierStatic] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryLocalQuantitiesStellerator(IdsBaseClass):
    """
    Set of local quantities for stellerators.

    :ivar effective_helical_ripple: Effective helical ripple for 1/nu
        neoclassical regime (see [Beidler, C. D., and W. N. G. Hitchon,
        1994, Plasma Phys. Control. Fusion 35, 317])
    :ivar plateau_factor: Plateau factor, as defined in equation (25) of
        reference [Stroth U. et al 1998 Plasma Phys. Control. Fusion 40
        1551]
    :ivar iota: Rotational transform (1/q)
    """
    class Meta:
        name = "summary_local_quantities_stellerator"

    effective_helical_ripple: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    plateau_factor: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    iota: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryNeutronRatesReaction(IdsBaseClass):
    """
    Neutron rates per reaction.

    :ivar total: Total neutron rate coming from this reaction
    :ivar thermal: Neutron rate coming from thermal plasma
    :ivar beam_thermal: Neutron rate coming from NBI beam - plasma
        reactions
    :ivar beam_beam: Neutron rate coming from NBI beam self reactions
    """
    class Meta:
        name = "summary_neutron_rates_reaction"

    total: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    thermal: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    beam_thermal: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    beam_beam: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryNeutronReaction(IdsBaseClass):
    """
    Neutron fluxes per reaction.

    :ivar total: Total neutron flux coming from this reaction
    :ivar thermal: Neutron flux coming from thermal plasma
    :ivar beam_thermal: Neutron flux coming from NBI beam - plasma
        reactions
    :ivar beam_beam: Neutron flux coming from NBI beam self reactions
    """
    class Meta:
        name = "summary_neutron_reaction"

    total: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    thermal: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    beam_thermal: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    beam_beam: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryPedestalFitLinearNe(IdsBaseClass):
    """
    Quantities related to linear fit of pedestal profiles for a given physical
    quantity (density or pressure)

    :ivar separatrix: Value at separatrix
    :ivar pedestal_height: Pedestal height
    :ivar pedestal_width: Pedestal full width in normalised poloidal
        flux
    :ivar pedestal_position: Pedestal position in normalised poloidal
        flux
    :ivar offset: Offset of the parent quantity in the SOL
    :ivar d_dpsi_norm: Core slope of the parent quantity
    :ivar d_dpsi_norm_max: Maximum gradient of the parent quantity (with
        respect to the normalised poloidal flux) in the pedestal
    """
    class Meta:
        name = "summary_pedestal_fit_linear_ne"

    separatrix: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    pedestal_height: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    pedestal_width: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    pedestal_position: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    offset: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    d_dpsi_norm: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    d_dpsi_norm_max: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryPedestalFitLinearTe(IdsBaseClass):
    """
    Quantities related to linear fit of pedestal profiles for a given physical
    quantity (temperature)

    :ivar pedestal_height: Pedestal height
    :ivar pedestal_width: Pedestal full width in normalised poloidal
        flux
    :ivar pedestal_position: Pedestal position in normalised poloidal
        flux
    :ivar offset: Offset of the parent quantity in the SOL
    :ivar d_dpsi_norm: Core slope of the parent quantity
    :ivar d_dpsi_norm_max: Maximum gradient of the parent quantity (with
        respect to the normalised poloidal flux) in the pedestal
    """
    class Meta:
        name = "summary_pedestal_fit_linear_te"

    pedestal_height: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    pedestal_width: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    pedestal_position: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    offset: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    d_dpsi_norm: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    d_dpsi_norm_max: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryPedestalFitNe(IdsBaseClass):
    """
    Quantities related to a generic fit of pedestal profiles for a given physical
    quantity (density or pressure)

    :ivar separatrix: Value at separatrix
    :ivar pedestal_height: Pedestal height
    :ivar pedestal_width: Pedestal full width in normalised poloidal
        flux
    :ivar pedestal_position: Pedestal position in normalised poloidal
        flux
    :ivar offset: Offset of the parent quantity in the SOL
    :ivar d_dpsi_norm: Core slope of the parent quantity
    :ivar d_dpsi_norm_max: Maximum gradient of the parent quantity (with
        respect to the normalised poloidal flux) in the pedestal
    :ivar d_dpsi_norm_max_position: Position (in terms of normalised
        poloidal flux) of the maximum gradient of the parent quantity in
        the pedestal
    """
    class Meta:
        name = "summary_pedestal_fit_ne"

    separatrix: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    pedestal_height: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    pedestal_width: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    pedestal_position: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    offset: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    d_dpsi_norm: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    d_dpsi_norm_max: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    d_dpsi_norm_max_position: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryPedestalFitStabilityMethod(IdsBaseClass):
    """
    MHD stability analysis of the pedestal (for a given method for calculating the
    bootstrap current)

    :ivar alpha_critical: Critical normalized pressure gradient
        determined with self-consistent runs with an MHD stability code.
        Details of the method for scanning parameters in the series of
        runs must be described in the 'source' node
    :ivar alpha_ratio: Ratio of alpha_critical over alpha_experimental
    :ivar t_e_pedestal_top_critical: Critical electron temperature at
        pedestal top determined with self-consistent runs with an MHD
        stability code. Details of the method for scanning parameters in
        the series of runs must be described in the 'source' node
    """
    class Meta:
        name = "summary_pedestal_fit_stability_method"

    alpha_critical: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    alpha_ratio: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    t_e_pedestal_top_critical: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryPedestalFitTe(IdsBaseClass):
    """
    Quantities related to a generic fit of pedestal profiles for a given physical
    quantity (temperature)

    :ivar pedestal_height: Pedestal height
    :ivar pedestal_width: Pedestal full width in normalised poloidal
        flux
    :ivar pedestal_position: Pedestal position in normalised poloidal
        flux
    :ivar offset: Offset of the parent quantity in the SOL
    :ivar d_dpsi_norm: Core slope of the parent quantity
    :ivar d_dpsi_norm_max: Maximum gradient of the parent quantity (with
        respect to the normalised poloidal flux) in the pedestal
    :ivar d_dpsi_norm_max_position: Position (in terms of normalised
        poloidal flux) of the maximum gradient of the parent quantity in
        the pedestal
    """
    class Meta:
        name = "summary_pedestal_fit_te"

    pedestal_height: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    pedestal_width: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    pedestal_position: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    offset: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    d_dpsi_norm: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    d_dpsi_norm_max: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    d_dpsi_norm_max_position: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryPellets(IdsBaseClass):
    """
    Pellet related quantities.

    :ivar occurrence: Flag set to 1 if there is any pellet injected
        during the pulse, 0 otherwise
    """
    class Meta:
        name = "summary_pellets"

    occurrence: Optional[SummaryConstantInt0D] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryPlasmaCompositionSpecies(IdsBaseClass):
    """
    Description of simple species (elements) without declaration of their
    ionisation state.

    :ivar a: Mass of atom
    :ivar z_n: Nuclear charge
    :ivar label: String identifying the species (e.g. H, D, T, ...)
    """
    class Meta:
        name = "summary_plasma_composition_species"

    a: Optional[SummaryConstantFlt0D] = field(
        default=None
    )
    z_n: Optional[SummaryConstantFlt0D] = field(
        default=None
    )
    label: Optional[SummaryConstantStr0D] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryRmp(IdsBaseClass):
    """
    Resonant magnetic perturbations related quantities.

    :ivar occurrence: Flag set to 1 if resonant magnetic perturbations
        are used during the pulse, 0 otherwise
    """
    class Meta:
        name = "summary_rmp"

    occurrence: Optional[SummaryConstantInt0D] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryRunaways(IdsBaseClass):
    """
    Runaway electrons.

    :ivar particles: Number of runaway electrons
    :ivar current: Parallel current driven by the runaway electrons
    """
    class Meta:
        name = "summary_runaways"

    particles: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    current: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryRzphi0DStatic(IdsBaseClass):
    """
    Structure for R, Z, Phi positions (0D, static) + source information.

    :ivar r: Major radius
    :ivar z: Height
    :ivar phi: Toroidal angle
    """
    class Meta:
        name = "summary_rzphi0d_static"

    r: Optional[SummaryStaticFlt0D] = field(
        default=None
    )
    z: Optional[SummaryStaticFlt0D] = field(
        default=None
    )
    phi: Optional[SummaryStaticFlt0D] = field(
        default=None
    )


@dataclass(slots=True)
class SummarySol(IdsBaseClass):
    """
    Scrape-Off-Layer characteristics.

    :ivar t_e_decay_length: Electron temperature radial decay length
        inv(grad Te/Te)
    :ivar t_i_average_decay_length: Ion temperature (average over ion
        species) radial decay length inv(grad Ti/Ti)
    :ivar n_e_decay_length: Electron density radial decay length
        inv(grad ne/ne)
    :ivar n_i_total_decay_length: Ion density radial decay length
        inv(grad ni/ni)
    :ivar heat_flux_e_decay_length: Electron heat flux radial decay
        length inv(grad qe/qe)
    :ivar heat_flux_i_decay_length: Ion heat flux radial decay length
        inv(grad qi/qi)
    :ivar power_radiated: Power radiated from the SOL
    :ivar pressure_neutral: Neutral pressure in the SOL
    """
    class Meta:
        name = "summary_sol"

    t_e_decay_length: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    t_i_average_decay_length: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    n_e_decay_length: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    n_i_total_decay_length: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    heat_flux_e_decay_length: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    heat_flux_i_decay_length: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power_radiated: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    pressure_neutral: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )


@dataclass(slots=True)
class SummarySpecies(IdsBaseClass):
    """
    List of ion species used in summary.

    :ivar hydrogen: Hydrogen (H)
    :ivar deuterium: Deuterium (D)
    :ivar tritium: Tritium (T)
    :ivar helium_3: Helium isotope with 3 nucleons (3He)
    :ivar helium_4: Helium isotope with 4 nucleons (4He)
    :ivar beryllium: Beryllium (Be)
    :ivar lithium: Lithium (Li)
    :ivar carbon: Carbon (C)
    :ivar nitrogen: Nitrogen (N)
    :ivar neon: Neon (Ne)
    :ivar argon: Argon (Ar)
    :ivar xenon: Xenon (Xe)
    :ivar oxygen: Oxygen (O)
    :ivar tungsten: Tungsten (W)
    :ivar iron: Iron (Fe)
    :ivar krypton: Krypton (Kr)
    """
    class Meta:
        name = "summary_species"

    hydrogen: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    deuterium: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    tritium: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    helium_3: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    helium_4: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    beryllium: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    lithium: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    carbon: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    nitrogen: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    neon: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    argon: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    xenon: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    oxygen: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    tungsten: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    iron: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    krypton: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )


@dataclass(slots=True)
class SummarySpeciesTorAngle(IdsBaseClass):
    """
    List of ion species used in summary with tor_angle cocos transform.

    :ivar hydrogen: Hydrogen (H)
    :ivar deuterium: Deuterium (D)
    :ivar tritium: Tritium (T)
    :ivar helium_3: Helium isotope with 3 nucleons (3He)
    :ivar helium_4: Helium isotope with 4 nucleons (4He)
    :ivar beryllium: Beryllium (Be)
    :ivar lithium: Lithium (Li)
    :ivar carbon: Carbon (C)
    :ivar nitrogen: Nitrogen (N)
    :ivar neon: Neon (Ne)
    :ivar argon: Argon (Ar)
    :ivar xenon: Xenon (Xe)
    :ivar oxygen: Oxygen (O)
    :ivar tungsten: Tungsten (W)
    :ivar iron: Iron (Fe)
    :ivar krypton: Krypton (Kr)
    """
    class Meta:
        name = "summary_species_tor_angle"

    hydrogen: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    deuterium: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    tritium: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    helium_3: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    helium_4: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    beryllium: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    lithium: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    carbon: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    nitrogen: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    neon: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    argon: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    xenon: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    oxygen: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    tungsten: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    iron: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )
    krypton: Optional[SummaryDynamicFlt1DRootParent2] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryWall(IdsBaseClass):
    """
    Wall characteristics.

    :ivar material: Wall material
    :ivar evaporation: Chemical formula of the evaporated material or
        gas used to cover the vaccum vessel wall. NONE for no
        evaporation.
    """
    class Meta:
        name = "summary_wall"

    material: Optional[IdentifierStatic] = field(
        default=None
    )
    evaporation: Optional[SummaryStaticStr0D] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryAverageQuantities(IdsBaseClass):
    """
    Set of average quantities.

    :ivar t_e: Electron temperature
    :ivar t_i_average: Ion temperature (average over ion species)
    :ivar n_e: Electron density
    :ivar dn_e_dt: Time derivative of the electron density
    :ivar n_i: Ion density per species
    :ivar n_i_total: Total ion density (sum over species)
    :ivar zeff: Effective charge
    :ivar meff_hydrogenic: Effective mass of the hydrogenic species (MH.
        nH+MD.nD+MT.nT)/(nH+nD+nT)
    :ivar isotope_fraction_hydrogen: Fraction of hydrogen density among
        the hydrogenic species (nH/(nH+nD+nT))
    """
    class Meta:
        name = "summary_average_quantities"

    t_e: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    t_i_average: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    n_e: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    dn_e_dt: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    n_i: Optional[SummarySpecies] = field(
        default=None
    )
    n_i_total: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    zeff: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    meff_hydrogenic: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    isotope_fraction_hydrogen: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryHCdNbi(IdsBaseClass):
    """
    NBI unit.

    :ivar species: Injected species
    :ivar power: NBI power coupled to the plasma by this unit (i.e.
        without shine-through and fast ion losses)
    :ivar power_launched: NBI power launched into the vacuum vessel from
        this unit
    :ivar current: Parallel current driven by this NBI unit
    :ivar position: R, Z, Phi position of the NBI unit centre
    :ivar tangency_radius: Tangency radius (major radius where the
        central line of a NBI unit is tangent to a circle around the
        torus)
    :ivar angle: Angle of inclination between a beamlet at the centre of
        the injection unit surface and the horizontal plane
    :ivar direction: Direction of the beam seen from above the torus: -1
        = clockwise; 1 = counter clockwise
    :ivar energy: Full energy of the injected species (acceleration of a
        single atom)
    :ivar beam_current_fraction: Fractions of beam current distributed
        among the different energies, the first index corresponds to the
        fast neutrals energy (1:full, 2: half, 3: one third)
    :ivar beam_power_fraction: Fractions of beam power distributed among
        the different energies, the first index corresponds to the fast
        neutrals energy (1:full, 2: half, 3: one third)
    """
    class Meta:
        name = "summary_h_cd_nbi"

    species: Optional[SummaryPlasmaCompositionSpecies] = field(
        default=None
    )
    power: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power_launched: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    current: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    position: Optional[SummaryRzphi0DStatic] = field(
        default=None
    )
    tangency_radius: Optional[SummaryStaticFlt0D] = field(
        default=None
    )
    angle: Optional[SummaryStaticFlt0D] = field(
        default=None
    )
    direction: Optional[SummaryStaticInt0D] = field(
        default=None
    )
    energy: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    beam_current_fraction: Optional[SummaryDynamicFlt2DFraction2] = field(
        default=None
    )
    beam_power_fraction: Optional[SummaryDynamicFlt2DFraction2] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryLocalQuantities(IdsBaseClass):
    """
    Set of local quantities.

    :ivar position: Radial position at which physics quantities are
        evaluated
    :ivar t_e: Electron temperature
    :ivar t_i_average: Ion temperature (average over ion species)
    :ivar n_e: Electron density
    :ivar n_i: Ion density per species
    :ivar n_i_total: Total ion density (sum over species)
    :ivar zeff: Effective charge
    :ivar momentum_tor: Total plasma toroidal momentum, summed over ion
        species and electrons
    :ivar velocity_tor: Ion toroidal rotation velocity, per species
    :ivar q: Safety factor
    :ivar magnetic_shear: Magnetic shear, defined as rho_tor/q .
        dq/drho_tor
    :ivar e_field_parallel: Average on the magnetic surface of
        (e_field.b_field) / B0, where B0 is global_quantities/b0/value
    """
    class Meta:
        name = "summary_local_quantities"

    position: Optional[SummaryLocalPosition] = field(
        default=None
    )
    t_e: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    t_i_average: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    n_e: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    n_i: Optional[SummarySpecies] = field(
        default=None
    )
    n_i_total: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    zeff: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    momentum_tor: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    velocity_tor: Optional[SummarySpeciesTorAngle] = field(
        default=None
    )
    q: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    magnetic_shear: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    e_field_parallel: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryLocalQuantitiesNoPositionName(IdsBaseClass):
    """
    Set of local quantities without radial position, for localisations outside the
    LCFS, with a name.

    :ivar name: Name of the limiter or divertor plate. Standard names
        are : LI (resp. LO) for lower inner (resp. outer) plates;  UI
        (resp. UO) for upper inner (resp. outer) plates.
    :ivar t_e: Electron temperature
    :ivar t_i_average: Ion temperature (average over ion species)
    :ivar n_e: Electron density
    :ivar n_i: Ion density per species
    :ivar n_i_total: Total ion density (sum over species)
    :ivar zeff: Effective charge
    :ivar flux_expansion: Magnetic flux expansion as defined by Stangeby
        : ratio between the poloidal field at the midplane separatrix
        and the poloidal field at the strike-point see formula attached,
        where u means upstream (midplane separatrix) and t means at
        divertor target (downstream).
    :ivar power_flux_peak: Peak power flux on the divertor target or
        limiter surface
    """
    class Meta:
        name = "summary_local_quantities_no_position_name"

    name: Optional[SummaryStaticStr0D] = field(
        default=None
    )
    t_e: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    t_i_average: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    n_e: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    n_i: Optional[SummarySpecies] = field(
        default=None
    )
    n_i_total: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    zeff: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    flux_expansion: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power_flux_peak: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryLocalQuantitiesRZ(IdsBaseClass):
    """
    Set of local quantities, including an R,Z position.

    :ivar position: Radial position at which physics quantities are
        evaluated
    :ivar t_e: Electron temperature
    :ivar t_i_average: Ion temperature (average over ion species)
    :ivar n_e: Electron density
    :ivar n_i: Ion density per species
    :ivar n_i_total: Total ion density (sum over species)
    :ivar zeff: Effective charge
    :ivar momentum_tor: Total plasma toroidal momentum, summed over ion
        species and electrons
    :ivar velocity_tor: Ion toroidal rotation velocity, per species
    :ivar q: Safety factor (IMAS uses COCOS=11: only positive when
        toroidal current and magnetic field are in same direction)
    :ivar magnetic_shear: Magnetic shear, defined as rho_tor/q .
        dq/drho_tor
    :ivar b_field: Magnetic field
    :ivar e_field_parallel: Average on the magnetic surface of
        (e_field.b_field) / B0, where B0 is global_quantities/b0/value
    """
    class Meta:
        name = "summary_local_quantities_r_z"

    position: Optional[SummaryLocalPositionRZ] = field(
        default=None
    )
    t_e: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    t_i_average: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    n_e: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    n_i: Optional[SummarySpecies] = field(
        default=None
    )
    n_i_total: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    zeff: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    momentum_tor: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    velocity_tor: Optional[SummarySpeciesTorAngle] = field(
        default=None
    )
    q: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    magnetic_shear: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    b_field: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    e_field_parallel: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryNeutron(IdsBaseClass):
    """
    Description of neutron fluxes.

    :ivar total: Total neutron flux from all reactions
    :ivar thermal: Neutron flux from all plasma thermal reactions
    :ivar dd: Neutron fluxes from DD reactions
    :ivar dt: Neutron fluxes from DT reactions
    :ivar tt: Neutron fluxes from TT reactions
    """
    class Meta:
        name = "summary_neutron"

    total: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    thermal: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    dd: Optional[SummaryNeutronReaction] = field(
        default=None
    )
    dt: Optional[SummaryNeutronReaction] = field(
        default=None
    )
    tt: Optional[SummaryNeutronReaction] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryNeutronRates(IdsBaseClass):
    """
    Description of neutron rates.

    :ivar total: Total neutron rate from all reactions
    :ivar thermal: Neutron rate from all plasma thermal reactions
    :ivar dd: Neutron rates from DD reactions
    :ivar dt: Neutron rates from DT reactions
    :ivar tt: Neutron rates from TT reactions
    """
    class Meta:
        name = "summary_neutron_rates"

    total: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    thermal: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    dd: Optional[SummaryNeutronRatesReaction] = field(
        default=None
    )
    dt: Optional[SummaryNeutronRatesReaction] = field(
        default=None
    )
    tt: Optional[SummaryNeutronRatesReaction] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryPedestalFitLinear(IdsBaseClass):
    """
    Quantities related to linear fit of pedestal profiles.

    :ivar n_e: Electron density related quantities
    :ivar t_e: Electron temperature related quantities
    :ivar pressure_electron: Electron pressure related quantities
    :ivar energy_thermal_pedestal_electron: Pedestal stored thermal
        energy for electrons
    :ivar energy_thermal_pedestal_ion: Pedestal stored thermal energy
        for ions
    :ivar volume_inside_pedestal: Plasma volume enclosed between the
        magnetic axis and the top of the pedestal
    :ivar beta_pol_pedestal_top_electron_average: Poloidal beta at
        pressure pedestal top for electrons using the flux surface
        average magnetic poloidal field
    :ivar beta_pol_pedestal_top_electron_lfs: Poloidal beta at pressure
        pedestal top for electrons using the low field side magnetic
        poloidal field
    :ivar beta_pol_pedestal_top_electron_hfs: Poloidal beta at pressure
        pedestal top for electrons using the high field side magnetic
        poloidal field
    :ivar nustar_pedestal_top_electron: Normalised collisionality at
        pressure pedestal top for electrons
    :ivar rhostar_pedestal_top_electron_lfs: Normalised Larmor radius at
        pressure pedestal top for electrons using the low field side
        magnetic field (important for spherical tokamaks)
    :ivar rhostar_pedestal_top_electron_hfs: Normalised Larmor radius at
        pressure pedestal top for electrons using the high field side
        magnetic field (important for spherical tokamaks)
    :ivar rhostar_pedestal_top_electron_magnetic_axis: Normalised Larmor
        radius at pressure pedestal top for electrons using the magnetic
        field on the magnetic axis (definition used in most tokamak
        literature)
    :ivar b_field_pol_pedestal_top_average: Poloidal field calculated at
        the position of the pressure pedestal top (as determined by the
        fit) and averaged over the flux surface
    :ivar b_field_pol_pedestal_top_hfs: Poloidal field calculated at the
        position of the pressure pedestal top (as determined by the fit)
        on the high field side
    :ivar b_field_pol_pedestal_top_lfs: Poloidal field calculated at the
        position of the pressure pedestal top (as determined by the fit)
        on the low field side
    :ivar b_field_pedestal_top_hfs: Total magnetic field calculated at
        the position of the pressure pedestal top (as determined by the
        fit) on the high field side
    :ivar b_field_pedestal_top_lfs: Total magnetic field calculated at
        the position of the pressure pedestal top (as determined by the
        fit) on the low field side
    :ivar b_field_tor_pedestal_top_hfs: Toroidal field calculated at the
        position of the pressure pedestal top (as determined by the fit)
        on the high field side
    :ivar b_field_tor_pedestal_top_lfs: Toroidal field calculated at the
        position of the pressure pedestal top (as determined by the fit)
        on the low field side
    :ivar coulomb_factor_pedestal_top: Coulomb factor log(lambda) at the
        position of the pressure pedestal top (as determined by the fit)
    :ivar parameters: Parameters of the fit
    """
    class Meta:
        name = "summary_pedestal_fit_linear"

    n_e: Optional[SummaryPedestalFitLinearNe] = field(
        default=None
    )
    t_e: Optional[SummaryPedestalFitLinearTe] = field(
        default=None
    )
    pressure_electron: Optional[SummaryPedestalFitNe] = field(
        default=None
    )
    energy_thermal_pedestal_electron: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    energy_thermal_pedestal_ion: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    volume_inside_pedestal: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    beta_pol_pedestal_top_electron_average: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    beta_pol_pedestal_top_electron_lfs: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    beta_pol_pedestal_top_electron_hfs: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    nustar_pedestal_top_electron: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    rhostar_pedestal_top_electron_lfs: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    rhostar_pedestal_top_electron_hfs: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    rhostar_pedestal_top_electron_magnetic_axis: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    b_field_pol_pedestal_top_average: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    b_field_pol_pedestal_top_hfs: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    b_field_pol_pedestal_top_lfs: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    b_field_pedestal_top_hfs: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    b_field_pedestal_top_lfs: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    b_field_tor_pedestal_top_hfs: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    b_field_tor_pedestal_top_lfs: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    coulomb_factor_pedestal_top: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    parameters: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryPedestalFitStability(IdsBaseClass):
    """
    MHD stability analysis of the pedestal (for a given fit of the profiles)

    :ivar alpha_experimental: Experimental normalized pressure gradient
        reconstructed by an MHD stability code (with assumptions on the
        ion pressure). See definition in [Miller PoP 5 (1998),973,Eq.
        42]
    :ivar bootstrap_current_sauter: MHD calculations of the critical
        alpha parameter using the Sauter formula for the calculation of
        the bootstrap current, from Phys. Plasmas 6 (1999) 2834
    :ivar bootstrap_current_hager: MHD calculations of the critical
        alpha parameter using the Hager formula for the calculation of
        the bootstrap current, from Phys. Plasmas 23 (2016) 042503
    """
    class Meta:
        name = "summary_pedestal_fit_stability"

    alpha_experimental: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    bootstrap_current_sauter: Optional[SummaryPedestalFitStabilityMethod] = field(
        default=None
    )
    bootstrap_current_hager: Optional[SummaryPedestalFitStabilityMethod] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryFusion(IdsBaseClass):
    """
    Fusion reactions.

    :ivar power: Power coupled to the plasma by fusion reactions
    :ivar current: Parallel current driven by this fusion reactions
    :ivar neutron_fluxes: Neutron fluxes from various reactions
    :ivar neutron_rates: Neutron rates from various reactions
    :ivar neutron_power_total: Total neutron power (from all reactions).
        Sum over each type of reaction (DD, DT, TT for thermal, beam-
        plasma, beam-beam, etc.) of the neutron production rate times
        the average neutron birth energy
    """
    class Meta:
        name = "summary_fusion"

    power: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    current: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    neutron_fluxes: Optional[SummaryNeutron] = field(
        default=None
    )
    neutron_rates: Optional[SummaryNeutronRates] = field(
        default=None
    )
    neutron_power_total: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryHCd(IdsBaseClass):
    """
    Heating and current drive related parameters.

    :ivar ec: Set of ECRH/ECCD launchers
    :ivar nbi: Set of NBI units
    :ivar ic: Set of ICRH launchers
    :ivar lh: Set of LHCD launchers
    :ivar power_ec: Total EC power coupled to the plasma
    :ivar power_launched_ec: Total EC power launched from EC launchers
        into the vacuum vessel
    :ivar power_nbi: Total NBI power coupled to the plasma
    :ivar power_launched_nbi: Total NBI power launched from neutral beam
        injectors into the vacuum vessel
    :ivar power_launched_nbi_co_injected_ratio: Ratio of co-injected
        beam launched power to total NBI launched power. Is set to 1 for
        purely perpendicular injection
    :ivar power_ic: Total IC power coupled to the plasma
    :ivar power_launched_ic: Total IC power launched from IC antennas
        into the vacuum vessel
    :ivar power_lh: Total LH power coupled to the plasma
    :ivar power_launched_lh: Total LH power launched from LH antennas
        into the vacuum vessel
    :ivar power_additional: Total additional external power
        (NBI+EC+IC+LH, without ohmic) coupled to the plasma
    """
    class Meta:
        name = "summary_h_cd"

    ec: list[SummaryHCdEc] = field(
        default_factory=list,
        metadata={
            "max_occurs": 6,
        }
    )
    nbi: list[SummaryHCdNbi] = field(
        default_factory=list,
        metadata={
            "max_occurs": 32,
        }
    )
    ic: list[SummaryHCdIc] = field(
        default_factory=list,
        metadata={
            "max_occurs": 6,
        }
    )
    lh: list[SummaryHCdLh] = field(
        default_factory=list,
        metadata={
            "max_occurs": 6,
        }
    )
    power_ec: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power_launched_ec: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power_nbi: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power_launched_nbi: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power_launched_nbi_co_injected_ratio: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power_ic: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power_launched_ic: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power_lh: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power_launched_lh: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    power_additional: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryLocal(IdsBaseClass):
    """
    Set of locations.

    :ivar magnetic_axis: Parameters at magnetic axis
    :ivar separatrix: Parameters at separatrix (intersection of the
        separatrix and the outboard midplane)
    :ivar separatrix_average: Flux surface averaged parameters at
        separatrix (flux-surface average over the entire core-SOL
        boundary separatrix)
    :ivar pedestal: Parameters at pedestal top
    :ivar itb: Parameters at internal transport barrier
    :ivar limiter: Parameters at the limiter tangency point
    :ivar divertor_plate: Parameters at a divertor plate
    :ivar divertor_target: Parameters at a divertor target
    :ivar r_eff_norm_2_3: Parameters at r_eff_norm = 2/3, where
        r_eff_norm is the stellarator effective minor radius normalised
        to its value at the last closed flux surface
    """
    class Meta:
        name = "summary_local"

    magnetic_axis: Optional[SummaryLocalQuantitiesRZ] = field(
        default=None
    )
    separatrix: Optional[SummaryLocalQuantities] = field(
        default=None
    )
    separatrix_average: Optional[SummaryLocalQuantities] = field(
        default=None
    )
    pedestal: Optional[SummaryLocalQuantities] = field(
        default=None
    )
    itb: Optional[SummaryLocalQuantities] = field(
        default=None
    )
    limiter: Optional[SummaryLocalQuantitiesNoPositionName] = field(
        default=None
    )
    divertor_plate: list[SummaryLocalQuantitiesNoPositionName] = field(
        default_factory=list,
        metadata={
            "max_occurs": 4,
        }
    )
    divertor_target: list[SummaryLocalQuantitiesNoPositionName] = field(
        default_factory=list,
        metadata={
            "max_occurs": 4,
        }
    )
    r_eff_norm_2_3: Optional[SummaryLocalQuantitiesStellerator] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryPedestalFit(IdsBaseClass):
    """
    Quantities related to generic fit of pedestal profiles.

    :ivar n_e: Electron density related quantities
    :ivar t_e: Electron temperature related quantities
    :ivar pressure_electron: Electron pressure related quantities
    :ivar energy_thermal_pedestal_electron: Pedestal stored thermal
        energy for electrons
    :ivar energy_thermal_pedestal_ion: Pedestal stored thermal energy
        for ions
    :ivar volume_inside_pedestal: Plasma volume enclosed between the
        magnetic axis and the top of the pedestal
    :ivar alpha_electron_pedestal_max: Maximum value in the pedestal of
        the alpha parameter for electron pressure (see [Miller PoP 5
        (1998),973,Eq. 42])
    :ivar alpha_electron_pedestal_max_position: Position in normalised
        poloidal flux of the maximum value in the pedestal of the alpha
        parameter for electron pressure (see [Miller PoP 5
        (1998),973,Eq. 42])
    :ivar beta_pol_pedestal_top_electron_average: Poloidal beta at
        pressure pedestal top for electrons using the flux surface
        average magnetic poloidal field
    :ivar beta_pol_pedestal_top_electron_lfs: Poloidal beta at pedestal
        top for electrons using the low field side magnetic poloidal
        field
    :ivar beta_pol_pedestal_top_electron_hfs: Poloidal beta at pressure
        pedestal top for electrons using the high field side magnetic
        poloidal field
    :ivar nustar_pedestal_top_electron: Normalised collisionality at
        pressure pedestal top for electrons
    :ivar rhostar_pedestal_top_electron_lfs: Normalised Larmor radius at
        pressure pedestal top for electrons using the low field side
        magnetic field (important for spherical tokamaks)
    :ivar rhostar_pedestal_top_electron_hfs: Normalised Larmor radius at
        pressure pedestal top for electrons using the high field side
        magnetic field (important for spherical tokamaks)
    :ivar rhostar_pedestal_top_electron_magnetic_axis: Normalised Larmor
        radius at pressure pedestal top for electrons using the magnetic
        field on the magnetic axis (definition used in most tokamak
        litterature)
    :ivar b_field_pol_pedestal_top_average: Poloidal field calculated at
        the position of the pressure pedestal top (as determined by the
        fit) and averaged over the flux surface
    :ivar b_field_pol_pedestal_top_hfs: Poloidal field calculated at the
        position of the pressure pedestal top (as determined by the fit)
        on the high field side
    :ivar b_field_pol_pedestal_top_lfs: Poloidal field calculated at the
        position of the pressure pedestal top (as determined by the fit)
        on the low field side
    :ivar b_field_pedestal_top_hfs: Total magnetic field calculated at
        the position of the pressure pedestal top (as determined by the
        fit) on the high field side
    :ivar b_field_pedestal_top_lfs: Total magnetic field calculated at
        the position of the pressure pedestal top (as determined by the
        fit) on the low field side
    :ivar b_field_tor_pedestal_top_hfs: Toroidal field calculated at the
        position of the pressure pedestal top (as determined by the fit)
        on the high field side
    :ivar b_field_tor_pedestal_top_lfs: Toroidal field calculated at the
        position of the pressure pedestal top (as determined by the fit)
        on the low field side
    :ivar coulomb_factor_pedestal_top: Coulomb factor log(lambda) at the
        position of the pressure pedestal top (as determined by the fit)
    :ivar stability: MHD stability analysis of the pedestal (for this
        fit of the profiles)
    :ivar parameters: Parameters of the fit
    """
    class Meta:
        name = "summary_pedestal_fit"

    n_e: Optional[SummaryPedestalFitNe] = field(
        default=None
    )
    t_e: Optional[SummaryPedestalFitTe] = field(
        default=None
    )
    pressure_electron: Optional[SummaryPedestalFitNe] = field(
        default=None
    )
    energy_thermal_pedestal_electron: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    energy_thermal_pedestal_ion: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    volume_inside_pedestal: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    alpha_electron_pedestal_max: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    alpha_electron_pedestal_max_position: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    beta_pol_pedestal_top_electron_average: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    beta_pol_pedestal_top_electron_lfs: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    beta_pol_pedestal_top_electron_hfs: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    nustar_pedestal_top_electron: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    rhostar_pedestal_top_electron_lfs: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    rhostar_pedestal_top_electron_hfs: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    rhostar_pedestal_top_electron_magnetic_axis: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    b_field_pol_pedestal_top_average: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    b_field_pol_pedestal_top_hfs: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    b_field_pol_pedestal_top_lfs: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    b_field_pedestal_top_hfs: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    b_field_pedestal_top_lfs: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    b_field_tor_pedestal_top_hfs: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    b_field_tor_pedestal_top_lfs: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    coulomb_factor_pedestal_top: Optional[SummaryDynamicFlt1DRoot] = field(
        default=None
    )
    stability: Optional[SummaryPedestalFitStability] = field(
        default=None
    )
    parameters: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class SummaryPedestalFits(IdsBaseClass):
    """
    Quantities derived from specific fits of pedestal profiles, typically used in
    the Pedestal Database.

    :ivar mtanh: Quantities related to "mtanh" fit
    :ivar linear: Quantities related to linear fit
    """
    class Meta:
        name = "summary_pedestal_fits"

    mtanh: Optional[SummaryPedestalFit] = field(
        default=None
    )
    linear: Optional[SummaryPedestalFitLinear] = field(
        default=None
    )


@dataclass(slots=True)
class Summary(IdsBaseClass):
    """Summary of physics quantities from a simulation or an experiment.

    Dynamic quantities are either taken at given time slices (indicated
    in the "time" vector) or time-averaged over an interval (in such
    case the "time_width" of the interval is indicated and the "time"
    vector represents the end of each time interval).

    :ivar ids_properties:
    :ivar tag: Tag qualifying this data entry (or a list of data
        entries)
    :ivar configuration: Device configuration (the content may be
        device-specific)
    :ivar magnetic_shear_flag: Magnetic field shear indicator for
        stellarators: 0 for shearless stellarators (W7-A, W7-AS, W7-X);
        1, otherwise. See [Stroth U. et al 1996 Nucl. Fusion 36 1063]
    :ivar stationary_phase_flag: This flag is set to one if the pulse is
        in a stationary phase from the point of the of the energy
        content (if the time derivative of the energy dW/dt can be
        neglected when calculating tau_E as W/(P_abs-dW/dt).)
    :ivar midplane: Choice of midplane definition (use the lowest index
        number if more than one value is relevant)
    :ivar global_quantities: Various global quantities derived from the
        profiles
    :ivar local: Plasma parameter values at different locations
    :ivar boundary: Description of the plasma boundary
    :ivar pedestal_fits: Quantities derived from specific fits of
        pedestal profiles, typically used in the Pedestal Database.
    :ivar line_average: Line average plasma parameters
    :ivar volume_average: Volume average plasma parameters
    :ivar disruption: Disruption characteristics, if the pulse is
        terminated by a disruption
    :ivar elms: Edge Localized Modes related quantities
    :ivar fusion: Fusion reactions
    :ivar gas_injection_rates: Gas injection rates in equivalent
        electrons.s^-1
    :ivar gas_injection_accumulated: Accumulated injected gas since the
        plasma breakdown in equivalent electrons
    :ivar gas_injection_prefill: Accumulated injected gas during the
        prefill in equivalent electrons
    :ivar heating_current_drive: Heating and current drive parameters
    :ivar kicks: Vertical kicks of the plasma position
    :ivar pellets: Pellet related quantities
    :ivar rmps: Resonant magnetic perturbations related quantities
    :ivar runaways: Runaway electrons
    :ivar scrape_off_layer: Scrape-Off-Layer (SOL) characteristics
    :ivar wall: Wall characteristics
    :ivar limiter: Limiter characteristics
    :ivar time_breakdown: Time of the plasma breakdown
    :ivar plasma_duration: Duration of existence of a confined plasma
        during the pulse
    :ivar time_width: In case the time-dependent quantities of this IDS
        are averaged over a time interval, this node is the width of
        this time interval (empty otherwise). By convention, the time
        interval starts at time-time_width and ends at time.
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "summary"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    tag: Optional[EntryTag] = field(
        default=None
    )
    configuration: Optional[SummaryStaticStr0D] = field(
        default=None
    )
    magnetic_shear_flag: Optional[SummaryStaticInt0D] = field(
        default=None
    )
    stationary_phase_flag: Optional[SummaryDynamicInt1DRoot] = field(
        default=None
    )
    midplane: Optional[IdentifierStatic] = field(
        default=None
    )
    global_quantities: Optional[SummaryGlobalQuantities] = field(
        default=None
    )
    local: Optional[SummaryLocal] = field(
        default=None
    )
    boundary: Optional[SummaryBoundary] = field(
        default=None
    )
    pedestal_fits: Optional[SummaryPedestalFits] = field(
        default=None
    )
    line_average: Optional[SummaryAverageQuantities] = field(
        default=None
    )
    volume_average: Optional[SummaryAverageQuantities] = field(
        default=None
    )
    disruption: Optional[SummaryDisruption] = field(
        default=None
    )
    elms: Optional[SummaryElms] = field(
        default=None
    )
    fusion: Optional[SummaryFusion] = field(
        default=None
    )
    gas_injection_rates: Optional[SummaryGasInjection] = field(
        default=None
    )
    gas_injection_accumulated: Optional[SummaryGasInjectionAccumulated] = field(
        default=None
    )
    gas_injection_prefill: Optional[SummaryGasInjectionPrefill] = field(
        default=None
    )
    heating_current_drive: Optional[SummaryHCd] = field(
        default=None
    )
    kicks: Optional[SummaryKicks] = field(
        default=None
    )
    pellets: Optional[SummaryPellets] = field(
        default=None
    )
    rmps: Optional[SummaryRmp] = field(
        default=None
    )
    runaways: Optional[SummaryRunaways] = field(
        default=None
    )
    scrape_off_layer: Optional[SummarySol] = field(
        default=None
    )
    wall: Optional[SummaryWall] = field(
        default=None
    )
    limiter: Optional[SummaryLimiter] = field(
        default=None
    )
    time_breakdown: Optional[SummaryConstantFlt0D] = field(
        default=None
    )
    plasma_duration: Optional[SummaryConstantFlt0D] = field(
        default=None
    )
    time_width: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
