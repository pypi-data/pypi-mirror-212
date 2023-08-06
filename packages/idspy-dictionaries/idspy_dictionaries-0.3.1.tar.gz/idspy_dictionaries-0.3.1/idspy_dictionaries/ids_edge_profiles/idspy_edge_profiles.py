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
class EdgeProfilesVectorComponents1(IdsBaseClass):
    """
    Vector components in predefined directions for 1D profiles, assuming
    edge_radial_grid one level above.

    :ivar radial: Radial component
    :ivar diamagnetic: Diamagnetic component
    :ivar parallel: Parallel component
    :ivar poloidal: Poloidal component
    :ivar toroidal: Toroidal component
    """
    class Meta:
        name = "edge_profiles_vector_components_1"

    radial: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    diamagnetic: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    poloidal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    toroidal: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class EdgeProfilesVectorComponents2(IdsBaseClass):
    """
    Vector components in predefined directions for 1D profiles, assuming
    edge_radial_grid two levels above.

    :ivar radial: Radial component
    :ivar diamagnetic: Diamagnetic component
    :ivar parallel: Parallel component
    :ivar poloidal: Poloidal component
    :ivar toroidal: Toroidal component
    """
    class Meta:
        name = "edge_profiles_vector_components_2"

    radial: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    diamagnetic: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    poloidal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    toroidal: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class EdgeProfilesVectorComponents3(IdsBaseClass):
    """
    Vector components in predefined directions for 1D profiles, assuming
    edge_radial_grid 3 levels above.

    :ivar radial: Radial component
    :ivar diamagnetic: Diamagnetic component
    :ivar parallel: Parallel component
    :ivar poloidal: Poloidal component
    :ivar toroidal: Toroidal component
    """
    class Meta:
        name = "edge_profiles_vector_components_3"

    radial: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    diamagnetic: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    poloidal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    toroidal: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class EdgeRadialGrid(IdsBaseClass):
    """
    1D radial grid for edge_profiles IDSs.

    :ivar rho_pol_norm: Normalised poloidal flux coordinate =
        sqrt((psi(rho)-psi(magnetic_axis) /
        (psi(LCFS)-psi(magnetic_axis)))
    :ivar psi: Poloidal magnetic flux
    :ivar rho_tor_norm: Normalised toroidal flux coordinate. The
        normalizing value for rho_tor_norm, is the toroidal flux
        coordinate at the equilibrium boundary (LCFS or 99.x % of the
        LCFS in case of a fixed boundary equilibium calculation, see
        time_slice/boundary/b_flux_pol_norm in the equilibrium IDS)
    :ivar rho_tor: Toroidal flux coordinate. rho_tor =
        sqrt(b_flux_tor/(pi*b0)) ~ sqrt(pi*r^2*b0/(pi*b0)) ~ r [m]. The
        toroidal field used in its definition is indicated under
        vacuum_toroidal_field/b0
    :ivar volume: Volume enclosed inside the magnetic surface
    :ivar area: Cross-sectional area of the flux surface
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
        name = "edge_radial_grid"

    rho_pol_norm: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    psi: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    rho_tor_norm: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    rho_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    volume: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    area: Optional[ndarray[(int,), float]] = field(
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
class GenericGridScalarSinglePosition(IdsBaseClass):
    """
    Scalar values at a single position on a generic grid (dynamic within a type 3
    AoS)

    :ivar grid_index: Index of the grid used to represent this quantity
    :ivar grid_subset_index: Index of the grid subset the data is
        provided on
    :ivar value: Scalar value of the quantity on the grid subset
        (corresponding to a single local position or to an integrated
        value over the subset)
    """
    class Meta:
        name = "generic_grid_scalar_single_position"

    grid_index: int = field(
        default=999999999
    )
    grid_subset_index: int = field(
        default=999999999
    )
    value: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class GenericGridVectorComponents(IdsBaseClass):
    """
    Vector components in predefined directions on a generic grid (dynamic within a
    type 3 AoS)

    :ivar grid_index: Index of the grid used to represent this quantity
    :ivar grid_subset_index: Index of the grid subset the data is
        provided on
    :ivar radial: Radial component, one scalar value is provided per
        element in the grid subset.
    :ivar radial_coefficients: Interpolation coefficients for the radial
        component, to be used for a high precision evaluation of the
        physical quantity with finite elements, provided per element in
        the grid subset (first dimension).
    :ivar diamagnetic: Diamagnetic component, one scalar value is
        provided per element in the grid subset.
    :ivar diamagnetic_coefficients: Interpolation coefficients for the
        diamagnetic component, to be used for a high precision
        evaluation of the physical quantity with finite elements,
        provided per element in the grid subset (first dimension).
    :ivar parallel: Parallel component, one scalar value is provided per
        element in the grid subset.
    :ivar parallel_coefficients: Interpolation coefficients for the
        parallel component, to be used for a high precision evaluation
        of the physical quantity with finite elements, provided per
        element in the grid subset (first dimension).
    :ivar poloidal: Poloidal component, one scalar value is provided per
        element in the grid subset.
    :ivar poloidal_coefficients: Interpolation coefficients for the
        poloidal component, to be used for a high precision evaluation
        of the physical quantity with finite elements, provided per
        element in the grid subset (first dimension).
    :ivar toroidal: Toroidal component, one scalar value is provided per
        element in the grid subset.
    :ivar toroidal_coefficients: Interpolation coefficients for the
        toroidal component, to be used for a high precision evaluation
        of the physical quantity with finite elements, provided per
        element in the grid subset (first dimension).
    :ivar r: Component along the major radius axis, one scalar value is
        provided per element in the grid subset.
    :ivar r_coefficients: Interpolation coefficients for the component
        along the major radius axis, to be used for a high precision
        evaluation of the physical quantity with finite elements,
        provided per element in the grid subset (first dimension).
    :ivar z: Component along the height axis, one scalar value is
        provided per element in the grid subset.
    :ivar z_coefficients: Interpolation coefficients for the component
        along the height axis, to be used for a high precision
        evaluation of the physical quantity with finite elements,
        provided per element in the grid subset (first dimension).
    """
    class Meta:
        name = "generic_grid_vector_components"

    grid_index: int = field(
        default=999999999
    )
    grid_subset_index: int = field(
        default=999999999
    )
    radial: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    radial_coefficients: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    diamagnetic: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    diamagnetic_coefficients: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    parallel_coefficients: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    poloidal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    poloidal_coefficients: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    toroidal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    toroidal_coefficients: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    r: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    r_coefficients: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    z: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    z_coefficients: Optional[ndarray[(int,int), float]] = field(
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
class PlasmaCompositionNeutralElement(IdsBaseClass):
    """
    Element entering in the composition of the neutral atom or molecule (within a
    type 3 AoS)

    :ivar a: Mass of atom
    :ivar z_n: Nuclear charge
    :ivar atoms_n: Number of atoms of this element in the molecule
    :ivar multiplicity: Multiplicity of the atom
    """
    class Meta:
        name = "plasma_composition_neutral_element"

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
class EdgeProfiles1DFit(IdsBaseClass):
    """
    Edge profile fit information.

    :ivar measured: Measured values
    :ivar source: Path to the source data for each measurement in the
        IMAS data dictionary, e.g. ece/channel(i)/t_e for the electron
        temperature on the i-th channel in the ECE IDS
    :ivar time_measurement: Exact time slices used from the time array
        of the measurement source data. If the time slice does not exist
        in the time array of the source data, it means linear
        interpolation has been used
    :ivar time_measurement_slice_method: Method used to slice the data :
        index = 0 means using exact time slice of the measurement, 1
        means linear interpolation, ...
    :ivar time_measurement_width: In case the measurements are averaged
        over a time interval, this node is the full width of this time
        interval (empty otherwise). In case the slicing/averaging method
        doesn't use a hard time interval cutoff, this width is the
        characteristic time span of the slicing/averaging method. By
        convention, the time interval starts at time_measurement-
        time_width and ends at time_measurement.
    :ivar local: Integer flag : 1 means local measurement, 0 means line-
        integrated measurement
    :ivar rho_tor_norm: Normalised toroidal flux coordinate of each
        measurement (local value for a local measurement, minimum value
        reached by the line of sight for a line measurement)
    :ivar rho_pol_norm: Normalised poloidal flux coordinate of each
        measurement (local value for a local measurement, minimum value
        reached by the line of sight for a line measurement)
    :ivar weight: Weight given to each measured value
    :ivar reconstructed: Value reconstructed from the fit
    :ivar chi_squared: Squared error normalized by the weighted standard
        deviation considered in the minimization process : chi_squared =
        weight^2 *(reconstructed - measured)^2 / sigma^2, where sigma is
        the standard deviation of the measurement error
    :ivar parameters: List of the fit specific parameters in XML format
    """
    class Meta:
        name = "edge_profiles_1d_fit"

    measured: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    source: Optional[list[str]] = field(
        default=None
    )
    time_measurement: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    time_measurement_slice_method: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    time_measurement_width: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    local: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    rho_tor_norm: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    rho_pol_norm: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    weight: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    reconstructed: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    chi_squared: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    parameters: str = field(
        default=""
    )


@dataclass(slots=True)
class EdgeProfilesGgdFastElectrons(IdsBaseClass):
    """
    Fast sampled quantities related to electrons.

    :ivar temperature: Temperature, given at various positions (grid
        subset of size 1)
    :ivar density: Density (thermal+non-thermal), given at various
        positions (grid subset of size 1)
    """
    class Meta:
        name = "edge_profiles_ggd_fast_electrons"

    temperature: list[GenericGridScalarSinglePosition] = field(
        default_factory=list
    )
    density: list[GenericGridScalarSinglePosition] = field(
        default_factory=list
    )


@dataclass(slots=True)
class EdgeProfilesGgdFastIon(IdsBaseClass):
    """
    Fast sampled quantities related to a given ion species.

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed).
    :ivar label: String identifying the species (e.g. H+, D+, T+, He+2,
        C+, D2, DT, CD4, ...)
    :ivar neutral_index: Index of the corresponding neutral species in
        the ../../neutral array
    :ivar content: Particle content = total number of particles for this
        ion species in the volume of the grid subset, for various grid
        subsets
    :ivar temperature: Temperature (average over states when multiple
        states are considered), given at various positions (grid subset
        of size 1)
    :ivar density: Density (thermal+non-thermal) (sum over states when
        multiple states are considered), given at various positions
        (grid subset of size 1)
    """
    class Meta:
        name = "edge_profiles_ggd_fast_ion"

    element: list[PlasmaCompositionNeutralElement] = field(
        default_factory=list
    )
    z_ion: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    neutral_index: int = field(
        default=999999999
    )
    content: list[GenericGridScalarSinglePosition] = field(
        default_factory=list
    )
    temperature: list[GenericGridScalarSinglePosition] = field(
        default_factory=list
    )
    density: list[GenericGridScalarSinglePosition] = field(
        default_factory=list
    )


@dataclass(slots=True)
class EdgeProfilesNeutralState(IdsBaseClass):
    """
    Quantities related to the a given state of the neutral species.

    :ivar label: String identifying state
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar neutral_type: Neutral type (if the considered state is a
        neutral), in terms of energy. ID =1: cold; 2: thermal; 3: fast;
        4: NBI
    :ivar velocity: Velocity
    :ivar temperature: Temperature
    :ivar density: Density (thermal+non-thermal)
    :ivar density_thermal: Density of thermal particles
    :ivar density_fast: Density of fast (non-thermal) particles
    :ivar pressure: Pressure (thermal+non-thermal)
    :ivar pressure_thermal: Pressure (thermal) associated with random
        motion ~average((v-average(v))^2)
    :ivar pressure_fast_perpendicular: Fast (non-thermal) perpendicular
        pressure
    :ivar pressure_fast_parallel: Fast (non-thermal) parallel pressure
    """
    class Meta:
        name = "edge_profiles_neutral_state"

    label: str = field(
        default=""
    )
    electron_configuration: str = field(
        default=""
    )
    vibrational_level: float = field(
        default=9e+40
    )
    vibrational_mode: str = field(
        default=""
    )
    neutral_type: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    velocity: Optional[EdgeProfilesVectorComponents3] = field(
        default=None
    )
    temperature: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast_perpendicular: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class EdgeProfilesTimeSliceElectrons(IdsBaseClass):
    """
    Quantities related to electrons.

    :ivar temperature: Temperature, given on various grid subsets
    :ivar density: Density (thermal+non-thermal), given on various grid
        subsets
    :ivar density_fast: Density of fast (non-thermal) particles, given
        on various grid subsets
    :ivar pressure: Pressure, given on various grid subsets
    :ivar pressure_fast_perpendicular: Fast (non-thermal) perpendicular
        pressure, given on various grid subsets
    :ivar pressure_fast_parallel: Fast (non-thermal) parallel pressure,
        given on various grid subsets
    :ivar velocity: Velocity, given on various grid subsets
    :ivar distribution_function: Distribution function, given on various
        grid subsets
    """
    class Meta:
        name = "edge_profiles_time_slice_electrons"

    temperature: list[GenericGridScalar] = field(
        default_factory=list
    )
    density: list[GenericGridScalar] = field(
        default_factory=list
    )
    density_fast: list[GenericGridScalar] = field(
        default_factory=list
    )
    pressure: list[GenericGridScalar] = field(
        default_factory=list
    )
    pressure_fast_perpendicular: list[GenericGridScalar] = field(
        default_factory=list
    )
    pressure_fast_parallel: list[GenericGridScalar] = field(
        default_factory=list
    )
    velocity: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    distribution_function: list[GenericGridScalar] = field(
        default_factory=list
    )


@dataclass(slots=True)
class EdgeProfilesTimeSliceIonChargeState(IdsBaseClass):
    """
    Quantities related to a given charge state of the ion species.

    :ivar z_min: Minimum Z of the state bundle (z_min = z_max = 0 for a
        neutral)
    :ivar z_max: Maximum Z of the state bundle (equal to z_min if no
        bundle)
    :ivar z_average: Average Z of the state bundle (equal to z_min if no
        bundle), = sum (Z*x_z) where x_z is the relative concentration
        of a given charge state in the bundle, i.e. sum(x_z) = 1 over
        the bundle, given on various grid subsets
    :ivar z_square_average: Average Z square of the state bundle (equal
        to z_min if no bundle), = sum (Z^2*x_z) where x_z is the
        relative concentration of a given charge state in the bundle,
        i.e. sum(x_z) = 1 over the bundle, given on various grid subsets
    :ivar ionisation_potential: Cumulative and average ionisation
        potential to reach a given bundle. Defined as sum (x_z* (sum of
        Epot from z'=0 to z-1)), where Epot is the ionisation potential
        of ion Xz_+, and x_z is the relative concentration of a given
        charge state in the bundle, i.e. sum(x_z) = 1 over the bundle,
        given on various grid subsets
    :ivar label: String identifying state (e.g. C+, C+2 , C+3, C+4, C+5,
        C+6, ...)
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar temperature: Temperature, given on various grid subsets
    :ivar density: Density (thermal+non-thermal), given on various grid
        subsets
    :ivar density_fast: Density of fast (non-thermal) particles, given
        on various grid subsets
    :ivar pressure: Pressure, given on various grid subsets
    :ivar pressure_fast_perpendicular: Fast (non-thermal) perpendicular
        pressure, given on various grid subsets
    :ivar pressure_fast_parallel: Fast (non-thermal) parallel pressure,
        given on various grid subsets
    :ivar velocity: Velocity, given on various grid subsets
    :ivar velocity_diamagnetic: Velocity due to the diamagnetic drift,
        given on various grid subsets
    :ivar velocity_exb: Velocity due to the ExB drift, given on various
        grid subsets
    :ivar energy_density_kinetic: Kinetic energy density, given on
        various grid subsets
    :ivar distribution_function: Distribution function, given on various
        grid subsets
    """
    class Meta:
        name = "edge_profiles_time_slice_ion_charge_state"

    z_min: float = field(
        default=9e+40
    )
    z_max: float = field(
        default=9e+40
    )
    z_average: list[GenericGridScalar] = field(
        default_factory=list
    )
    z_square_average: list[GenericGridScalar] = field(
        default_factory=list
    )
    ionisation_potential: list[GenericGridScalar] = field(
        default_factory=list
    )
    label: str = field(
        default=""
    )
    electron_configuration: str = field(
        default=""
    )
    vibrational_level: float = field(
        default=9e+40
    )
    vibrational_mode: str = field(
        default=""
    )
    temperature: list[GenericGridScalar] = field(
        default_factory=list
    )
    density: list[GenericGridScalar] = field(
        default_factory=list
    )
    density_fast: list[GenericGridScalar] = field(
        default_factory=list
    )
    pressure: list[GenericGridScalar] = field(
        default_factory=list
    )
    pressure_fast_perpendicular: list[GenericGridScalar] = field(
        default_factory=list
    )
    pressure_fast_parallel: list[GenericGridScalar] = field(
        default_factory=list
    )
    velocity: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    velocity_diamagnetic: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    velocity_exb: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    energy_density_kinetic: list[GenericGridScalar] = field(
        default_factory=list
    )
    distribution_function: list[GenericGridScalar] = field(
        default_factory=list
    )


@dataclass(slots=True)
class EdgeProfilesTimeSliceNeutralState(IdsBaseClass):
    """
    Quantities related to a given state of the neutral species.

    :ivar label: String identifying state
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar neutral_type: Neutral type, in terms of energy. ID =1: cold;
        2: thermal; 3: fast; 4: NBI
    :ivar temperature: Temperature, given on various grid subsets
    :ivar density: Density (thermal+non-thermal), given on various grid
        subsets
    :ivar density_fast: Density of fast (non-thermal) particles, given
        on various grid subsets
    :ivar pressure: Pressure, given on various grid subsets
    :ivar pressure_fast_perpendicular: Fast (non-thermal) perpendicular
        pressure, given on various grid subsets
    :ivar pressure_fast_parallel: Fast (non-thermal) parallel pressure,
        given on various grid subsets
    :ivar velocity: Velocity, given on various grid subsets
    :ivar velocity_diamagnetic: Velocity due to the diamagnetic drift,
        given on various grid subsets
    :ivar velocity_exb: Velocity due to the ExB drift, given on various
        grid subsets
    :ivar energy_density_kinetic: Kinetic energy density, given on
        various grid subsets
    :ivar distribution_function: Distribution function, given on various
        grid subsets
    """
    class Meta:
        name = "edge_profiles_time_slice_neutral_state"

    label: str = field(
        default=""
    )
    electron_configuration: str = field(
        default=""
    )
    vibrational_level: float = field(
        default=9e+40
    )
    vibrational_mode: str = field(
        default=""
    )
    neutral_type: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    temperature: list[GenericGridScalar] = field(
        default_factory=list
    )
    density: list[GenericGridScalar] = field(
        default_factory=list
    )
    density_fast: list[GenericGridScalar] = field(
        default_factory=list
    )
    pressure: list[GenericGridScalar] = field(
        default_factory=list
    )
    pressure_fast_perpendicular: list[GenericGridScalar] = field(
        default_factory=list
    )
    pressure_fast_parallel: list[GenericGridScalar] = field(
        default_factory=list
    )
    velocity: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    velocity_diamagnetic: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    velocity_exb: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    energy_density_kinetic: list[GenericGridScalar] = field(
        default_factory=list
    )
    distribution_function: list[GenericGridScalar] = field(
        default_factory=list
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
class EdgeProfileNeutral(IdsBaseClass):
    """
    Quantities related to a given neutral species.

    :ivar element: List of elements forming the atom or molecule
    :ivar label: String identifying the species (e.g. H, D, T, He, C,
        D2, DT, CD4, ...)
    :ivar ion_index: Index of the corresponding ion species in the
        ../../ion array
    :ivar temperature: Temperature (average over charge states when
        multiple charge states are considered)
    :ivar density: Density (thermal+non-thermal) (sum over charge states
        when multiple charge states are considered)
    :ivar density_thermal: Density (thermal) (sum over charge states
        when multiple charge states are considered)
    :ivar density_fast: Density of fast (non-thermal) particles (sum
        over charge states when multiple charge states are considered)
    :ivar pressure: Pressure (thermal+non-thermal) (sum over charge
        states when multiple charge states are considered)
    :ivar pressure_thermal: Pressure (thermal) associated with random
        motion ~average((v-average(v))^2) (sum over charge states when
        multiple charge states are considered)
    :ivar pressure_fast_perpendicular: Fast (non-thermal) perpendicular
        pressure  (sum over charge states when multiple charge states
        are considered)
    :ivar pressure_fast_parallel: Fast (non-thermal) parallel pressure
        (sum over charge states when multiple charge states are
        considered)
    :ivar velocity: Velocity (average over charge states when multiple
        charge states are considered)
    :ivar multiple_states_flag: Multiple states calculation flag :
        0-Only one state is considered; 1-Multiple states are considered
        and are described in the state structure
    :ivar state: Quantities related to the different states of the
        species (energy, excitation, ...)
    """
    class Meta:
        name = "edge_profile_neutral"

    element: list[PlasmaCompositionNeutralElement] = field(
        default_factory=list
    )
    label: str = field(
        default=""
    )
    ion_index: int = field(
        default=999999999
    )
    temperature: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast_perpendicular: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    velocity: Optional[EdgeProfilesVectorComponents2] = field(
        default=None
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[EdgeProfilesNeutralState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class EdgeProfilesGgdFast(IdsBaseClass):
    """Quantities provided at a faster sampling rate than the full ggd quantities,
    on a reduced set of positions.

    Positions are described by a set of grid_subsets of size 1

    :ivar electrons: Quantities related to the electrons
    :ivar ion: Quantities related to the different ion species
    :ivar energy_thermal: Plasma energy content = 3/2 * integral over
        the volume of the grid subset of the thermal pressure (summed
        over all species), for various grid subsets
    :ivar time: Time
    """
    class Meta:
        name = "edge_profiles_ggd_fast"

    electrons: Optional[EdgeProfilesGgdFastElectrons] = field(
        default=None
    )
    ion: list[EdgeProfilesGgdFastIon] = field(
        default_factory=list
    )
    energy_thermal: list[GenericGridScalarSinglePosition] = field(
        default_factory=list
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class EdgeProfilesIonsChargeStates2(IdsBaseClass):
    """
    Quantities related to the a given state of the ion species.

    :ivar z_min: Minimum Z of the charge state bundle
    :ivar z_max: Maximum Z of the charge state bundle (equal to z_min if
        no bundle)
    :ivar z_average: Average Z of the charge state bundle, volume
        averaged over the plasma radius (equal to z_min if no bundle), =
        sum (Z*x_z) where x_z is the relative concentration of a given
        charge state in the bundle, i.e. sum(x_z) = 1 over the bundle.
    :ivar z_square_average: Average Z square of the charge state bundle,
        volume averaged over the plasma radius (equal to z_min squared
        if no bundle), = sum (Z^2*x_z) where x_z is the relative
        concentration of a given charge state in the bundle, i.e.
        sum(x_z) = 1 over the bundle.
    :ivar z_average_1d: Average charge profile of the charge state
        bundle (equal to z_min if no bundle), = sum (Z*x_z) where x_z is
        the relative concentration of a given charge state in the
        bundle, i.e. sum(x_z) = 1 over the bundle.
    :ivar z_average_square_1d: Average square charge profile of the
        charge state bundle (equal to z_min squared if no bundle), = sum
        (Z^2*x_z) where x_z is the relative concentration of a given
        charge state in the bundle, i.e. sum(x_z) = 1 over the bundle.
    :ivar ionisation_potential: Cumulative and average ionisation
        potential to reach a given bundle. Defined as sum (x_z* (sum of
        Epot from z'=0 to z-1)), where Epot is the ionisation potential
        of ion Xz_+, and x_z is the relative concentration of a given
        charge state in the bundle, i.e. sum(x_z) = 1 over the bundle.
    :ivar label: String identifying state (e.g. C+, C+2 , C+3, C+4, C+5,
        C+6, ...)
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar velocity: Velocity
    :ivar rotation_frequency_tor: Toroidal rotation frequency (i.e.
        toroidal velocity divided by the major radius at which the
        toroidal velocity is taken)
    :ivar temperature: Temperature
    :ivar density: Density (thermal+non-thermal)
    :ivar density_fit: Information on the fit used to obtain the density
        profile
    :ivar density_thermal: Density of thermal particles
    :ivar density_fast: Density of fast (non-thermal) particles
    :ivar pressure: Pressure (thermal+non-thermal)
    :ivar pressure_thermal: Pressure (thermal) associated with random
        motion ~average((v-average(v))^2)
    :ivar pressure_fast_perpendicular: Fast (non-thermal) perpendicular
        pressure
    :ivar pressure_fast_parallel: Fast (non-thermal) parallel pressure
    """
    class Meta:
        name = "edge_profiles_ions_charge_states2"

    z_min: float = field(
        default=9e+40
    )
    z_max: float = field(
        default=9e+40
    )
    z_average: float = field(
        default=9e+40
    )
    z_square_average: float = field(
        default=9e+40
    )
    z_average_1d: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    z_average_square_1d: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    ionisation_potential: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    electron_configuration: str = field(
        default=""
    )
    vibrational_level: float = field(
        default=9e+40
    )
    vibrational_mode: str = field(
        default=""
    )
    velocity: Optional[EdgeProfilesVectorComponents3] = field(
        default=None
    )
    rotation_frequency_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    temperature: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density_fit: Optional[EdgeProfiles1DFit] = field(
        default=None
    )
    density_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast_perpendicular: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class EdgeProfilesProfiles1DElectrons(IdsBaseClass):
    """
    Quantities related to electrons.

    :ivar temperature: Temperature
    :ivar temperature_validity: Indicator of the validity of the
        temperature profile. 0: valid from automated processing, 1:
        valid and certified by the RO; - 1 means problem identified in
        the data processing (request verification by the RO), -2:
        invalid data, should not be used
    :ivar temperature_fit: Information on the fit used to obtain the
        temperature profile
    :ivar density: Density (thermal+non-thermal)
    :ivar density_validity: Indicator of the validity of the density
        profile. 0: valid from automated processing, 1: valid and
        certified by the RO; - 1 means problem identified in the data
        processing (request verification by the RO), -2: invalid data,
        should not be used
    :ivar density_fit: Information on the fit used to obtain the density
        profile
    :ivar density_thermal: Density of thermal particles
    :ivar density_fast: Density of fast (non-thermal) particles
    :ivar pressure: Pressure (thermal+non-thermal)
    :ivar pressure_thermal: Pressure (thermal) associated with random
        motion ~average((v-average(v))^2)
    :ivar pressure_fast_perpendicular: Fast (non-thermal) perpendicular
        pressure
    :ivar pressure_fast_parallel: Fast (non-thermal) parallel pressure
    :ivar velocity_tor: Toroidal velocity
    :ivar velocity_pol: Poloidal velocity
    :ivar velocity: Velocity
    :ivar collisionality_norm: Collisionality normalised to the bounce
        frequency
    """
    class Meta:
        name = "edge_profiles_profiles_1d_electrons"

    temperature: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    temperature_validity: int = field(
        default=999999999
    )
    temperature_fit: Optional[EdgeProfiles1DFit] = field(
        default=None
    )
    density: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density_validity: int = field(
        default=999999999
    )
    density_fit: Optional[EdgeProfiles1DFit] = field(
        default=None
    )
    density_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_thermal: Optional[ndarray[(int,), float]] = field(
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
    velocity: Optional[EdgeProfilesVectorComponents2] = field(
        default=None
    )
    collisionality_norm: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class EdgeProfilesTimeSliceIon(IdsBaseClass):
    """
    Quantities related to a given ion species.

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed).
    :ivar label: String identifying the species (e.g. H+, D+, T+, He+2,
        C+, D2, DT, CD4, ...)
    :ivar neutral_index: Index of the corresponding neutral species in
        the ../../neutral array
    :ivar temperature: Temperature (average over states when multiple
        states are considered), given on various grid subsets
    :ivar density: Density (thermal+non-thermal) (sum over states when
        multiple states are considered), given on various grid subsets
    :ivar density_fast: Density of fast (non-thermal) particles (sum
        over states when multiple states are considered), given on
        various grid subsets
    :ivar pressure: Pressure (average over states when multiple states
        are considered), given on various grid subsets
    :ivar pressure_fast_perpendicular: Fast (non-thermal) perpendicular
        pressure (average over states when multiple states are
        considered), given on various grid subsets
    :ivar pressure_fast_parallel: Fast (non-thermal) parallel pressure
        (average over states when multiple states are considered), given
        on various grid subsets
    :ivar velocity: Velocity (average over states when multiple states
        are considered), given on various grid subsets
    :ivar energy_density_kinetic: Kinetic energy density (sum over
        states when multiple states are considered), given on various
        grid subsets
    :ivar multiple_states_flag: Multiple state calculation flag : 0-Only
        one state is considered; 1-Multiple states are considered and
        are described in the state structure
    :ivar state: Quantities related to the different states of the
        species (ionisation, energy, excitation, ...)
    """
    class Meta:
        name = "edge_profiles_time_slice_ion"

    element: list[PlasmaCompositionNeutralElement] = field(
        default_factory=list
    )
    z_ion: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    neutral_index: int = field(
        default=999999999
    )
    temperature: list[GenericGridScalar] = field(
        default_factory=list
    )
    density: list[GenericGridScalar] = field(
        default_factory=list
    )
    density_fast: list[GenericGridScalar] = field(
        default_factory=list
    )
    pressure: list[GenericGridScalar] = field(
        default_factory=list
    )
    pressure_fast_perpendicular: list[GenericGridScalar] = field(
        default_factory=list
    )
    pressure_fast_parallel: list[GenericGridScalar] = field(
        default_factory=list
    )
    velocity: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    energy_density_kinetic: list[GenericGridScalar] = field(
        default_factory=list
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[EdgeProfilesTimeSliceIonChargeState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class EdgeProfilesTimeSliceNeutral(IdsBaseClass):
    """
    Quantities related to a given neutral species.

    :ivar element: List of elements forming the atom or molecule
    :ivar label: String identifying the species (e.g. H, D, T, He, C,
        D2, DT, CD4, ...)
    :ivar ion_index: Index of the corresponding ion species in the
        ../../ion array
    :ivar temperature: Temperature (average over states when multiple
        states are considered), given on various grid subsets
    :ivar density: Density (thermal+non-thermal) (sum over states when
        multiple states are considered), given on various grid subsets
    :ivar density_fast: Density of fast (non-thermal) particles (sum
        over states when multiple states are considered), given on
        various grid subsets
    :ivar pressure: Pressure (average over states when multiple states
        are considered), given on various grid subsets
    :ivar pressure_fast_perpendicular: Fast (non-thermal) perpendicular
        pressure (average over states when multiple states are
        considered), given on various grid subsets
    :ivar pressure_fast_parallel: Fast (non-thermal) parallel pressure
        (average over states when multiple states are considered), given
        on various grid subsets
    :ivar velocity: Velocity (average over states when multiple states
        are considered), given on various grid subsets
    :ivar energy_density_kinetic: Kinetic energy density (sum over
        states when multiple states are considered), given on various
        grid subsets
    :ivar multiple_states_flag: Multiple state calculation flag : 0-Only
        one state is considered; 1-Multiple states are considered and
        are described in the state structure
    :ivar state: Quantities related to the different states of the
        species (energy, excitation, ...)
    """
    class Meta:
        name = "edge_profiles_time_slice_neutral"

    element: list[PlasmaCompositionNeutralElement] = field(
        default_factory=list
    )
    label: str = field(
        default=""
    )
    ion_index: int = field(
        default=999999999
    )
    temperature: list[GenericGridScalar] = field(
        default_factory=list
    )
    density: list[GenericGridScalar] = field(
        default_factory=list
    )
    density_fast: list[GenericGridScalar] = field(
        default_factory=list
    )
    pressure: list[GenericGridScalar] = field(
        default_factory=list
    )
    pressure_fast_perpendicular: list[GenericGridScalar] = field(
        default_factory=list
    )
    pressure_fast_parallel: list[GenericGridScalar] = field(
        default_factory=list
    )
    velocity: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    energy_density_kinetic: list[GenericGridScalar] = field(
        default_factory=list
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[EdgeProfilesTimeSliceNeutralState] = field(
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
class EdgeProfileIons(IdsBaseClass):
    """
    Quantities related to a given ion species.

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed), volume averaged over plasma radius
    :ivar label: String identifying ion (e.g. H, D, T, He, C, D2, ...)
    :ivar neutral_index: Index of the corresponding neutral species in
        the ../../neutral array
    :ivar z_ion_1d: Average charge of the ion species (sum of states
        charge weighted by state density and divided by ion density)
    :ivar z_ion_square_1d: Average square charge of the ion species (sum
        of states square charge weighted by state density and divided by
        ion density)
    :ivar temperature: Temperature (average over charge states when
        multiple charge states are considered)
    :ivar temperature_validity: Indicator of the validity of the
        temperature profile. 0: valid from automated processing, 1:
        valid and certified by the RO; - 1 means problem identified in
        the data processing (request verification by the RO), -2:
        invalid data, should not be used
    :ivar temperature_fit: Information on the fit used to obtain the
        temperature profile
    :ivar density: Density (thermal+non-thermal) (sum over charge states
        when multiple charge states are considered)
    :ivar density_validity: Indicator of the validity of the density
        profile. 0: valid from automated processing, 1: valid and
        certified by the RO; - 1 means problem identified in the data
        processing (request verification by the RO), -2: invalid data,
        should not be used
    :ivar density_fit: Information on the fit used to obtain the density
        profile
    :ivar density_thermal: Density (thermal) (sum over charge states
        when multiple charge states are considered)
    :ivar density_fast: Density of fast (non-thermal) particles (sum
        over charge states when multiple charge states are considered)
    :ivar pressure: Pressure (thermal+non-thermal) (sum over charge
        states when multiple charge states are considered)
    :ivar pressure_thermal: Pressure (thermal) associated with random
        motion ~average((v-average(v))^2) (sum over charge states when
        multiple charge states are considered)
    :ivar pressure_fast_perpendicular: Fast (non-thermal) perpendicular
        pressure  (sum over charge states when multiple charge states
        are considered)
    :ivar pressure_fast_parallel: Fast (non-thermal) parallel pressure
        (sum over charge states when multiple charge states are
        considered)
    :ivar velocity_tor: Toroidal velocity (average over charge states
        when multiple charge states are considered)
    :ivar velocity_pol: Poloidal velocity (average over charge states
        when multiple charge states are considered)
    :ivar rotation_frequency_tor: Toroidal rotation frequency  (i.e.
        toroidal velocity divided by the major radius at which the
        toroidal velocity is taken) (average over charge states when
        multiple charge states are considered)
    :ivar velocity: Velocity (average over charge states when multiple
        charge states are considered) at the position of maximum major
        radius on every flux surface
    :ivar multiple_states_flag: Multiple states calculation flag :
        0-Only the 'ion' level is considered and the 'state' array of
        structure is empty; 1-Ion states are considered and are
        described in the 'state' array of structure
    :ivar state: Quantities related to the different states of the
        species (ionisation, energy, excitation, ...)
    """
    class Meta:
        name = "edge_profile_ions"

    element: list[PlasmaCompositionNeutralElement] = field(
        default_factory=list
    )
    z_ion: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    neutral_index: int = field(
        default=999999999
    )
    z_ion_1d: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    z_ion_square_1d: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    temperature: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    temperature_validity: int = field(
        default=999999999
    )
    temperature_fit: Optional[EdgeProfiles1DFit] = field(
        default=None
    )
    density: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density_validity: int = field(
        default=999999999
    )
    density_fit: Optional[EdgeProfiles1DFit] = field(
        default=None
    )
    density_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_thermal: Optional[ndarray[(int,), float]] = field(
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
    rotation_frequency_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    velocity: Optional[EdgeProfilesVectorComponents2] = field(
        default=None
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[EdgeProfilesIonsChargeStates2] = field(
        default_factory=list
    )


@dataclass(slots=True)
class EdgeProfilesTimeSlice(IdsBaseClass):
    """
    Edge plasma description for a given time slice.

    :ivar electrons: Quantities related to the electrons
    :ivar ion: Quantities related to the different ion species
    :ivar neutral: Quantities related to the different neutral species
    :ivar t_i_average: Ion temperature (averaged on ion species), given
        on various grid subsets
    :ivar n_i_total_over_n_e: Ratio of total ion density (sum over ion
        species) over electron density. (thermal+non-thermal), given on
        various grid subsets
    :ivar zeff: Effective charge, given on various grid subsets
    :ivar pressure_thermal: Thermal pressure (electrons+ions), given on
        various grid subsets
    :ivar pressure_perpendicular: Total perpendicular pressure
        (electrons+ions, thermal+non-thermal), given on various grid
        subsets
    :ivar pressure_parallel: Total parallel pressure (electrons+ions,
        thermal+non-thermal), given on various grid subsets
    :ivar j_total: Total current density, given on various grid subsets
    :ivar j_parallel: Current due to parallel electric and thermo-
        electric conductivity and potential and electron temperature
        gradients along the field line, differences away from ambipolar
        flow in the parallel direction between ions and electrons (this
        is not the parallel component of j_total)
    :ivar j_anomalous: Anomalous current density, given on various grid
        subsets
    :ivar j_inertial: Inertial current density, given on various grid
        subsets
    :ivar j_ion_neutral_friction: Current density due to ion neutral
        friction, given on various grid subsets
    :ivar j_parallel_viscosity: Current density due to the parallel
        viscosity, given on various grid subsets
    :ivar j_perpendicular_viscosity: Current density due to the
        perpendicular viscosity, given on various grid subsets
    :ivar j_heat_viscosity: Current density due to the heat viscosity,
        given on various grid subsets
    :ivar j_pfirsch_schlueter: Current density due to Pfirsch-Schlüter
        effects, given on various grid subsets
    :ivar j_diamagnetic: Current density due to the diamgnetic drift,
        given on various grid subsets
    :ivar e_field: Electric field, given on various grid subsets
    :ivar phi_potential: Electric potential, given on various grid
        subsets
    :ivar time: Time
    """
    class Meta:
        name = "edge_profiles_time_slice"

    electrons: Optional[EdgeProfilesTimeSliceElectrons] = field(
        default=None
    )
    ion: list[EdgeProfilesTimeSliceIon] = field(
        default_factory=list
    )
    neutral: list[EdgeProfilesTimeSliceNeutral] = field(
        default_factory=list
    )
    t_i_average: list[GenericGridScalar] = field(
        default_factory=list
    )
    n_i_total_over_n_e: list[GenericGridScalar] = field(
        default_factory=list
    )
    zeff: list[GenericGridScalar] = field(
        default_factory=list
    )
    pressure_thermal: list[GenericGridScalar] = field(
        default_factory=list
    )
    pressure_perpendicular: list[GenericGridScalar] = field(
        default_factory=list
    )
    pressure_parallel: list[GenericGridScalar] = field(
        default_factory=list
    )
    j_total: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    j_parallel: list[GenericGridScalar] = field(
        default_factory=list
    )
    j_anomalous: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    j_inertial: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    j_ion_neutral_friction: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    j_parallel_viscosity: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    j_perpendicular_viscosity: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    j_heat_viscosity: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    j_pfirsch_schlueter: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    j_diamagnetic: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    e_field: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    phi_potential: list[GenericGridScalar] = field(
        default_factory=list
    )
    time: Optional[float] = field(
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
class EdgeProfilesProfiles1D(IdsBaseClass):
    """
    1D radial profiles for edge.

    :ivar grid: Radial grid
    :ivar electrons: Quantities related to the electrons
    :ivar ion: Quantities related to the different ion species, in the
        sense of isonuclear or isomolecular sequences. Ionisation states
        (and other types of states) must be differentiated at the state
        level below
    :ivar neutral: Quantities related to the different neutral species
    :ivar t_i_average: Ion temperature (averaged on charge states and
        ion species)
    :ivar t_i_average_fit: Information on the fit used to obtain the
        t_i_average profile
    :ivar n_i_total_over_n_e: Ratio of total ion density (sum over
        species and charge states) over electron density. (thermal+non-
        thermal)
    :ivar n_i_thermal_total: Total ion thermal density (sum over species
        and charge states)
    :ivar momentum_tor: Total plasma toroidal momentum, summed over ion
        species and electrons weighted by their density and major
        radius, i.e. sum_over_species(n*R*m*Vphi)
    :ivar zeff: Effective charge
    :ivar zeff_fit: Information on the fit used to obtain the zeff
        profile
    :ivar pressure_ion_total: Total (sum over ion species) thermal ion
        pressure
    :ivar pressure_thermal: Thermal pressure (electrons+ions)
    :ivar pressure_perpendicular: Total perpendicular pressure
        (electrons+ions, thermal+non-thermal)
    :ivar pressure_parallel: Total parallel pressure (electrons+ions,
        thermal+non-thermal)
    :ivar j_total: Total parallel current density = average(jtot.B) /
        B0, where B0 = edge_profiles/Vacuum_Toroidal_Field/ B0
    :ivar current_parallel_inside: Parallel current driven inside the
        flux surface. Cumulative surface integral of j_total
    :ivar j_tor: Total toroidal current density = average(J_Tor/R) /
        average(1/R)
    :ivar j_ohmic: Ohmic parallel current density = average(J_Ohmic.B) /
        B0, where B0 = edge_profiles/Vacuum_Toroidal_Field/ B0
    :ivar j_non_inductive: Non-inductive (includes bootstrap) parallel
        current density = average(jni.B) / B0, where B0 =
        edge_profiles/Vacuum_Toroidal_Field/ B0
    :ivar j_bootstrap: Bootstrap current density =
        average(J_Bootstrap.B) / B0, where B0 =
        edge_profiles/Vacuum_Toroidal_Field/ B0
    :ivar conductivity_parallel: Parallel conductivity
    :ivar e_field_parallel: Parallel electric field = average(E.B) / B0,
        where edge_profiles/Vacuum_Toroidal_Field/ B0
    :ivar e_field: Electric field, averaged on the magnetic surface. E.g
        for the parallel component, average(E.B) / B0, using
        edge_profiles/vacuum_toroidal_field/b0
    :ivar phi_potential: Electrostatic potential, averaged on the
        magnetic flux surface
    :ivar rotation_frequency_tor_sonic: Derivative of the flux surface
        averaged electrostatic potential with respect to the poloidal
        flux, multiplied by -1. This quantity is the toroidal angular
        rotation frequency due to the ExB drift, introduced in formula
        (43) of Hinton and Wong, Physics of Fluids 3082 (1985), also
        referred to as sonic flow in regimes in which the toroidal
        velocity is dominant over the poloidal velocity
    :ivar q: Safety factor
    :ivar magnetic_shear: Magnetic shear, defined as rho_tor/q .
        dq/drho_tor
    :ivar time: Time
    """
    class Meta:
        name = "edge_profiles_profiles_1d"

    grid: Optional[EdgeRadialGrid] = field(
        default=None
    )
    electrons: Optional[EdgeProfilesProfiles1DElectrons] = field(
        default=None
    )
    ion: list[EdgeProfileIons] = field(
        default_factory=list
    )
    neutral: list[EdgeProfileNeutral] = field(
        default_factory=list
    )
    t_i_average: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    t_i_average_fit: Optional[EdgeProfiles1DFit] = field(
        default=None
    )
    n_i_total_over_n_e: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    n_i_thermal_total: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    momentum_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    zeff: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    zeff_fit: Optional[EdgeProfiles1DFit] = field(
        default=None
    )
    pressure_ion_total: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_perpendicular: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    j_total: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    current_parallel_inside: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    j_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    j_ohmic: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    j_non_inductive: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    j_bootstrap: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    conductivity_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    e_field_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    e_field: Optional[EdgeProfilesVectorComponents1] = field(
        default=None
    )
    phi_potential: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    rotation_frequency_tor_sonic: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    q: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    magnetic_shear: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class GenericGridAos3Root(IdsBaseClass):
    """
    Generic grid (being itself the root of a type 3 AoS)

    :ivar identifier: Grid identifier
    :ivar path: Path of the grid, including the IDS name, in case of
        implicit reference to a grid_ggd node described in another IDS.
        To be filled only if the grid is not described explicitly in
        this grid_ggd structure. Example syntax:
        IDS::wall/0/description_ggd(1)/grid_ggd, means that the grid is
        located in the wall IDS, occurrence 0, with relative path
        description_ggd(1)/grid_ggd, using Fortran index convention
        (here : first index of the array)
    :ivar space: Set of grid spaces
    :ivar grid_subset: Grid subsets
    :ivar time: Time
    """
    class Meta:
        name = "generic_grid_aos3_root"

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
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class EdgeProfiles(IdsBaseClass):
    """
    Edge plasma profiles (includes the scrape-off layer and possibly part of the
    confined plasma)

    :ivar ids_properties:
    :ivar vacuum_toroidal_field: Characteristics of the vacuum toroidal
        field (used in rho_tor definition and in the normalization of
        current densities)
    :ivar midplane: Choice of midplane definition (use the lowest index
        number if more than one value is relevant)
    :ivar profiles_1d: SOL radial profiles for various time slices,
        taken on outboard equatorial mid-plane
    :ivar grid_ggd: Grid (using the Generic Grid Description), for
        various time slices. The timebase of this array of structure
        must be a subset of the ggd timebase
    :ivar ggd: Edge plasma quantities represented using the general grid
        description, for various time slices. The timebase of this array
        of structure must be a subset of the ggd_fast timebase (only if
        the ggd_fast array of structure is used)
    :ivar ggd_fast: Quantities provided at a faster sampling rate than
        the full ggd quantities. These are either integrated quantities
        or local quantities provided on a reduced set of positions.
        Positions and integration domains are described by a set of
        grid_subsets (of size 1 for a position).
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "edge_profiles"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    vacuum_toroidal_field: Optional[BTorVacuum1] = field(
        default=None
    )
    midplane: Optional[IdentifierStatic] = field(
        default=None
    )
    profiles_1d: list[EdgeProfilesProfiles1D] = field(
        default_factory=list
    )
    grid_ggd: list[GenericGridAos3Root] = field(
        default_factory=list
    )
    ggd: list[EdgeProfilesTimeSlice] = field(
        default_factory=list
    )
    ggd_fast: list[EdgeProfilesGgdFast] = field(
        default_factory=list
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
