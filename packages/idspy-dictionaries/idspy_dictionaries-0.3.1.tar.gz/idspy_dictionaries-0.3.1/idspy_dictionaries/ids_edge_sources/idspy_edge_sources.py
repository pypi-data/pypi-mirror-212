#__version__='0.3.1'
#__imas_commit__='dd6854b4d07'
#__imas_version__='3.7.1'
from ..dataclasses_idsschema import IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Dict, Optional


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
class EdgeSourcesSourceGgdElectrons(IdsBaseClass):
    """
    Source terms related to electrons.

    :ivar particles: Source term for electron density equation, given on
        various grid subsets
    :ivar energy: Source term for the electron energy equation, given on
        various grid subsets
    """
    class Meta:
        name = "edge_sources_source_ggd_electrons"

    particles: list[GenericGridScalar] = field(
        default_factory=list
    )
    energy: list[GenericGridScalar] = field(
        default_factory=list
    )


@dataclass(slots=True)
class EdgeSourcesSourceGgdFastIon(IdsBaseClass):
    """
    Integrated source terms related to a given ion species (fast sampled data)

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed)
    :ivar label: String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)
    :ivar neutral_index: Index of the corresponding neutral species in
        the ../../neutral array
    :ivar power: Total power source or sink related to this ion species,
        integrated over the volume of the grid subset, for various grid
        subsets.
    """
    class Meta:
        name = "edge_sources_source_ggd_fast_ion"

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
    power: list[GenericGridScalarSinglePosition] = field(
        default_factory=list
    )


@dataclass(slots=True)
class EdgeSourcesSourceGgdIonState(IdsBaseClass):
    """
    Source terms related to the a given state of the ion species.

    :ivar z_min: Minimum Z of the state bundle
    :ivar z_max: Maximum Z of the state bundle
    :ivar label: String identifying state (e.g. C+, C+2 , C+3, C+4, C+5,
        C+6, ...)
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar particles: Source term for the state density transport
        equation
    :ivar energy: Source terms for the state energy transport equation
    :ivar momentum: Source term for momentum equations, on various grid
        subsets
    """
    class Meta:
        name = "edge_sources_source_ggd_ion_state"

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
    particles: list[GenericGridScalar] = field(
        default_factory=list
    )
    energy: list[GenericGridScalar] = field(
        default_factory=list
    )
    momentum: list[GenericGridVectorComponents] = field(
        default_factory=list
    )


@dataclass(slots=True)
class EdgeSourcesSourceGgdNeutralState(IdsBaseClass):
    """
    Source terms related to the a given state of the neutral species.

    :ivar label: String identifying state
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar neutral_type: Neutral type, in terms of energy. ID =1: cold;
        2: thermal; 3: fast; 4: NBI
    :ivar particles: Source term for the state density transport
        equation
    :ivar energy: Source terms for the state energy transport equation
    :ivar momentum: Source term for momentum equations, on various grid
        subsets
    """
    class Meta:
        name = "edge_sources_source_ggd_neutral_state"

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
    neutral_type: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    particles: list[GenericGridScalar] = field(
        default_factory=list
    )
    energy: list[GenericGridScalar] = field(
        default_factory=list
    )
    momentum: list[GenericGridVectorComponents] = field(
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
class EdgeSourcesSourceGgdFast(IdsBaseClass):
    """
    Integrated source terms given on the ggd at a given time slice (fast sampled
    data)

    :ivar ion: Source term integrals related to the various ion species
    :ivar time: Time
    """
    class Meta:
        name = "edge_sources_source_ggd_fast"

    ion: list[EdgeSourcesSourceGgdFastIon] = field(
        default_factory=list
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class EdgeSourcesSourceGgdIon(IdsBaseClass):
    """
    Source terms related to a given ion species.

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed)
    :ivar label: String identifying ion (e.g. H, D, T, He, C, D2, ...)
    :ivar neutral_index: Index of the corresponding neutral species in
        the ../../neutral array
    :ivar particles: Source term for ion density equation, on various
        grid subsets
    :ivar energy: Source term for the ion energy transport equation, on
        various grid subsets
    :ivar momentum: Source term for momentum equations (sum over states
        when multiple states are considered), on various grid subsets
    :ivar multiple_states_flag: Multiple states calculation flag :
        0-Only the 'ion' level is considered and the 'state' array of
        structure is empty; 1-Ion states are considered and are
        described in the 'state' array of structure
    :ivar state: Source terms related to the different states of the
        species (ionisation, energy, excitation, ...)
    """
    class Meta:
        name = "edge_sources_source_ggd_ion"

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
    particles: list[GenericGridScalar] = field(
        default_factory=list
    )
    energy: list[GenericGridScalar] = field(
        default_factory=list
    )
    momentum: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[EdgeSourcesSourceGgdIonState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class EdgeSourcesSourceGgdNeutral(IdsBaseClass):
    """
    Source terms related to a given neutral species.

    :ivar element: List of elements forming the atom or molecule
    :ivar label: String identifying neutral (e.g. H, D, T, He, C, ...)
    :ivar ion_index: Index of the corresponding ion species in the
        ../../ion array
    :ivar particles: Source term for ion density equation, on various
        grid subsets
    :ivar energy: Source term for the ion energy transport equation, on
        various grid subsets
    :ivar momentum: Source term for momentum equations (sum over states
        when multiple states are considered), on various grid subsets
    :ivar multiple_states_flag: Multiple states calculation flag :
        0-Only one state is considered; 1-Multiple states are considered
        and are described in the state structure
    :ivar state: Source terms related to the different states of the
        species (energy, excitation, ...)
    """
    class Meta:
        name = "edge_sources_source_ggd_neutral"

    element: list[PlasmaCompositionNeutralElement] = field(
        default_factory=list
    )
    label: str = field(
        default=""
    )
    ion_index: int = field(
        default=999999999
    )
    particles: list[GenericGridScalar] = field(
        default_factory=list
    )
    energy: list[GenericGridScalar] = field(
        default_factory=list
    )
    momentum: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[EdgeSourcesSourceGgdNeutralState] = field(
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
class EdgeSourcesSourceGgd(IdsBaseClass):
    """
    Source terms for a given time slice.

    :ivar electrons: Sources for electrons
    :ivar ion: Source terms related to the different ion species, in the
        sense of isonuclear or isomolecular sequences. Ionisation states
        (and other types of states) must be differentiated at the state
        level below
    :ivar neutral: Source terms related to the different neutral species
    :ivar total_ion_energy: Source term for the total (summed over ion
        species) energy equation, on various grid subsets
    :ivar momentum: Source term for total momentum equations, on various
        grid subsets
    :ivar current: Current density source
    :ivar time: Time
    """
    class Meta:
        name = "edge_sources_source_ggd"

    electrons: Optional[EdgeSourcesSourceGgdElectrons] = field(
        default=None
    )
    ion: list[EdgeSourcesSourceGgdIon] = field(
        default_factory=list
    )
    neutral: list[EdgeSourcesSourceGgdNeutral] = field(
        default_factory=list
    )
    total_ion_energy: list[GenericGridScalar] = field(
        default_factory=list
    )
    momentum: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    current: list[GenericGridScalar] = field(
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
class EdgeSourcesSource(IdsBaseClass):
    """
    Source terms for a given actuator.

    :ivar identifier: Source term identifier (process causing this
        source term)
    :ivar species: Species causing this source term (if relevant, e.g. a
        particular ion or neutral state in case of line radiation)
    :ivar ggd: Source terms represented using the general grid
        description, for various time slices
    :ivar ggd_fast: Quantities provided at a faster sampling rate than
        the full ggd quantities. These are either integrated quantities
        or local quantities provided on a reduced set of positions.
        Positions and integration domains are described by a set of
        grid_subsets (of size 1 for a position).
    """
    class Meta:
        name = "edge_sources_source"

    identifier: Optional[Identifier] = field(
        default=None
    )
    species: Optional[DistributionSpecies] = field(
        default=None
    )
    ggd: list[EdgeSourcesSourceGgd] = field(
        default_factory=list
    )
    ggd_fast: list[EdgeSourcesSourceGgdFast] = field(
        default_factory=list
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
class EdgeSources(IdsBaseClass):
    """Edge plasma sources.

    Energy terms correspond to the full kinetic energy equation (i.e.
    the energy flux takes into account the energy transported by the
    particle flux)

    :ivar ids_properties:
    :ivar midplane: Choice of midplane definition (use the lowest index
        number if more than one value is relevant)
    :ivar grid_ggd: Grid (using the Generic Grid Description), for
        various time slices. The timebase of this array of structure
        must be a subset of the ggd timebases
    :ivar source: Set of source terms
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "edge_sources"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    midplane: Optional[IdentifierStatic] = field(
        default=None
    )
    grid_ggd: list[GenericGridAos3Root] = field(
        default_factory=list
    )
    source: list[EdgeSourcesSource] = field(
        default_factory=list,
        metadata={
            "max_occurs": 80,
        }
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
