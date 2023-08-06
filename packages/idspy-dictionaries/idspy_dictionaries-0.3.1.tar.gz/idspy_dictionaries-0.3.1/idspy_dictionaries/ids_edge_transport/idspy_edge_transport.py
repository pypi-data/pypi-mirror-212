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
class SignalInt1D(IdsBaseClass):
    """
    Signal (INT_1D) with its time base.

    :ivar time: Time
    """
    class Meta:
        name = "signal_int_1d"

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
            default="INT_1D"
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
class CodeWithTimebase(IdsBaseClass):
    """Description of code-specific parameters when they are gathered below an
    array of structure (e.g. in case of multiple models or sources gathered in a
    single IDS).

    The only difference with the generic code element is the existence
    of a data+time structure for the dynamic signals (output_flag)

    :ivar name: Name of software used
    :ivar commit: Unique commit reference of software
    :ivar version: Unique version (tag) of software
    :ivar repository: URL of software repository
    :ivar parameters: List of the code specific parameters in XML format
    :ivar output_flag: Output flag : 0 means the run is successful,
        other values mean some difficulty has been encountered, the
        exact meaning is then code specific. Negative values mean the
        result shall not be used.
    """
    class Meta:
        name = "code_with_timebase"

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
    output_flag: Optional[SignalInt1D] = field(
        default=None
    )


@dataclass(slots=True)
class EdgeTransportModelDensity(IdsBaseClass):
    """
    Transport coefficients for energy equations.

    :ivar d: Effective diffusivity, on various grid subsets
    :ivar v: Effective convection, on various grid subsets
    :ivar flux: Flux, on various grid subsets
    :ivar flux_limiter: Flux limiter coefficient, on various grid
        subsets
    """
    class Meta:
        name = "edge_transport_model_density"

    d: list[GenericGridScalar] = field(
        default_factory=list
    )
    v: list[GenericGridScalar] = field(
        default_factory=list
    )
    flux: list[GenericGridScalar] = field(
        default_factory=list
    )
    flux_limiter: list[GenericGridScalar] = field(
        default_factory=list
    )


@dataclass(slots=True)
class EdgeTransportModelEnergy(IdsBaseClass):
    """
    Transport coefficients for energy equations.

    :ivar d: Effective diffusivity, on various grid subsets
    :ivar v: Effective convection, on various grid subsets
    :ivar flux: Flux, on various grid subsets
    :ivar flux_limiter: Flux limiter coefficient, on various grid
        subsets
    """
    class Meta:
        name = "edge_transport_model_energy"

    d: list[GenericGridScalar] = field(
        default_factory=list
    )
    v: list[GenericGridScalar] = field(
        default_factory=list
    )
    flux: list[GenericGridScalar] = field(
        default_factory=list
    )
    flux_limiter: list[GenericGridScalar] = field(
        default_factory=list
    )


@dataclass(slots=True)
class EdgeTransportModelGgdFastElectrons(IdsBaseClass):
    """
    Transport coefficients related to electrons (fast sampled data)

    :ivar particle_flux_integrated: Total number of particles of this
        species crossing a surface per unit time, for various surfaces
        (grid subsets)
    :ivar power: Power carried by this species crossing a surface, for
        various surfaces (grid subsets)
    """
    class Meta:
        name = "edge_transport_model_ggd_fast_electrons"

    particle_flux_integrated: list[GenericGridScalarSinglePosition] = field(
        default_factory=list
    )
    power: list[GenericGridScalarSinglePosition] = field(
        default_factory=list
    )


@dataclass(slots=True)
class EdgeTransportModelGgdFastIon(IdsBaseClass):
    """
    Transport coefficients related to a given ion species (fast sampled data)

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed)
    :ivar label: String identifying ion (e.g. H, D, T, He, C, D2, ...)
    :ivar neutral_index: Index of the corresponding neutral species in
        the ../../neutral array
    :ivar particle_flux_integrated: Total number of particles of this
        species crossing a surface per unit time, for various surfaces
        (grid subsets)
    """
    class Meta:
        name = "edge_transport_model_ggd_fast_ion"

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
    particle_flux_integrated: list[GenericGridScalarSinglePosition] = field(
        default_factory=list
    )


@dataclass(slots=True)
class EdgeTransportModelGgdFastNeutral(IdsBaseClass):
    """
    Transport coefficients related to a given neutral species (fast sampled data)

    :ivar element: List of elements forming the atom or molecule
    :ivar label: String identifying neutral (e.g. H, D, T, He, C, ...)
    :ivar ion_index: Index of the corresponding ion species in the
        ../../ion array
    :ivar particle_flux_integrated: Total number of particles of this
        species crossing a surface per unit time, for various surfaces
        (grid subsets)
    """
    class Meta:
        name = "edge_transport_model_ggd_fast_neutral"

    element: list[PlasmaCompositionNeutralElement] = field(
        default_factory=list
    )
    label: str = field(
        default=""
    )
    ion_index: int = field(
        default=999999999
    )
    particle_flux_integrated: list[GenericGridScalarSinglePosition] = field(
        default_factory=list
    )


@dataclass(slots=True)
class EdgeTransportModelMomentum(IdsBaseClass):
    """
    Transport coefficients for momentum equations.

    :ivar d: Effective diffusivity, on various grid subsets
    :ivar v: Effective convection, on various grid subsets
    :ivar flux: Flux, on various grid subsets
    :ivar flux_limiter: Flux limiter coefficient, on various grid
        subsets
    """
    class Meta:
        name = "edge_transport_model_momentum"

    d: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    v: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    flux: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    flux_limiter: list[GenericGridVectorComponents] = field(
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
class EdgeTransportModelElectrons(IdsBaseClass):
    """
    Transport coefficients related to electrons.

    :ivar particles: Transport quantities for the electron density
        equation
    :ivar energy: Transport quantities for the electron energy equation
    """
    class Meta:
        name = "edge_transport_model_electrons"

    particles: Optional[EdgeTransportModelDensity] = field(
        default=None
    )
    energy: Optional[EdgeTransportModelEnergy] = field(
        default=None
    )


@dataclass(slots=True)
class EdgeTransportModelGgdFast(IdsBaseClass):
    """
    Transport coefficient given on the ggd at a given time slice (fast sampled
    data)

    :ivar electrons: Transport quantities and flux integrals related to
        the electrons
    :ivar ion: Transport coefficients and flux integrals related to the
        various ion species, in the sense of isonuclear or isomolecular
        sequences. Ionisation states (and other types of states) must be
        differentiated at the state level below
    :ivar neutral: Transport coefficients and flux integrals related to
        the various ion and neutral species
    :ivar power_ion_total: Power carried by all ions (sum over ions
        species) crossing a surface, for various surfaces (grid subsets)
    :ivar energy_flux_max: Maximum power density over a surface, for
        various surfaces (grid subsets)
    :ivar power: Power (sum over all species) crossing a surface, for
        various surfaces (grid subsets)
    :ivar time: Time
    """
    class Meta:
        name = "edge_transport_model_ggd_fast"

    electrons: Optional[EdgeTransportModelGgdFastElectrons] = field(
        default=None
    )
    ion: list[EdgeTransportModelGgdFastIon] = field(
        default_factory=list
    )
    neutral: list[EdgeTransportModelGgdFastNeutral] = field(
        default_factory=list
    )
    power_ion_total: list[GenericGridScalarSinglePosition] = field(
        default_factory=list
    )
    energy_flux_max: list[GenericGridScalarSinglePosition] = field(
        default_factory=list
    )
    power: list[GenericGridScalarSinglePosition] = field(
        default_factory=list
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class EdgeTransportModelIonState(IdsBaseClass):
    """
    Transport coefficients related to a given state of the ion species.

    :ivar z_min: Minimum Z of the state bundle
    :ivar z_max: Maximum Z of the state bundle
    :ivar label: String identifying state (e.g. C+, C+2 , C+3, C+4, C+5,
        C+6, ...)
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar particles: Transport quantities related to density equation of
        the state considered (thermal+non-thermal)
    :ivar energy: Transport quantities related to the energy equation of
        the state considered
    :ivar momentum: Transport coefficients related to the momentum
        equations of the state considered. The various components two
        levels below this node refer to the momentum vector components,
        while their flux is given in the direction perpendicular to the
        edges or faces of the grid.
    """
    class Meta:
        name = "edge_transport_model_ion_state"

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
    particles: Optional[EdgeTransportModelDensity] = field(
        default=None
    )
    energy: Optional[EdgeTransportModelEnergy] = field(
        default=None
    )
    momentum: Optional[EdgeTransportModelMomentum] = field(
        default=None
    )


@dataclass(slots=True)
class EdgeTransportModelNeutralState(IdsBaseClass):
    """
    Transport coefficients related to a given state of the neutral species.

    :ivar label: String identifying state
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar neutral_type: Neutral type, in terms of energy. ID =1: cold;
        2: thermal; 3: fast; 4: NBI
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar particles: Transport quantities related to density equation of
        the state considered (thermal+non-thermal)
    :ivar energy: Transport quantities related to the energy equation of
        the state considered
    :ivar momentum: Transport coefficients related to the momentum
        equations of the state considered. The various components two
        levels below this node refer to the momentum vector components,
        while their flux is given in the direction perpendicular to the
        edges or faces of the grid.
    """
    class Meta:
        name = "edge_transport_model_neutral_state"

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
    particles: Optional[EdgeTransportModelDensity] = field(
        default=None
    )
    energy: Optional[EdgeTransportModelEnergy] = field(
        default=None
    )
    momentum: Optional[EdgeTransportModelMomentum] = field(
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
class EdgeTransportModelIon(IdsBaseClass):
    """
    Transport coefficients related to a given ion species.

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed)
    :ivar label: String identifying ion (e.g. H, D, T, He, C, D2, ...)
    :ivar neutral_index: Index of the corresponding neutral species in
        the ../../neutral array
    :ivar particles: Transport related to the ion density equation
    :ivar energy: Transport coefficients related to the ion energy
        equation
    :ivar momentum: Transport coefficients for the ion momentum
        equations. The various components two levels below this node
        refer to the momentum vector components, while their flux is
        given in the direction perpendicular to the edges or faces of
        the grid.
    :ivar multiple_states_flag: Multiple states calculation flag :
        0-Only the 'ion' level is considered and the 'state' array of
        structure is empty; 1-Ion states are considered and are
        described in the 'state' array of structure
    :ivar state: Transport coefficients related to the different states
        of the species
    """
    class Meta:
        name = "edge_transport_model_ion"

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
    particles: Optional[EdgeTransportModelDensity] = field(
        default=None
    )
    energy: Optional[EdgeTransportModelEnergy] = field(
        default=None
    )
    momentum: Optional[EdgeTransportModelMomentum] = field(
        default=None
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[EdgeTransportModelIonState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class EdgeTransportModelNeutral(IdsBaseClass):
    """
    Transport coefficients related to a given neutral species.

    :ivar element: List of elements forming the atom or molecule
    :ivar label: String identifying neutral (e.g. H, D, T, He, C, ...)
    :ivar ion_index: Index of the corresponding ion species in the
        ../../ion array
    :ivar particles: Transport related to the ion density equation
    :ivar energy: Transport coefficients related to the ion energy
        equation
    :ivar momentum: Transport coefficients for the neutral momentum
        equations. The various components two levels below this node
        refer to the momentum vector components, while their flux is
        given in the direction perpendicular to the edges or faces of
        the grid.
    :ivar multiple_states_flag: Multiple states calculation flag :
        0-Only one state is considered; 1-Multiple states are considered
        and are described in the state structure
    :ivar state: Transport coefficients related to the different states
        of the species
    """
    class Meta:
        name = "edge_transport_model_neutral"

    element: list[PlasmaCompositionNeutralElement] = field(
        default_factory=list
    )
    label: str = field(
        default=""
    )
    ion_index: int = field(
        default=999999999
    )
    particles: Optional[EdgeTransportModelDensity] = field(
        default=None
    )
    energy: Optional[EdgeTransportModelEnergy] = field(
        default=None
    )
    momentum: Optional[EdgeTransportModelMomentum] = field(
        default=None
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[EdgeTransportModelNeutralState] = field(
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
class EdgeTransportModelGgd(IdsBaseClass):
    """
    Transport coefficient given on the ggd at a given time slice.

    :ivar conductivity: Conductivity, on various grid subsets
    :ivar electrons: Transport quantities related to the electrons
    :ivar total_ion_energy: Transport coefficients for the total (summed
        over ion  species) energy equation
    :ivar momentum: Transport coefficients for total momentum equation.
        The various components two levels below this node refer to the
        momentum vector components, while their flux is given in the
        direction perpendicular to the edges or faces of the grid.
    :ivar ion: Transport coefficients related to the various ion
        species, in the sense of isonuclear or isomolecular sequences.
        Ionisation states (and other types of states) must be
        differentiated at the state level below
    :ivar neutral: Transport coefficients related to the various neutral
        species
    :ivar time: Time
    """
    class Meta:
        name = "edge_transport_model_ggd"

    conductivity: list[GenericGridVectorComponents] = field(
        default_factory=list
    )
    electrons: Optional[EdgeTransportModelElectrons] = field(
        default=None
    )
    total_ion_energy: Optional[EdgeTransportModelEnergy] = field(
        default=None
    )
    momentum: Optional[EdgeTransportModelMomentum] = field(
        default=None
    )
    ion: list[EdgeTransportModelIon] = field(
        default_factory=list
    )
    neutral: list[EdgeTransportModelNeutral] = field(
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
class EdgeTransportModel(IdsBaseClass):
    """
    Transport coefficients for a given model.

    :ivar identifier: Transport model identifier
    :ivar flux_multiplier: Multiplier applied to the particule flux when
        adding its contribution in the expression of the heat flux : can
        be 0, 3/2 or 5/2
    :ivar ggd: Transport coefficients represented using the general grid
        description, for various time slices. Fluxes are given in the
        direction perpendicular to the edges or faces of the grid (flow
        crossing that surface divided by its actual area). Radial fluxes
        are positive when they are directed away from the magnetic axis.
        Poloidal fluxes are positive when they are directed in such a
        way that they travel clockwise around the magnetic axis
        (poloidal plane viewed such that the centerline of the tokamak
        is on the left). Parallel fluxes are positive when they are co-
        directed with the magnetic field. Toroidal fluxes are positive
        if travelling counter-clockwise when looking at the plasma from
        above
    :ivar ggd_fast: Quantities provided at a faster sampling rate than
        the full ggd quantities. These are either integrated quantities
        or local quantities provided on a reduced set of positions.
        Positions and integration domains are described by a set of
        grid_subsets (of size 1 for a position).
    :ivar code: Code-specific parameters used for this model
    """
    class Meta:
        name = "edge_transport_model"

    identifier: Optional[Identifier] = field(
        default=None
    )
    flux_multiplier: float = field(
        default=9e+40
    )
    ggd: list[EdgeTransportModelGgd] = field(
        default_factory=list
    )
    ggd_fast: list[EdgeTransportModelGgdFast] = field(
        default_factory=list
    )
    code: Optional[CodeWithTimebase] = field(
        default=None
    )


@dataclass(slots=True)
class EdgeTransport(IdsBaseClass):
    """Edge plasma transport.

    Energy terms correspond to the full kinetic energy equation (i.e.
    the energy flux takes into account the energy transported by the
    particle flux)

    :ivar ids_properties:
    :ivar midplane: Choice of midplane definition (use the lowest index
        number if more than one value is relevant)
    :ivar grid_ggd: Grid (using the Generic Grid Description), for
        various time slices. The timebase of this array of structure
        must be a subset of the ggd timebases
    :ivar model: Transport is described by a combination of various
        transport models
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "edge_transport"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    midplane: Optional[IdentifierStatic] = field(
        default=None
    )
    grid_ggd: list[GenericGridAos3Root] = field(
        default_factory=list
    )
    model: list[EdgeTransportModel] = field(
        default_factory=list,
        metadata={
            "max_occurs": 10,
        }
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
