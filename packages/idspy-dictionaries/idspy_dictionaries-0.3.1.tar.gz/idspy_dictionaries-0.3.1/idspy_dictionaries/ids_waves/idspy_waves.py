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
class WavesCpx1D(IdsBaseClass):
    """
    Structure for 1D complex number, real and imaginary parts.

    :ivar real: Real part
    :ivar imaginary: Imaginary part
    """
    class Meta:
        name = "waves_CPX_1D"

    real: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    imaginary: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class WavesCpxAmpPhase1D(IdsBaseClass):
    """
    Structure for 1D complex number, amplitude and phase.

    :ivar amplitude: Amplitude
    :ivar phase: Phase
    """
    class Meta:
        name = "waves_CPX_amp_phase_1D"

    amplitude: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    phase: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class WavesCpxAmpPhase2D(IdsBaseClass):
    """
    Structure for 2D complex number, amplitude and phase.

    :ivar amplitude: Amplitude
    :ivar phase: Phase
    """
    class Meta:
        name = "waves_CPX_amp_phase_2D"

    amplitude: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    phase: Optional[ndarray[(int,int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class WavesCoherentWaveBeamTracingBeamK(IdsBaseClass):
    """
    Beam wave vector.

    :ivar k_r: Wave vector component in the major radius direction
    :ivar k_z: Wave vector component in the vertical direction
    :ivar k_tor: Wave vector component in the toroidal direction
    :ivar n_parallel: Parallel refractive index
    :ivar n_perpendicular: Perpendicular refractive index
    :ivar n_tor: Toroidal wave number, contains a single value if
        varying_ntor = 1 to avoid useless repetition constant values
    :ivar varying_n_tor: Flag telling whether n_tor is constant along
        the ray path (0) or varying (1)
    """
    class Meta:
        name = "waves_coherent_wave_beam_tracing_beam_k"

    k_r: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    k_z: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    k_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    n_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    n_perpendicular: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    n_tor: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    varying_n_tor: int = field(
        default=999999999
    )


@dataclass(slots=True)
class WavesCoherentWaveBeamTracingElectrons(IdsBaseClass):
    """
    Electrons related quantities for beam tracing.

    :ivar power: Power absorbed along the beam by the species
    """
    class Meta:
        name = "waves_coherent_wave_beam_tracing_electrons"

    power: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class WavesCoherentWaveBeamTracingIonState(IdsBaseClass):
    """
    State related quantities for beam tracing.

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
    :ivar power: Power absorbed along the beam by the species
    """
    class Meta:
        name = "waves_coherent_wave_beam_tracing_ion_state"

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
    power: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class WavesCoherentWaveBeamTracingPowerFlow(IdsBaseClass):
    """
    Power flow for beam tracing.

    :ivar perpendicular: Normalized power flow in the direction
        perpendicular to the magnetic field
    :ivar parallel: Normalized power flow in the direction parallel to
        the magnetic field
    """
    class Meta:
        name = "waves_coherent_wave_beam_tracing_power_flow"

    perpendicular: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class WavesCoherentWaveGlobalQuantitiesElectrons(IdsBaseClass):
    """
    Global quantities related to electrons.

    :ivar power_thermal: Wave power absorbed by the thermal particle
        population
    :ivar power_thermal_n_tor: Wave power absorbed by the thermal
        particle population per toroidal mode number
    :ivar power_fast: Wave power absorbed by the fast particle
        population
    :ivar power_fast_n_tor: Wave power absorbed by the fast particle
        population per toroidal mode number
    :ivar distribution_assumption: Assumption on the distribution
        function used by the wave solver to calculate the power
        deposition on this species: 0 = Maxwellian (linear absorption);
        1 = quasi-linear (F given by a distributions IDS).
    """
    class Meta:
        name = "waves_coherent_wave_global_quantities_electrons"

    power_thermal: float = field(
        default=9e+40
    )
    power_thermal_n_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_fast: float = field(
        default=9e+40
    )
    power_fast_n_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    distribution_assumption: int = field(
        default=999999999
    )


@dataclass(slots=True)
class WavesCoherentWaveGlobalQuantitiesIonState(IdsBaseClass):
    """
    Global quantities related to a given ion species state.

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
    :ivar power_thermal: Wave power absorbed by the thermal particle
        population
    :ivar power_thermal_n_tor: Wave power absorbed by the thermal
        particle population per toroidal mode number
    :ivar power_fast: Wave power absorbed by the fast particle
        population
    :ivar power_fast_n_tor: Wave power absorbed by the fast particle
        population per toroidal mode number
    """
    class Meta:
        name = "waves_coherent_wave_global_quantities_ion_state"

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
    power_thermal_n_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_fast: float = field(
        default=9e+40
    )
    power_fast_n_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class WavesCoherentWaveProfiles1DElectrons(IdsBaseClass):
    """
    Radial profiles (RF waves) related to electrons.

    :ivar power_density_thermal: Flux surface averaged absorbed wave
        power density on the thermal species
    :ivar power_density_thermal_n_tor: Flux surface averaged absorbed
        wave power density on the thermal species, per toroidal mode
        number
    :ivar power_density_fast: Flux surface averaged absorbed wave power
        density on the fast species
    :ivar power_density_fast_n_tor: Flux surface averaged absorbed wave
        power density on the fast species, per toroidal mode number
    :ivar power_inside_thermal: Absorbed wave power on thermal species
        inside a flux surface (cumulative volume integral of the
        absorbed power density)
    :ivar power_inside_thermal_n_tor: Absorbed wave power on thermal
        species inside a flux surface (cumulative volume integral of the
        absorbed power density), per toroidal mode number
    :ivar power_inside_fast: Absorbed wave power on thermal species
        inside a flux surface (cumulative volume integral of the
        absorbed power density)
    :ivar power_inside_fast_n_tor: Absorbed wave power on thermal
        species inside a flux surface (cumulative volume integral of the
        absorbed power density), per toroidal mode number
    """
    class Meta:
        name = "waves_coherent_wave_profiles_1d_electrons"

    power_density_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_density_thermal_n_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    power_density_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_density_fast_n_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    power_inside_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_inside_thermal_n_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    power_inside_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_inside_fast_n_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class WavesCoherentWaveProfiles1DIonState(IdsBaseClass):
    """
    Radial profiles (RF waves) related to a given ion species state.

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
    :ivar power_density_thermal: Flux surface averaged absorbed wave
        power density on the thermal species
    :ivar power_density_thermal_n_tor: Flux surface averaged absorbed
        wave power density on the thermal species, per toroidal mode
        number
    :ivar power_density_fast: Flux surface averaged absorbed wave power
        density on the fast species
    :ivar power_density_fast_n_tor: Flux surface averaged absorbed wave
        power density on the fast species, per toroidal mode number
    :ivar power_inside_thermal: Absorbed wave power on thermal species
        inside a flux surface (cumulative volume integral of the
        absorbed power density)
    :ivar power_inside_thermal_n_tor: Absorbed wave power on thermal
        species inside a flux surface (cumulative volume integral of the
        absorbed power density), per toroidal mode number
    :ivar power_inside_fast: Absorbed wave power on thermal species
        inside a flux surface (cumulative volume integral of the
        absorbed power density)
    :ivar power_inside_fast_n_tor: Absorbed wave power on thermal
        species inside a flux surface (cumulative volume integral of the
        absorbed power density), per toroidal mode number
    """
    class Meta:
        name = "waves_coherent_wave_profiles_1d_ion_state"

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
    power_density_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_density_thermal_n_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    power_density_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_density_fast_n_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    power_inside_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_inside_thermal_n_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    power_inside_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_inside_fast_n_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class WavesCoherentWaveProfiles2DElectrons(IdsBaseClass):
    """
    Global quantities related to electrons.

    :ivar power_density_thermal: Absorbed wave power density on the
        thermal species
    :ivar power_density_thermal_n_tor: Absorbed wave power density on
        the thermal species, per toroidal mode number
    :ivar power_density_fast: Absorbed wave power density on the fast
        species
    :ivar power_density_fast_n_tor: Absorbed wave power density on the
        fast species, per toroidal mode number
    """
    class Meta:
        name = "waves_coherent_wave_profiles_2d_electrons"

    power_density_thermal: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    power_density_thermal_n_tor: Optional[ndarray[(int,int, int), float]] = field(
        default=None
    )
    power_density_fast: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    power_density_fast_n_tor: Optional[ndarray[(int,int, int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class WavesCoherentWaveProfiles2DIonState(IdsBaseClass):
    """
    Global quantities related to a given ion species state.

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
    :ivar power_density_thermal: Absorbed wave power density on the
        thermal species
    :ivar power_density_thermal_n_tor: Absorbed wave power density on
        the thermal species, per toroidal mode number
    :ivar power_density_fast: Absorbed wave power density on the fast
        species
    :ivar power_density_fast_n_tor: Absorbed wave power density on the
        fast species, per toroidal mode number
    """
    class Meta:
        name = "waves_coherent_wave_profiles_2d_ion_state"

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
    power_density_thermal: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    power_density_thermal_n_tor: Optional[ndarray[(int,int, int), float]] = field(
        default=None
    )
    power_density_fast: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    power_density_fast_n_tor: Optional[ndarray[(int,int, int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class WavesRzphipsitheta1DDynamicAos3(IdsBaseClass):
    """
    Structure for R, Z, Phi, Psi, Theta positions (1D, dynamic within a type 3
    array of structure)

    :ivar r: Major radius
    :ivar z: Height
    :ivar phi: Toroidal angle
    :ivar psi: Poloidal flux
    :ivar theta: Poloidal angle
    """
    class Meta:
        name = "waves_rzphipsitheta1d_dynamic_aos3"

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
    theta: Optional[ndarray[(int,), float]] = field(
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
class WavesCoherentWaveBeamTracingBeamEField(IdsBaseClass):
    """
    Components of the electric field for beam tracing.

    :ivar plus: Left hand polarised electric field component
    :ivar minus: Right hand polarised electric field component
    :ivar parallel: Parallel to magnetic field polarised electric field
        component
    """
    class Meta:
        name = "waves_coherent_wave_beam_tracing_beam_e_field"

    plus: Optional[WavesCpx1D] = field(
        default=None
    )
    minus: Optional[WavesCpx1D] = field(
        default=None
    )
    parallel: Optional[WavesCpx1D] = field(
        default=None
    )


@dataclass(slots=True)
class WavesCoherentWaveBeamTracingIon(IdsBaseClass):
    """
    Ion related quantities for beam tracing.

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed).
    :ivar label: String identifying the species (e.g. H+, D+, T+, He+2,
        C+, D2, DT, CD4, ...)
    :ivar power: Power absorbed along the beam by the species
    :ivar multiple_states_flag: Multiple state calculation flag : 0-Only
        one state is considered; 1-Multiple states are considered and
        are described in the state structure
    :ivar state: Collisional exchange with the various states of the ion
        species (ionisation, energy, excitation, ...)
    """
    class Meta:
        name = "waves_coherent_wave_beam_tracing_ion"

    element: list[PlasmaCompositionNeutralElement] = field(
        default_factory=list
    )
    z_ion: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    power: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[WavesCoherentWaveBeamTracingIonState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class WavesCoherentWaveFullWaveBField(IdsBaseClass):
    """
    Components of the full wave magnetic field.

    :ivar parallel: Parallel (to the static magnetic field) component of
        the wave magnetic field, given on various grid subsets
    :ivar normal: Magnitude of wave magnetic field normal to a flux
        surface, given on various grid subsets
    :ivar bi_normal: Magnitude of perpendicular (to the static magnetic
        field) wave magnetic field tangent to a flux surface, given on
        various grid subsets
    """
    class Meta:
        name = "waves_coherent_wave_full_wave_b_field"

    parallel: list[GenericGridScalar] = field(
        default_factory=list
    )
    normal: list[GenericGridScalar] = field(
        default_factory=list
    )
    bi_normal: list[GenericGridScalar] = field(
        default_factory=list
    )


@dataclass(slots=True)
class WavesCoherentWaveFullWaveEField(IdsBaseClass):
    """
    Components of the full wave electric field.

    :ivar plus: Left hand circularly polarised component of the
        perpendicular (to the static magnetic field) electric field,
        given on various grid subsets
    :ivar minus: Right hand circularly polarised component of the
        perpendicular (to the static magnetic field) electric field,
        given on various grid subsets
    :ivar parallel: Parallel (to the static magnetic field) component of
        electric field, given on various grid subsets
    :ivar normal: Magnitude of wave electric field normal to a flux
        surface, given on various grid subsets
    :ivar bi_normal: Magnitude of perpendicular (to the static magnetic
        field) wave electric field tangent to a flux surface, given on
        various grid subsets
    """
    class Meta:
        name = "waves_coherent_wave_full_wave_e_field"

    plus: list[GenericGridScalar] = field(
        default_factory=list
    )
    minus: list[GenericGridScalar] = field(
        default_factory=list
    )
    parallel: list[GenericGridScalar] = field(
        default_factory=list
    )
    normal: list[GenericGridScalar] = field(
        default_factory=list
    )
    bi_normal: list[GenericGridScalar] = field(
        default_factory=list
    )


@dataclass(slots=True)
class WavesCoherentWaveGlobalQuantitiesIon(IdsBaseClass):
    """
    Global quantities related to a given ion species.

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed).
    :ivar label: String identifying the species (e.g. H+, D+, T+, He+2,
        C+, D2, DT, CD4, ...)
    :ivar power_thermal: Wave power absorbed by the thermal particle
        population
    :ivar power_thermal_n_tor: Wave power absorbed by the thermal
        particle population per toroidal mode number
    :ivar power_fast: Wave power absorbed by the fast particle
        population
    :ivar power_fast_n_tor: Wave power absorbed by the fast particle
        population per toroidal mode number
    :ivar multiple_states_flag: Multiple state calculation flag : 0-Only
        one state is considered; 1-Multiple states are considered and
        are described in the state structure
    :ivar distribution_assumption: Assumption on the distribution
        function used by the wave solver to calculate the power
        deposition on this species: 0 = Maxwellian (linear absorption);
        1 = quasi-linear (F given by a distributions IDS).
    :ivar state: Collisional exchange with the various states of the ion
        species (ionisation, energy, excitation, ...)
    """
    class Meta:
        name = "waves_coherent_wave_global_quantities_ion"

    element: list[PlasmaCompositionNeutralElement] = field(
        default_factory=list
    )
    z_ion: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    power_thermal: float = field(
        default=9e+40
    )
    power_thermal_n_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_fast: float = field(
        default=9e+40
    )
    power_fast_n_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    distribution_assumption: int = field(
        default=999999999
    )
    state: list[WavesCoherentWaveGlobalQuantitiesIonState] = field(
        default_factory=list
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
class WavesCoherentWaveProfiles1DIon(IdsBaseClass):
    """
    Radial profiles (RF waves) related to a given ion species.

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed).
    :ivar label: String identifying the species (e.g. H+, D+, T+, He+2,
        C+, D2, DT, CD4, ...)
    :ivar power_density_thermal: Flux surface averaged absorbed wave
        power density on the thermal species
    :ivar power_density_thermal_n_tor: Flux surface averaged absorbed
        wave power density on the thermal species, per toroidal mode
        number
    :ivar power_density_fast: Flux surface averaged absorbed wave power
        density on the fast species
    :ivar power_density_fast_n_tor: Flux surface averaged absorbed wave
        power density on the fast species, per toroidal mode number
    :ivar power_inside_thermal: Absorbed wave power on thermal species
        inside a flux surface (cumulative volume integral of the
        absorbed power density)
    :ivar power_inside_thermal_n_tor: Absorbed wave power on thermal
        species inside a flux surface (cumulative volume integral of the
        absorbed power density), per toroidal mode number
    :ivar power_inside_fast: Absorbed wave power on thermal species
        inside a flux surface (cumulative volume integral of the
        absorbed power density)
    :ivar power_inside_fast_n_tor: Absorbed wave power on thermal
        species inside a flux surface (cumulative volume integral of the
        absorbed power density), per toroidal mode number
    :ivar multiple_states_flag: Multiple state calculation flag : 0-Only
        one state is considered; 1-Multiple states are considered and
        are described in the state structure
    :ivar state: Collisional exchange with the various states of the ion
        species (ionisation, energy, excitation, ...)
    """
    class Meta:
        name = "waves_coherent_wave_profiles_1d_ion"

    element: list[PlasmaCompositionNeutralElement] = field(
        default_factory=list
    )
    z_ion: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    power_density_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_density_thermal_n_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    power_density_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_density_fast_n_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    power_inside_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_inside_thermal_n_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    power_inside_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_inside_fast_n_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[WavesCoherentWaveProfiles1DIonState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class WavesCoherentWaveProfiles2DGrid(IdsBaseClass):
    """
    2D grid for waves.

    :ivar type: Grid type: index=0: Rectangular grid in the (R,Z)
        coordinates; index=1: Rectangular grid in the (radial,
        theta_geometric) coordinates; index=2: Rectangular grid in the
        (radial, theta_straight) coordinates. index=3: unstructured
        grid.
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
        name = "waves_coherent_wave_profiles_2d_grid"

    type: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    r: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    z: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    theta_straight: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    theta_geometric: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    rho_tor_norm: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    rho_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    psi: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    volume: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    area: Optional[ndarray[(int,int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class WavesCoherentWaveProfiles2DIon(IdsBaseClass):
    """
    Global quantities related to a given ion species.

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed).
    :ivar label: String identifying the species (e.g. H+, D+, T+, He+2,
        C+, D2, DT, CD4, ...)
    :ivar power_density_thermal: Absorbed wave power density on the
        thermal species
    :ivar power_density_thermal_n_tor: Absorbed wave power density on
        the thermal species, per toroidal mode number
    :ivar power_density_fast: Absorbed wave power density on the fast
        species
    :ivar power_density_fast_n_tor: Absorbed wave power density on the
        fast species, per toroidal mode number
    :ivar multiple_states_flag: Multiple state calculation flag : 0-Only
        one state is considered; 1-Multiple states are considered and
        are described in the state structure
    :ivar state: Collisional exchange with the various states of the ion
        species (ionisation, energy, excitation, ...)
    """
    class Meta:
        name = "waves_coherent_wave_profiles_2d_ion"

    element: list[PlasmaCompositionNeutralElement] = field(
        default_factory=list
    )
    z_ion: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    power_density_thermal: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    power_density_thermal_n_tor: Optional[ndarray[(int,int, int), float]] = field(
        default=None
    )
    power_density_fast: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    power_density_fast_n_tor: Optional[ndarray[(int,int, int), float]] = field(
        default=None
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[WavesCoherentWaveProfiles2DIonState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class WavesProfiles1DEFieldNTor(IdsBaseClass):
    """
    Components of the surface averaged electric field.

    :ivar plus: Left hand polarised electric field component for every
        flux surface
    :ivar minus: Right hand polarised electric field component for every
        flux surface
    :ivar parallel: Parallel electric field component for every flux
        surface
    """
    class Meta:
        name = "waves_profiles_1d_e_field_n_tor"

    plus: Optional[WavesCpxAmpPhase1D] = field(
        default=None
    )
    minus: Optional[WavesCpxAmpPhase1D] = field(
        default=None
    )
    parallel: Optional[WavesCpxAmpPhase1D] = field(
        default=None
    )


@dataclass(slots=True)
class WavesProfiles2DEFieldNTor(IdsBaseClass):
    """
    Components of the surface averaged electric field.

    :ivar plus: Left hand polarised electric field component
    :ivar minus: Right hand polarised electric field component
    :ivar parallel: Parallel electric field component
    """
    class Meta:
        name = "waves_profiles_2d_e_field_n_tor"

    plus: Optional[WavesCpxAmpPhase2D] = field(
        default=None
    )
    minus: Optional[WavesCpxAmpPhase2D] = field(
        default=None
    )
    parallel: Optional[WavesCpxAmpPhase2D] = field(
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
class WavesCoherentWaveBeamTracingBeam(IdsBaseClass):
    """
    Beam description.

    :ivar power_initial: Initial power in the ray/beam
    :ivar length: Ray/beam curvilinear length
    :ivar position: Position of the ray/beam along its path
    :ivar wave_vector: Wave vector of the ray/beam along its path
    :ivar e_field: Electric field polarization of the ray/beam along its
        path
    :ivar power_flow_norm: Normalised power flow
    :ivar electrons: Quantities related to the electrons
    :ivar ion: Quantities related to the different ion species
    """
    class Meta:
        name = "waves_coherent_wave_beam_tracing_beam"

    power_initial: float = field(
        default=9e+40
    )
    length: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    position: Optional[WavesRzphipsitheta1DDynamicAos3] = field(
        default=None
    )
    wave_vector: Optional[WavesCoherentWaveBeamTracingBeamK] = field(
        default=None
    )
    e_field: Optional[WavesCoherentWaveBeamTracingBeamEField] = field(
        default=None
    )
    power_flow_norm: Optional[WavesCoherentWaveBeamTracingPowerFlow] = field(
        default=None
    )
    electrons: Optional[WavesCoherentWaveBeamTracingElectrons] = field(
        default=None
    )
    ion: list[WavesCoherentWaveBeamTracingIon] = field(
        default_factory=list
    )


@dataclass(slots=True)
class WavesCoherentWaveGlobalQuantities(IdsBaseClass):
    """
    Global quantities (RF waves) for a given time slice.

    :ivar frequency: Wave frequency
    :ivar n_tor: Toroidal mode numbers
    :ivar power: Total absorbed wave power
    :ivar power_n_tor: Absorbed wave power per toroidal mode number
    :ivar current_tor: Wave driven toroidal current from a stand alone
        calculation (not consistent with other sources)
    :ivar current_tor_n_tor: Wave driven toroidal current from a stand
        alone calculation (not consistent with other sources) per
        toroidal mode number
    :ivar electrons: Quantities related to the electrons
    :ivar ion: Quantities related to the different ion species
    :ivar time: Time
    """
    class Meta:
        name = "waves_coherent_wave_global_quantities"

    frequency: float = field(
        default=9e+40
    )
    n_tor: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    power: float = field(
        default=9e+40
    )
    power_n_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    current_tor: float = field(
        default=9e+40
    )
    current_tor_n_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    electrons: Optional[WavesCoherentWaveGlobalQuantitiesElectrons] = field(
        default=None
    )
    ion: list[WavesCoherentWaveGlobalQuantitiesIon] = field(
        default_factory=list
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class WavesCoherentWaveProfiles1D(IdsBaseClass):
    """
    Radial profiles (RF waves) for a given time slice.

    :ivar grid: Radial grid
    :ivar n_tor: Toroidal mode numbers
    :ivar power_density: Flux surface averaged total absorbed wave power
        density (electrons + ion + fast populations)
    :ivar power_density_n_tor: Flux surface averaged absorbed wave power
        density per toroidal mode number
    :ivar power_inside: Total absorbed wave power (electrons + ion +
        fast populations) inside a flux surface (cumulative volume
        integral of the absorbed power density)
    :ivar power_inside_n_tor: Total absorbed wave power (electrons + ion
        + fast populations) inside a flux surface (cumulative volume
        integral of the absorbed power density), per toroidal mode
        number
    :ivar current_tor_inside: Wave driven toroidal current, inside a
        flux surface
    :ivar current_tor_inside_n_tor: Wave driven toroidal current, inside
        a flux surface, per toroidal mode number
    :ivar current_parallel_density: Flux surface averaged wave driven
        parallel current density = average(j.B) / B0, where B0 =
        vacuum_toroidal_field/b0.
    :ivar current_parallel_density_n_tor: Flux surface averaged wave
        driven parallel current density, per toroidal mode number
    :ivar e_field_n_tor: Components of the electric field per toroidal
        mode number, averaged over the flux surface, where the averaged
        is weighted with the power deposition density, such that e_field
        = ave(e_field.power_density) / ave(power_density)
    :ivar k_perpendicular: Perpendicular wave vector,  averaged over the
        flux surface, where the averaged is weighted with the power
        deposition density, such that k_perpendicular =
        ave(k_perpendicular.power_density) / ave(power_density), for
        every flux surface and every toroidal number
    :ivar electrons: Quantities related to the electrons
    :ivar ion: Quantities related to the different ion species
    :ivar time: Time
    """
    class Meta:
        name = "waves_coherent_wave_profiles_1d"

    grid: Optional[CoreRadialGrid] = field(
        default=None
    )
    n_tor: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    power_density: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_density_n_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    power_inside: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_inside_n_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    current_tor_inside: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    current_tor_inside_n_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    current_parallel_density: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    current_parallel_density_n_tor: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    e_field_n_tor: list[WavesProfiles1DEFieldNTor] = field(
        default_factory=list
    )
    k_perpendicular: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    electrons: Optional[WavesCoherentWaveProfiles1DElectrons] = field(
        default=None
    )
    ion: list[WavesCoherentWaveProfiles1DIon] = field(
        default_factory=list
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class WavesCoherentWaveProfiles2D(IdsBaseClass):
    """
    2D profiles (RF waves) for a given time slice.

    :ivar grid: 2D grid in a poloidal cross-section
    :ivar n_tor: Toroidal mode numbers
    :ivar power_density: Total absorbed wave power density (electrons +
        ion + fast populations)
    :ivar power_density_n_tor: Absorbed wave power density per toroidal
        mode number
    :ivar e_field_n_tor: Components of the electric field per toroidal
        mode number
    :ivar electrons: Quantities related to the electrons
    :ivar ion: Quantities related to the different ion species
    :ivar time: Time
    """
    class Meta:
        name = "waves_coherent_wave_profiles_2d"

    grid: Optional[WavesCoherentWaveProfiles2DGrid] = field(
        default=None
    )
    n_tor: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    power_density: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    power_density_n_tor: Optional[ndarray[(int,int, int), float]] = field(
        default=None
    )
    e_field_n_tor: list[WavesProfiles2DEFieldNTor] = field(
        default_factory=list
    )
    electrons: Optional[WavesCoherentWaveProfiles2DElectrons] = field(
        default=None
    )
    ion: list[WavesCoherentWaveProfiles2DIon] = field(
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
class WavesCoherentWaveBeamTracing(IdsBaseClass):
    """
    Beam tracing calculations for a given time slice.

    :ivar beam: Set of rays/beams describing the wave propagation
    :ivar time: Time
    """
    class Meta:
        name = "waves_coherent_wave_beam_tracing"

    beam: list[WavesCoherentWaveBeamTracingBeam] = field(
        default_factory=list
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
class WavesCoherentWaveFullWave(IdsBaseClass):
    """
    Full wave solution for a given time slice.

    :ivar grid: Grid description
    :ivar e_field: Components of the wave electric field
    :ivar b_field: Components of the wave magnetic field
    :ivar k_perpendicular: Perpendicular wave vector, given on various
        grid subsets
    :ivar time: Time
    """
    class Meta:
        name = "waves_coherent_wave_full_wave"

    grid: Optional[GenericGridDynamic] = field(
        default=None
    )
    e_field: Optional[WavesCoherentWaveFullWaveEField] = field(
        default=None
    )
    b_field: Optional[WavesCoherentWaveFullWaveBField] = field(
        default=None
    )
    k_perpendicular: list[GenericGridScalar] = field(
        default_factory=list
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class WavesCoherentWave(IdsBaseClass):
    """
    Source terms for a given actuator.

    :ivar identifier: Identifier of the coherent wave, in terms of the
        type and name of the antenna driving the wave and an index
        separating waves driven by the same antenna.
    :ivar wave_solver_type: Type of wave deposition solver used for this
        wave. Index = 1 for beam/ray tracing; index = 2 for full wave
    :ivar global_quantities: Global quantities for various time slices
    :ivar profiles_1d: Source radial profiles (flux surface averaged
        quantities) for various time slices
    :ivar profiles_2d: 2D profiles in poloidal cross-section, for
        various time slices
    :ivar beam_tracing: Beam tracing calculations, for various time
        slices
    :ivar full_wave: Solution by a full wave code, given on a generic
        grid description, for various time slices
    """
    class Meta:
        name = "waves_coherent_wave"

    identifier: Optional[WavesCoherentWaveIdentifier] = field(
        default=None
    )
    wave_solver_type: Optional[Identifier] = field(
        default=None
    )
    global_quantities: list[WavesCoherentWaveGlobalQuantities] = field(
        default_factory=list
    )
    profiles_1d: list[WavesCoherentWaveProfiles1D] = field(
        default_factory=list
    )
    profiles_2d: list[WavesCoherentWaveProfiles2D] = field(
        default_factory=list
    )
    beam_tracing: list[WavesCoherentWaveBeamTracing] = field(
        default_factory=list
    )
    full_wave: list[WavesCoherentWaveFullWave] = field(
        default_factory=list
    )


@dataclass(slots=True)
class Waves(IdsBaseClass):
    """RF wave propagation and deposition.

    Note that current estimates in this IDS are a priori not taking into
    account synergies between multiple sources (a convergence loop with
    Fokker-Planck calculations is required to account for such
    synergies)

    :ivar ids_properties:
    :ivar coherent_wave: Wave description for each frequency
    :ivar vacuum_toroidal_field: Characteristics of the vacuum toroidal
        field (used in rho_tor definition)
    :ivar magnetic_axis: Magnetic axis position (used to define a
        poloidal angle for the 2D profiles)
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "waves"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    coherent_wave: list[WavesCoherentWave] = field(
        default_factory=list,
        metadata={
            "max_occurs": 100,
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
