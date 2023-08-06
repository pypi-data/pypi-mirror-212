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
class RadiationProcessGlobalVolume(IdsBaseClass):
    """
    Global quantities (emissions) related to a given volume.

    :ivar power: Total power emitted by all species
    :ivar power_ion_total: Total power emitted by all ion species
    :ivar power_neutral_total: Total power emitted by all neutral
        species
    :ivar power_electrons: Power emitted by electrons
    """
    class Meta:
        name = "radiation_process_global_volume"

    power: float = field(
        default=9e+40
    )
    power_ion_total: float = field(
        default=9e+40
    )
    power_neutral_total: float = field(
        default=9e+40
    )
    power_electrons: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class RadiationProcessProfiles1DElectrons(IdsBaseClass):
    """
    Process terms related to electrons.

    :ivar emissivity: Emissivity from this species
    :ivar power_inside: Radiated power from inside the flux surface
        (volume integral of the emissivity inside the flux surface)
    """
    class Meta:
        name = "radiation_process_profiles_1d_electrons"

    emissivity: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_inside: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class RadiationProcessProfiles1DIonsChargeStates(IdsBaseClass):
    """
    Process terms related to the a given state of the ion species.

    :ivar z_min: Minimum Z of the charge state bundle
    :ivar z_max: Maximum Z of the charge state bundle
    :ivar label: String identifying charge state (e.g. C+, C+2 , C+3,
        C+4, C+5, C+6, ...)
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar emissivity: Emissivity from this species
    :ivar power_inside: Radiated power from inside the flux surface
        (volume integral of the emissivity inside the flux surface)
    """
    class Meta:
        name = "radiation_process_profiles_1d_ions_charge_states"

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
    electron_configuration: str = field(
        default=""
    )
    emissivity: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_inside: Optional[ndarray[(int,), float]] = field(
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
class RadiationProcessGgdElectrons(IdsBaseClass):
    """
    Process terms related to electrons.

    :ivar emissivity: Emissivity from this species, on various grid
        subsets
    """
    class Meta:
        name = "radiation_process_ggd_electrons"

    emissivity: list[GenericGridScalar] = field(
        default_factory=list
    )


@dataclass(slots=True)
class RadiationProcessGgdIonChargeStates(IdsBaseClass):
    """
    Process terms related to a given state of the ion species.

    :ivar z_min: Minimum Z of the charge state bundle
    :ivar z_max: Maximum Z of the charge state bundle
    :ivar label: String identifying charge state (e.g. C+, C+2 , C+3,
        C+4, C+5, C+6, ...)
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar emissivity: Emissivity from this state, on various grid
        subsets
    """
    class Meta:
        name = "radiation_process_ggd_ion_charge_states"

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
    electron_configuration: str = field(
        default=""
    )
    emissivity: list[GenericGridScalar] = field(
        default_factory=list
    )


@dataclass(slots=True)
class RadiationProcessGgdNeutralState(IdsBaseClass):
    """
    Process terms related to a given state of the neutral species.

    :ivar label: String identifying state
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar neutral_type: Neutral type (if the considered state is a
        neutral), in terms of energy. ID =1: cold; 2: thermal; 3: fast;
        4: NBI
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar emissivity: Emissivity from this state, on various grid
        subsets
    """
    class Meta:
        name = "radiation_process_ggd_neutral_state"

    label: str = field(
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
    electron_configuration: str = field(
        default=""
    )
    emissivity: list[GenericGridScalar] = field(
        default_factory=list
    )


@dataclass(slots=True)
class RadiationProcessGlobal(IdsBaseClass):
    """
    Process global quantities for a given time slice.

    :ivar inside_lcfs: Emissions from the core plasma, inside the last
        closed flux surface
    :ivar inside_vessel: Total emissions inside the vacuum vessel
    :ivar time: Time
    """
    class Meta:
        name = "radiation_process_global"

    inside_lcfs: Optional[RadiationProcessGlobalVolume] = field(
        default=None
    )
    inside_vessel: Optional[RadiationProcessGlobalVolume] = field(
        default=None
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class RadiationProcessProfiles1DIons(IdsBaseClass):
    """
    Process terms related to a given ion species.

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed)
    :ivar label: String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)
    :ivar neutral_index: Index of the corresponding neutral species in
        the ../../neutral array
    :ivar emissivity: Emissivity from this species
    :ivar power_inside: Radiated power from inside the flux surface
        (volume integral of the emissivity inside the flux surface)
    :ivar multiple_states_flag: Multiple states calculation flag :
        0-Only one state is considered; 1-Multiple states are considered
        and are described in the state structure
    :ivar state: Process terms related to the different charge states of
        the species (ionisation, energy, excitation, ...)
    """
    class Meta:
        name = "radiation_process_profiles_1d_ions"

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
    emissivity: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_inside: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[RadiationProcessProfiles1DIonsChargeStates] = field(
        default_factory=list
    )


@dataclass(slots=True)
class RadiationProcessProfiles1DNeutralState(IdsBaseClass):
    """
    Process terms related to the a given state of the neutral species.

    :ivar label: String identifying state
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar neutral_type: Neutral type (if the considered state is a
        neutral), in terms of energy. ID =1: cold; 2: thermal; 3: fast;
        4: NBI
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar emissivity: Emissivity from this species
    :ivar power_inside: Radiated power from inside the flux surface
        (volume integral of the emissivity inside the flux surface)
    """
    class Meta:
        name = "radiation_process_profiles_1d_neutral_state"

    label: str = field(
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
    electron_configuration: str = field(
        default=""
    )
    emissivity: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_inside: Optional[ndarray[(int,), float]] = field(
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
class RadiationProcessGgdIon(IdsBaseClass):
    """
    Process terms related to a given ion species.

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed)
    :ivar label: String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)
    :ivar neutral_index: Index of the corresponding neutral species in
        the ../../neutral array
    :ivar emissivity: Emissivity from this species, on various grid
        subsets
    :ivar multiple_states_flag: Multiple states calculation flag :
        0-Only one state is considered; 1-Multiple states are considered
        and are described in the state structure
    :ivar state: Process terms related to the different charge states of
        the species (ionisation, energy, excitation, ...)
    """
    class Meta:
        name = "radiation_process_ggd_ion"

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
    emissivity: list[GenericGridScalar] = field(
        default_factory=list
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[RadiationProcessGgdIonChargeStates] = field(
        default_factory=list
    )


@dataclass(slots=True)
class RadiationProcessGgdNeutral(IdsBaseClass):
    """
    Process terms related to a given neutral species.

    :ivar element: List of elements forming the atom or molecule
    :ivar label: String identifying the neutral species (e.g. H, D, T,
        He, C, ...)
    :ivar ion_index: Index of the corresponding ion species in the
        ../../ion array
    :ivar emissivity: Emissivity from this species, on various grid
        subsets
    :ivar multiple_states_flag: Multiple states calculation flag :
        0-Only one state is considered; 1-Multiple states are considered
        and are described in the state structure
    :ivar state: Process terms related to the different charge states of
        the species (energy, excitation, ...)
    """
    class Meta:
        name = "radiation_process_ggd_neutral"

    element: list[PlasmaCompositionNeutralElement] = field(
        default_factory=list
    )
    label: str = field(
        default=""
    )
    ion_index: int = field(
        default=999999999
    )
    emissivity: list[GenericGridScalar] = field(
        default_factory=list
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[RadiationProcessGgdNeutralState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class RadiationProcessProfiles1DNeutral(IdsBaseClass):
    """
    Process terms related to a given neutral species.

    :ivar element: List of elements forming the atom or molecule
    :ivar label: String identifying the neutral species (e.g. H, D, T,
        He, C, ...)
    :ivar ion_index: Index of the corresponding ion species in the
        ../../ion array
    :ivar emissivity: Emissivity from this species
    :ivar power_inside: Radiated power from inside the flux surface
        (volume integral of the emissivity inside the flux surface)
    :ivar multiple_states_flag: Multiple states calculation flag :
        0-Only one state is considered; 1-Multiple states are considered
        and are described in the state structure
    :ivar state: Process terms related to the different charge states of
        the species (energy, excitation, ...)
    """
    class Meta:
        name = "radiation_process_profiles_1d_neutral"

    element: list[PlasmaCompositionNeutralElement] = field(
        default_factory=list
    )
    label: str = field(
        default=""
    )
    ion_index: int = field(
        default=999999999
    )
    emissivity: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_inside: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[RadiationProcessProfiles1DNeutralState] = field(
        default_factory=list
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
class RadiationProcessGgd(IdsBaseClass):
    """
    Process terms for a given time slice (using the GGD)

    :ivar electrons: Process terms related to electrons
    :ivar ion: Process terms related to the different ion species
    :ivar neutral: Process terms related to the different neutral
        species
    :ivar time: Time
    """
    class Meta:
        name = "radiation_process_ggd"

    electrons: Optional[RadiationProcessGgdElectrons] = field(
        default=None
    )
    ion: list[RadiationProcessGgdIon] = field(
        default_factory=list
    )
    neutral: list[RadiationProcessGgdNeutral] = field(
        default_factory=list
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class RadiationProcessProfiles1D(IdsBaseClass):
    """
    Process terms for a given time slice.

    :ivar grid: Radial grid
    :ivar electrons: Processs terms related to electrons
    :ivar emissivity_ion_total: Emissivity (summed over ion  species)
    :ivar power_inside_ion_total: Total power from ion species (summed
        over ion  species) inside the flux surface (volume integral of
        the emissivity inside the flux surface)
    :ivar emissivity_neutral_total: Emissivity (summed over neutral
        species)
    :ivar power_inside_neutral_total: Total power from ion species
        (summed over neutral species) inside the flux surface (volume
        integral of the emissivity inside the flux surface)
    :ivar ion: Process terms related to the different ion species
    :ivar neutral: Process terms related to the different neutral
        species
    :ivar time: Time
    """
    class Meta:
        name = "radiation_process_profiles_1d"

    grid: Optional[CoreRadialGrid] = field(
        default=None
    )
    electrons: Optional[RadiationProcessProfiles1DElectrons] = field(
        default=None
    )
    emissivity_ion_total: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_inside_ion_total: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    emissivity_neutral_total: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_inside_neutral_total: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    ion: list[RadiationProcessProfiles1DIons] = field(
        default_factory=list
    )
    neutral: list[RadiationProcessProfiles1DNeutral] = field(
        default_factory=list
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
class RadiationProcess(IdsBaseClass):
    """
    Process terms for a given actuator.

    :ivar identifier: Process identifier
    :ivar global_quantities: Scalar volume integrated quantities
    :ivar profiles_1d: Emissivity radial profiles for various time
        slices
    :ivar ggd: Emissivities represented using the general grid
        description, for various time slices
    """
    class Meta:
        name = "radiation_process"

    identifier: Optional[Identifier] = field(
        default=None
    )
    global_quantities: list[RadiationProcessGlobal] = field(
        default_factory=list
    )
    profiles_1d: list[RadiationProcessProfiles1D] = field(
        default_factory=list
    )
    ggd: list[RadiationProcessGgd] = field(
        default_factory=list
    )


@dataclass(slots=True)
class Radiation(IdsBaseClass):
    """
    Radiation emitted by the plasma and neutrals.

    :ivar ids_properties:
    :ivar vacuum_toroidal_field: Characteristics of the vacuum toroidal
        field (used in rho_tor definition)
    :ivar grid_ggd: Grid (using the Generic Grid Description), for
        various time slices. The timebase of this array of structure
        must be a subset of the process/ggd timebases
    :ivar process: Set of emission processes. The radiation
        characteristics are described at the level of the originating
        entity. For instance describe line radiation from neutrals under
        profiles_1d/neutral. Line and recombination radiation under
        profiles_1d/ion. Bremsstrahlung radiation under
        profiles_1d/neutral and ion ...
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "radiation"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    vacuum_toroidal_field: Optional[BTorVacuum1] = field(
        default=None
    )
    grid_ggd: list[GenericGridAos3Root] = field(
        default_factory=list
    )
    process: list[RadiationProcess] = field(
        default_factory=list,
        metadata={
            "max_occurs": 20,
        }
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
