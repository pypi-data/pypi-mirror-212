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
class IdentifierDynamicAos31D(IdsBaseClass):
    """Standard type for identifiers (1D arrays for each node), dynamic within type
    3 array of structures (index on time).

    The three fields: name, index and description are all
    representations of the same information. Associated with each
    application of this identifier-type, there should be a translation
    table defining the three fields for all objects to be identified.

    :ivar names: Short string identifiers
    :ivar indices: Integer identifiers (enumeration index within a
        list). Private identifier values must be indicated by a negative
        index.
    :ivar descriptions: Verbose description
    """
    class Meta:
        name = "identifier_dynamic_aos3_1d"

    names: Optional[list[str]] = field(
        default=None
    )
    indices: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    descriptions: Optional[list[str]] = field(
        default=None
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
class Rz1DDynamicAosTime(IdsBaseClass):
    """
    Structure for list of R, Z positions (1D list of Npoints, dynamic within a type
    3 array of structures (index on time), with time as sibling)

    :ivar r: Major radius
    :ivar z: Height
    :ivar time: Time
    """
    class Meta:
        name = "rz1d_dynamic_aos_time"

    r: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    z: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class Rz1DStatic(IdsBaseClass):
    """
    Structure for list of R, Z positions (1D, constant)

    :ivar r: Major radius
    :ivar z: Height
    """
    class Meta:
        name = "rz1d_static"

    r: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    z: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class Rz1DStaticClosedFlag(IdsBaseClass):
    """
    Structure for list of R, Z positions (1D, constant) and closed flag.

    :ivar r: Major radius
    :ivar z: Height
    :ivar closed: Flag identifying whether the contour is closed (1) or
        open (0)
    """
    class Meta:
        name = "rz1d_static_closed_flag"

    r: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    z: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    closed: int = field(
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
class TemperatureReference(IdsBaseClass):
    """
    Structure describing the reference temperature for which static data are given.

    :ivar description: Description of how the reference temperature is
        defined : for which object, at which location, ...
    """
    class Meta:
        name = "temperature_reference"

    description: str = field(
        default=""
    )

    @dataclass(slots=True)
    class Data(IdsBaseClass):
        """
        :ivar class_of: Class of Data Item
        """
        class_of: str = field(
            init=False,
            default="FLT_0D"
        )


@dataclass(slots=True)
class WallGlobalQuantititesElectrons(IdsBaseClass):
    """
    Simple 0D description of plasma-wall interaction, related to electrons.

    :ivar pumping_speed: Pumped particle flux (in equivalent electrons)
    :ivar particle_flux_from_plasma: Particle flux from the plasma (in
        equivalent electrons)
    :ivar particle_flux_from_wall: Particle flux from the wall
        corresponding to the conversion into various neutral types
        (first dimension: 1: cold; 2: thermal; 3: fast), in equivalent
        electrons
    :ivar gas_puff: Gas puff rate (in equivalent electrons)
    :ivar power_inner_target: Electron power on the inner target
    :ivar power_outer_target: Electron power on the inner target
    """
    class Meta:
        name = "wall_global_quantitites_electrons"

    pumping_speed: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    particle_flux_from_plasma: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    particle_flux_from_wall: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    gas_puff: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_inner_target: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_outer_target: Optional[ndarray[(int,), float]] = field(
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
class GenericGridIdentifier(IdsBaseClass):
    """
    Identifier values on a generic grid (dynamic within a type 3 AoS)

    :ivar grid_index: Index of the grid used to represent this quantity
    :ivar grid_subset_index: Index of the grid subset the data is
        provided on
    :ivar identifiers: Identifier values, one value is provided per
        element in the grid subset. If the size of the child arrays is
        1, their value applies to all elements of the subset.
    """
    class Meta:
        name = "generic_grid_identifier"

    grid_index: int = field(
        default=999999999
    )
    grid_subset_index: int = field(
        default=999999999
    )
    identifiers: Optional[IdentifierDynamicAos31D] = field(
        default=None
    )


@dataclass(slots=True)
class Vessel2DAnnular(IdsBaseClass):
    """
    2D vessel annular description.

    :ivar outline_inner: Inner vessel outline. Do NOT repeat the first
        point for closed contours
    :ivar outline_outer: Outer vessel outline. Do NOT repeat the first
        point for closed contours
    :ivar centreline: Centreline, i.e. middle of the vessel layer as a
        series of point. Do NOT repeat the first point for closed
        contours
    :ivar thickness: Thickness of the vessel layer  in the perpendicular
        direction to the centreline. Thickness(i) is the thickness of
        the layer between centreline/r(i),z(i) and
        centreline/r(i+1),z(i+1)
    :ivar resistivity: Resistivity of the vessel unit
    """
    class Meta:
        name = "vessel_2d_annular"

    outline_inner: Optional[Rz1DStaticClosedFlag] = field(
        default=None
    )
    outline_outer: Optional[Rz1DStaticClosedFlag] = field(
        default=None
    )
    centreline: Optional[Rz1DStaticClosedFlag] = field(
        default=None
    )
    thickness: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    resistivity: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class Vessel2DElement(IdsBaseClass):
    """
    2D vessel block element description.

    :ivar name: Name of the block element
    :ivar outline: Outline of the block element. Do NOT repeat the first
        point for closed contours
    :ivar resistivity: Resistivity of the block element
    :ivar j_tor: Toroidal current induced in this block element
    :ivar resistance: Resistance of the block element
    """
    class Meta:
        name = "vessel_2d_element"

    name: str = field(
        default=""
    )
    outline: Optional[Rz1DStaticClosedFlag] = field(
        default=None
    )
    resistivity: float = field(
        default=9e+40
    )
    j_tor: Optional[SignalFlt1D] = field(
        default=None
    )
    resistance: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class Wall2DLimiterUnit(IdsBaseClass):
    """
    2D limiter unit description.

    :ivar name: Name of the limiter unit
    :ivar closed: Flag identifying whether the contour is closed (1) or
        open (0)
    :ivar outline: Irregular outline of the limiting surface. Do NOT
        repeat the first point for closed contours
    :ivar phi_extensions: Simplified description of toroidal angle
        extensions of the unit, by a list of zones defined by their
        centre and full width (in toroidal angle).  In each of these
        zones, the unit outline remains the same. Leave this node empty
        for an axisymmetric unit. The first dimension gives the centre
        and full width toroidal angle values for the unit. The second
        dimension represents the toroidal occurrences of the unit
        countour (i.e. the number of toroidal zones).
    :ivar resistivity: Resistivity of the limiter unit
    """
    class Meta:
        name = "wall_2d_limiter_unit"

    name: str = field(
        default=""
    )
    closed: int = field(
        default=999999999
    )
    outline: Optional[Rz1DStatic] = field(
        default=None
    )
    phi_extensions: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    resistivity: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class Wall2DMobileUnit(IdsBaseClass):
    """
    2D mobile parts description.

    :ivar name: Name of the mobile unit
    :ivar closed: Flag identifying whether the contour is closed (1) or
        open (0)
    :ivar outline: Irregular outline of the mobile unit, for a set of
        time slices. Do NOT repeat the first point for closed contours
    :ivar phi_extensions: Simplified description of toroidal angle
        extensions of the unit, by a list of zones defined by their
        centre and full width (in toroidal angle).  In each of these
        zones, the unit outline remains the same. Leave this node empty
        for an axisymmetric unit. The first dimension gives the centre
        and full width toroidal angle values for the unit. The second
        dimension represents the toroidal occurrences of the unit
        countour (i.e. the number of toroidal zones).
    :ivar resistivity: Resistivity of the mobile unit
    """
    class Meta:
        name = "wall_2d_mobile_unit"

    name: str = field(
        default=""
    )
    closed: int = field(
        default=999999999
    )
    outline: list[Rz1DDynamicAosTime] = field(
        default_factory=list
    )
    phi_extensions: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    resistivity: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class WallDescriptionGgdEnergyIonState(IdsBaseClass):
    """
    Ion state energy fluxes related to the 3D wall description using the GGD.

    :ivar z_min: Minimum Z of the charge state bundle
    :ivar z_max: Maximum Z of the charge state bundle
    :ivar label: String identifying charge state (e.g. C+, C+2 , C+3,
        C+4, C+5, C+6, ...)
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar incident: Incident fluxes for various wall components (grid
        subsets)
    :ivar emitted: Emitted fluxes for various wall components (grid
        subsets)
    """
    class Meta:
        name = "wall_description_ggd_energy_ion_state"

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
    incident: list[GenericGridScalar] = field(
        default_factory=list
    )
    emitted: list[GenericGridScalar] = field(
        default_factory=list
    )


@dataclass(slots=True)
class WallDescriptionGgdEnergyNeutralState(IdsBaseClass):
    """
    Neutral state energy fluxes related to the 3D wall description using the GGD.

    :ivar label: String identifying state
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar neutral_type: Neutral type, in terms of energy. ID =1: cold;
        2: thermal; 3: fast; 4: NBI
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar incident: Incident fluxes for various wall components (grid
        subsets)
    :ivar emitted: Emitted fluxes for various wall components (grid
        subsets)
    """
    class Meta:
        name = "wall_description_ggd_energy_neutral_state"

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
    incident: list[GenericGridScalar] = field(
        default_factory=list
    )
    emitted: list[GenericGridScalar] = field(
        default_factory=list
    )


@dataclass(slots=True)
class WallDescriptionGgdEnergySimple(IdsBaseClass):
    """
    Incident and emitted energy fluxes related to the 3D wall description using the
    GGD.

    :ivar incident: Incident fluxes for various wall components (grid
        subsets)
    :ivar emitted: Emitted fluxes for various wall components (grid
        subsets)
    """
    class Meta:
        name = "wall_description_ggd_energy_simple"

    incident: list[GenericGridScalar] = field(
        default_factory=list
    )
    emitted: list[GenericGridScalar] = field(
        default_factory=list
    )


@dataclass(slots=True)
class WallDescriptionGgdParticleEl(IdsBaseClass):
    """
    Electron fluxes related to the 3D wall description using the GGD.

    :ivar incident: Incident fluxes for various wall components (grid
        subsets)
    :ivar emitted: Emitted fluxes for various wall components (grid
        subsets)
    """
    class Meta:
        name = "wall_description_ggd_particle_el"

    incident: list[GenericGridScalar] = field(
        default_factory=list
    )
    emitted: list[GenericGridScalar] = field(
        default_factory=list
    )


@dataclass(slots=True)
class WallDescriptionGgdParticleIonState(IdsBaseClass):
    """
    Ion state fluxes related to the 3D wall description using the GGD.

    :ivar z_min: Minimum Z of the charge state bundle
    :ivar z_max: Maximum Z of the charge state bundle
    :ivar label: String identifying charge state (e.g. C+, C+2 , C+3,
        C+4, C+5, C+6, ...)
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar incident: Incident fluxes for various wall components (grid
        subsets)
    :ivar emitted: Emitted fluxes for various wall components (grid
        subsets)
    """
    class Meta:
        name = "wall_description_ggd_particle_ion_state"

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
    incident: list[GenericGridScalar] = field(
        default_factory=list
    )
    emitted: list[GenericGridScalar] = field(
        default_factory=list
    )


@dataclass(slots=True)
class WallDescriptionGgdParticleNeutralState(IdsBaseClass):
    """
    Neutral state fluxes related to the 3D wall description using the GGD.

    :ivar label: String identifying state
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar neutral_type: Neutral type, in terms of energy. ID =1: cold;
        2: thermal; 3: fast; 4: NBI
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar incident: Incident fluxes for various wall components (grid
        subsets)
    :ivar emitted: Emitted fluxes for various wall components (grid
        subsets)
    """
    class Meta:
        name = "wall_description_ggd_particle_neutral_state"

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
    incident: list[GenericGridScalar] = field(
        default_factory=list
    )
    emitted: list[GenericGridScalar] = field(
        default_factory=list
    )


@dataclass(slots=True)
class WallDescriptionGgdRecyclingIonState(IdsBaseClass):
    """
    Ion state fluxes related to the 3D wall description using the GGD.

    :ivar z_min: Minimum Z of the charge state bundle
    :ivar z_max: Maximum Z of the charge state bundle
    :ivar label: String identifying charge state (e.g. C+, C+2 , C+3,
        C+4, C+5, C+6, ...)
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar coefficient: Recycling coefficient for various wall components
        (grid subsets)
    """
    class Meta:
        name = "wall_description_ggd_recycling_ion_state"

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
    coefficient: list[GenericGridScalar] = field(
        default_factory=list
    )


@dataclass(slots=True)
class WallDescriptionGgdRecyclingNeutralState(IdsBaseClass):
    """
    Neutral state fluxes related to the 3D wall description using the GGD.

    :ivar label: String identifying state
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar neutral_type: Neutral type, in terms of energy. ID =1: cold;
        2: thermal; 3: fast; 4: NBI
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar coefficient: Recycling coefficient for various wall components
        (grid subsets)
    """
    class Meta:
        name = "wall_description_ggd_recycling_neutral_state"

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
    coefficient: list[GenericGridScalar] = field(
        default_factory=list
    )


@dataclass(slots=True)
class WallGlobalQuantititesNeutralOrigin(IdsBaseClass):
    """
    This structure allows distinguishing the species causing the sputtering.

    :ivar element: List of elements forming the atom or molecule of the
        incident species
    :ivar label: String identifying the incident species (e.g. H, D,
        CD4, ...)
    :ivar energies: Array of energies of this incident species, on which
        the sputtering_physical_coefficient is tabulated
    :ivar sputtering_physical_coefficient: Effective coefficient of
        physical sputtering for various neutral types (first dimension:
        1: cold; 2: thermal; 3: fast), due to this incident species and
        for various energies (second dimension)
    :ivar sputtering_chemical_coefficient: Effective coefficient of
        chemical sputtering for various neutral types (first dimension:
        1: cold; 2: thermal; 3: fast), due to this incident species
    """
    class Meta:
        name = "wall_global_quantitites_neutral_origin"

    element: list[PlasmaCompositionNeutralElementConstant] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    label: str = field(
        default=""
    )
    energies: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    sputtering_physical_coefficient: Optional[ndarray[(int,int, int), float]] = field(
        default=None
    )
    sputtering_chemical_coefficient: Optional[ndarray[(int,int), float]] = field(
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
class Vessel2DUnit(IdsBaseClass):
    """
    2D vessel unit description.

    :ivar name: Name of the unit
    :ivar identifier: Identifier of the unit
    :ivar annular: Annular representation of a layer by two contours,
        inner and outer. Alternatively, the layer can be described by a
        centreline and thickness.
    :ivar element: Set of block elements
    """
    class Meta:
        name = "vessel_2d_unit"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    annular: Optional[Vessel2DAnnular] = field(
        default=None
    )
    element: list[Vessel2DElement] = field(
        default_factory=list,
        metadata={
            "max_occurs": 38,
        }
    )


@dataclass(slots=True)
class Wall2DLimiter(IdsBaseClass):
    """
    2D limiter description.

    :ivar type: Type of the limiter description. index = 0 for the
        official single contour limiter and 1 for the official disjoint
        PFC structure like first wall. Additional representations needed
        on a code-by-code basis follow same incremental pair tagging
        starting on index =2
    :ivar unit: Set of limiter units
    """
    class Meta:
        name = "wall_2d_limiter"

    type: Optional[IdentifierStatic] = field(
        default=None
    )
    unit: list[Wall2DLimiterUnit] = field(
        default_factory=list,
        metadata={
            "max_occurs": 33,
        }
    )


@dataclass(slots=True)
class Wall2DMobile(IdsBaseClass):
    """
    2D mobile parts description.

    :ivar type: Type of the description
    :ivar unit: Set of mobile units
    """
    class Meta:
        name = "wall_2d_mobile"

    type: Optional[IdentifierStatic] = field(
        default=None
    )
    unit: list[Wall2DMobileUnit] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )


@dataclass(slots=True)
class WallDescriptionGgdEnergyIon(IdsBaseClass):
    """
    Ion energy fluxes related to the 3D wall description using the GGD.

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed)
    :ivar label: String identifying ion (e.g. H, D, T, He, C, D2, ...)
    :ivar neutral_index: Index of the corresponding neutral species in
        the ../../neutral array
    :ivar incident: Incident fluxes for various wall components (grid
        subsets)
    :ivar emitted: Emitted fluxes for various wall components (grid
        subsets)
    :ivar multiple_states_flag: Multiple states calculation flag :
        0-Only the 'ion' level is considered and the 'state' array of
        structure is empty; 1-Ion states are considered and are
        described in the 'state' array of structure
    :ivar state: Fluxes related to the different states of the species
    """
    class Meta:
        name = "wall_description_ggd_energy_ion"

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
    incident: list[GenericGridScalar] = field(
        default_factory=list
    )
    emitted: list[GenericGridScalar] = field(
        default_factory=list
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[WallDescriptionGgdEnergyIonState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class WallDescriptionGgdEnergyNeutral(IdsBaseClass):
    """
    Neutral energy fluxes related to the 3D wall description using the GGD.

    :ivar element: List of elements forming the atom or molecule
    :ivar label: String identifying neutral (e.g. H, D, T, He, C, ...)
    :ivar ion_index: Index of the corresponding ion species in the
        ../../ion array
    :ivar incident: Incident fluxes for various wall components (grid
        subsets)
    :ivar emitted: Emitted fluxes for various wall components (grid
        subsets)
    :ivar multiple_states_flag: Multiple states calculation flag :
        0-Only one state is considered; 1-Multiple states are considered
        and are described in the state structure
    :ivar state: Fluxes related to the different states of the species
    """
    class Meta:
        name = "wall_description_ggd_energy_neutral"

    element: list[PlasmaCompositionNeutralElement] = field(
        default_factory=list
    )
    label: str = field(
        default=""
    )
    ion_index: int = field(
        default=999999999
    )
    incident: list[GenericGridScalar] = field(
        default_factory=list
    )
    emitted: list[GenericGridScalar] = field(
        default_factory=list
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[WallDescriptionGgdEnergyNeutralState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class WallDescriptionGgdMaterial(IdsBaseClass):
    """
    Material forming the wall with GGD description.

    :ivar grid_subset: Material is described for various wall components
        (grid subsets), using the identifier convention below
    :ivar time: Time
    """
    class Meta:
        name = "wall_description_ggd_material"

    grid_subset: list[GenericGridIdentifier] = field(
        default_factory=list
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class WallDescriptionGgdParticleIon(IdsBaseClass):
    """
    Ion fluxes related to the 3D wall description using the GGD.

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed)
    :ivar label: String identifying ion (e.g. H, D, T, He, C, D2, ...)
    :ivar neutral_index: Index of the corresponding neutral species in
        the ../../neutral array
    :ivar incident: Incident fluxes for various wall components (grid
        subsets)
    :ivar emitted: Emitted fluxes for various wall components (grid
        subsets)
    :ivar multiple_states_flag: Multiple states calculation flag :
        0-Only the 'ion' level is considered and the 'state' array of
        structure is empty; 1-Ion states are considered and are
        described in the 'state' array of structure
    :ivar state: Fluxes related to the different states of the species
    """
    class Meta:
        name = "wall_description_ggd_particle_ion"

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
    incident: list[GenericGridScalar] = field(
        default_factory=list
    )
    emitted: list[GenericGridScalar] = field(
        default_factory=list
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[WallDescriptionGgdParticleIonState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class WallDescriptionGgdParticleNeutral(IdsBaseClass):
    """
    Neutral fluxes related to the 3D wall description using the GGD.

    :ivar element: List of elements forming the atom or molecule
    :ivar label: String identifying neutral (e.g. H, D, T, He, C, ...)
    :ivar ion_index: Index of the corresponding ion species in the
        ../../ion array
    :ivar incident: Incident fluxes for various wall components (grid
        subsets)
    :ivar emitted: Emitted fluxes for various wall components (grid
        subsets)
    :ivar multiple_states_flag: Multiple states calculation flag :
        0-Only one state is considered; 1-Multiple states are considered
        and are described in the state structure
    :ivar state: Fluxes related to the different states of the species
    """
    class Meta:
        name = "wall_description_ggd_particle_neutral"

    element: list[PlasmaCompositionNeutralElement] = field(
        default_factory=list
    )
    label: str = field(
        default=""
    )
    ion_index: int = field(
        default=999999999
    )
    incident: list[GenericGridScalar] = field(
        default_factory=list
    )
    emitted: list[GenericGridScalar] = field(
        default_factory=list
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[WallDescriptionGgdParticleNeutralState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class WallDescriptionGgdRecyclingIon(IdsBaseClass):
    """
    Ion fluxes related to the 3D wall description using the GGD.

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed)
    :ivar label: String identifying ion (e.g. H, D, T, He, C, D2, ...)
    :ivar neutral_index: Index of the corresponding neutral species in
        the ../../neutral array
    :ivar coefficient: Recycling coefficient for various wall components
        (grid subsets)
    :ivar multiple_states_flag: Multiple states calculation flag :
        0-Only the 'ion' level is considered and the 'state' array of
        structure is empty; 1-Ion states are considered and are
        described in the 'state' array of structure
    :ivar state: Fluxes related to the different states of the species
    """
    class Meta:
        name = "wall_description_ggd_recycling_ion"

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
    coefficient: list[GenericGridScalar] = field(
        default_factory=list
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[WallDescriptionGgdRecyclingIonState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class WallDescriptionGgdRecyclingNeutral(IdsBaseClass):
    """
    Neutral fluxes related to the 3D wall description using the GGD.

    :ivar element: List of elements forming the atom or molecule
    :ivar label: String identifying neutral (e.g. H, D, T, He, C, ...)
    :ivar ion_index: Index of the corresponding ion species in the
        ../../ion array
    :ivar coefficient: Recycling coefficient for various wall components
        (grid subsets)
    :ivar multiple_states_flag: Multiple states calculation flag :
        0-Only one state is considered; 1-Multiple states are considered
        and are described in the state structure
    :ivar state: Fluxes related to the different states of the species
    """
    class Meta:
        name = "wall_description_ggd_recycling_neutral"

    element: list[PlasmaCompositionNeutralElement] = field(
        default_factory=list
    )
    label: str = field(
        default=""
    )
    ion_index: int = field(
        default=999999999
    )
    coefficient: list[GenericGridScalar] = field(
        default_factory=list
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[WallDescriptionGgdRecyclingNeutralState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class WallGlobalQuantititesNeutral(IdsBaseClass):
    """
    Simple 0D description of plasma-wall interaction, related to a given neutral
    species.

    :ivar element: List of elements forming the atom or molecule
    :ivar label: String identifying the species (e.g. H, D, CD4, ...)
    :ivar pumping_speed: Pumped particle flux for that species
    :ivar particle_flux_from_plasma: Particle flux from the plasma for
        that species
    :ivar particle_flux_from_wall: Particle flux from the wall
        corresponding to the conversion into various neutral types
        (first dimension: 1: cold; 2: thermal; 3: fast)
    :ivar gas_puff: Gas puff rate for that species
    :ivar wall_inventory: Wall inventory, i.e. cumulated exchange of
        neutral species between plasma and wall from t = 0, positive if
        a species has gone to the wall, for that species
    :ivar recycling_particles_coefficient: Particle recycling
        coefficient corresponding to the conversion into various neutral
        types (first dimension: 1: cold; 2: thermal; 3: fast)
    :ivar recycling_energy_coefficient: Energy recycling coefficient
        corresponding to the conversion into various neutral types
        (first dimension: 1: cold; 2: thermal; 3: fast)
    :ivar incident_species: Sputtering coefficients due to a set of
        incident species
    """
    class Meta:
        name = "wall_global_quantitites_neutral"

    element: list[PlasmaCompositionNeutralElementConstant] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    label: str = field(
        default=""
    )
    pumping_speed: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    particle_flux_from_plasma: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    particle_flux_from_wall: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    gas_puff: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    wall_inventory: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    recycling_particles_coefficient: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    recycling_energy_coefficient: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    incident_species: list[WallGlobalQuantititesNeutralOrigin] = field(
        default_factory=list,
        metadata={
            "max_occurs": 10,
        }
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
class Vessel2D(IdsBaseClass):
    """
    2D vessel description.

    :ivar type: Type of the description. index = 0 for the official
        single/multiple annular representation and 1 for the official
        block element representation for each unit. Additional
        representations needed on a code-by-code basis follow same
        incremental pair tagging starting on index=2
    :ivar unit: Set of units
    """
    class Meta:
        name = "vessel_2d"

    type: Optional[IdentifierStatic] = field(
        default=None
    )
    unit: list[Vessel2DUnit] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )


@dataclass(slots=True)
class WallDescriptionGgdKinetic(IdsBaseClass):
    """
    Energy fluxes due to kinetic energy of particles related to the 3D wall
    description using the GGD.

    :ivar electrons: Electron fluxes. Fluxes are given at the wall,
        after the sheath.
    :ivar ion: Fluxes related to the various ion species, in the sense
        of isonuclear or isomolecular sequences. Ionisation states (and
        other types of states) must be differentiated at the state level
        below. Fluxes are given at the wall, after the sheath.
    :ivar neutral: Neutral species fluxes
    """
    class Meta:
        name = "wall_description_ggd_kinetic"

    electrons: Optional[WallDescriptionGgdEnergySimple] = field(
        default=None
    )
    ion: list[WallDescriptionGgdEnergyIon] = field(
        default_factory=list
    )
    neutral: list[WallDescriptionGgdParticleNeutral] = field(
        default_factory=list
    )


@dataclass(slots=True)
class WallDescriptionGgdParticle(IdsBaseClass):
    """
    Patricle fluxes related to the 3D wall description using the GGD.

    :ivar electrons: Electron fluxes
    :ivar ion: Fluxes related to the various ion species, in the sense
        of isonuclear or isomolecular sequences. Ionisation states (and
        other types of states) must be differentiated at the state level
        below
    :ivar neutral: Neutral species fluxes
    """
    class Meta:
        name = "wall_description_ggd_particle"

    electrons: Optional[WallDescriptionGgdParticleEl] = field(
        default=None
    )
    ion: list[WallDescriptionGgdParticleIon] = field(
        default_factory=list
    )
    neutral: list[WallDescriptionGgdParticleNeutral] = field(
        default_factory=list
    )


@dataclass(slots=True)
class WallDescriptionGgdRecombination(IdsBaseClass):
    """
    Energy fluxes due to recombination related to the 3D wall description using the
    GGD.

    :ivar ion: Fluxes related to the various ion species, in the sense
        of isonuclear or isomolecular sequences. Ionisation states (and
        other types of states) must be differentiated at the state level
        below
    :ivar neutral: Neutral species fluxes
    """
    class Meta:
        name = "wall_description_ggd_recombination"

    ion: list[WallDescriptionGgdEnergyIon] = field(
        default_factory=list
    )
    neutral: list[WallDescriptionGgdParticleNeutral] = field(
        default_factory=list
    )


@dataclass(slots=True)
class WallDescriptionGgdRecycling(IdsBaseClass):
    """
    Recycling coefficients in the 3D wall description using the GGD.

    :ivar ion: Recycling coefficients for the various ion species, in
        the sense of isonuclear or isomolecular sequences. Ionisation
        states (and other types of states) must be differentiated at the
        state level below
    :ivar neutral: Recycling coefficients for the various neutral
        species
    """
    class Meta:
        name = "wall_description_ggd_recycling"

    ion: list[WallDescriptionGgdRecyclingIon] = field(
        default_factory=list
    )
    neutral: list[WallDescriptionGgdRecyclingNeutral] = field(
        default_factory=list
    )


@dataclass(slots=True)
class WallGlobalQuantitites(IdsBaseClass):
    """
    Simple 0D description of plasma-wall interaction.

    :ivar electrons: Quantities related to electrons
    :ivar neutral: Quantities related to the various neutral species
    :ivar temperature: Wall temperature
    :ivar power_incident: Total power incident on the wall. This power
        is split in the various physical categories listed below
    :ivar power_conducted: Power conducted by the plasma onto the wall
    :ivar power_convected: Power convected by the plasma onto the wall
    :ivar power_radiated: Net radiated power from plasma onto the wall
        (incident-reflected)
    :ivar power_black_body: Black body radiated power emitted from the
        wall (emissivity is included)
    :ivar power_neutrals: Net power from neutrals on the wall  (positive
        means power is deposited on the wall)
    :ivar power_recombination_plasma: Power deposited on the wall due to
        recombination of plasma ions
    :ivar power_recombination_neutrals: Power deposited on the wall due
        to recombination of neutrals into a ground state (e.g.
        molecules)
    :ivar power_currents: Power deposited on the wall due to electric
        currents (positive means power is deposited on the target)
    :ivar power_to_cooling: Power to cooling systems
    :ivar power_inner_target_ion_total: Total ion (summed over ion
        species) power on the inner target
    :ivar power_density_inner_target_max: Maximum power density on the
        inner target
    :ivar power_density_outer_target_max: Maximum power density on the
        outer target
    :ivar current_tor: Toroidal current flowing in the vacuum vessel
    """
    class Meta:
        name = "wall_global_quantitites"

    electrons: Optional[WallGlobalQuantititesElectrons] = field(
        default=None
    )
    neutral: list[WallGlobalQuantititesNeutral] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    temperature: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_incident: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_conducted: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_convected: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_radiated: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_black_body: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_neutrals: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_recombination_plasma: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_recombination_neutrals: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_currents: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_to_cooling: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_inner_target_ion_total: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_density_inner_target_max: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_density_outer_target_max: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    current_tor: Optional[ndarray[(int,), float]] = field(
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
class Wall2D(IdsBaseClass):
    """
    2D wall description.

    :ivar type: Type of the description. index = 0 for equilibrium codes
        (single closed limiter and vessel); 1 for gas-tight walls
        (disjoint PFCs with inner vessel as last limiter_unit; no vessel
        structure); 2 for free boundary codes (disjoint PFCs and vessel)
    :ivar limiter: Description of the immobile limiting surface(s) or
        plasma facing components for defining the Last Closed Flux
        Surface.
    :ivar mobile: In case of mobile plasma facing components, use the
        time-dependent description below this node to provide the full
        outline of the closest PFC surfaces to the plasma. Even in such
        a case, the 'limiter' structure is still used to provide the
        outermost limiting surface (can be used e.g. to define the
        boundary of the mesh of equilibrium reconstruction codes)
    :ivar vessel: Mechanical structure of the vacuum vessel. The vessel
        is described as a set of nested layers with given physics
        properties; Two representations are admitted for each vessel
        unit : annular (two contours) or block elements.
    """
    class Meta:
        name = "wall_2d"

    type: Optional[IdentifierStatic] = field(
        default=None
    )
    limiter: Optional[Wall2DLimiter] = field(
        default=None
    )
    mobile: Optional[Wall2DMobile] = field(
        default=None
    )
    vessel: Optional[Vessel2D] = field(
        default=None
    )


@dataclass(slots=True)
class WallDescriptionGgdEnergy(IdsBaseClass):
    """
    Patricle energy fluxes related to the 3D wall description using the GGD.

    :ivar radiation: Total radiation, not split by process
    :ivar current: Current energy fluxes
    :ivar recombination: Wall recombination
    :ivar kinetic: Energy fluxes due to the kinetic energy of particles
    """
    class Meta:
        name = "wall_description_ggd_energy"

    radiation: Optional[WallDescriptionGgdEnergySimple] = field(
        default=None
    )
    current: Optional[WallDescriptionGgdEnergySimple] = field(
        default=None
    )
    recombination: Optional[WallDescriptionGgdRecombination] = field(
        default=None
    )
    kinetic: Optional[WallDescriptionGgdKinetic] = field(
        default=None
    )


@dataclass(slots=True)
class WallDescriptionGgdGgd(IdsBaseClass):
    """
    Physics quantities related to the 3D wall description using the GGD.

    :ivar power_density: Net power density arriving on the wall surface,
        for various wall components (grid subsets)
    :ivar temperature: Temperature of the wall, for various wall
        components (grid subsets)
    :ivar v_biasing: Electric potential applied to the wall element by
        outside means, for various wall components (grid subsets).
        Different from the plasma electric potential or the sheath
        potential drop.
    :ivar recycling: Fraction of incoming particles that is reflected
        back to the vacuum chamber
    :ivar particle_fluxes: Particle fluxes. The incident and emitted
        components are distinguished. The net flux received by the wall
        is equal to incident - emitted
    :ivar energy_fluxes: Energy fluxes. The incident and emitted
        components are distinguished. The net flux received by the wall
        is equal to incident - emitted
    :ivar time: Time
    """
    class Meta:
        name = "wall_description_ggd_ggd"

    power_density: list[GenericGridScalar] = field(
        default_factory=list
    )
    temperature: list[GenericGridScalar] = field(
        default_factory=list
    )
    v_biasing: list[GenericGridScalar] = field(
        default_factory=list
    )
    recycling: Optional[WallDescriptionGgdRecycling] = field(
        default=None
    )
    particle_fluxes: Optional[WallDescriptionGgdParticle] = field(
        default=None
    )
    energy_fluxes: Optional[WallDescriptionGgdEnergy] = field(
        default=None
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class WallDescriptionGgd(IdsBaseClass):
    """
    3D wall description using the GGD.

    :ivar type: Type of wall: index = 0 for gas tight and 1 for a wall
        with holes/open ports
    :ivar grid_ggd: Wall geometry described using the Generic Grid
        Description, for various time slices (in case of mobile wall
        elements). The timebase of this array of structure must be a
        subset of the timebase on which physical quantities are
        described (../ggd structure). Grid_subsets are used to describe
        various  wall components in a modular way.
    :ivar material: Material of each grid_ggd object, given for each
        slice of the grid_ggd time base (the material is not supposed to
        change, but grid_ggd may evolve with time)
    :ivar ggd: Wall physics quantities represented using the general
        grid description, for various time slices.
    """
    class Meta:
        name = "wall_description_ggd"

    type: Optional[IdentifierStatic] = field(
        default=None
    )
    grid_ggd: list[GenericGridAos3Root] = field(
        default_factory=list
    )
    material: list[WallDescriptionGgdMaterial] = field(
        default_factory=list
    )
    ggd: list[WallDescriptionGgdGgd] = field(
        default_factory=list
    )


@dataclass(slots=True)
class Wall(IdsBaseClass):
    """
    Description of the torus wall and its interaction with the plasma.

    :ivar ids_properties:
    :ivar temperature_reference: Reference temperature for which the
        machine description data is given in this IDS
    :ivar first_wall_surface_area: First wall surface area
    :ivar first_wall_power_flux_peak: Peak power flux on the first wall
    :ivar first_wall_enclosed_volume: Volume available to gas or plasma
        enclosed by the first wall contour
    :ivar global_quantities: Simple 0D description of plasma-wall
        interaction
    :ivar description_2d: Set of 2D wall descriptions, for each type of
        possible physics or engineering configurations necessary (gas
        tight vs wall with ports and holes, coarse vs fine
        representation, single contour limiter, disjoint gapped plasma
        facing components, ...). A simplified description of the
        toroidal extension of the 2D contours is also provided by using
        the phi_extensions nodes.
    :ivar description_ggd: Set of 3D wall descriptions, described using
        the GGD, for each type of possible physics or engineering
        configurations necessary (gas tight vs wall with ports and
        holes, coarse vs fine representation, ...).
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "wall"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    temperature_reference: Optional[TemperatureReference] = field(
        default=None
    )
    first_wall_surface_area: float = field(
        default=9e+40
    )
    first_wall_power_flux_peak: Optional[SignalFlt1D] = field(
        default=None
    )
    first_wall_enclosed_volume: float = field(
        default=9e+40
    )
    global_quantities: Optional[WallGlobalQuantitites] = field(
        default=None
    )
    description_2d: list[Wall2D] = field(
        default_factory=list,
        metadata={
            "max_occurs": 3,
        }
    )
    description_ggd: list[WallDescriptionGgd] = field(
        default_factory=list,
        metadata={
            "max_occurs": 3,
        }
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
