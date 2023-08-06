#__version__='0.3.1'
#__imas_commit__='dd6854b4d07'
#__imas_version__='3.7.1'
from ..dataclasses_idsschema import IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


@dataclass(slots=True)
class AmnsDataCoordinateSystemCoordinate(IdsBaseClass):
    """Description of a coordinate for atomic data tables.

    Can be either a range of real values or a set of discrete values (if
    interp_type=0)

    :ivar label: Description of coordinate (e.g. "Electron temperature")
    :ivar values: Coordinate values
    :ivar interpolation_type: Interpolation strategy in this coordinate
        direction. Integer flag: 0=discrete (no interpolation);
        1=linear; ...
    :ivar extrapolation_type: Extrapolation strategy when leaving the
        domain. The first value of the vector describes the behaviour at
        lower bound, the second describes the at upper bound. Possible
        values: 0=none, report error; 1=boundary value; 2=linear
        extrapolation
    :ivar value_labels: String description of discrete coordinate values
        (if interpolation_type=0). E.g., for spectroscopic lines, the
        spectroscopic description of the transition.
    :ivar units: Units of coordinate (e.g. eV)
    :ivar transformation: Coordinate transformation applied to
        coordinate values stored in coord. Integer flag: 0=none;
        1=log10; 2=ln
    :ivar spacing: Flag for specific coordinate spacing (for
        optimization purposes). Integer flag: 0=undefined; 1=uniform;
        ...
    """
    class Meta:
        name = "amns_data_coordinate_system_coordinate"

    label: str = field(
        default=""
    )
    values: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    interpolation_type: int = field(
        default=999999999
    )
    extrapolation_type: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    value_labels: Optional[list[str]] = field(
        default=None
    )
    units: str = field(
        default=""
    )
    transformation: int = field(
        default=999999999
    )
    spacing: int = field(
        default=999999999
    )


@dataclass(slots=True)
class AmnsDataDataEntry(IdsBaseClass):
    """
    Definition of a given AMNS data entry.

    :ivar description: Description of this data entry
    :ivar shot: Shot number = Mass*1000+Nuclear_charge
    :ivar run: Which run number is the active run number for this
        version
    """
    class Meta:
        name = "amns_data_data_entry"

    description: str = field(
        default=""
    )
    shot: int = field(
        default=999999999
    )
    run: int = field(
        default=999999999
    )


@dataclass(slots=True)
class AmnsDataProcessChargeState(IdsBaseClass):
    """Process tables for a given charge state.

    Only one table is used for that process, defined by
    process(:)/table_dimension

    :ivar label: String identifying charge state (e.g. C+, C+2 , C+3,
        C+4, C+5, C+6, ...)
    :ivar z_min: Minimum Z of the charge state bundle
    :ivar z_max: Maximum Z of the charge state bundle (equal to z_min if
        no bundle)
    :ivar table_0d: 0D table describing the process data
    :ivar table_1d: 1D table describing the process data
    :ivar table_2d: 2D table describing the process data
    :ivar table_3d: 3D table describing the process data
    :ivar table_4d: 4D table describing the process data
    :ivar table_5d: 5D table describing the process data
    :ivar table_6d: 6D table describing the process data
    """
    class Meta:
        name = "amns_data_process_charge_state"

    label: str = field(
        default=""
    )
    z_min: float = field(
        default=9e+40
    )
    z_max: float = field(
        default=9e+40
    )
    table_0d: float = field(
        default=9e+40
    )
    table_1d: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    table_2d: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    table_3d: Optional[ndarray[(int,int, int), float]] = field(
        default=None
    )
    table_4d: Optional[ndarray[(int,int,int,int), float]] = field(
        default=None
    )
    table_5d: Optional[ndarray[(int,int,int,int,int), float]] = field(
        default=None
    )
    table_6d: Optional[ndarray[(int,int,int,int,int,int), float]] = field(
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
class AmnsDataCoordinateSystem(IdsBaseClass):
    """
    Description of a coordinate system for atomic data tables.

    :ivar coordinate: Set of coordinates for that coordinate system. A
        coordinate an be either a range of real values or a set of
        discrete values (if interpolation_type=0)
    """
    class Meta:
        name = "amns_data_coordinate_system"

    coordinate: list[AmnsDataCoordinateSystemCoordinate] = field(
        default_factory=list,
        metadata={
            "max_occurs": 6,
        }
    )


@dataclass(slots=True)
class AmnsDataProcessReactant(IdsBaseClass):
    """
    Process reactant or product definition.

    :ivar label: String identifying reaction participant (e.g. "D", "e",
        "W", "CD4", "photon", "n")
    :ivar element: List of elements forming the atom (in such case, this
        array should be of size 1) or molecule. Mass of atom and nuclear
        charge should be set to 0 for photons and electrons. The mass of
        atom shouldn't be set for an atomic process that is not isotope
        dependent.
    :ivar role: Identifier for the role of this paricipant in the
        reaction. For surface reactions distinguish between projectile
        and wall.
    :ivar mass: Mass of the participant
    :ivar charge: Charge number of the participant
    :ivar relative_charge: This is a flag indicating that charges are
        absolute (if set to 0), relative (if 1) or irrelevant (-1);
        relative would be used to categorize the ionization reactions
        from i to i+1 for all charge states; in the case of bundles, the
        +1 relative indicates the next bundle
    :ivar multiplicity: Multiplicity in the reaction
    :ivar metastable: An array identifying the metastable; if zero-
        length, then not a metastable; if of length 1, then the value
        indicates the electronic level for the metastable (mostly used
        for atoms/ions); if of length 2, then the 1st would indicate the
        electronic level and the second the vibrational level for the
        metastable (mostly used for molecules and molecular ions); if of
        length 3, then the 1st would indicate the electronic level, the
        second the vibrational level and the third the rotational level
        for the metastable (mostly used for molecules and molecular
        ions)
    :ivar metastable_label: Label identifying in text form the
        metastable
    """
    class Meta:
        name = "amns_data_process_reactant"

    label: str = field(
        default=""
    )
    element: list[PlasmaCompositionNeutralElementConstant] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    role: Optional[Identifier] = field(
        default=None
    )
    mass: float = field(
        default=9e+40
    )
    charge: float = field(
        default=9e+40
    )
    relative_charge: int = field(
        default=999999999
    )
    multiplicity: float = field(
        default=9e+40
    )
    metastable: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    metastable_label: str = field(
        default=""
    )


@dataclass(slots=True)
class AmnsDataRelease(IdsBaseClass):
    """
    Definition of a given release of an AMNS data release.

    :ivar description: Description of this release
    :ivar date: Date of this release
    :ivar data_entry: For this release, list of each data item (i.e.
        shot/run pair containing the actual data) included in this
        release
    """
    class Meta:
        name = "amns_data_release"

    description: str = field(
        default=""
    )
    date: str = field(
        default=""
    )
    data_entry: list[AmnsDataDataEntry] = field(
        default_factory=list,
        metadata={
            "max_occurs": 30,
        }
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
class AmnsDataProcess(IdsBaseClass):
    """
    Definition of a process and its data.

    :ivar source: Filename or subroutine name used to provide this data
    :ivar provider: Name of the person in charge of producing this data
    :ivar citation: Reference to publication(s)
    :ivar label: String identifying the process (e.g. EI, RC, ...)
    :ivar reactants: Set of reactants involved in this process
    :ivar products: Set of products resulting of this process
    :ivar table_dimension: Table dimensionality of the process (1 to 6),
        valid for all charge states. Indicates which of the tables is
        filled (below the charge_state node)
    :ivar coordinate_index: Index in tables_coord, specifying what
        coordinate systems to use for this process (valid for all
        tables)
    :ivar result_label: Description of the process result (rate, cross
        section, sputtering yield, ...)
    :ivar result_units: Units of the process result
    :ivar result_transformation: Transformation of the process result.
        Integer flag: 0=no transformation; 1=10^; 2=exp()
    :ivar charge_state: Process tables for a set of charge states. Only
        one table is used for that process, defined by
        process(:)/table_dimension
    """
    class Meta:
        name = "amns_data_process"

    source: str = field(
        default=""
    )
    provider: str = field(
        default=""
    )
    citation: str = field(
        default=""
    )
    label: str = field(
        default=""
    )
    reactants: list[AmnsDataProcessReactant] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    products: list[AmnsDataProcessReactant] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    table_dimension: int = field(
        default=999999999
    )
    coordinate_index: int = field(
        default=999999999
    )
    result_label: str = field(
        default=""
    )
    result_units: str = field(
        default=""
    )
    result_transformation: int = field(
        default=999999999
    )
    charge_state: list[AmnsDataProcessChargeState] = field(
        default_factory=list,
        metadata={
            "max_occurs": 75,
        }
    )


@dataclass(slots=True)
class AmnsData(IdsBaseClass):
    """Atomic, molecular, nuclear and surface physics data.

    Each occurrence contains the data for a given element (nuclear
    charge), describing various physical processes. For each process,
    data tables are organized by charge states. The coordinate system
    used by the data tables is described under the coordinate_system
    node.

    :ivar ids_properties:
    :ivar z_n: Nuclear charge
    :ivar a: Mass of atom
    :ivar process: Description and data for a set of physical processes.
    :ivar coordinate_system: Array of possible coordinate systems for
        process tables
    :ivar release: List of available releases of the AMNS data; each
        element contains information about the AMNS data that is
        included in the release. This part of the IDS is filled and
        stored only into shot/run=0/1, playing the role of a catalogue.
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "amns_data"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    z_n: float = field(
        default=9e+40
    )
    a: float = field(
        default=9e+40
    )
    process: list[AmnsDataProcess] = field(
        default_factory=list,
        metadata={
            "max_occurs": 20,
        }
    )
    coordinate_system: list[AmnsDataCoordinateSystem] = field(
        default_factory=list,
        metadata={
            "max_occurs": 20,
        }
    )
    release: list[AmnsDataRelease] = field(
        default_factory=list,
        metadata={
            "max_occurs": 100,
        }
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
