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
class DistributionMarkersOrbit(IdsBaseClass):
    """Test particles for a given time slice : orbit integrals

    :ivar expressions: List of the expressions f(n_tor,m_pol,k,q,...)
        used in the orbit integrals
    :ivar n_tor: Array of toroidal mode numbers, n_tor, where quantities
        vary as exp(i.n_tor.phi) and phi runs anticlockwise when viewed
        from above
    :ivar m_pol: Array of poloidal mode numbers, where quantities vary
        as exp(-i.m_pol.theta) and theta is the angle defined by the
        choice of ../../coordinate_identifier, with its centre at the
        magnetic axis recalled at the root of this IDS
    :ivar bounce_harmonics: Array of bounce harmonics k
    :ivar values: Values of the orbit integrals
    """
    class Meta:
        name = "distribution_markers_orbit"

    expressions: Optional[list[str]] = field(
        default=None
    )
    n_tor: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    m_pol: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    bounce_harmonics: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    values: Optional[ndarray[(int, int, int, int, int), complex]] = field(
        default=None
    )


@dataclass(slots=True)
class DistributionMarkersOrbitInstant(IdsBaseClass):
    """Test particles for a given time slice : orbit integrals

    :ivar expressions: List of the expressions f(eq) used in the orbit
        integrals
    :ivar time_orbit: Time array along the markers last orbit
    :ivar values: Values of the orbit integrals
    """
    class Meta:
        name = "distribution_markers_orbit_instant"

    expressions: Optional[list[str]] = field(
        default=None
    )
    time_orbit: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    values: Optional[ndarray[(int, int, int ), complex]] = field(
        default=None
    )


@dataclass(slots=True)
class DistributionsDGlobalQuantitiesCollisionsElectrons(IdsBaseClass):
    """
    Global quantities for collisions with electrons.

    :ivar power_thermal: Collisional power to the thermal particle
        population
    :ivar power_fast: Collisional power to the fast particle population
    :ivar torque_thermal_tor: Collisional toroidal torque to the thermal
        particle population
    :ivar torque_fast_tor: Collisional toroidal torque to the fast
        particle population
    """
    class Meta:
        name = "distributions_d_global_quantities_collisions_electrons"

    power_thermal: float = field(
        default=9e+40
    )
    power_fast: float = field(
        default=9e+40
    )
    torque_thermal_tor: float = field(
        default=9e+40
    )
    torque_fast_tor: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class DistributionsDGlobalQuantitiesCollisionsIonState(IdsBaseClass):
    """
    Global quantities for collisions with a given ion species state.

    :ivar z_min: Minimum Z of the charge state bundle (z_min = z_max = 0
        for a neutral)
    :ivar z_max: Maximum Z of the charge state bundle (equal to z_min if
        no bundle)
    :ivar label: String identifying charge state (e.g. C+, C+2 , C+3,
        C+4, C+5, C+6, ...)
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar power_thermal: Collisional power to the thermal particle
        population
    :ivar power_fast: Collisional power to the fast particle population
    :ivar torque_thermal_tor: Collisional toroidal torque to the thermal
        particle population
    :ivar torque_fast_tor: Collisional toroidal torque to the fast
        particle population
    """
    class Meta:
        name = "distributions_d_global_quantities_collisions_ion_state"

    z_min: float = field(
        default=9e+40
    )
    z_max: float = field(
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
    power_thermal: float = field(
        default=9e+40
    )
    power_fast: float = field(
        default=9e+40
    )
    torque_thermal_tor: float = field(
        default=9e+40
    )
    torque_fast_tor: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class DistributionsDGlobalQuantitiesThermalised(IdsBaseClass):
    """
    Global quantities for thermalisation source/sinks.

    :ivar particles: Source rate of thermal particles due to the
        thermalisation of fast particles
    :ivar power: Power input to the thermal particle population due to
        the thermalisation of fast particles
    :ivar torque: Torque input to the thermal particle population due to
        the thermalisation of fast particles
    """
    class Meta:
        name = "distributions_d_global_quantities_thermalised"

    particles: float = field(
        default=9e+40
    )
    power: float = field(
        default=9e+40
    )
    torque: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class DistributionsDProfiles1DCollisionsElectrons(IdsBaseClass):
    """
    1D profiles for collisions with electrons.

    :ivar power_thermal: Collisional power density to the thermal
        particle population
    :ivar power_fast: Collisional power density to the fast particle
        population
    :ivar torque_thermal_tor: Collisional toroidal torque density to the
        thermal particle population
    :ivar torque_fast_tor: Collisional toroidal torque density to the
        fast particle population
    """
    class Meta:
        name = "distributions_d_profiles_1d_collisions_electrons"

    power_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    torque_thermal_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    torque_fast_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class DistributionsDProfiles1DCollisionsIonState(IdsBaseClass):
    """
    1D profiles for collisions with a given ion species state.

    :ivar z_min: Minimum Z of the charge state bundle (z_min = z_max = 0
        for a neutral)
    :ivar z_max: Maximum Z of the charge state bundle (equal to z_min if
        no bundle)
    :ivar label: String identifying charge state (e.g. C+, C+2 , C+3,
        C+4, C+5, C+6, ...)
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar power_thermal: Collisional power density to the thermal
        particle population
    :ivar power_fast: Collisional power density to the fast particle
        population
    :ivar torque_thermal_tor: Collisional toroidal torque density to the
        thermal particle population
    :ivar torque_fast_tor: Collisional toroidal torque density to the
        fast particle population
    """
    class Meta:
        name = "distributions_d_profiles_1d_collisions_ion_state"

    z_min: float = field(
        default=9e+40
    )
    z_max: float = field(
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
    power_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    torque_thermal_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    torque_fast_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class DistributionsDProfiles1DPartialCollisionsElectrons(IdsBaseClass):
    """
    1D profiles for collisions with electrons.

    :ivar power_thermal: Collisional power density to the thermal
        particle population
    :ivar power_fast: Collisional power density to the fast particle
        population
    :ivar torque_thermal_tor: Collisional toroidal torque density to the
        thermal particle population
    :ivar torque_fast_tor: Collisional toroidal torque density to the
        fast particle population
    """
    class Meta:
        name = "distributions_d_profiles_1d_partial_collisions_electrons"

    power_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    torque_thermal_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    torque_fast_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class DistributionsDProfiles1DPartialCollisionsIonState(IdsBaseClass):
    """
    1D profiles for collisions with a given ion species state.

    :ivar z_min: Minimum Z of the charge state bundle (z_min = z_max = 0
        for a neutral)
    :ivar z_max: Maximum Z of the charge state bundle (equal to z_min if
        no bundle)
    :ivar label: String identifying charge state (e.g. C+, C+2 , C+3,
        C+4, C+5, C+6, ...)
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar power_thermal: Collisional power density to the thermal
        particle population
    :ivar power_fast: Collisional power density to the fast particle
        population
    :ivar torque_thermal_tor: Collisional toroidal torque density to the
        thermal particle population
    :ivar torque_fast_tor: Collisional toroidal torque density to the
        fast particle population
    """
    class Meta:
        name = "distributions_d_profiles_1d_partial_collisions_ion_state"

    z_min: float = field(
        default=9e+40
    )
    z_max: float = field(
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
    power_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    torque_thermal_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    torque_fast_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class DistributionsDProfiles1DThermalised(IdsBaseClass):
    """
    1D profiles of thermalisation source/sinks.

    :ivar particles: Source rate of thermal particle density due to the
        thermalisation of fast particles
    :ivar energy: Source rate of energy density within the thermal
        particle population due to the thermalisation of fast particles
    :ivar momentum_tor: Source rate of toroidal angular momentum density
        within the thermal particle population due to the thermalisation
        of fast particles
    """
    class Meta:
        name = "distributions_d_profiles_1d_thermalised"

    particles: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    energy: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    momentum_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class DistributionsDProfiles2DCollisionsElectrons(IdsBaseClass):
    """
    2D profiles for collisions with electrons.

    :ivar power_thermal: Collisional power density to the thermal
        particle population
    :ivar power_fast: Collisional power density to the fast particle
        population
    :ivar torque_thermal_tor: Collisional toroidal torque density to the
        thermal particle population
    :ivar torque_fast_tor: Collisional toroidal torque density to the
        fast particle population
    """
    class Meta:
        name = "distributions_d_profiles_2d_collisions_electrons"

    power_thermal: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    power_fast: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    torque_thermal_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    torque_fast_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class DistributionsDProfiles2DCollisionsIonState(IdsBaseClass):
    """
    2D profiles for collisions with a given ion species state.

    :ivar z_min: Minimum Z of the charge state bundle (z_min = z_max = 0
        for a neutral)
    :ivar z_max: Maximum Z of the charge state bundle (equal to z_min if
        no bundle)
    :ivar label: String identifying charge state (e.g. C+, C+2 , C+3,
        C+4, C+5, C+6, ...)
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar power_thermal: Collisional power density to the thermal
        particle population
    :ivar power_fast: Collisional power density to the fast particle
        population
    :ivar torque_thermal_tor: Collisional toroidal torque density to the
        thermal particle population
    :ivar torque_fast_tor: Collisional toroidal torque density to the
        fast particle population
    """
    class Meta:
        name = "distributions_d_profiles_2d_collisions_ion_state"

    z_min: float = field(
        default=9e+40
    )
    z_max: float = field(
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
    power_thermal: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    power_fast: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    torque_thermal_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    torque_fast_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class DistributionsDProfiles2DPartialCollisionsElectrons(IdsBaseClass):
    """
    2D profiles for collisions with electrons.

    :ivar power_thermal: Collisional power density to the thermal
        particle population
    :ivar power_fast: Collisional power density to the fast particle
        population
    :ivar torque_thermal_tor: Collisional toroidal torque density to the
        thermal particle population
    :ivar torque_fast_tor: Collisional toroidal torque density to the
        fast particle population
    """
    class Meta:
        name = "distributions_d_profiles_2d_partial_collisions_electrons"

    power_thermal: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    power_fast: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    torque_thermal_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    torque_fast_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class DistributionsDProfiles2DPartialCollisionsIonState(IdsBaseClass):
    """
    2D profiles for collisions with a given ion species state.

    :ivar z_min: Minimum Z of the charge state bundle (z_min = z_max = 0
        for a neutral)
    :ivar z_max: Maximum Z of the charge state bundle (equal to z_min if
        no bundle)
    :ivar label: String identifying charge state (e.g. C+, C+2 , C+3,
        C+4, C+5, C+6, ...)
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar power_thermal: Collisional power density to the thermal
        particle population
    :ivar power_fast: Collisional power density to the fast particle
        population
    :ivar torque_thermal_tor: Collisional toroidal torque density to the
        thermal particle population
    :ivar torque_fast_tor: Collisional toroidal torque density to the
        fast particle population
    """
    class Meta:
        name = "distributions_d_profiles_2d_partial_collisions_ion_state"

    z_min: float = field(
        default=9e+40
    )
    z_max: float = field(
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
    power_thermal: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    power_fast: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    torque_thermal_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    torque_fast_tor: Optional[ndarray[(int,int), float]] = field(
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
class PlasmaCompositionIonStateConstant(IdsBaseClass):
    """
    Definition of an ion state (when describing the plasma composition) (constant)

    :ivar z_min: Minimum Z of the charge state bundle (z_min = z_max = 0
        for a neutral)
    :ivar z_max: Maximum Z of the charge state bundle (equal to z_min if
        no bundle)
    :ivar label: String identifying ion state (e.g. C+, C+2 , C+3, C+4,
        C+5, C+6, ...)
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    """
    class Meta:
        name = "plasma_composition_ion_state_constant"

    z_min: float = field(
        default=9e+40
    )
    z_max: float = field(
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
class Rz1DDynamic1(IdsBaseClass):
    """
    Structure for list of R, Z positions (1D, dynamic), time at the root of the
    IDS.

    :ivar r: Major radius
    :ivar z: Height
    """
    class Meta:
        name = "rz1d_dynamic_1"

    r: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    z: Optional[ndarray[(int,), float]] = field(
        default=None
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
class DistributionMarkers(IdsBaseClass):
    """
    Test particles for a given time slice.

    :ivar coordinate_identifier: Set of coordinate identifiers,
        coordinates on which the markers are represented
    :ivar weights: Weight of the markers, i.e. number of real particles
        represented by each marker. The dimension of the vector
        correspond to the number of markers
    :ivar positions: Position of the markers in the set of coordinates.
        The first dimension corresponds to the number of markers, the
        second dimension to the set of coordinates
    :ivar orbit_integrals: Integrals along the markers orbit. These
        dimensionless expressions are of the form: (1/tau) integral
        (f(n_tor,m_pol,k,eq,...) dt) from time - tau to time, where tau
        is the transit/trapping time of the marker and f() a
        dimensionless function (phase factor,drift,etc) of the
        equilibrium (e.g. q) and perturbation (Fourier harmonics
        n_tor,m_pol and bounce harmonic k) along the particles orbits.
        In fact the integrals are taken during the last orbit of each
        marker at the time value of the time node below
    :ivar orbit_integrals_instant: Integrals/quantities along the
        markers orbit. These dimensionless expressions are of the form:
        (1/tau) integral ( f(eq) dt) from time - tau to time_orbit for
        different values of time_orbit in the interval from time - tau
        to time, where tau is the transit/trapping time of the marker
        and f(eq) a dimensionless function (phase, drift,q,etc) of the
        equilibrium along the markers orbits. The integrals are taken
        during the last orbit of each marker at the time value of the
        time node below
    :ivar toroidal_mode: In case the orbit integrals are calculated for
        a given MHD perturbation, index of the toroidal mode considered.
        Refers to the time_slice/toroidal_mode array of the MHD_LINEAR
        IDS in which this perturbation is described
    :ivar time: Time
    """
    class Meta:
        name = "distribution_markers"

    coordinate_identifier: list[IdentifierDynamicAos3] = field(
        default_factory=list
    )
    weights: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    positions: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    orbit_integrals: Optional[DistributionMarkersOrbit] = field(
        default=None
    )
    orbit_integrals_instant: Optional[DistributionMarkersOrbitInstant] = field(
        default=None
    )
    toroidal_mode: int = field(
        default=999999999
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class DistributionProcessIdentifier(IdsBaseClass):
    """
    Identifier an NBI or fusion reaction process intervening affecting a
    distribution function.

    :ivar type: Process type. index=1 for NBI; index=2 for nuclear
        reaction (reaction unspecified); index=3 for nuclear reaction:
        T(d,n)4He [D+T-&gt;He4+n]; index=4 for nuclear reaction:
        He3(d,p)4He [He3+D-&gt;He4+p]; index=5 for nuclear reaction:
        D(d,p)T [D+D-&gt;T+p]; index=6 for nuclear reaction: D(d,n)3He
        [D+D-&gt;He3+n]; index=7 for runaway processes
    :ivar reactant_energy: For nuclear reaction source, energy of the
        reactants. index = 0 for a sum over all energies; index = 1 for
        thermal-thermal; index = 2 for beam-beam; index = 3 for beam-
        thermal
    :ivar nbi_energy: For NBI source, energy of the accelerated species
        considered. index = 0 for a sum over all energies; index = 1 for
        full energiy; index = 2 for half energy; index = 3 for third
        energy
    :ivar nbi_unit: Index of the NBI unit considered. Refers to the
        "unit" array of the NBI IDS. 0 means sum over all NBI units.
    :ivar nbi_beamlets_group: Index of the NBI beamlets group
        considered. Refers to the "unit/beamlets_group" array of the NBI
        IDS. 0 means sum over all beamlets groups.
    """
    class Meta:
        name = "distribution_process_identifier"

    type: Optional[Identifier] = field(
        default=None
    )
    reactant_energy: Optional[Identifier] = field(
        default=None
    )
    nbi_energy: Optional[Identifier] = field(
        default=None
    )
    nbi_unit: int = field(
        default=999999999
    )
    nbi_beamlets_group: int = field(
        default=999999999
    )


@dataclass(slots=True)
class DistributionsDFastFilter(IdsBaseClass):
    """
    Description of how the fast and the thermal particle populations are separated.

    :ivar method: Method used to separate the fast and thermal particle
        population (indices TBD)
    :ivar energy: Energy at which the fast and thermal particle
        populations were separated, as a function of radius
    """
    class Meta:
        name = "distributions_d_fast_filter"

    method: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    energy: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class DistributionsDGgdExpansion(IdsBaseClass):
    """
    Expansion of the distribution function for a given time slice, using a GGD
    representation.

    :ivar grid_subset: Values of the distribution function expansion,
        for various grid subsets
    """
    class Meta:
        name = "distributions_d_ggd_expansion"

    grid_subset: list[GenericGridScalar] = field(
        default_factory=list
    )


@dataclass(slots=True)
class DistributionsDGlobalQuantitiesCollisionsIon(IdsBaseClass):
    """
    Global quantities for collisions with a given ion species.

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed).
    :ivar label: String identifying the species (e.g. H+, D+, T+, He+2,
        C+, D2, DT, CD4, ...)
    :ivar neutral_index: Index of the corresponding neutral species in
        the ../../neutral array
    :ivar power_thermal: Collisional power to the thermal particle
        population
    :ivar power_fast: Collisional power to the fast particle population
    :ivar torque_thermal_tor: Collisional toroidal torque to the thermal
        particle population
    :ivar torque_fast_tor: Collisional toroidal torque to the fast
        particle population
    :ivar multiple_states_flag: Multiple state calculation flag : 0-Only
        one state is considered; 1-Multiple states are considered and
        are described in the state structure
    :ivar state: Collisional exchange with the various states of the ion
        species (ionisation, energy, excitation, ...)
    """
    class Meta:
        name = "distributions_d_global_quantities_collisions_ion"

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
    power_thermal: float = field(
        default=9e+40
    )
    power_fast: float = field(
        default=9e+40
    )
    torque_thermal_tor: float = field(
        default=9e+40
    )
    torque_fast_tor: float = field(
        default=9e+40
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[DistributionsDGlobalQuantitiesCollisionsIonState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class DistributionsDProfiles1DCollisionsIon(IdsBaseClass):
    """
    1D profiles for collisions with a given ion species.

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed).
    :ivar label: String identifying the species (e.g. H+, D+, T+, He+2,
        C+, D2, DT, CD4, ...)
    :ivar neutral_index: Index of the corresponding neutral species in
        the ../../neutral array
    :ivar power_thermal: Collisional power density to the thermal
        particle population
    :ivar power_fast: Collisional power density to the fast particle
        population
    :ivar torque_thermal_tor: Collisional toroidal torque density to the
        thermal particle population
    :ivar torque_fast_tor: Collisional toroidal torque density to the
        fast particle population
    :ivar multiple_states_flag: Multiple state calculation flag : 0-Only
        one state is considered; 1-Multiple states are considered and
        are described in the state structure
    :ivar state: Collisional exchange with the various states of the ion
        species (ionisation, energy, excitation, ...)
    """
    class Meta:
        name = "distributions_d_profiles_1d_collisions_ion"

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
    power_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    torque_thermal_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    torque_fast_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[DistributionsDProfiles1DCollisionsIonState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class DistributionsDProfiles1DPartialCollisionsIon(IdsBaseClass):
    """
    1D profiles for collisions with a given ion species.

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed).
    :ivar label: String identifying the species (e.g. H+, D+, T+, He+2,
        C+, D2, DT, CD4, ...)
    :ivar neutral_index: Index of the corresponding neutral species in
        the ../../neutral array
    :ivar power_thermal: Collisional power density to the thermal
        particle population
    :ivar power_fast: Collisional power density to the fast particle
        population
    :ivar torque_thermal_tor: Collisional toroidal torque density to the
        thermal particle population
    :ivar torque_fast_tor: Collisional toroidal torque density to the
        fast particle population
    :ivar multiple_states_flag: Multiple state calculation flag : 0-Only
        one state is considered; 1-Multiple states are considered and
        are described in the state structure
    :ivar state: Collisional exchange with the various states of the ion
        species (ionisation, energy, excitation, ...)
    """
    class Meta:
        name = "distributions_d_profiles_1d_partial_collisions_ion"

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
    power_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    torque_thermal_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    torque_fast_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[DistributionsDProfiles1DPartialCollisionsIonState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class DistributionsDProfiles2DCollisionsIon(IdsBaseClass):
    """
    2D profiles for collisions with a given ion species.

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed).
    :ivar label: String identifying the species (e.g. H+, D+, T+, He+2,
        C+, D2, DT, CD4, ...)
    :ivar neutral_index: Index of the corresponding neutral species in
        the ../../neutral array
    :ivar power_thermal: Collisional power density to the thermal
        particle population
    :ivar power_fast: Collisional power density to the fast particle
        population
    :ivar torque_thermal_tor: Collisional toroidal torque density to the
        thermal particle population
    :ivar torque_fast_tor: Collisional toroidal torque density to the
        fast particle population
    :ivar multiple_states_flag: Multiple state calculation flag : 0-Only
        one state is considered; 1-Multiple states are considered and
        are described in the state structure
    :ivar state: Collisional exchange with the various states of the ion
        species (ionisation, energy, excitation, ...)
    """
    class Meta:
        name = "distributions_d_profiles_2d_collisions_ion"

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
    power_thermal: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    power_fast: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    torque_thermal_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    torque_fast_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[DistributionsDProfiles2DCollisionsIonState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class DistributionsDProfiles2DGrid(IdsBaseClass):
    """
    2D grid for the distribution.

    :ivar type: Grid type: index=0: Rectangular grid in the (R,Z)
        coordinates; index=1: Rectangular grid in the (radial,
        theta_geometric) coordinates; index=2: Rectangular grid in the
        (radial, theta_straight) coordinates.
    :ivar r: Major radius
    :ivar z: Height
    :ivar theta_straight: Straight field line poloidal angle
    :ivar theta_geometric: Geometrical poloidal angle
    :ivar rho_tor_norm: Normalised toroidal flux coordinate. The
        normalizing value for rho_tor_norm, is the toroidal flux
        coordinate at the equilibrium boundary (LCFS or 99.x % of the
        LCFS in case of a fixed boundary equilibium calculation)
    :ivar rho_tor: Toroidal flux coordinate. The toroidal field used in
        its definition is indicated under vacuum_toroidal_field/b0
    :ivar psi: Poloidal magnetic flux
    :ivar volume: Volume enclosed inside the magnetic surface
    :ivar area: Cross-sectional area of the flux surface
    """
    class Meta:
        name = "distributions_d_profiles_2d_grid"

    type: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    r: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    z: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    theta_straight: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    theta_geometric: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    rho_tor_norm: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    rho_tor: Optional[ndarray[(int,), float]] = field(
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


@dataclass(slots=True)
class DistributionsDProfiles2DPartialCollisionsIon(IdsBaseClass):
    """
    2D profiles for collisions with a given ion species.

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed).
    :ivar label: String identifying the species (e.g. H+, D+, T+, He+2,
        C+, D2, DT, CD4, ...)
    :ivar neutral_index: Index of the corresponding neutral species in
        the ../../neutral array
    :ivar power_thermal: Collisional power density to the thermal
        particle population
    :ivar power_fast: Collisional power density to the fast particle
        population
    :ivar torque_thermal_tor: Collisional toroidal torque density to the
        thermal particle population
    :ivar torque_fast_tor: Collisional toroidal torque density to the
        fast particle population
    :ivar multiple_states_flag: Multiple state calculation flag : 0-Only
        one state is considered; 1-Multiple states are considered and
        are described in the state structure
    :ivar state: Collisional exchange with the various states of the ion
        species (ionisation, energy, excitation, ...)
    """
    class Meta:
        name = "distributions_d_profiles_2d_partial_collisions_ion"

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
    power_thermal: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    power_fast: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    torque_thermal_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    torque_fast_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[DistributionsDProfiles2DPartialCollisionsIonState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class DistributionsDSourceIdentifier(IdsBaseClass):
    """
    Identifier of the source/sink term (wave or particle source process)

    :ivar type: Type of the source term. Index  = 1 for a wave, index =
        2 for a particle source process
    :ivar wave_index: Index into distribution/wave
    :ivar process_index: Index into distribution/process
    """
    class Meta:
        name = "distributions_d_source_identifier"

    type: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    wave_index: int = field(
        default=999999999
    )
    process_index: int = field(
        default=999999999
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
class PlasmaCompositionIonsConstant(IdsBaseClass):
    """
    Description of plasma ions (constant)

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed)
    :ivar label: String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)
    :ivar state: Quantities related to the different states of the
        species (ionisation, energy, excitation, ...)
    """
    class Meta:
        name = "plasma_composition_ions_constant"

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
    state: Optional[PlasmaCompositionIonStateConstant] = field(
        default=None
    )


@dataclass(slots=True)
class PlasmaCompositionNeutralStateConstant(IdsBaseClass):
    """
    Definition of a neutral state (when describing the plasma composition)
    (constant)

    :ivar label: String identifying neutral state
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar neutral_type: Neutral type, in terms of energy. ID =1: cold;
        2: thermal; 3: fast; 4: NBI
    """
    class Meta:
        name = "plasma_composition_neutral_state_constant"

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
    neutral_type: Optional[Identifier] = field(
        default=None
    )


@dataclass(slots=True)
class WavesCoherentWaveIdentifier(IdsBaseClass):
    """
    Wave identifier.

    :ivar type: Wave/antenna type. index=1 for name=EC; index=2 for
        name=IC; index=3 for name=LH
    :ivar antenna_name: Name of the antenna that launches this wave.
        Corresponds to the name specified in antennas/ec(i)/name, or
        antennas/ic(i)/name or antennas/lh(i)/name (depends of
        antenna/wave type) in the ANTENNAS IDS.
    :ivar index_in_antenna: Index of the wave (starts at 1), separating
        different waves generated from a single antenna.
    """
    class Meta:
        name = "waves_coherent_wave_identifier"

    type: Optional[Identifier] = field(
        default=None
    )
    antenna_name: str = field(
        default=""
    )
    index_in_antenna: int = field(
        default=999999999
    )


@dataclass(slots=True)
class DistributionsDGlobalQuantitiesCollisions(IdsBaseClass):
    """
    Global quantities for collisions.

    :ivar electrons: Collisional exchange with electrons
    :ivar ion: Collisional exchange with the various ion species
    """
    class Meta:
        name = "distributions_d_global_quantities_collisions"

    electrons: Optional[DistributionsDGlobalQuantitiesCollisionsElectrons] = field(
        default=None
    )
    ion: list[DistributionsDGlobalQuantitiesCollisionsIon] = field(
        default_factory=list
    )


@dataclass(slots=True)
class DistributionsDGlobalQuantitiesSource(IdsBaseClass):
    """
    Global quantities for a given source/sink term.

    :ivar identifier: Identifier of the wave or particle source process,
        defined respectively in distribution/wave or
        distribution/process
    :ivar particles: Particle source rate
    :ivar power: Total power of the source
    :ivar torque_tor: Total toroidal torque of the source
    """
    class Meta:
        name = "distributions_d_global_quantities_source"

    identifier: Optional[DistributionsDSourceIdentifier] = field(
        default=None
    )
    particles: float = field(
        default=9e+40
    )
    power: float = field(
        default=9e+40
    )
    torque_tor: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class DistributionsDProfiles1DCollisions(IdsBaseClass):
    """
    1D profiles for collisions.

    :ivar electrons: Collisional exchange with electrons
    :ivar ion: Collisional exchange with the various ion species
    """
    class Meta:
        name = "distributions_d_profiles_1d_collisions"

    electrons: Optional[DistributionsDProfiles1DCollisionsElectrons] = field(
        default=None
    )
    ion: list[DistributionsDProfiles1DCollisionsIon] = field(
        default_factory=list
    )


@dataclass(slots=True)
class DistributionsDProfiles1DPartialCollisions(IdsBaseClass):
    """
    1D profiles for collisions.

    :ivar electrons: Collisional exchange with electrons
    :ivar ion: Collisional exchange with the various ion species
    """
    class Meta:
        name = "distributions_d_profiles_1d_partial_collisions"

    electrons: Optional[DistributionsDProfiles1DPartialCollisionsElectrons] = field(
        default=None
    )
    ion: list[DistributionsDProfiles1DPartialCollisionsIon] = field(
        default_factory=list
    )


@dataclass(slots=True)
class DistributionsDProfiles1DPartialSource(IdsBaseClass):
    """
    1D profiles for a given source/sink term.

    :ivar identifier: Identifier of the wave or particle source process,
        defined respectively in distribution/wave or
        distribution/process
    :ivar particles: Source rate of thermal particle density
    :ivar energy: Source rate of energy density
    :ivar momentum_tor: Source rate of toroidal angular momentum density
    """
    class Meta:
        name = "distributions_d_profiles_1d_partial_source"

    identifier: Optional[DistributionsDSourceIdentifier] = field(
        default=None
    )
    particles: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    energy: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    momentum_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class DistributionsDProfiles1DSource(IdsBaseClass):
    """
    1D profiles for a given source/sink term.

    :ivar identifier: Identifier of the wave or particle source process,
        defined respectively in distribution/wave or
        distribution/process
    :ivar particles: Source rate of thermal particle density
    :ivar energy: Source rate of energy density
    :ivar momentum_tor: Source rate of toroidal angular momentum density
    """
    class Meta:
        name = "distributions_d_profiles_1d_source"

    identifier: Optional[DistributionsDSourceIdentifier] = field(
        default=None
    )
    particles: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    energy: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    momentum_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class DistributionsDProfiles2DCollisions(IdsBaseClass):
    """
    2D profiles for collisions.

    :ivar electrons: Collisional exchange with electrons
    :ivar ion: Collisional exchange with the various ion species
    """
    class Meta:
        name = "distributions_d_profiles_2d_collisions"

    electrons: Optional[DistributionsDProfiles2DCollisionsElectrons] = field(
        default=None
    )
    ion: list[DistributionsDProfiles2DCollisionsIon] = field(
        default_factory=list
    )


@dataclass(slots=True)
class DistributionsDProfiles2DPartialCollisions(IdsBaseClass):
    """
    2D profiles for collisions.

    :ivar electrons: Collisional exchange with electrons
    :ivar ion: Collisional exchange with the various ion species
    """
    class Meta:
        name = "distributions_d_profiles_2d_partial_collisions"

    electrons: Optional[DistributionsDProfiles2DPartialCollisionsElectrons] = field(
        default=None
    )
    ion: list[DistributionsDProfiles2DPartialCollisionsIon] = field(
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
class PlasmaCompositionNeutralConstant(IdsBaseClass):
    """
    Definition of plasma neutral (constant)

    :ivar element: List of elements forming the atom or molecule
    :ivar label: String identifying neutral (e.g. H, D, T, He, C, ...)
    :ivar state: State of the species (energy, excitation, ...)
    """
    class Meta:
        name = "plasma_composition_neutral_constant"

    element: list[PlasmaCompositionNeutralElementConstant] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    label: str = field(
        default=""
    )
    state: Optional[PlasmaCompositionNeutralStateConstant] = field(
        default=None
    )


@dataclass(slots=True)
class DistributionSpecies(IdsBaseClass):
    """
    Description of a species in a distribution function related IDS.

    :ivar type: Species type. index=1 for electron; index=2 for ion
        species in a single/average state (refer to ion structure);
        index=3 for ion species in a particular state (refer to
        ion/state structure);  index=4 for neutral species in a
        single/average state (refer to neutral structure); index=5 for
        neutral species in a particular state (refer to neutral/state
        structure);  index=6 for neutron; index=7 for photon
    :ivar ion: Description of the ion or neutral species, used if
        type/index = 2 or 3
    :ivar neutral: Description of the neutral species, used if
        type/index = 4 or 5
    """
    class Meta:
        name = "distribution_species"

    type: Optional[Identifier] = field(
        default=None
    )
    ion: Optional[PlasmaCompositionIonsConstant] = field(
        default=None
    )
    neutral: Optional[PlasmaCompositionNeutralConstant] = field(
        default=None
    )


@dataclass(slots=True)
class DistributionsDGlobalQuantities(IdsBaseClass):
    """
    Global quantities from the distribution, for a given time slice.

    :ivar particles_n: Number of particles in the distribution, i.e. the
        volume integral of the density (note: this is the number of real
        particles and not markers)
    :ivar particles_fast_n: Number of fast particles in the
        distribution, i.e. the volume integral of the density (note:
        this is the number of real particles and not markers)
    :ivar energy: Total energy in the distribution
    :ivar energy_fast: Total energy of the fast particles in the
        distribution
    :ivar energy_fast_parallel: Parallel energy of the fast particles in
        the distribution
    :ivar torque_tor_j_radial: Toroidal torque due to radial currents
    :ivar current_tor: Toroidal current driven by the distribution
    :ivar collisions: Power and torque exchanged between the species
        described by the distribution and the different plasma species
        through collisions
    :ivar thermalisation: Volume integrated source of thermal particles,
        momentum and energy due to thermalisation. Here thermalisation
        refers to non-thermal particles, sufficiently assimilated to the
        thermal background to be re-categorised as thermal particles.
        Note that this source may also be negative if thermal particles
        are being accelerated such that they form a distinct non-thermal
        contribution, e.g. due run-away of RF interactions.
    :ivar source: Set of volume integrated sources and sinks of
        particles, momentum and energy included in the Fokker-Planck
        modelling, related to the various waves or particle source
        processes affecting the distribution
    :ivar time: Time
    """
    class Meta:
        name = "distributions_d_global_quantities"

    particles_n: float = field(
        default=9e+40
    )
    particles_fast_n: float = field(
        default=9e+40
    )
    energy: float = field(
        default=9e+40
    )
    energy_fast: float = field(
        default=9e+40
    )
    energy_fast_parallel: float = field(
        default=9e+40
    )
    torque_tor_j_radial: float = field(
        default=9e+40
    )
    current_tor: float = field(
        default=9e+40
    )
    collisions: Optional[DistributionsDGlobalQuantitiesCollisions] = field(
        default=None
    )
    thermalisation: Optional[DistributionsDGlobalQuantitiesThermalised] = field(
        default=None
    )
    source: list[DistributionsDGlobalQuantitiesSource] = field(
        default_factory=list
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class DistributionsDProfiles1DPartial(IdsBaseClass):
    """
    1D profiles from specific particles in the distribution (trapped, co or
    counter-passing)

    :ivar density: Density (thermal+non-thermal)
    :ivar density_fast: Density of fast particles
    :ivar pressure: Pressure (thermal+non-thermal)
    :ivar pressure_fast: Pressure of fast particles
    :ivar pressure_fast_parallel: Pressure of fast particles in the
        parallel direction
    :ivar current_tor: Total toroidal driven current density (including
        electron and thermal ion back-current, or drag-current)
    :ivar current_fast_tor: Total toroidal driven current density of
        fast (non-thermal) particles (excluding electron and thermal ion
        back-current, or drag-current)
    :ivar torque_tor_j_radial: Toroidal torque due to radial currents
    :ivar collisions: Power and torque exchanged between the species
        described by the distribution and the different plasma species
        through collisions
    :ivar source: Set of flux averaged sources and sinks of particles,
        momentum and energy included in the Fokker-Planck modelling,
        related to the various waves or particle source processes
        affecting the distribution
    """
    class Meta:
        name = "distributions_d_profiles_1d_partial"

    density: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    current_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    current_fast_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    torque_tor_j_radial: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    collisions: Optional[DistributionsDProfiles1DPartialCollisions] = field(
        default=None
    )
    source: list[DistributionsDProfiles1DPartialSource] = field(
        default_factory=list
    )


@dataclass(slots=True)
class DistributionsDProfiles2DPartial(IdsBaseClass):
    """
    2D profiles from specific particles in the distribution (trapped, co or
    counter-passing)

    :ivar density: Density (thermal+non-thermal)
    :ivar density_fast: Density of fast particles
    :ivar pressure: Pressure (thermal+non-thermal)
    :ivar pressure_fast: Pressure of fast particles
    :ivar pressure_fast_parallel: Pressure of fast particles in the
        parallel direction
    :ivar current_tor: Total toroidal driven current density (including
        electron and thermal ion back-current, or drag-current)
    :ivar current_fast_tor: Total toroidal driven current density of
        fast (non-thermal) particles (excluding electron and thermal ion
        back-current, or drag-current)
    :ivar torque_tor_j_radial: Toroidal torque due to radial currents
    :ivar collisions: Power and torque exchanged between the species
        described by the distribution and the different plasma species
        through collisions
    """
    class Meta:
        name = "distributions_d_profiles_2d_partial"

    density: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    density_fast: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    pressure: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    pressure_fast: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    pressure_fast_parallel: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    current_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    current_fast_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    torque_tor_j_radial: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    collisions: Optional[DistributionsDProfiles2DPartialCollisions] = field(
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
class DistributionsDProfiles1D(IdsBaseClass):
    """
    1D profiles from the distribution, for a given time slice.

    :ivar grid: Radial grid
    :ivar fast_filter: Description of how the fast and the thermal
        particle populations are separated
    :ivar density: Density (thermal+non-thermal)
    :ivar density_fast: Density of fast particles
    :ivar pressure: Pressure (thermal+non-thermal)
    :ivar pressure_fast: Pressure of fast particles
    :ivar pressure_fast_parallel: Pressure of fast particles in the
        parallel direction
    :ivar current_tor: Total toroidal driven current density (including
        electron and thermal ion back-current, or drag-current)
    :ivar current_fast_tor: Total toroidal driven current density of
        fast (non-thermal) particles (excluding electron and thermal ion
        back-current, or drag-current)
    :ivar torque_tor_j_radial: Toroidal torque due to radial currents
    :ivar collisions: Power and torque exchanged between the species
        described by the distribution and the different plasma species
        through collisions
    :ivar thermalisation: Flux surface averaged source of thermal
        particles, momentum and energy due to thermalisation. Here
        thermalisation refers to non-thermal particles, sufficiently
        assimilated to the thermal background to be re-categorised as
        thermal particles. Note that this source may also be negative if
        thermal particles are being accelerated such that they form a
        distinct non-thermal contribution, e.g. due run-away of RF
        interactions.
    :ivar source: Set of flux averaged sources and sinks of particles,
        momentum and energy included in the Fokker-Planck modelling,
        related to the various waves or particle source processes
        affecting the distribution
    :ivar trapped: Flux surface averaged profile evaluated using the
        trapped particle part of the distribution.
    :ivar co_passing: Flux surface averaged profile evaluated using the
        co-passing particle part of the distribution.
    :ivar counter_passing: Flux surface averaged profile evaluated using
        the counter-passing particle part of the distribution.
    :ivar time: Time
    """
    class Meta:
        name = "distributions_d_profiles_1d"

    grid: Optional[CoreRadialGrid] = field(
        default=None
    )
    fast_filter: Optional[DistributionsDFastFilter] = field(
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
    pressure_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    current_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    current_fast_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    torque_tor_j_radial: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    collisions: Optional[DistributionsDProfiles1DCollisions] = field(
        default=None
    )
    thermalisation: Optional[DistributionsDProfiles1DThermalised] = field(
        default=None
    )
    source: list[DistributionsDProfiles1DSource] = field(
        default_factory=list
    )
    trapped: Optional[DistributionsDProfiles1DPartial] = field(
        default=None
    )
    co_passing: Optional[DistributionsDProfiles1DPartial] = field(
        default=None
    )
    counter_passing: Optional[DistributionsDProfiles1DPartial] = field(
        default=None
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class DistributionsDProfiles2D(IdsBaseClass):
    """
    2D profiles from the distribution, for a given time slice.

    :ivar grid: Grid. The grid has to be rectangular in a pair of
        coordinates, as specified in type
    :ivar density: Density (thermal+non-thermal)
    :ivar density_fast: Density of fast particles
    :ivar pressure: Pressure (thermal+non-thermal)
    :ivar pressure_fast: Pressure of fast particles
    :ivar pressure_fast_parallel: Pressure of fast particles in the
        parallel direction
    :ivar current_tor: Total toroidal driven current density (including
        electron and thermal ion back-current, or drag-current)
    :ivar current_fast_tor: Total toroidal driven current density of
        fast (non-thermal) particles (excluding electron and thermal ion
        back-current, or drag-current)
    :ivar torque_tor_j_radial: Toroidal torque due to radial currents
    :ivar collisions: Power and torque exchanged between the species
        described by the distribution and the different plasma species
        through collisions
    :ivar trapped: Flux surface averaged profile evaluated using the
        trapped particle part of the distribution.
    :ivar co_passing: Flux surface averaged profile evaluated using the
        co-passing particle part of the distribution.
    :ivar counter_passing: Flux surface averaged profile evaluated using
        the counter-passing particle part of the distribution.
    :ivar time: Time
    """
    class Meta:
        name = "distributions_d_profiles_2d"

    grid: Optional[DistributionsDProfiles2DGrid] = field(
        default=None
    )
    density: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    density_fast: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    pressure: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    pressure_fast: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    pressure_fast_parallel: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    current_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    current_fast_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    torque_tor_j_radial: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    collisions: Optional[DistributionsDProfiles2DCollisions] = field(
        default=None
    )
    trapped: Optional[DistributionsDProfiles2DPartial] = field(
        default=None
    )
    co_passing: Optional[DistributionsDProfiles2DPartial] = field(
        default=None
    )
    counter_passing: Optional[DistributionsDProfiles2DPartial] = field(
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
class DistributionsDGgd(IdsBaseClass):
    """
    Distribution function for a given time slice, using a GGD representation.

    :ivar grid: Grid description
    :ivar temperature: Reference temperature profile used to define the
        local thermal energy and the thermal velocity (for normalisation
        of the grid coordinates)
    :ivar expansion: Distribution function expanded into a vector of
        successive approximations. The first element in the vector
        (expansion(1)) is the zeroth order distribution function, while
        the K:th element in the vector (expansion(K)) is the K:th
        correction, such that the total distribution function is a sum
        over all elements in the expansion vector.
    :ivar expansion_fd3v: Distribution function multiplied by the volume
        of the local velocity cell d3v, expanded into a vector of
        successive approximations. The first element in the vector
        (expansion(1)) is the zeroth order distribution function, while
        the K:th element in the vector (expansion(K)) is the K:th
        correction, such that the total distribution function is a sum
        over all elements in the expansion vector.
    :ivar time: Time
    """
    class Meta:
        name = "distributions_d_ggd"

    grid: Optional[GenericGridDynamic] = field(
        default=None
    )
    temperature: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    expansion: list[DistributionsDGgdExpansion] = field(
        default_factory=list
    )
    expansion_fd3v: list[DistributionsDGgdExpansion] = field(
        default_factory=list
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class DistributionsD(IdsBaseClass):
    """
    Description of a given distribution function.

    :ivar wave: List all waves affecting the distribution, identified as
        in waves/coherent_wave(i)/identifier in the waves IDS
    :ivar process: List all processes (NBI units, fusion reactions, ...)
        affecting the distribution, identified as in
        distribution_sources/source(i)/process in the
        DISTRIBUTION_SOURCES IDS
    :ivar gyro_type: Defines how to interpret the spatial coordinates: 1
        = given at the actual particle birth point; 2 =given at the gyro
        centre of the birth point
    :ivar species: Species described by this distribution
    :ivar global_quantities: Global quantities (integrated over plasma
        volume for moments of the distribution, collisional exchange and
        source terms), for various time slices
    :ivar profiles_1d: Radial profiles (flux surface averaged
        quantities) for various time slices
    :ivar profiles_2d: 2D profiles in the poloidal plane for various
        time slices
    :ivar is_delta_f: If is_delta_f=1, then the distribution represents
        the deviation from a Maxwellian; is_delta_f=0, then the
        distribution represents all particles, i.e. the full-f solution
    :ivar ggd: Distribution represented using the ggd, for various time
        slices
    :ivar markers: Distribution represented by a set of markers (test
        particles)
    """
    class Meta:
        name = "distributions_d"

    wave: list[WavesCoherentWaveIdentifier] = field(
        default_factory=list,
        metadata={
            "max_occurs": 10,
        }
    )
    process: list[DistributionProcessIdentifier] = field(
        default_factory=list,
        metadata={
            "max_occurs": 33,
        }
    )
    gyro_type: int = field(
        default=999999999
    )
    species: Optional[DistributionSpecies] = field(
        default=None
    )
    global_quantities: list[DistributionsDGlobalQuantities] = field(
        default_factory=list
    )
    profiles_1d: list[DistributionsDProfiles1D] = field(
        default_factory=list
    )
    profiles_2d: list[DistributionsDProfiles2D] = field(
        default_factory=list
    )
    is_delta_f: int = field(
        default=999999999
    )
    ggd: list[DistributionsDGgd] = field(
        default_factory=list
    )
    markers: list[DistributionMarkers] = field(
        default_factory=list
    )


@dataclass(slots=True)
class Distributions(IdsBaseClass):
    """Distribution function(s) of one or many particle species.

    This structure is specifically designed to handle non-Maxwellian
    distribution function generated during heating and current drive,
    typically solved using a Fokker-Planck calculation perturbed by a
    heating scheme (e.g. IC, EC, LH, NBI, or alpha heating) and then
    relaxed by Coloumb collisions.

    :ivar ids_properties:
    :ivar distribution: Set of distribution functions. Every
        distribution function has to be associated with only one
        particle species, specified in distri_vec/species/, but there
        could be multiple distribution function for each species. In
        this case, the fast particle populations should be superposed
    :ivar vacuum_toroidal_field: Characteristics of the vacuum toroidal
        field (used in rho_tor definition and in the normalization of
        current densities)
    :ivar magnetic_axis: Magnetic axis position (used to define a
        poloidal angle for the 2D profiles)
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "distributions"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    distribution: list[DistributionsD] = field(
        default_factory=list,
        metadata={
            "max_occurs": 33,
        }
    )
    vacuum_toroidal_field: Optional[BTorVacuum1] = field(
        default=None
    )
    magnetic_axis: Optional[Rz1DDynamic1] = field(
        default=None
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
