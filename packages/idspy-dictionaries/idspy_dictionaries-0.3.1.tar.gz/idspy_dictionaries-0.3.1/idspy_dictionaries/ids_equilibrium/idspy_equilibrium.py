#__version__='0.3.1'
#__imas_commit__='dd6854b4d07'
#__imas_version__='3.7.1'
from ..dataclasses_idsschema import IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Dict, Optional


@dataclass(slots=True)
class BTorVacuum1(IdsBaseClass):
    """Characteristics of the vacuum toroidal field.

    Time coordinate at the root of the IDS

    :ivar r0: Reference major radius where the vacuum toroidal magnetic
        field is given (usually a fixed position such as the middle of
        the vessel at the equatorial midplane)
    :ivar b0: Vacuum toroidal field at R0 [T]; Positive sign means anti-
        clockwise when viewing from above. The product R0B0 must be
        consistent with the b_tor_vacuum_r field of the tf IDS.
    """
    class Meta:
        name = "b_tor_vacuum_1"

    r0: float = field(
        default=9e+40
    )
    b0: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class EquilibriumBoundaryClosest(IdsBaseClass):
    """
    Position and distance to the plasma boundary of the point of the first wall
    which is the closest to plasma boundary.

    :ivar r: Major radius
    :ivar z: Height
    :ivar distance: Distance to the plasma boundary
    """
    class Meta:
        name = "equilibrium_boundary_closest"

    r: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )
    distance: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class EquilibriumConstraints0D(IdsBaseClass):
    """
    Scalar constraint, no cocos transform.

    :ivar measured: Measured value
    :ivar source: Path to the source data for this measurement in the
        IMAS data dictionary
    :ivar time_measurement: Exact time slice used from the time array of
        the measurement source data. If the time slice does not exist in
        the time array of the source data, it means linear interpolation
        has been used
    :ivar exact: Integer flag : 1 means exact data, taken as an exact
        input without being fitted; 0 means the equilibrium code does a
        least square fit
    :ivar weight: Weight given to the measurement
    :ivar reconstructed: Value calculated from the reconstructed
        equilibrium
    :ivar chi_squared: Squared error normalized by the standard
        deviation considered in the minimization process : chi_squared =
        weight^2 *(reconstructed - measured)^2 / sigma^2, where sigma is
        the standard deviation of the measurement error
    """
    class Meta:
        name = "equilibrium_constraints_0D"

    measured: float = field(
        default=9e+40
    )
    source: str = field(
        default=""
    )
    time_measurement: float = field(
        default=9e+40
    )
    exact: int = field(
        default=999999999
    )
    weight: float = field(
        default=9e+40
    )
    reconstructed: float = field(
        default=9e+40
    )
    chi_squared: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class EquilibriumConstraints0DB0Like(IdsBaseClass):
    """
    Scalar constraint, b0_like cocos transform.

    :ivar measured: Measured value
    :ivar source: Path to the source data for this measurement in the
        IMAS data dictionary
    :ivar time_measurement: Exact time slice used from the time array of
        the measurement source data. If the time slice does not exist in
        the time array of the source data, it means linear interpolation
        has been used
    :ivar exact: Integer flag : 1 means exact data, taken as an exact
        input without being fitted; 0 means the equilibrium code does a
        least square fit
    :ivar weight: Weight given to the measurement
    :ivar reconstructed: Value calculated from the reconstructed
        equilibrium
    :ivar chi_squared: Squared error normalized by the standard
        deviation considered in the minimization process : chi_squared =
        weight^2 *(reconstructed - measured)^2 / sigma^2, where sigma is
        the standard deviation of the measurement error
    """
    class Meta:
        name = "equilibrium_constraints_0D_b0_like"

    measured: float = field(
        default=9e+40
    )
    source: str = field(
        default=""
    )
    time_measurement: float = field(
        default=9e+40
    )
    exact: int = field(
        default=999999999
    )
    weight: float = field(
        default=9e+40
    )
    reconstructed: float = field(
        default=9e+40
    )
    chi_squared: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class EquilibriumConstraints0DIpLike(IdsBaseClass):
    """
    Scalar constraint, ip_like cocos transform.

    :ivar measured: Measured value
    :ivar source: Path to the source data for this measurement in the
        IMAS data dictionary
    :ivar time_measurement: Exact time slice used from the time array of
        the measurement source data. If the time slice does not exist in
        the time array of the source data, it means linear interpolation
        has been used
    :ivar exact: Integer flag : 1 means exact data, taken as an exact
        input without being fitted; 0 means the equilibrium code does a
        least square fit
    :ivar weight: Weight given to the measurement
    :ivar reconstructed: Value calculated from the reconstructed
        equilibrium
    :ivar chi_squared: Squared error normalized by the standard
        deviation considered in the minimization process : chi_squared =
        weight^2 *(reconstructed - measured)^2 / sigma^2, where sigma is
        the standard deviation of the measurement error
    """
    class Meta:
        name = "equilibrium_constraints_0D_ip_like"

    measured: float = field(
        default=9e+40
    )
    source: str = field(
        default=""
    )
    time_measurement: float = field(
        default=9e+40
    )
    exact: int = field(
        default=999999999
    )
    weight: float = field(
        default=9e+40
    )
    reconstructed: float = field(
        default=9e+40
    )
    chi_squared: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class EquilibriumConstraints0DOneLike(IdsBaseClass):
    """
    Scalar constraint, one_like cocos transform.

    :ivar measured: Measured value
    :ivar source: Path to the source data for this measurement in the
        IMAS data dictionary
    :ivar time_measurement: Exact time slice used from the time array of
        the measurement source data. If the time slice does not exist in
        the time array of the source data, it means linear interpolation
        has been used
    :ivar exact: Integer flag : 1 means exact data, taken as an exact
        input without being fitted; 0 means the equilibrium code does a
        least square fit
    :ivar weight: Weight given to the measurement
    :ivar reconstructed: Value calculated from the reconstructed
        equilibrium
    :ivar chi_squared: Squared error normalized by the standard
        deviation considered in the minimization process : chi_squared =
        weight^2 *(reconstructed - measured)^2 / sigma^2, where sigma is
        the standard deviation of the measurement error
    """
    class Meta:
        name = "equilibrium_constraints_0D_one_like"

    measured: float = field(
        default=9e+40
    )
    source: str = field(
        default=""
    )
    time_measurement: float = field(
        default=9e+40
    )
    exact: int = field(
        default=999999999
    )
    weight: float = field(
        default=9e+40
    )
    reconstructed: float = field(
        default=9e+40
    )
    chi_squared: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class EquilibriumConstraints0DPsiLike(IdsBaseClass):
    """
    Scalar constraint, psi_like cocos transform.

    :ivar measured: Measured value
    :ivar source: Path to the source data for this measurement in the
        IMAS data dictionary
    :ivar time_measurement: Exact time slice used from the time array of
        the measurement source data. If the time slice does not exist in
        the time array of the source data, it means linear interpolation
        has been used
    :ivar exact: Integer flag : 1 means exact data, taken as an exact
        input without being fitted; 0 means the equilibrium code does a
        least square fit
    :ivar weight: Weight given to the measurement
    :ivar reconstructed: Value calculated from the reconstructed
        equilibrium
    :ivar chi_squared: Squared error normalized by the standard
        deviation considered in the minimization process : chi_squared =
        weight^2 *(reconstructed - measured)^2 / sigma^2, where sigma is
        the standard deviation of the measurement error
    """
    class Meta:
        name = "equilibrium_constraints_0D_psi_like"

    measured: float = field(
        default=9e+40
    )
    source: str = field(
        default=""
    )
    time_measurement: float = field(
        default=9e+40
    )
    exact: int = field(
        default=999999999
    )
    weight: float = field(
        default=9e+40
    )
    reconstructed: float = field(
        default=9e+40
    )
    chi_squared: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class EquilibriumGap(IdsBaseClass):
    """
    Gap for describing the plasma boundary.

    :ivar name: Name of the gap
    :ivar identifier: Identifier of the gap
    :ivar r: Major radius of the reference point
    :ivar z: Height of the reference point
    :ivar angle: Angle measured clockwise from radial cylindrical vector
        (grad R) to gap vector (pointing away from reference point)
    :ivar value: Value of the gap, i.e. distance between the reference
        point and the separatrix along the gap direction
    """
    class Meta:
        name = "equilibrium_gap"

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
    value: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class EquilibriumGlobalQuantitiesCurrentCentre(IdsBaseClass):
    """
    R, Z, and vertical velocity of current centre, dynamic within a type 3 array of
    structure (index on time)

    :ivar r: Major radius of the current center, defined as integral
        over the poloidal cross section of (j_tor*r*dS) / Ip
    :ivar z: Height of the current center, defined as integral over the
        poloidal cross section of (j_tor*z*dS) / Ip
    :ivar velocity_z: Vertical velocity of the current center
    """
    class Meta:
        name = "equilibrium_global_quantities_current_centre"

    r: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )
    velocity_z: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class EquilibriumGlobalQuantitiesMagneticAxis(IdsBaseClass):
    """
    R, Z, and Btor at magnetic axis, dynamic within a type 3 array of structure
    (index on time)

    :ivar r: Major radius of the magnetic axis
    :ivar z: Height of the magnetic axis
    :ivar b_tor: Total toroidal magnetic field at the magnetic axis
    :ivar b_field_tor: Total toroidal magnetic field at the magnetic
        axis
    """
    class Meta:
        name = "equilibrium_global_quantities_magnetic_axis"

    r: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )
    b_tor: float = field(
        default=9e+40
    )
    b_field_tor: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class EquilibriumGlobalQuantitiesQmin(IdsBaseClass):
    """
    Position and value of q_min.

    :ivar value: Minimum q value
    :ivar rho_tor_norm: Minimum q position in normalised toroidal flux
        coordinate
    """
    class Meta:
        name = "equilibrium_global_quantities_qmin"

    value: float = field(
        default=9e+40
    )
    rho_tor_norm: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class EquilibriumProfiles1DRz1DDynamicAos(IdsBaseClass):
    """
    Structure for list of R, Z positions (1D list of Npoints, dynamic within a type
    3 array of structures (index on time)), with coordinates referring to
    profiles_1d/psi.

    :ivar r: Major radius
    :ivar z: Height
    """
    class Meta:
        name = "equilibrium_profiles_1d_rz1d_dynamic_aos"

    r: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    z: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class EquilibriumProfiles2DGrid(IdsBaseClass):
    """
    Definition of the 2D grid.

    :ivar dim1: First dimension values
    :ivar dim2: Second dimension values
    :ivar volume_element: Elementary plasma volume of plasma enclosed in
        the cell formed by the nodes [dim1(i) dim2(j)], [dim1(i+1)
        dim2(j)], [dim1(i) dim2(j+1)] and [dim1(i+1) dim2(j+1)]
    """
    class Meta:
        name = "equilibrium_profiles_2d_grid"

    dim1: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    dim2: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    volume_element: Optional[ndarray[(int,int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class GenericGridDynamicGridSubsetElementObject(IdsBaseClass):
    """
    Generic grid, object part of an element part of a grid_subset (dynamic within a
    type 3 AoS)

    :ivar space: Index of the space from which that object is taken
    :ivar dimension: Dimension of the object
    :ivar index: Object index
    """
    class Meta:
        name = "generic_grid_dynamic_grid_subset_element_object"

    space: int = field(
        default=999999999
    )
    dimension: int = field(
        default=999999999
    )
    index: int = field(
        default=999999999
    )


@dataclass(slots=True)
class GenericGridDynamicGridSubsetMetric(IdsBaseClass):
    """
    Generic grid, metric description for a given grid_subset and base (dynamic
    within a type 3 AoS)

    :ivar jacobian: Metric Jacobian
    :ivar tensor_covariant: Covariant metric tensor, given on each
        element of the subgrid (first dimension)
    :ivar tensor_contravariant: Contravariant metric tensor, given on
        each element of the subgrid (first dimension)
    """
    class Meta:
        name = "generic_grid_dynamic_grid_subset_metric"

    jacobian: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    tensor_covariant: Optional[ndarray[(int,int, int), float]] = field(
        default=None
    )
    tensor_contravariant: Optional[ndarray[(int,int, int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class GenericGridDynamicSpaceDimensionObjectBoundary(IdsBaseClass):
    """
    Generic grid, description of an object boundary and its neighbours (dynamic
    within a type 3 AoS)

    :ivar index: Index of this (n-1)-dimensional boundary object
    :ivar neighbours: List of indices of the n-dimensional objects
        adjacent to the given n-dimensional object. An object can
        possibly have multiple neighbours on a boundary
    """
    class Meta:
        name = "generic_grid_dynamic_space_dimension_object_boundary"

    index: int = field(
        default=999999999
    )
    neighbours: Optional[ndarray[(int,), int]] = field(
        default=None
    )


@dataclass(slots=True)
class GenericGridScalar(IdsBaseClass):
    """
    Scalar values on a generic grid (dynamic within a type 3 AoS)

    :ivar grid_index: Index of the grid used to represent this quantity
    :ivar grid_subset_index: Index of the grid subset the data is
        provided on
    :ivar values: One scalar value is provided per element in the grid
        subset.
    :ivar coefficients: Interpolation coefficients, to be used for a
        high precision evaluation of the physical quantity with finite
        elements, provided per element in the grid subset (first
        dimension).
    """
    class Meta:
        name = "generic_grid_scalar"

    grid_index: int = field(
        default=999999999
    )
    grid_subset_index: int = field(
        default=999999999
    )
    values: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    coefficients: Optional[ndarray[(int,int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class IdentifierDynamicAos3(IdsBaseClass):
    """Standard type for identifiers (dynamic within type 3 array of structures
    (index on time)).

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
        name = "identifier_dynamic_aos3"

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
class Rz0DDynamicAos(IdsBaseClass):
    """
    Structure for scalar R, Z positions, dynamic within a type 3 array of
    structures (index on time)

    :ivar r: Major radius
    :ivar z: Height
    """
    class Meta:
        name = "rz0d_dynamic_aos"

    r: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class Rz1DDynamicAos(IdsBaseClass):
    """
    Structure for list of R, Z positions (1D list of Npoints, dynamic within a type
    3 array of structures (index on time))

    :ivar r: Major radius
    :ivar z: Height
    """
    class Meta:
        name = "rz1d_dynamic_aos"

    r: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    z: Optional[ndarray[(int,), float]] = field(
        default=None
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
class EquilibriumBoundary(IdsBaseClass):
    """Geometry of the plasma boundary typically taken at psi_norm = 99.x % of the separatrix

    :ivar type: 0 (limiter) or 1 (diverted)
    :ivar outline: RZ outline of the plasma boundary
    :ivar lcfs: RZ description of the plasma boundary
    :ivar psi_norm: Value of the normalised poloidal flux at which the
        boundary is taken (typically 99.x %), the flux being normalised
        to its value at the separatrix
    :ivar b_flux_pol_norm: Value of the normalised poloidal flux at
        which the boundary is taken
    :ivar psi: Value of the poloidal flux at which the boundary is taken
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
    :ivar squareness_upper_inner: Upper inner squareness of the plasma
        boundary (definition from T. Luce, Plasma Phys. Control. Fusion
        55 (2013) 095009)
    :ivar squareness_upper_outer: Upper outer squareness of the plasma
        boundary (definition from T. Luce, Plasma Phys. Control. Fusion
        55 (2013) 095009)
    :ivar squareness_lower_inner: Lower inner squareness of the plasma
        boundary (definition from T. Luce, Plasma Phys. Control. Fusion
        55 (2013) 095009)
    :ivar squareness_lower_outer: Lower outer squareness of the plasma
        boundary (definition from T. Luce, Plasma Phys. Control. Fusion
        55 (2013) 095009)
    :ivar x_point: Array of X-points, for each of them the RZ position
        is given
    :ivar strike_point: Array of strike points, for each of them the RZ
        position is given
    :ivar active_limiter_point: RZ position of the active limiter point
        (point of the plasma boundary in contact with the limiter)
    """
    class Meta:
        name = "equilibrium_boundary"

    type: int = field(
        default=999999999
    )
    outline: Optional[Rz1DDynamicAos] = field(
        default=None
    )
    lcfs: Optional[Rz1DDynamicAos] = field(
        default=None
    )
    psi_norm: float = field(
        default=9e+40
    )
    b_flux_pol_norm: float = field(
        default=9e+40
    )
    psi: float = field(
        default=9e+40
    )
    geometric_axis: Optional[Rz0DDynamicAos] = field(
        default=None
    )
    minor_radius: float = field(
        default=9e+40
    )
    elongation: float = field(
        default=9e+40
    )
    elongation_upper: float = field(
        default=9e+40
    )
    elongation_lower: float = field(
        default=9e+40
    )
    triangularity: float = field(
        default=9e+40
    )
    triangularity_upper: float = field(
        default=9e+40
    )
    triangularity_lower: float = field(
        default=9e+40
    )
    squareness_upper_inner: float = field(
        default=9e+40
    )
    squareness_upper_outer: float = field(
        default=9e+40
    )
    squareness_lower_inner: float = field(
        default=9e+40
    )
    squareness_lower_outer: float = field(
        default=9e+40
    )
    x_point: list[Rz0DDynamicAos] = field(
        default_factory=list
    )
    strike_point: list[Rz0DDynamicAos] = field(
        default_factory=list
    )
    active_limiter_point: Optional[Rz0DDynamicAos] = field(
        default=None
    )


@dataclass(slots=True)
class EquilibriumBoundarySecondSeparatrix(IdsBaseClass):
    """
    Geometry of the plasma boundary at the secondary separatrix.

    :ivar outline: RZ outline of the plasma boundary
    :ivar psi: Value of the poloidal flux at the separatrix
    :ivar distance_inner_outer: Distance between the inner and outer
        separatrices, in the major radius direction, at the plasma
        outboard and at the height corresponding to the maximum R for
        the inner separatrix.
    :ivar x_point: Array of X-points, for each of them the RZ position
        is given
    :ivar strike_point: Array of strike points, for each of them the RZ
        position is given
    """
    class Meta:
        name = "equilibrium_boundary_second_separatrix"

    outline: Optional[Rz1DDynamicAos] = field(
        default=None
    )
    psi: float = field(
        default=9e+40
    )
    distance_inner_outer: float = field(
        default=9e+40
    )
    x_point: list[Rz0DDynamicAos] = field(
        default_factory=list
    )
    strike_point: list[Rz0DDynamicAos] = field(
        default_factory=list
    )


@dataclass(slots=True)
class EquilibriumBoundarySeparatrix(IdsBaseClass):
    """
    Geometry of the plasma boundary at the separatrix.

    :ivar type: 0 (limiter) or 1 (diverted)
    :ivar outline: RZ outline of the plasma boundary
    :ivar psi: Value of the poloidal flux at the separatrix
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
    :ivar squareness_upper_inner: Upper inner squareness of the plasma
        boundary (definition from T. Luce, Plasma Phys. Control. Fusion
        55 (2013) 095009)
    :ivar squareness_upper_outer: Upper outer squareness of the plasma
        boundary (definition from T. Luce, Plasma Phys. Control. Fusion
        55 (2013) 095009)
    :ivar squareness_lower_inner: Lower inner squareness of the plasma
        boundary (definition from T. Luce, Plasma Phys. Control. Fusion
        55 (2013) 095009)
    :ivar squareness_lower_outer: Lower outer squareness of the plasma
        boundary (definition from T. Luce, Plasma Phys. Control. Fusion
        55 (2013) 095009)
    :ivar x_point: Array of X-points, for each of them the RZ position
        is given
    :ivar strike_point: Array of strike points, for each of them the RZ
        position is given
    :ivar active_limiter_point: RZ position of the active limiter point
        (point of the plasma boundary in contact with the limiter)
    :ivar closest_wall_point: Position and distance to the plasma
        boundary of the point of the first wall which is the closest to
        plasma boundary
    :ivar dr_dz_zero_point: Outboard point on the separatrix on which
        dr/dz = 0 (local maximum of the major radius of the separatrix).
        In case of multiple local maxima, the closest one from
        z=z_magnetic_axis is chosen.
    :ivar gap: Set of gaps, defined by a reference point and a
        direction.
    """
    class Meta:
        name = "equilibrium_boundary_separatrix"

    type: int = field(
        default=999999999
    )
    outline: Optional[Rz1DDynamicAos] = field(
        default=None
    )
    psi: float = field(
        default=9e+40
    )
    geometric_axis: Optional[Rz0DDynamicAos] = field(
        default=None
    )
    minor_radius: float = field(
        default=9e+40
    )
    elongation: float = field(
        default=9e+40
    )
    elongation_upper: float = field(
        default=9e+40
    )
    elongation_lower: float = field(
        default=9e+40
    )
    triangularity: float = field(
        default=9e+40
    )
    triangularity_upper: float = field(
        default=9e+40
    )
    triangularity_lower: float = field(
        default=9e+40
    )
    squareness_upper_inner: float = field(
        default=9e+40
    )
    squareness_upper_outer: float = field(
        default=9e+40
    )
    squareness_lower_inner: float = field(
        default=9e+40
    )
    squareness_lower_outer: float = field(
        default=9e+40
    )
    x_point: list[Rz0DDynamicAos] = field(
        default_factory=list
    )
    strike_point: list[Rz0DDynamicAos] = field(
        default_factory=list
    )
    active_limiter_point: Optional[Rz0DDynamicAos] = field(
        default=None
    )
    closest_wall_point: Optional[EquilibriumBoundaryClosest] = field(
        default=None
    )
    dr_dz_zero_point: Optional[Rz0DDynamicAos] = field(
        default=None
    )
    gap: list[EquilibriumGap] = field(
        default_factory=list
    )


@dataclass(slots=True)
class EquilibriumConstraints0DPosition(IdsBaseClass):
    """
    Scalar constraint with R,Z,phi position.

    :ivar measured: Measured value
    :ivar position: Position at which this measurement is given
    :ivar source: Path to the source data for this measurement in the
        IMAS data dictionary
    :ivar time_measurement: Exact time slice used from the time array of
        the measurement source data. If the time slice does not exist in
        the time array of the source data, it means linear interpolation
        has been used
    :ivar exact: Integer flag : 1 means exact data, taken as an exact
        input without being fitted; 0 means the equilibrium code does a
        least square fit
    :ivar weight: Weight given to the measurement
    :ivar reconstructed: Value calculated from the reconstructed
        equilibrium
    :ivar chi_squared: Squared error normalized by the standard
        deviation considered in the minimization process : chi_squared =
        weight^2 *(reconstructed - measured)^2 / sigma^2, where sigma is
        the standard deviation of the measurement error
    """
    class Meta:
        name = "equilibrium_constraints_0D_position"

    measured: float = field(
        default=9e+40
    )
    position: Optional[Rzphi0DDynamicAos3] = field(
        default=None
    )
    source: str = field(
        default=""
    )
    time_measurement: float = field(
        default=9e+40
    )
    exact: int = field(
        default=999999999
    )
    weight: float = field(
        default=9e+40
    )
    reconstructed: float = field(
        default=9e+40
    )
    chi_squared: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class EquilibriumConstraintsMagnetisation(IdsBaseClass):
    """
    Magnetisation constraints along R and Z axis.

    :ivar magnetisation_r: Magnetisation M of the iron core segment
        along the major radius axis, assumed to be constant inside a
        given iron segment. Reminder : H = 1/mu0 * B - mur * M;
    :ivar magnetisation_z: Magnetisation M of the iron core segment
        along the vertical axis, assumed to be constant inside a given
        iron segment. Reminder : H = 1/mu0 * B - mur * M;
    """
    class Meta:
        name = "equilibrium_constraints_magnetisation"

    magnetisation_r: Optional[EquilibriumConstraints0D] = field(
        default=None
    )
    magnetisation_z: Optional[EquilibriumConstraints0D] = field(
        default=None
    )


@dataclass(slots=True)
class EquilibriumConstraintsPurePosition(IdsBaseClass):
    """
    R,Z position constraint.

    :ivar position_measured: Measured or estimated position
    :ivar source: Path to the source data for this measurement in the
        IMAS data dictionary
    :ivar time_measurement: Exact time slice used from the time array of
        the measurement source data. If the time slice does not exist in
        the time array of the source data, it means linear interpolation
        has been used
    :ivar exact: Integer flag : 1 means exact data, taken as an exact
        input without being fitted; 0 means the equilibrium code does a
        least square fit
    :ivar weight: Weight given to the measurement
    :ivar position_reconstructed: Position estimated from the
        reconstructed equilibrium
    :ivar chi_squared_r: Squared error on the major radius normalized by
        the standard deviation considered in the minimization process :
        chi_squared = weight^2 *(position_reconstructed/r -
        position_measured/r)^2 / sigma^2, where sigma is the standard
        deviation of the measurement error
    :ivar chi_squared_z: Squared error on the altitude normalized by the
        standard deviation considered in the minimization process :
        chi_squared = weight^2 *(position_reconstructed/z -
        position_measured/z)^2 / sigma^2, where sigma is the standard
        deviation of the measurement error
    """
    class Meta:
        name = "equilibrium_constraints_pure_position"

    position_measured: Optional[Rz0DDynamicAos] = field(
        default=None
    )
    source: str = field(
        default=""
    )
    time_measurement: float = field(
        default=9e+40
    )
    exact: int = field(
        default=999999999
    )
    weight: float = field(
        default=9e+40
    )
    position_reconstructed: Optional[Rz0DDynamicAos] = field(
        default=None
    )
    chi_squared_r: float = field(
        default=9e+40
    )
    chi_squared_z: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class EquilibriumConvergence(IdsBaseClass):
    """
    Convergence details for the equilibrium calculation.

    :ivar iterations_n: Number of iterations carried out in the
        convergence loop
    :ivar grad_shafranov_deviation_expression: Expression for
        calculating the residual deviation between the left and right
        hand side of the Grad Shafranov equation
    :ivar grad_shafranov_deviation_value: Value of the residual
        deviation between the left and right hand side of the Grad
        Shafranov equation, evaluated as per
        grad_shafranov_deviation_expression
    """
    class Meta:
        name = "equilibrium_convergence"

    iterations_n: int = field(
        default=999999999
    )
    grad_shafranov_deviation_expression: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    grad_shafranov_deviation_value: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class EquilibriumCoordinateSystem(IdsBaseClass):
    """
    Flux surface coordinate system on a square grid of flux and poloidal angle.

    :ivar grid_type: Type of coordinate system
    :ivar grid: Definition of the 2D grid
    :ivar r: Values of the major radius on the grid
    :ivar z: Values of the Height on the grid
    :ivar jacobian: Absolute value of the jacobian of the coordinate
        system
    :ivar tensor_covariant: Covariant metric tensor on every point of
        the grid described by grid_type
    :ivar tensor_contravariant: Contravariant metric tensor on every
        point of the grid described by grid_type
    :ivar g11_covariant: metric coefficients g11,  covariant metric
        tensor for the grid described by grid_type
    :ivar g12_covariant: metric coefficients g12, covariant metric
        tensor for the grid described by grid_type
    :ivar g13_covariant: metric coefficients g13, covariant metric
        tensor for the grid described by grid_type
    :ivar g22_covariant: metric coefficients g22, covariant metric
        tensor for the grid described by grid_type
    :ivar g23_covariant: metric coefficients g23,  covariant metric
        tensor for the grid described by grid_type
    :ivar g33_covariant: metric coefficients g33, covariant metric
        tensor for the grid described by grid_type
    :ivar g11_contravariant: metric coefficients g11, contravariant
        metric tensor for the grid described by grid_type
    :ivar g12_contravariant: metric coefficients g12, contravariant
        metric tensor for the grid described by grid_type
    :ivar g13_contravariant: metric coefficients g13,  contravariant
        metric tensor for the grid described by grid_type
    :ivar g22_contravariant: metric coefficients g22,  contravariant
        metric tensor for the grid described by grid_type
    :ivar g23_contravariant: metric coefficients g23, contravariant
        metric tensor for the grid described by grid_type
    :ivar g33_contravariant: metric coefficients g33,  contravariant
        metric tensor for the grid described by grid_type
    """
    class Meta:
        name = "equilibrium_coordinate_system"

    grid_type: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    grid: Optional[EquilibriumProfiles2DGrid] = field(
        default=None
    )
    r: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    z: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    jacobian: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    tensor_covariant: Optional[ndarray[(int,int,int,int), float]] = field(
        default=None
    )
    tensor_contravariant: Optional[ndarray[(int,int,int,int), float]] = field(
        default=None
    )
    g11_covariant: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    g12_covariant: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    g13_covariant: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    g22_covariant: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    g23_covariant: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    g33_covariant: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    g11_contravariant: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    g12_contravariant: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    g13_contravariant: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    g22_contravariant: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    g23_contravariant: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    g33_contravariant: Optional[ndarray[(int,int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class EquilibriumProfiles1D(IdsBaseClass):
    """
    Equilibrium profiles (1D radial grid) as a function of the poloidal flux.

    :ivar psi: Poloidal flux
    :ivar phi: Toroidal flux
    :ivar pressure: Pressure
    :ivar f: Diamagnetic function (F=R B_Phi)
    :ivar dpressure_dpsi: Derivative of pressure w.r.t. psi
    :ivar f_df_dpsi: Derivative of F w.r.t. Psi, multiplied with F
    :ivar j_tor: Flux surface averaged toroidal current density =
        average(j_tor/R) / average(1/R)
    :ivar j_parallel: Flux surface averaged parallel current density =
        average(j.B) / B0, where B0 =
        Equilibrium/Global/Toroidal_Field/B0
    :ivar q: Safety factor (IMAS uses COCOS=11: only positive when
        toroidal current and magnetic field are in same direction)
    :ivar magnetic_shear: Magnetic shear, defined as rho_tor/q .
        dq/drho_tor
    :ivar r_inboard: Radial coordinate (major radius) on the inboard
        side of the magnetic axis
    :ivar r_outboard: Radial coordinate (major radius) on the outboard
        side of the magnetic axis
    :ivar rho_tor: Toroidal flux coordinate = sqrt(phi/(pi*b0)), where
        the toroidal flux, phi, corresponds to
        time_slice/profiles_1d/phi, the toroidal magnetic field, b0,
        corresponds to vacuum_toroidal_field/b0 and pi can be found in
        the IMAS constants
    :ivar rho_tor_norm: Normalised toroidal flux coordinate. The
        normalizing value for rho_tor_norm, is the toroidal flux
        coordinate at the equilibrium boundary (LCFS or 99.x % of the
        LCFS in case of a fixed boundary equilibium calculation)
    :ivar dpsi_drho_tor: Derivative of Psi with respect to Rho_Tor
    :ivar geometric_axis: RZ position of the geometric axis of the
        magnetic surfaces (defined as (Rmin+Rmax) / 2 and (Zmin+Zmax) /
        2 of the surface)
    :ivar elongation: Elongation
    :ivar triangularity_upper: Upper triangularity w.r.t. magnetic axis
    :ivar triangularity_lower: Lower triangularity w.r.t. magnetic axis
    :ivar squareness_upper_inner: Upper inner squareness (definition
        from T. Luce, Plasma Phys. Control. Fusion 55 (2013) 095009)
    :ivar squareness_upper_outer: Upper outer squareness (definition
        from T. Luce, Plasma Phys. Control. Fusion 55 (2013) 095009)
    :ivar squareness_lower_inner: Lower inner squareness (definition
        from T. Luce, Plasma Phys. Control. Fusion 55 (2013) 095009)
    :ivar squareness_lower_outer: Lower outer squareness (definition
        from T. Luce, Plasma Phys. Control. Fusion 55 (2013) 095009)
    :ivar volume: Volume enclosed in the flux surface
    :ivar rho_volume_norm: Normalised square root of enclosed volume
        (radial coordinate). The normalizing value is the enclosed
        volume at the equilibrium boundary (LCFS or 99.x % of the LCFS
        in case of a fixed boundary equilibium calculation)
    :ivar dvolume_dpsi: Radial derivative of the volume enclosed in the
        flux surface with respect to Psi
    :ivar dvolume_drho_tor: Radial derivative of the volume enclosed in
        the flux surface with respect to Rho_Tor
    :ivar area: Cross-sectional area of the flux surface
    :ivar darea_dpsi: Radial derivative of the cross-sectional area of
        the flux surface with respect to psi
    :ivar darea_drho_tor: Radial derivative of the cross-sectional area
        of the flux surface with respect to rho_tor
    :ivar surface: Surface area of the toroidal flux surface
    :ivar trapped_fraction: Trapped particle fraction
    :ivar gm1: Flux surface averaged 1/R^2
    :ivar gm2: Flux surface averaged |grad_rho_tor|^2/R^2
    :ivar gm3: Flux surface averaged |grad_rho_tor|^2
    :ivar gm4: Flux surface averaged 1/B^2
    :ivar gm5: Flux surface averaged B^2
    :ivar gm6: Flux surface averaged |grad_rho_tor|^2/B^2
    :ivar gm7: Flux surface averaged |grad_rho_tor|
    :ivar gm8: Flux surface averaged R
    :ivar gm9: Flux surface averaged 1/R
    :ivar b_average: Flux surface averaged B
    :ivar b_field_average: Flux surface averaged modulus of B (always
        positive, irrespective of the sign convention for the B-field
        direction).
    :ivar b_min: Minimum(B) on the flux surface
    :ivar b_field_min: Minimum(modulus(B)) on the flux surface (always
        positive, irrespective of the sign convention for the B-field
        direction)
    :ivar b_max: Maximum(B) on the flux surface
    :ivar b_field_max: Maximum(modulus(B)) on the flux surface (always
        positive, irrespective of the sign convention for the B-field
        direction)
    :ivar beta_pol: Poloidal beta profile. Defined as betap = 4 int(p
        dV) / [R_0 * mu_0 * Ip^2]
    :ivar mass_density: Mass density
    """
    class Meta:
        name = "equilibrium_profiles_1d"

    psi: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    phi: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    f: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    dpressure_dpsi: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    f_df_dpsi: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    j_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    j_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    q: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    magnetic_shear: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    r_inboard: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    r_outboard: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    rho_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    rho_tor_norm: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    dpsi_drho_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    geometric_axis: Optional[EquilibriumProfiles1DRz1DDynamicAos] = field(
        default=None
    )
    elongation: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    triangularity_upper: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    triangularity_lower: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    squareness_upper_inner: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    squareness_upper_outer: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    squareness_lower_inner: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    squareness_lower_outer: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    volume: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    rho_volume_norm: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    dvolume_dpsi: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    dvolume_drho_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    area: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    darea_dpsi: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    darea_drho_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    surface: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    trapped_fraction: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    gm1: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    gm2: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    gm3: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    gm4: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    gm5: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    gm6: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    gm7: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    gm8: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    gm9: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    b_average: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    b_field_average: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    b_min: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    b_field_min: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    b_max: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    b_field_max: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    beta_pol: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    mass_density: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class EquilibriumProfiles2D(IdsBaseClass):
    """
    Equilibrium 2D profiles in the poloidal plane.

    :ivar type: Type of profiles (distinguishes contribution from
        plasma, vaccum fields and total fields)
    :ivar grid_type: Selection of one of a set of grid types
    :ivar grid: Definition of the 2D grid (the content of dim1 and dim2
        is defined by the selected grid_type)
    :ivar r: Values of the major radius on the grid
    :ivar z: Values of the Height on the grid
    :ivar psi: Values of the poloidal flux at the grid in the poloidal
        plane
    :ivar theta: Values of the poloidal angle on the grid
    :ivar phi: Toroidal flux
    :ivar j_tor: Toroidal plasma current density
    :ivar j_parallel: Defined as (j.B)/B0 where j and B are the current
        density and magnetic field vectors and B0 is the (signed) vacuum
        toroidal magnetic field strength at the geometric reference
        point (R0,Z0). It is formally not the component of the plasma
        current density parallel to the magnetic field
    :ivar b_r: R component of the poloidal magnetic field
    :ivar b_field_r: R component of the poloidal magnetic field
    :ivar b_z: Z component of the poloidal magnetic field
    :ivar b_field_z: Z component of the poloidal magnetic field
    :ivar b_tor: Toroidal component of the magnetic field
    :ivar b_field_tor: Toroidal component of the magnetic field
    """
    class Meta:
        name = "equilibrium_profiles_2d"

    type: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    grid_type: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    grid: Optional[EquilibriumProfiles2DGrid] = field(
        default=None
    )
    r: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    z: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    psi: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    theta: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    phi: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    j_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    j_parallel: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    b_r: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    b_field_r: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    b_z: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    b_field_z: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    b_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    b_field_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class EqulibriumGlobalQuantities(IdsBaseClass):
    """
    0D parameters of the equilibrium.

    :ivar beta_pol: Poloidal beta. Defined as betap = 4 int(p dV) / [R_0
        * mu_0 * Ip^2]
    :ivar beta_tor: Toroidal beta, defined as the volume-averaged total
        perpendicular pressure divided by (B0^2/(2*mu0)), i.e.
        beta_toroidal = 2 mu0 int(p dV) / V / B0^2
    :ivar beta_normal: Normalised toroidal beta, defined as 100 *
        beta_tor * a[m] * B0 [T] / ip [MA]
    :ivar ip: Plasma current (toroidal component). Positive sign means
        anti-clockwise when viewed from above.
    :ivar li_3: Internal inductance
    :ivar volume: Total plasma volume
    :ivar area: Area of the LCFS poloidal cross section
    :ivar surface: Surface area of the toroidal flux surface
    :ivar length_pol: Poloidal length of the magnetic surface
    :ivar psi_axis: Poloidal flux at the magnetic axis
    :ivar psi_boundary: Poloidal flux at the selected plasma boundary
    :ivar magnetic_axis: Magnetic axis position and toroidal field
    :ivar current_centre: Position and vertical velocity of the current
        centre
    :ivar q_axis: q at the magnetic axis
    :ivar q_95: q at the 95% poloidal flux surface (IMAS uses COCOS=11:
        only positive when toroidal current and magnetic field are in
        same direction)
    :ivar q_min: Minimum q value and position
    :ivar energy_mhd: Plasma energy content = 3/2 * int(p,dV) with p
        being the total pressure (thermal + fast particles) [J]. Time-
        dependent; Scalar
    :ivar w_mhd: Plasma energy content = 3/2 * int(p,dV) with p being
        the total pressure (thermal + fast particles) [J]. Time-
        dependent; Scalar
    :ivar psi_external_average: Average (over the plasma poloidal cross
        section) plasma poloidal magnetic flux produced by all external
        circuits (CS and PF coils, eddy currents, VS in-vessel coils),
        given by the following formula : int(psi_external.j_tor.dS) / Ip
    :ivar v_external: External voltage, i.e. time derivative of
        psi_external_average (with a minus sign : -
        d_psi_external_average/d_time)
    :ivar plasma_inductance: Plasma inductance 2 E_magnetic/Ip^2, where
        E_magnetic = 1/2 * int(psi.j_tor.dS) (integral over the plasma
        poloidal cross-section)
    :ivar plasma_resistance: Plasma resistance = int(e_field.j.dV) /
        Ip^2
    """
    class Meta:
        name = "equlibrium_global_quantities"

    beta_pol: float = field(
        default=9e+40
    )
    beta_tor: float = field(
        default=9e+40
    )
    beta_normal: float = field(
        default=9e+40
    )
    ip: float = field(
        default=9e+40
    )
    li_3: float = field(
        default=9e+40
    )
    volume: float = field(
        default=9e+40
    )
    area: float = field(
        default=9e+40
    )
    surface: float = field(
        default=9e+40
    )
    length_pol: float = field(
        default=9e+40
    )
    psi_axis: float = field(
        default=9e+40
    )
    psi_boundary: float = field(
        default=9e+40
    )
    magnetic_axis: Optional[EquilibriumGlobalQuantitiesMagneticAxis] = field(
        default=None
    )
    current_centre: Optional[EquilibriumGlobalQuantitiesCurrentCentre] = field(
        default=None
    )
    q_axis: float = field(
        default=9e+40
    )
    q_95: float = field(
        default=9e+40
    )
    q_min: Optional[EquilibriumGlobalQuantitiesQmin] = field(
        default=None
    )
    energy_mhd: float = field(
        default=9e+40
    )
    w_mhd: float = field(
        default=9e+40
    )
    psi_external_average: float = field(
        default=9e+40
    )
    v_external: float = field(
        default=9e+40
    )
    plasma_inductance: float = field(
        default=9e+40
    )
    plasma_resistance: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class GenericGridDynamicGridSubsetElement(IdsBaseClass):
    """
    Generic grid, element part of a grid_subset (dynamic within a type 3 AoS)

    :ivar object_value: Set of objects defining the element
    """
    class Meta:
        name = "generic_grid_dynamic_grid_subset_element"

    object_value: list[GenericGridDynamicGridSubsetElementObject] = field(
        default_factory=list
    )


@dataclass(slots=True)
class GenericGridDynamicSpaceDimensionObject(IdsBaseClass):
    """
    Generic grid, list of objects of a given dimension within a space (dynamic
    within a type 3 AoS)

    :ivar boundary: Set of  (n-1)-dimensional objects defining the
        boundary of this n-dimensional object
    :ivar geometry: Geometry data associated with the object, its
        detailed content is defined by ../../geometry_content. Its
        dimension depends on the type of object, geometry and coordinate
        considered.
    :ivar nodes: List of nodes forming this object (indices to
        objects_per_dimension(1)%object(:) in Fortran notation)
    :ivar measure: Measure of the space object, i.e. physical size
        (length for 1d, area for 2d, volume for 3d objects,...)
    :ivar geometry_2d: 2D geometry data associated with the object. Its
        dimension depends on the type of object, geometry and coordinate
        considered. Typically, the first dimension represents the object
        coordinates, while the second dimension would represent the
        values of the various degrees of freedom of the finite element
        attached to the object.
    """
    class Meta:
        name = "generic_grid_dynamic_space_dimension_object"

    boundary: list[GenericGridDynamicSpaceDimensionObjectBoundary] = field(
        default_factory=list
    )
    geometry: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    nodes: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    measure: float = field(
        default=9e+40
    )
    geometry_2d: Optional[ndarray[(int,int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class EquilibriumConstraints(IdsBaseClass):
    """
    Measurements to constrain the equilibrium, output values and accuracy of the
    fit.

    :ivar b_field_tor_vacuum_r: Vacuum field times major radius in the
        toroidal field magnet. Positive sign means anti-clockwise when
        viewed from above
    :ivar bpol_probe: Set of poloidal field probes
    :ivar diamagnetic_flux: Diamagnetic flux
    :ivar faraday_angle: Set of faraday angles
    :ivar mse_polarisation_angle: Set of MSE polarisation angles
    :ivar flux_loop: Set of flux loops
    :ivar ip: Plasma current. Positive sign means anti-clockwise when
        viewed from above
    :ivar iron_core_segment: Magnetisation M of a set of iron core
        segments
    :ivar n_e: Set of local density measurements
    :ivar n_e_line: Set of line integrated density measurements
    :ivar pf_current: Current in a set of poloidal field coils
    :ivar pf_passive_current: Current in a set of axisymmetric passive
        conductors
    :ivar pressure: Set of total pressure estimates
    :ivar q: Set of safety factor estimates at various positions
    :ivar x_point: Array of X-points, for each of them the RZ position
        is given
    :ivar strike_point: Array of strike points, for each of them the RZ
        position is given
    """
    class Meta:
        name = "equilibrium_constraints"

    b_field_tor_vacuum_r: Optional[EquilibriumConstraints0D] = field(
        default=None
    )
    bpol_probe: list[EquilibriumConstraints0DOneLike] = field(
        default_factory=list
    )
    diamagnetic_flux: Optional[EquilibriumConstraints0DB0Like] = field(
        default=None
    )
    faraday_angle: list[EquilibriumConstraints0D] = field(
        default_factory=list
    )
    mse_polarisation_angle: list[EquilibriumConstraints0D] = field(
        default_factory=list
    )
    flux_loop: list[EquilibriumConstraints0DPsiLike] = field(
        default_factory=list
    )
    ip: Optional[EquilibriumConstraints0DIpLike] = field(
        default=None
    )
    iron_core_segment: list[EquilibriumConstraintsMagnetisation] = field(
        default_factory=list
    )
    n_e: list[EquilibriumConstraints0D] = field(
        default_factory=list
    )
    n_e_line: list[EquilibriumConstraints0D] = field(
        default_factory=list
    )
    pf_current: list[EquilibriumConstraints0DIpLike] = field(
        default_factory=list
    )
    pf_passive_current: list[EquilibriumConstraints0D] = field(
        default_factory=list
    )
    pressure: list[EquilibriumConstraints0D] = field(
        default_factory=list
    )
    q: list[EquilibriumConstraints0DPosition] = field(
        default_factory=list
    )
    x_point: list[EquilibriumConstraintsPurePosition] = field(
        default_factory=list
    )
    strike_point: list[EquilibriumConstraintsPurePosition] = field(
        default_factory=list
    )


@dataclass(slots=True)
class GenericGridDynamicGridSubset(IdsBaseClass):
    """
    Generic grid grid_subset (dynamic within a type 3 AoS)

    :ivar identifier: Grid subset identifier
    :ivar dimension: Space dimension of the grid subset elements. This
        must be equal to the sum of the dimensions of the individual
        objects forming the element.
    :ivar element: Set of elements defining the grid subset. An element
        is defined by a combination of objects from potentially all
        spaces
    :ivar base: Set of bases for the grid subset. For each base, the
        structure describes the projection of the base vectors on the
        canonical frame of the grid.
    :ivar metric: Metric of the canonical frame onto Cartesian
        coordinates
    """
    class Meta:
        name = "generic_grid_dynamic_grid_subset"

    identifier: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    dimension: int = field(
        default=999999999
    )
    element: list[GenericGridDynamicGridSubsetElement] = field(
        default_factory=list
    )
    base: list[GenericGridDynamicGridSubsetMetric] = field(
        default_factory=list
    )
    metric: Optional[GenericGridDynamicGridSubsetMetric] = field(
        default=None
    )


@dataclass(slots=True)
class GenericGridDynamicSpaceDimension(IdsBaseClass):
    """
    Generic grid, list of dimensions within a space (dynamic within a type 3 AoS)

    :ivar object_value: Set of objects for a given dimension
    :ivar geometry_content: Content of the ../object/geometry node for
        this dimension
    """
    class Meta:
        name = "generic_grid_dynamic_space_dimension"

    object_value: list[GenericGridDynamicSpaceDimensionObject] = field(
        default_factory=list
    )
    geometry_content: Optional[IdentifierDynamicAos3] = field(
        default=None
    )


@dataclass(slots=True)
class GenericGridDynamicSpace(IdsBaseClass):
    """
    Generic grid space (dynamic within a type 3 AoS)

    :ivar identifier: Space identifier
    :ivar geometry_type: Type of space geometry (0: standard, 1:Fourier,
        &gt;1: Fourier with periodicity)
    :ivar coordinates_type: Type of coordinates describing the physical
        space, for every coordinate of the space. The size of this node
        therefore defines the dimension of the space. The meaning of
        these predefined integer constants can be found in the Data
        Dictionary under utilities/coordinate_identifier.xml
    :ivar objects_per_dimension: Definition of the space objects for
        every dimension (from one to the dimension of the highest-
        dimensional objects). The index correspond to 1=nodes, 2=edges,
        3=faces, 4=cells/volumes, .... For every index, a collection of
        objects of that dimension is described.
    """
    class Meta:
        name = "generic_grid_dynamic_space"

    identifier: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    geometry_type: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    coordinates_type: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    objects_per_dimension: list[GenericGridDynamicSpaceDimension] = field(
        default_factory=list
    )


@dataclass(slots=True)
class GenericGridDynamic(IdsBaseClass):
    """
    Generic grid (dynamic within a type 3 AoS)

    :ivar identifier: Grid identifier
    :ivar path: Path of the grid, including the IDS name, in case of
        implicit reference to a grid_ggd node described in another IDS.
        To be filled only if the grid is not described explicitly in
        this grid_ggd structure. Example syntax:
        'wall:0/description_ggd(1)/grid_ggd', means that the grid is
        located in the wall IDS, occurrence 0, with ids path
        'description_ggd(1)/grid_ggd'. See the link below for more
        details about IDS paths
    :ivar space: Set of grid spaces
    :ivar grid_subset: Grid subsets
    """
    class Meta:
        name = "generic_grid_dynamic"

    identifier: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    path: str = field(
        default=""
    )
    space: list[GenericGridDynamicSpace] = field(
        default_factory=list
    )
    grid_subset: list[GenericGridDynamicGridSubset] = field(
        default_factory=list
    )


@dataclass(slots=True)
class EquilibriumGgd(IdsBaseClass):
    """
    Equilibrium ggd representation.

    :ivar grid: Grid description
    :ivar r: Values of the major radius on various grid subsets
    :ivar z: Values of the Height on various grid subsets
    :ivar psi: Values of the poloidal flux, given on various grid
        subsets
    :ivar phi: Values of the toroidal flux, given on various grid
        subsets
    :ivar theta: Values of the poloidal angle, given on various grid
        subsets
    :ivar j_tor: Toroidal plasma current density, given on various grid
        subsets
    :ivar j_parallel: Parallel (to magnetic field) plasma current
        density, given on various grid subsets
    :ivar b_field_r: R component of the poloidal magnetic field, given
        on various grid subsets
    :ivar b_field_z: Z component of the poloidal magnetic field, given
        on various grid subsets
    :ivar b_field_tor: Toroidal component of the magnetic field, given
        on various grid subsets
    """
    class Meta:
        name = "equilibrium_ggd"

    grid: Optional[GenericGridDynamic] = field(
        default=None
    )
    r: list[GenericGridScalar] = field(
        default_factory=list
    )
    z: list[GenericGridScalar] = field(
        default_factory=list
    )
    psi: list[GenericGridScalar] = field(
        default_factory=list
    )
    phi: list[GenericGridScalar] = field(
        default_factory=list
    )
    theta: list[GenericGridScalar] = field(
        default_factory=list
    )
    j_tor: list[GenericGridScalar] = field(
        default_factory=list
    )
    j_parallel: list[GenericGridScalar] = field(
        default_factory=list
    )
    b_field_r: list[GenericGridScalar] = field(
        default_factory=list
    )
    b_field_z: list[GenericGridScalar] = field(
        default_factory=list
    )
    b_field_tor: list[GenericGridScalar] = field(
        default_factory=list
    )


@dataclass(slots=True)
class EquilibriumGgdArray(IdsBaseClass):
    """
    Multiple GGDs provided at a given time slice.

    :ivar grid: Set of GGD grids for describing the equilibrium, at a
        given time slice
    :ivar time: Time
    """
    class Meta:
        name = "equilibrium_ggd_array"

    grid: list[GenericGridDynamic] = field(
        default_factory=list
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class EquilibriumTimeSlice(IdsBaseClass):
    """
    Equilibrium at a given time slice.

    :ivar boundary: Description of the plasma boundary used by fixed-
        boundary codes and typically chosen at psi_norm = 99.x% of the
        separatrix
    :ivar boundary_separatrix: Description of the plasma boundary at the
        separatrix
    :ivar boundary_secondary_separatrix: Geometry of the secondary
        separatrix, defined as the outer flux surface with an X-point
    :ivar constraints: In case of equilibrium reconstruction under
        constraints, measurements used to constrain the equilibrium,
        reconstructed values and accuracy of the fit. The names of the
        child nodes correspond to the following definition: the solver
        aims at minimizing a cost function defined as : J=1/2*sum_i [
        weight_i^2 (reconstructed_i - measured_i)^2 / sigma_i^2 ]. in
        which sigma_i is the standard deviation of the measurement error
        (to be found in the IDS of the measurement)
    :ivar global_quantities: 0D parameters of the equilibrium
    :ivar profiles_1d: Equilibrium profiles (1D radial grid) as a
        function of the poloidal flux
    :ivar profiles_2d: Equilibrium 2D profiles in the poloidal plane.
        Multiple 2D representations of the equilibrium can be stored
        here.
    :ivar ggd: Set of equilibrium representations using the generic grid
        description
    :ivar coordinate_system: Flux surface coordinate system on a square
        grid of flux and poloidal angle
    :ivar convergence: Convergence details
    :ivar time: Time
    """
    class Meta:
        name = "equilibrium_time_slice"

    boundary: Optional[EquilibriumBoundary] = field(
        default=None
    )
    boundary_separatrix: Optional[EquilibriumBoundarySeparatrix] = field(
        default=None
    )
    boundary_secondary_separatrix: Optional[EquilibriumBoundarySecondSeparatrix] = field(
        default=None
    )
    constraints: Optional[EquilibriumConstraints] = field(
        default=None
    )
    global_quantities: Optional[EqulibriumGlobalQuantities] = field(
        default=None
    )
    profiles_1d: Optional[EquilibriumProfiles1D] = field(
        default=None
    )
    profiles_2d: list[EquilibriumProfiles2D] = field(
        default_factory=list
    )
    ggd: list[EquilibriumGgd] = field(
        default_factory=list
    )
    coordinate_system: Optional[EquilibriumCoordinateSystem] = field(
        default=None
    )
    convergence: Optional[EquilibriumConvergence] = field(
        default=None
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class Equilibrium(IdsBaseClass):
    """
    Description of a 2D, axi-symmetric, tokamak equilibrium; result of an
    equilibrium code.

    :ivar ids_properties:
    :ivar vacuum_toroidal_field: Characteristics of the vacuum toroidal
        field (used in rho_tor definition and in the normalization of
        current densities)
    :ivar grids_ggd: Grids (using the Generic Grid Description), for
        various time slices. The timebase of this array of structure
        must be a subset of the time_slice timebase
    :ivar time_slice: Set of equilibria at various time slices
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "equilibrium"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    vacuum_toroidal_field: Optional[BTorVacuum1] = field(
        default=None
    )
    grids_ggd: list[EquilibriumGgdArray] = field(
        default_factory=list
    )
    time_slice: list[EquilibriumTimeSlice] = field(
        default_factory=list
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
