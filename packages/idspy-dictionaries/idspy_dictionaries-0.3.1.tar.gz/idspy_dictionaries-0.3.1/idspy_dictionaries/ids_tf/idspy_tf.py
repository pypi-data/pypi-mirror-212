#__version__='0.3.1'
#__imas_commit__='dd6854b4d07'
#__imas_version__='3.7.1'
from ..dataclasses_idsschema import IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Dict, Optional


@dataclass(slots=True)
class DeltaRzphi1DStatic(IdsBaseClass):
    """
    Structure for R, Z, Phi relative positions (1D, static)

    :ivar delta_r: Major radii (relative to a reference point)
    :ivar delta_z: Heights (relative to a reference point)
    :ivar delta_phi: Toroidal angles (relative to a reference point)
    """
    class Meta:
        name = "delta_rzphi1d_static"

    delta_r: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    delta_z: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    delta_phi: Optional[ndarray[(int,), float]] = field(
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
class Rzphi1DStatic(IdsBaseClass):
    """
    Structure for list of R, Z, Phi positions (1D, static)

    :ivar r: Major radius
    :ivar z: Height
    :ivar phi: Toroidal angle (oriented counter-clockwise when viewing
        from above)
    """
    class Meta:
        name = "rzphi1d_static"

    r: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    z: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    phi: Optional[ndarray[(int,), float]] = field(
        default=None
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
class TfCoilConductorElements(IdsBaseClass):
    """
    Elements descibring the conductor contour.

    :ivar names: Name or description of every element
    :ivar types: Type of every element: 1: line segment, its ends are
        given by the start and end points; index = 2: arc of a circle;
        index = 3: full circle
    :ivar start_points: Position of the start point of every element
    :ivar intermediate_points: Position of an intermediate point along
        the arc of circle, for every element, providing the orientation
        of the element (must define with the corresponding start point
        an aperture angle strictly inferior to PI). Meaningful only if
        type/index = 2, fill with default/empty value otherwise
    :ivar end_points: Position of the end point of every element.
        Meaningful only if type/index = 1 or 2, fill with default/empty
        value otherwise
    :ivar centres: Position of the centre of the arc of a circle of
        every element (meaningful only if type/index = 2 or 3, fill with
        default/empty value otherwise)
    """
    class Meta:
        name = "tf_coil_conductor_elements"

    names: Optional[list[str]] = field(
        default=None
    )
    types: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    start_points: Optional[Rzphi1DStatic] = field(
        default=None
    )
    intermediate_points: Optional[Rzphi1DStatic] = field(
        default=None
    )
    end_points: Optional[Rzphi1DStatic] = field(
        default=None
    )
    centres: Optional[Rzphi1DStatic] = field(
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
class TfCoilConductor(IdsBaseClass):
    """
    Description of a conductor.

    :ivar elements: Set of geometrical elements (line segments and/or
        arcs of a circle) describing the contour of the TF conductor
        centre
    :ivar cross_section: The cross-section perpendicular to the TF
        conductor contour is described by a series of contour points,
        given by their relative position with respect to the start point
        of the first element. This cross-section is assumed constant for
        all elements.
    :ivar resistance: conductor resistance
    :ivar current: Current in the conductor (positive when it flows from
        the first to the last element)
    :ivar voltage: Voltage on the conductor terminals
    """
    class Meta:
        name = "tf_coil_conductor"

    elements: Optional[TfCoilConductorElements] = field(
        default=None
    )
    cross_section: Optional[DeltaRzphi1DStatic] = field(
        default=None
    )
    resistance: float = field(
        default=9e+40
    )
    current: Optional[SignalFlt1D] = field(
        default=None
    )
    voltage: Optional[SignalFlt1D] = field(
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
class TfCoil(IdsBaseClass):
    """
    Description of a given coil.

    :ivar name: Name of the coil
    :ivar identifier: Alphanumeric identifier of coil used for
        convenience
    :ivar conductor: Set of conductors inside the coil. The structure
        can be used with size 1 for a simplified description as a single
        conductor. A conductor is composed of several elements, serially
        connected, i.e. transporting the same current.
    :ivar turns: Number of total turns in a toroidal field coil. May be
        a fraction when describing the coil connections.
    :ivar resistance: Coil resistance
    :ivar current: Current in the coil
    :ivar voltage: Voltage on the coil terminals
    """
    class Meta:
        name = "tf_coil"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    conductor: list[TfCoilConductor] = field(
        default_factory=list,
        metadata={
            "max_occurs": 20,
        }
    )
    turns: float = field(
        default=9e+40
    )
    resistance: float = field(
        default=9e+40
    )
    current: Optional[SignalFlt1D] = field(
        default=None
    )
    voltage: Optional[SignalFlt1D] = field(
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
class TfGgd(IdsBaseClass):
    """
    Toroidal field map represented on ggd.

    :ivar grid: Grid description
    :ivar b_field_r: R component of the vacuum magnetic field, given on
        various grid subsets
    :ivar b_field_z: Z component of the vacuum magnetic field, given on
        various grid subsets
    :ivar b_field_tor: Toroidal component of the vacuum magnetic field,
        given on various grid subsets
    :ivar a_field_r: R component of the vacuum vector potential, given
        on various grid subsets
    :ivar a_field_z: Z component of the vacuum vector potential, given
        on various grid subsets
    :ivar a_field_tor: Toroidal component of the vacuum vector
        potential, given on various grid subsets
    :ivar time: Time
    """
    class Meta:
        name = "tf_ggd"

    grid: Optional[GenericGridDynamic] = field(
        default=None
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
    a_field_r: list[GenericGridScalar] = field(
        default_factory=list
    )
    a_field_z: list[GenericGridScalar] = field(
        default_factory=list
    )
    a_field_tor: list[GenericGridScalar] = field(
        default_factory=list
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class Tf(IdsBaseClass):
    """
    Toroidal field coils.

    :ivar ids_properties:
    :ivar r0: Reference major radius of the device (from the official
        description of the device). This node is the placeholder for
        this official machine description quantity (typically the middle
        of the vessel at the equatorial midplane, although the exact
        definition may depend on the device)
    :ivar is_periodic: Flag indicating whether coils are described one
        by one in the coil() structure (flag=0) or whether the coil
        structure represents only coils having different characteristics
        (flag = 1, n_coils must be filled in that case). In the latter
        case, the coil() sequence is repeated periodically around the
        torus.
    :ivar coils_n: Number of coils around the torus, in case is_periodic
        = 1
    :ivar coil: Set of coils around the tokamak
    :ivar field_map: Map of the vacuum field at various time slices,
        represented using the generic grid description
    :ivar b_field_tor_vacuum_r: Vacuum field times major radius in the
        toroidal field magnet. Positive sign means anti-clockwise when
        viewed from above
    :ivar delta_b_field_tor_vacuum_r: Variation of (vacuum field times
        major radius in the toroidal field magnet) from the start of the
        plasma.
    :ivar latency: Upper bound of the delay between input command
        received from the RT network and actuator starting to react.
        Applies globally to the system described by this IDS unless
        specific latencies (e.g. channel-specific or antenna-specific)
        are provided at a deeper level in the IDS structure.
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "tf"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    r0: float = field(
        default=9e+40
    )
    is_periodic: int = field(
        default=999999999
    )
    coils_n: int = field(
        default=999999999
    )
    coil: list[TfCoil] = field(
        default_factory=list,
        metadata={
            "max_occurs": 32,
        }
    )
    field_map: list[TfGgd] = field(
        default_factory=list
    )
    b_field_tor_vacuum_r: Optional[SignalFlt1D] = field(
        default=None
    )
    delta_b_field_tor_vacuum_r: Optional[SignalFlt1D] = field(
        default=None
    )
    latency: float = field(
        default=9e+40
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
