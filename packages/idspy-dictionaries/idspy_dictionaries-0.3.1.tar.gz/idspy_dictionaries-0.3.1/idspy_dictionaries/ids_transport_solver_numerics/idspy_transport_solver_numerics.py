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
class CoreRadialGrid(IdsBaseClass):
    """
    1D radial grid for core* IDSs.

    :ivar rho_tor_norm: Normalised toroidal flux coordinate. The
        normalizing value for rho_tor_norm, is the toroidal flux
        coordinate at the equilibrium boundary (LCFS or 99.x % of the
        LCFS in case of a fixed boundary equilibium calculation, see
        time_slice/boundary/b_flux_pol_norm in the equilibrium IDS)
    :ivar rho_tor: Toroidal flux coordinate. rho_tor =
        sqrt(b_flux_tor/(pi*b0)) ~ sqrt(pi*r^2*b0/(pi*b0)) ~ r [m]. The
        toroidal field used in its definition is indicated under
        vacuum_toroidal_field/b0
    :ivar rho_pol_norm: Normalised poloidal flux coordinate =
        sqrt((psi(rho)-psi(magnetic_axis)) /
        (psi(LCFS)-psi(magnetic_axis)))
    :ivar psi: Poloidal magnetic flux
    :ivar volume: Volume enclosed inside the magnetic surface
    :ivar area: Cross-sectional area of the flux surface
    :ivar surface: Surface area of the toroidal flux surface
    :ivar psi_magnetic_axis: Value of the poloidal magnetic flux at the
        magnetic axis (useful to normalize the psi array values when the
        radial grid doesn't go from the magnetic axis to the plasma
        boundary)
    :ivar psi_boundary: Value of the poloidal magnetic flux at the
        plasma boundary (useful to normalize the psi array values when
        the radial grid doesn't go from the magnetic axis to the plasma
        boundary)
    """
    class Meta:
        name = "core_radial_grid"

    rho_tor_norm: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    rho_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    rho_pol_norm: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    psi: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    volume: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    area: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    surface: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    psi_magnetic_axis: float = field(
        default=9e+40
    )
    psi_boundary: float = field(
        default=9e+40
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
class NumericsConvergenceEquationsSingleDelta(IdsBaseClass):
    """
    Delta between two iterations of the solvers on a given transport equation.

    :ivar value: Value of the relative deviation
    :ivar expression: Expression used by the solver to calculate the
        relative deviation
    """
    class Meta:
        name = "numerics_convergence_equations_single_delta"

    value: float = field(
        default=9e+40
    )
    expression: str = field(
        default=""
    )


@dataclass(slots=True)
class NumericsProfiles1DDerivativesChargeStateD(IdsBaseClass):
    """
    Quantities related to a given charge state, derivatives with respect to a given
    quantity.

    :ivar temperature: Temperature
    :ivar density: Density (thermal+non-thermal)
    :ivar density_fast: Density of fast (non-thermal) particles
    :ivar pressure: Pressure
    :ivar pressure_fast_perpendicular: Fast (non-thermal) perpendicular
        pressure
    :ivar pressure_fast_parallel: Fast (non-thermal) parallel pressure
    :ivar velocity_tor: Toroidal velocity
    :ivar velocity_pol: Poloidal velocity
    """
    class Meta:
        name = "numerics_profiles_1d_derivatives_charge_state_d"

    temperature: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast_perpendicular: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    velocity_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    velocity_pol: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class NumericsProfiles1DDerivativesElectronsD(IdsBaseClass):
    """
    Quantities related to electrons, derivatives with respect to a given quantity.

    :ivar temperature: Temperature
    :ivar density: Density (thermal+non-thermal)
    :ivar density_fast: Density of fast (non-thermal) particles
    :ivar pressure: Pressure
    :ivar pressure_fast_perpendicular: Fast (non-thermal) perpendicular
        pressure
    :ivar pressure_fast_parallel: Fast (non-thermal) parallel pressure
    :ivar velocity_tor: Toroidal velocity
    :ivar velocity_pol: Poloidal velocity
    """
    class Meta:
        name = "numerics_profiles_1d_derivatives_electrons_d"

    temperature: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast_perpendicular: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    velocity_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    velocity_pol: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class NumericsProfiles1DDerivativesIonD(IdsBaseClass):
    """
    Quantities related to an ion species, derivatives with respect to a given
    quantity.

    :ivar temperature: Temperature (average over charge states when
        multiple charge states are considered)
    :ivar density: Density (thermal+non-thermal) (sum over charge states
        when multiple charge states are considered)
    :ivar density_fast: Density of fast (non-thermal) particles (sum
        over charge states when multiple charge states are considered)
    :ivar pressure: Pressure (average over charge states when multiple
        charge states are considered)
    :ivar pressure_fast_perpendicular: Fast (non-thermal) perpendicular
        pressure  (average over charge states when multiple charge
        states are considered)
    :ivar pressure_fast_parallel: Fast (non-thermal) parallel pressure
        (average over charge states when multiple charge states are
        considered)
    :ivar velocity_tor: Toroidal velocity (average over charge states
        when multiple charge states are considered)
    :ivar velocity_pol: Poloidal velocity (average over charge states
        when multiple charge states are considered)
    """
    class Meta:
        name = "numerics_profiles_1d_derivatives_ion_d"

    temperature: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast_perpendicular: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    velocity_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    velocity_pol: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class NumericsProfiles1DDerivativesTotalIons(IdsBaseClass):
    """
    Quantities related to total ion quantities, derivatives with respect to a given
    quantity.

    :ivar n_i_total_over_n_e: Ratio of total ion density (sum over
        species and charge states) over electron density. (thermal+non-
        thermal)
    :ivar pressure_ion_total: Total thermal ion pressure
    """
    class Meta:
        name = "numerics_profiles_1d_derivatives_total_ions"

    n_i_total_over_n_e: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_ion_total: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class NumericsRestart(IdsBaseClass):
    """
    Description of a restart file.

    :ivar names: Names of the restart files
    :ivar descriptions: Descriptions of the restart files
    :ivar time: Time
    """
    class Meta:
        name = "numerics_restart"

    names: Optional[list[str]] = field(
        default=None
    )
    descriptions: Optional[list[str]] = field(
        default=None
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class NumericsSolver1DEquationCoefficient(IdsBaseClass):
    """
    Coefficient for transport equation.

    :ivar profile: Radial profile of the numerical coefficient
    """
    class Meta:
        name = "numerics_solver_1d_equation_coefficient"

    profile: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class NumericsSolver1DEquationControlFloat(IdsBaseClass):
    """
    FLT0D for control parameters.

    :ivar value: Value of the control parameter
    """
    class Meta:
        name = "numerics_solver_1d_equation_control_float"

    value: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class NumericsSolver1DEquationControlInt(IdsBaseClass):
    """
    INT0D for control parameters.

    :ivar value: Value of the control parameter
    """
    class Meta:
        name = "numerics_solver_1d_equation_control_int"

    value: int = field(
        default=999999999
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
class NumericsBc1DBc(IdsBaseClass):
    """
    Boundary conditions for a given transport equation.

    :ivar identifier: Identifier of the boundary condition type. ID = 1:
        value of the field y; 2: radial derivative of the field
        (-dy/drho_tor); 3: scale length of the field y/(-dy/drho_tor);
        4: flux; 5: generic boundary condition y expressed as
        a1y'+a2y=a3. 6: equation not solved;
    :ivar value: Value of the boundary condition. For ID = 1 to 4, only
        the first position in the vector is used. For ID = 5, all three
        positions are used, meaning respectively a1, a2, a3.
    :ivar rho_tor_norm: Position, in normalised toroidal flux, at which
        the boundary condition is imposed. Outside this position, the
        value of the data are considered to be prescribed.
    """
    class Meta:
        name = "numerics_bc_1d_bc"

    identifier: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    value: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    rho_tor_norm: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class NumericsBc1DCurrent(IdsBaseClass):
    """
    Boundary conditions for the current diffusion equation.

    :ivar identifier: Identifier of the boundary condition type. ID = 1:
        poloidal flux; 2: ip; 3: loop voltage; 4: undefined; 5: generic
        boundary condition y expressed as a1y'+a2y=a3. 6: equation not
        solved;
    :ivar value: Value of the boundary condition. For ID = 1 to 3, only
        the first position in the vector is used. For ID = 5, all three
        positions are used, meaning respectively a1, a2, a3.
    :ivar rho_tor_norm: Position, in normalised toroidal flux, at which
        the boundary condition is imposed. Outside this position, the
        value of the data are considered to be prescribed.
    """
    class Meta:
        name = "numerics_bc_1d_current"

    identifier: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    value: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    rho_tor_norm: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class NumericsBcGgdBc(IdsBaseClass):
    """
    Boundary conditions for a given transport equation.

    :ivar identifier: Identifier of the boundary condition type. List of
        options TBD.
    :ivar grid_index: Index of the grid used to represent this quantity
    :ivar grid_subset_index: Index of the grid subset the data is
        provided on
    :ivar values: List of vector components, one list per element in the
        grid subset. First dimenstion: element index. Second dimension:
        vector component index (for ID = 1 to 3, only the first position
        in the vector is used. For ID = 5, all three positions are used,
        meaning respectively a1, a2, a3)
    """
    class Meta:
        name = "numerics_bc_ggd_bc"

    identifier: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    grid_index: int = field(
        default=999999999
    )
    grid_subset_index: int = field(
        default=999999999
    )
    values: Optional[ndarray[(int,int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class NumericsBcGgdCurrent(IdsBaseClass):
    """
    Boundary conditions for the current diffusion equation.

    :ivar identifier: Identifier of the boundary condition type. List of
        options TBD.
    :ivar grid_index: Index of the grid used to represent this quantity
    :ivar grid_subset_index: Index of the grid subset the data is
        provided on
    :ivar values: List of vector components, one list per element in the
        grid subset. First dimenstion: element index. Second dimension:
        vector component index (for ID = 1 to 3, only the first position
        in the vector is used. For ID = 5, all three positions are used,
        meaning respectively a1, a2, a3)
    """
    class Meta:
        name = "numerics_bc_ggd_current"

    identifier: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    grid_index: int = field(
        default=999999999
    )
    grid_subset_index: int = field(
        default=999999999
    )
    values: Optional[ndarray[(int,int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class NumericsConvergenceEquationsSingle(IdsBaseClass):
    """
    Convergence details of a given transport equation.

    :ivar iterations_n: Number of iterations carried out in the
        convergence loop
    :ivar delta_relative: Relative deviation on the primary quantity of
        the transport equation between the present and the  previous
        iteration of the solver
    """
    class Meta:
        name = "numerics_convergence_equations_single"

    iterations_n: int = field(
        default=999999999
    )
    delta_relative: Optional[NumericsConvergenceEquationsSingleDelta] = field(
        default=None
    )


@dataclass(slots=True)
class NumericsProfiles1DDerivativesChargeState(IdsBaseClass):
    """
    Quantities related to a given charge state.

    :ivar z_min: Minimum Z of the charge state bundle
    :ivar z_max: Maximum Z of the charge state bundle
    :ivar label: String identifying charge state (e.g. C+, C+2 , C+3,
        C+4, C+5, C+6, ...)
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar is_neutral: Flag specifying if this state corresponds to a
        neutral (1) or not (0)
    :ivar neutral_type: Neutral type (if the considered state is a
        neutral), in terms of energy. ID =1: cold; 2: thermal; 3: fast;
        4: NBI
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar d_drho_tor_norm: Derivatives with respect to the normalised
        toroidal flux
    :ivar d2_drho_tor_norm2: Second derivatives with respect to the
        normalised toroidal flux
    :ivar d_dt: Derivatives with respect to time
    """
    class Meta:
        name = "numerics_profiles_1d_derivatives_charge_state"

    z_min: float = field(
        default=9e+40
    )
    z_max: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    vibrational_level: float = field(
        default=9e+40
    )
    vibrational_mode: str = field(
        default=""
    )
    is_neutral: int = field(
        default=999999999
    )
    neutral_type: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    electron_configuration: str = field(
        default=""
    )
    d_drho_tor_norm: Optional[NumericsProfiles1DDerivativesChargeStateD] = field(
        default=None
    )
    d2_drho_tor_norm2: Optional[NumericsProfiles1DDerivativesChargeStateD] = field(
        default=None
    )
    d_dt: Optional[NumericsProfiles1DDerivativesChargeStateD] = field(
        default=None
    )


@dataclass(slots=True)
class NumericsProfiles1DDerivativesElectrons(IdsBaseClass):
    """
    Quantities related to electrons.

    :ivar d_drho_tor_norm: Derivatives with respect to the normalised
        toroidal flux
    :ivar d2_drho_tor_norm2: Second derivatives with respect to the
        normalised toroidal flux
    :ivar d_dt: Derivatives with respect to time
    """
    class Meta:
        name = "numerics_profiles_1d_derivatives_electrons"

    d_drho_tor_norm: Optional[NumericsProfiles1DDerivativesElectronsD] = field(
        default=None
    )
    d2_drho_tor_norm2: Optional[NumericsProfiles1DDerivativesElectronsD] = field(
        default=None
    )
    d_dt: Optional[NumericsProfiles1DDerivativesElectronsD] = field(
        default=None
    )


@dataclass(slots=True)
class NumericsSolver1DEquationBc(IdsBaseClass):
    """
    Boundary conditions for a 1D transport equation.

    :ivar type: Boundary condition type
    :ivar value: Value of the boundary condition. For type/index = 1 to
        3, only the first position in the vector is used. For type/index
        = 5, all three positions are used, meaning respectively a1, a2,
        a3.
    :ivar position: Position, in terms of the primary coordinate, at
        which the boundary condition is imposed. Outside this position,
        the value of the data are considered to be prescribed (in case
        of a single boundary condition).
    """
    class Meta:
        name = "numerics_solver_1d_equation_bc"

    type: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    value: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    position: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class NumericsSolver1DEquationControlParameters(IdsBaseClass):
    """
    Solver-specific input or output quantities.

    :ivar integer0d: Set of integer type scalar control parameters
    :ivar real0d: Set of real type scalar control parameters
    """
    class Meta:
        name = "numerics_solver_1d_equation_control_parameters"

    integer0d: list[NumericsSolver1DEquationControlInt] = field(
        default_factory=list
    )
    real0d: list[NumericsSolver1DEquationControlFloat] = field(
        default_factory=list
    )


@dataclass(slots=True)
class NumericsSolver1DEquationPrimary(IdsBaseClass):
    """
    Profile and derivatives a the primary quantity for a 1D transport equation.

    :ivar identifier: Identifier of the primary quantity of the
        transport equation. The description node contains the path to
        the quantity in the physics IDS (example:
        core_profiles/profiles_1d/ion(1)/density)
    :ivar ion_index: If the primary quantity is related to a ion
        species, index of the corresponding species in the
        core_profiles/profiles_1d/ion array
    :ivar neutral_index: If the primary quantity is related to a neutral
        species, index of the corresponding species in the
        core_profiles/profiles_1d/neutral array
    :ivar state_index: If the primary quantity is related to a
        particular state (of an ion or a neutral species), index of the
        corresponding state in the core_profiles/profiles_1d/ion (or
        neutral)/state array
    :ivar profile: Profile of the primary quantity
    :ivar d_dr: Radial derivative with respect to the primary coordinate
    :ivar d2_dr2: Second order radial derivative with respect to the
        primary coordinate
    :ivar d_dt: Time derivative
    :ivar d_dt_cphi: Derivative with respect to time, at constant
        toroidal flux (for current diffusion equation)
    :ivar d_dt_cr: Derivative with respect to time, at constant primary
        coordinate coordinate (for current diffusion equation)
    """
    class Meta:
        name = "numerics_solver_1d_equation_primary"

    identifier: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    ion_index: int = field(
        default=999999999
    )
    neutral_index: int = field(
        default=999999999
    )
    state_index: int = field(
        default=999999999
    )
    profile: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    d_dr: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    d2_dr2: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    d_dt: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    d_dt_cphi: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    d_dt_cr: Optional[ndarray[(int,), float]] = field(
        default=None
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
class NumericsBc1DElectrons(IdsBaseClass):
    """
    Boundary conditions for the electron related transport equations.

    :ivar particles: Boundary condition for the electron density
        equation (density if ID = 1)
    :ivar energy: Boundary condition for the electron energy equation
        (temperature if ID = 1)
    """
    class Meta:
        name = "numerics_bc_1d_electrons"

    particles: Optional[NumericsBc1DBc] = field(
        default=None
    )
    energy: Optional[NumericsBc1DBc] = field(
        default=None
    )


@dataclass(slots=True)
class NumericsBc1DIonChargeState(IdsBaseClass):
    """
    Boundary conditions for a given charge state related transport equations.

    :ivar z_min: Minimum Z of the charge state bundle
    :ivar z_max: Maximum Z of the charge state bundle
    :ivar label: String identifying charge state (e.g. C+, C+2 , C+3,
        C+4, C+5, C+6, ...)
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar is_neutral: Flag specifying if this state corresponds to a
        neutral (1) or not (0)
    :ivar neutral_type: Neutral type (if the considered state is a
        neutral), in terms of energy. ID =1: cold; 2: thermal; 3: fast;
        4: NBI
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar particles: Boundary condition for the charge state density
        equation (density if ID = 1)
    :ivar energy: Boundary condition for the charge state energy
        equation (temperature if ID = 1)
    """
    class Meta:
        name = "numerics_bc_1d_ion_charge_state"

    z_min: float = field(
        default=9e+40
    )
    z_max: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    vibrational_level: float = field(
        default=9e+40
    )
    vibrational_mode: str = field(
        default=""
    )
    is_neutral: int = field(
        default=999999999
    )
    neutral_type: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    electron_configuration: str = field(
        default=""
    )
    particles: Optional[NumericsBc1DBc] = field(
        default=None
    )
    energy: Optional[NumericsBc1DBc] = field(
        default=None
    )


@dataclass(slots=True)
class NumericsBcGgdElectrons(IdsBaseClass):
    """
    Boundary conditions for the electron related transport equations.

    :ivar particles: Boundary condition for the electron density
        equation (density if ID = 1), on various grid subsets
    :ivar energy: Boundary condition for the electron energy equation
        (temperature if ID = 1), on various grid subsets
    """
    class Meta:
        name = "numerics_bc_ggd_electrons"

    particles: list[NumericsBcGgdBc] = field(
        default_factory=list
    )
    energy: list[NumericsBcGgdBc] = field(
        default_factory=list
    )


@dataclass(slots=True)
class NumericsBcGgdIonChargeState(IdsBaseClass):
    """
    Boundary conditions for a given charge state related transport equations.

    :ivar z_min: Minimum Z of the charge state bundle
    :ivar z_max: Maximum Z of the charge state bundle
    :ivar label: String identifying charge state (e.g. C+, C+2 , C+3,
        C+4, C+5, C+6, ...)
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar is_neutral: Flag specifying if this state corresponds to a
        neutral (1) or not (0)
    :ivar neutral_type: Neutral type (if the considered state is a
        neutral), in terms of energy. ID =1: cold; 2: thermal; 3: fast;
        4: NBI
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar particles: Boundary condition for the charge state density
        equation (density if ID = 1), on various grid subsets
    :ivar energy: Boundary condition for the charge state energy
        equation (temperature if ID = 1), on various grid subsets
    """
    class Meta:
        name = "numerics_bc_ggd_ion_charge_state"

    z_min: float = field(
        default=9e+40
    )
    z_max: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    vibrational_level: float = field(
        default=9e+40
    )
    vibrational_mode: str = field(
        default=""
    )
    is_neutral: int = field(
        default=999999999
    )
    neutral_type: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    electron_configuration: str = field(
        default=""
    )
    particles: list[NumericsBcGgdBc] = field(
        default_factory=list
    )
    energy: list[NumericsBcGgdBc] = field(
        default_factory=list
    )


@dataclass(slots=True)
class NumericsConvergenceEquationsElectrons(IdsBaseClass):
    """
    Convergence details for the electron related equations.

    :ivar particles: Convergence details of the electron density
        equation
    :ivar energy: Convergence details of the electron energy equation
    """
    class Meta:
        name = "numerics_convergence_equations_electrons"

    particles: Optional[NumericsConvergenceEquationsSingle] = field(
        default=None
    )
    energy: Optional[NumericsConvergenceEquationsSingle] = field(
        default=None
    )


@dataclass(slots=True)
class NumericsConvergenceEquationsIonChargeState(IdsBaseClass):
    """
    Boundary conditions for a given charge state related transport equations.

    :ivar z_min: Minimum Z of the charge state bundle
    :ivar z_max: Maximum Z of the charge state bundle
    :ivar label: String identifying charge state (e.g. C+, C+2 , C+3,
        C+4, C+5, C+6, ...)
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar is_neutral: Flag specifying if this state corresponds to a
        neutral (1) or not (0)
    :ivar neutral_type: Neutral type (if the considered state is a
        neutral), in terms of energy. ID =1: cold; 2: thermal; 3: fast;
        4: NBI
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar particles: Convergence details of the charge state density
        equation
    :ivar energy: Convergence details of the charge state energy
        equation
    """
    class Meta:
        name = "numerics_convergence_equations_ion_charge_state"

    z_min: float = field(
        default=9e+40
    )
    z_max: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    vibrational_level: float = field(
        default=9e+40
    )
    vibrational_mode: str = field(
        default=""
    )
    is_neutral: int = field(
        default=999999999
    )
    neutral_type: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    electron_configuration: str = field(
        default=""
    )
    particles: Optional[NumericsConvergenceEquationsSingle] = field(
        default=None
    )
    energy: Optional[NumericsConvergenceEquationsSingle] = field(
        default=None
    )


@dataclass(slots=True)
class NumericsProfiles1DDerivativesIon(IdsBaseClass):
    """
    Quantities related to an ion species.

    :ivar a: Mass of atom
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed)
    :ivar z_n: Nuclear charge
    :ivar label: String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)
    :ivar d_drho_tor_norm: Derivatives with respect to the normalised
        toroidal flux
    :ivar d2_drho_tor_norm2: Second derivatives with respect to the
        normalised toroidal flux
    :ivar d_dt: Derivatives with respect to time
    :ivar multiple_states_flag: Multiple state calculation flag : 0-Only
        one state is considered; 1-Multiple states are considered and
        are described in the state structure
    :ivar state: Quantities related to the different states of the
        species (ionisation, energy, excitation, ...)
    """
    class Meta:
        name = "numerics_profiles_1d_derivatives_ion"

    a: float = field(
        default=9e+40
    )
    z_ion: float = field(
        default=9e+40
    )
    z_n: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    d_drho_tor_norm: Optional[NumericsProfiles1DDerivativesIonD] = field(
        default=None
    )
    d2_drho_tor_norm2: Optional[NumericsProfiles1DDerivativesIonD] = field(
        default=None
    )
    d_dt: Optional[NumericsProfiles1DDerivativesIonD] = field(
        default=None
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[NumericsProfiles1DDerivativesChargeState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class NumericsSolver1DEquation(IdsBaseClass):
    """
    Numeric of a given 1D transport equation.

    :ivar primary_quantity: Profile and derivatives of the primary
        quantity of the transport equation
    :ivar computation_mode: Computation mode for this equation
    :ivar boundary_condition: Set of boundary conditions of the
        transport equation
    :ivar coefficient: Set of numerical coefficients involved in the
        transport equation
    :ivar convergence: Convergence details
    """
    class Meta:
        name = "numerics_solver_1d_equation"

    primary_quantity: Optional[NumericsSolver1DEquationPrimary] = field(
        default=None
    )
    computation_mode: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    boundary_condition: list[NumericsSolver1DEquationBc] = field(
        default_factory=list
    )
    coefficient: list[NumericsSolver1DEquationCoefficient] = field(
        default_factory=list
    )
    convergence: Optional[NumericsConvergenceEquationsSingle] = field(
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
class NumericsBc1DIon(IdsBaseClass):
    """
    Boundary conditions for a given ion species related transport equations.

    :ivar a: Mass of atom
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed)
    :ivar z_n: Nuclear charge
    :ivar label: String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)
    :ivar particles: Boundary condition for the ion density equation
        (density if ID = 1)
    :ivar energy: Boundary condition for the ion energy equation
        (temperature if ID = 1)
    :ivar multiple_states_flag: Multiple states calculation flag :
        0-Only one state is considered; 1-Multiple states are considered
        and are described in the state structure
    :ivar state: Quantities related to the different states of the
        species (ionisation, energy, excitation, ...)
    """
    class Meta:
        name = "numerics_bc_1d_ion"

    a: float = field(
        default=9e+40
    )
    z_ion: float = field(
        default=9e+40
    )
    z_n: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    particles: Optional[NumericsBc1DBc] = field(
        default=None
    )
    energy: Optional[NumericsBc1DBc] = field(
        default=None
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[NumericsBc1DIonChargeState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class NumericsBcGgdIon(IdsBaseClass):
    """
    Boundary conditions for a given ion species related transport equations.

    :ivar a: Mass of atom
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed)
    :ivar z_n: Nuclear charge
    :ivar label: String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)
    :ivar particles: Boundary condition for the ion density equation
        (density if ID = 1), on various grid subsets
    :ivar energy: Boundary condition for the ion energy equation
        (temperature if ID = 1), on various grid subsets
    :ivar multiple_states_flag: Multiple states calculation flag :
        0-Only one state is considered; 1-Multiple states are considered
        and are described in the state structure
    :ivar state: Quantities related to the different states of the
        species (ionisation, energy, excitation, ...)
    """
    class Meta:
        name = "numerics_bc_ggd_ion"

    a: float = field(
        default=9e+40
    )
    z_ion: float = field(
        default=9e+40
    )
    z_n: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    particles: list[NumericsBcGgdBc] = field(
        default_factory=list
    )
    energy: list[NumericsBcGgdBc] = field(
        default_factory=list
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[NumericsBcGgdIonChargeState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class NumericsConvergenceEquationsIon(IdsBaseClass):
    """
    Convergence details of a given ion species related transport equations.

    :ivar a: Mass of atom
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed)
    :ivar z_n: Nuclear charge
    :ivar label: String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)
    :ivar particles: Convergence details of the  ion density equation
    :ivar energy: Convergence details of the ion energy equation
    :ivar multiple_states_flag: Multiple state calculation flag : 0-Only
        one state is considered; 1-Multiple states are considered and
        are described in the state structure
    :ivar state: Convergence details of the related to the different
        states transport equations
    """
    class Meta:
        name = "numerics_convergence_equations_ion"

    a: float = field(
        default=9e+40
    )
    z_ion: float = field(
        default=9e+40
    )
    z_n: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    particles: Optional[NumericsConvergenceEquationsSingle] = field(
        default=None
    )
    energy: Optional[NumericsConvergenceEquationsSingle] = field(
        default=None
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[NumericsConvergenceEquationsIonChargeState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class NumericsProfiles1DDerivatives(IdsBaseClass):
    """
    Radial profiles derivatives for a given time slice.

    :ivar grid: Radial grid
    :ivar electrons: Quantities related to the electrons
    :ivar ion: Quantities related to the different ion species
    :ivar d_drho_tor_norm: Derivatives of total ion quantities with
        respect to the normalised toroidal flux
    :ivar d2_drho_tor_norm2: Second derivatives of total ion quantities
        with respect to the normalised toroidal flux
    :ivar d_dt: Derivatives of total ion quantities with respect to time
    :ivar dpsi_dt: Derivative of the poloidal flux profile with respect
        to time
    :ivar dpsi_dt_cphi: Derivative of the poloidal flux profile with
        respect to time, at constant toroidal flux
    :ivar dpsi_dt_crho_tor_norm: Derivative of the poloidal flux profile
        with respect to time, at constant normalised toroidal flux
        coordinate
    :ivar drho_tor_dt: Partial derivative of the toroidal flux
        coordinate profile with respect to time
    :ivar d_dvolume_drho_tor_dt: Partial derivative with respect to time
        of the derivative of the volume with respect to the toroidal
        flux coordinate
    :ivar dpsi_drho_tor: Derivative of the poloidal flux profile with
        respect to the toroidal flux coordinate
    :ivar d2psi_drho_tor2: Second derivative of the poloidal flux
        profile with respect to the toroidal flux coordinate
    :ivar time: Time
    """
    class Meta:
        name = "numerics_profiles_1d_derivatives"

    grid: Optional[CoreRadialGrid] = field(
        default=None
    )
    electrons: Optional[NumericsProfiles1DDerivativesElectrons] = field(
        default=None
    )
    ion: list[NumericsProfiles1DDerivativesIon] = field(
        default_factory=list
    )
    d_drho_tor_norm: Optional[NumericsProfiles1DDerivativesTotalIons] = field(
        default=None
    )
    d2_drho_tor_norm2: Optional[NumericsProfiles1DDerivativesTotalIons] = field(
        default=None
    )
    d_dt: Optional[NumericsProfiles1DDerivativesTotalIons] = field(
        default=None
    )
    dpsi_dt: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    dpsi_dt_cphi: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    dpsi_dt_crho_tor_norm: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    drho_tor_dt: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    d_dvolume_drho_tor_dt: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    dpsi_drho_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    d2psi_drho_tor2: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class NumericsSolver1D(IdsBaseClass):
    """
    Numerics related to 1D radial solver for a given time slice.

    :ivar grid: Radial grid
    :ivar equation: Set of transport equations
    :ivar control_parameters: Solver-specific input or output quantities
    :ivar drho_tor_dt: Partial derivative of the toroidal flux
        coordinate profile with respect to time
    :ivar d_dvolume_drho_tor_dt: Partial derivative with respect to time
        of the derivative of the volume with respect to the toroidal
        flux coordinate
    :ivar time: Time
    """
    class Meta:
        name = "numerics_solver_1d"

    grid: Optional[CoreRadialGrid] = field(
        default=None
    )
    equation: list[NumericsSolver1DEquation] = field(
        default_factory=list
    )
    control_parameters: Optional[NumericsSolver1DEquationControlParameters] = field(
        default=None
    )
    drho_tor_dt: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    d_dvolume_drho_tor_dt: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    time: Optional[float] = field(
        default=None
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
class NumericsBc1D(IdsBaseClass):
    """
    Boundary conditions of radial transport equations for a given time slice.

    :ivar current: Boundary condition for the current diffusion
        equation.
    :ivar electrons: Quantities related to the electrons
    :ivar ion: Quantities related to the different ion species
    :ivar energy_ion_total: Boundary condition for the ion total (sum
        over ion species) energy equation (temperature if ID = 1)
    :ivar momentum_tor: Boundary condition for the total plasma toroidal
        momentum equation (summed over ion species and electrons)
        (momentum if ID = 1)
    :ivar time: Time
    """
    class Meta:
        name = "numerics_bc_1d"

    current: Optional[NumericsBc1DCurrent] = field(
        default=None
    )
    electrons: Optional[NumericsBc1DElectrons] = field(
        default=None
    )
    ion: list[NumericsBc1DIon] = field(
        default_factory=list
    )
    energy_ion_total: Optional[NumericsBc1DBc] = field(
        default=None
    )
    momentum_tor: Optional[NumericsBc1DBc] = field(
        default=None
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class NumericsConvergenceEquation(IdsBaseClass):
    """
    Convergence details of a given transport equation.

    :ivar current: Convergence details of the current diffusion equation
    :ivar electrons: Quantities related to the electrons
    :ivar ion: Quantities related to the different ion species
    :ivar energy_ion_total: Convergence details of the ion total (sum
        over ion species) energy equation
    :ivar time: Time
    """
    class Meta:
        name = "numerics_convergence_equation"

    current: Optional[NumericsConvergenceEquationsSingle] = field(
        default=None
    )
    electrons: Optional[NumericsConvergenceEquationsElectrons] = field(
        default=None
    )
    ion: list[NumericsConvergenceEquationsIon] = field(
        default_factory=list
    )
    energy_ion_total: Optional[NumericsConvergenceEquationsSingle] = field(
        default=None
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class NumericsBcGgd(IdsBaseClass):
    """
    Boundary conditions of radial transport equations for a given time slice.

    :ivar grid: Grid description
    :ivar current: Boundary condition for the current diffusion
        equation, on various grid subsets
    :ivar electrons: Quantities related to the electrons
    :ivar ion: Quantities related to the different ion species
    :ivar time: Time
    """
    class Meta:
        name = "numerics_bc_ggd"

    grid: Optional[GenericGridDynamic] = field(
        default=None
    )
    current: list[NumericsBcGgdCurrent] = field(
        default_factory=list
    )
    electrons: Optional[NumericsBcGgdElectrons] = field(
        default=None
    )
    ion: list[NumericsBcGgdIon] = field(
        default_factory=list
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class NumericsConvergence(IdsBaseClass):
    """
    Convergence details.

    :ivar time_step: Internal time step used by the transport solver
        (assuming all transport equations are solved with the same time
        step)
    :ivar equations: Convergence details of the transport equations, for
        various time slices
    """
    class Meta:
        name = "numerics_convergence"

    time_step: Optional[SignalFlt1D] = field(
        default=None
    )
    equations: list[NumericsConvergenceEquation] = field(
        default_factory=list
    )


@dataclass(slots=True)
class TransportSolverNumerics(IdsBaseClass):
    """
    Numerical quantities used by transport solvers and convergence details.

    :ivar ids_properties:
    :ivar time_step: Internal time step used by the transport solver
        (assuming all transport equations are solved with the same time
        step)
    :ivar time_step_average: Average internal time step used by the
        transport solver between the previous and the current time
        stored for this quantity (assuming all transport equations are
        solved with the same time step)
    :ivar time_step_min: Minimum internal time step used by the
        transport solver between the previous and the current time
        stored for this quantity (assuming all transport equations are
        solved with the same time step)
    :ivar solver: Solver identifier
    :ivar primary_coordinate: Primary coordinate system with which the
        transport equations are solved. For a 1D transport solver: index
        = 1 means rho_tor_norm; 2 = rho_tor.
    :ivar solver_1d: Numerics related to 1D radial solver, for various
        time slices.
    :ivar derivatives_1d: Radial profiles derivatives for various time
        slices. To be removed when the solver_1d structure is finalized.
    :ivar boundary_conditions_1d: Boundary conditions of the radial
        transport equations for various time slices. To be removed when
        the solver_1d structure is finalized.
    :ivar boundary_conditions_ggd: Boundary conditions of the transport
        equations, provided on the GGD, for various time slices
    :ivar convergence: Convergence details To be removed when the
        solver_1d structure is finalized.
    :ivar vacuum_toroidal_field: Characteristics of the vacuum toroidal
        field (used in rho_tor definition and in the normalization of
        current densities)
    :ivar restart_files: Set of code-specific restart files for a given
        time slice. These files are managed by a physical application to
        ensure its restart during long simulations
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "transport_solver_numerics"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    time_step: Optional[SignalFlt1D] = field(
        default=None
    )
    time_step_average: Optional[SignalFlt1D] = field(
        default=None
    )
    time_step_min: Optional[SignalFlt1D] = field(
        default=None
    )
    solver: Optional[Identifier] = field(
        default=None
    )
    primary_coordinate: Optional[Identifier] = field(
        default=None
    )
    solver_1d: list[NumericsSolver1D] = field(
        default_factory=list
    )
    derivatives_1d: list[NumericsProfiles1DDerivatives] = field(
        default_factory=list
    )
    boundary_conditions_1d: list[NumericsBc1D] = field(
        default_factory=list
    )
    boundary_conditions_ggd: list[NumericsBcGgd] = field(
        default_factory=list
    )
    convergence: Optional[NumericsConvergence] = field(
        default=None
    )
    vacuum_toroidal_field: Optional[BTorVacuum1] = field(
        default=None
    )
    restart_files: list[NumericsRestart] = field(
        default_factory=list
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
