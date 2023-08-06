#__version__='0.3.1'
#__imas_commit__='dd6854b4d07'
#__imas_version__='3.7.1'
from ..dataclasses_idsschema import IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


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
class PlasmaInitiationGlobalQuantities(IdsBaseClass):
    """
    Global quantities.

    :ivar b_field_stray: Stray magnetic field at plasma position
    :ivar b_field_perpendicular: Perpendicular magnetic field at plasma
        position. b_field_perpendicular =
        sqrt(b_field_stray^2+b_field_eddy^2)
    :ivar connection_length: Average length of open magnetic field
        lines. In the case of fully closed field lines,
        connection_length = 1
    :ivar coulomb_logarithm: Coulomb logarithm
    """
    class Meta:
        name = "plasma_initiation_global_quantities"

    b_field_stray: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    b_field_perpendicular: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    connection_length: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    coulomb_logarithm: Optional[ndarray[(int,), float]] = field(
        default=None
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
class PlasmaInitiationFieldLines(IdsBaseClass):
    """
    Field lines tracing at a given time slice.

    :ivar grid_type: Selection of one of a set of grid types
    :ivar grid: Definition of the 2D grid (the content of dim1 and dim2
        is defined by the selected grid_type)
    :ivar townsend_or_closed_positions: List of all R, Z positions along
        all field lines encoutering Townsend condition or being closed
        field lines
    :ivar townsend_or_closed_grid_positions: List of all R, Z grid
        positions (from ../grid) containing field lines encoutering
        Townsend condition or being closed field lines
    :ivar starting_positions: Starting position to initiate field line
        tracing, for each field line
    :ivar e_field_townsend: Townsend electric field along each field
        line
    :ivar e_field_parallel: Parallel electric field along each field
        line
    :ivar lengths: Length of each field line
    :ivar pressure: Prefill gas pressure used in Townsend E field
        calculation
    :ivar open_fraction: Fraction of open field lines : ratio open
        fields lines / (open+closed field lines)
    :ivar time: Time
    """
    class Meta:
        name = "plasma_initiation_field_lines"

    grid_type: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    grid: Optional[EquilibriumProfiles2DGrid] = field(
        default=None
    )
    townsend_or_closed_positions: Optional[Rz1DDynamicAos] = field(
        default=None
    )
    townsend_or_closed_grid_positions: Optional[Rz1DDynamicAos] = field(
        default=None
    )
    starting_positions: Optional[Rz1DDynamicAos] = field(
        default=None
    )
    e_field_townsend: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    e_field_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    lengths: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure: float = field(
        default=9e+40
    )
    open_fraction: float = field(
        default=9e+40
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class PlasmaInitiation(IdsBaseClass):
    """
    Description the early phases of the plasma, before an equilibrium can be
    calculated.

    :ivar ids_properties:
    :ivar global_quantities: Global quantities
    :ivar b_field_lines: Magnetic field line tracing results, given at
        various time slices
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "plasma_initiation"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    global_quantities: Optional[PlasmaInitiationGlobalQuantities] = field(
        default=None
    )
    b_field_lines: list[PlasmaInitiationFieldLines] = field(
        default_factory=list
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
