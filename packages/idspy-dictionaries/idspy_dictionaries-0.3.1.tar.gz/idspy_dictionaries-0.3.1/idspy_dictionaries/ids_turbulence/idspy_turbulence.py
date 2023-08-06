#__version__='0.3.1'
#__imas_commit__='dd6854b4d07'
#__imas_version__='3.7.1'
from ..dataclasses_idsschema import IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


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
class TurbulenceProfiles2DElectrons(IdsBaseClass):
    """
    Quantities related to electrons.

    :ivar temperature: Temperature
    :ivar density: Density (thermal+non-thermal)
    :ivar density_thermal: Density of thermal particles
    """
    class Meta:
        name = "turbulence_profiles_2d_electrons"

    temperature: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    density: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    density_thermal: Optional[ndarray[(int,int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class TurbulenceProfiles2DGrid(IdsBaseClass):
    """
    Definition of the 2D grid with time.

    :ivar dim1: First dimension values
    :ivar dim2: Second dimension values
    :ivar time: Time
    """
    class Meta:
        name = "turbulence_profiles_2d_grid"

    dim1: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    dim2: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    time: Optional[float] = field(
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
class TurbulenceProfiles2DIons(IdsBaseClass):
    """
    Quantities related to a given ion species.

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed), volume averaged over plasma radius
    :ivar label: String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)
    :ivar neutral_index: Index of the corresponding neutral species in
        the ../../neutral array
    :ivar temperature: Temperature (average over charge states when
        multiple charge states are considered)
    :ivar density: Density (thermal+non-thermal) (sum over charge states
        when multiple charge states are considered)
    :ivar density_thermal: Density (thermal) (sum over charge states
        when multiple charge states are considered)
    """
    class Meta:
        name = "turbulence_profiles_2d_ions"

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
    temperature: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    density: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    density_thermal: Optional[ndarray[(int,int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class TurbulenceProfiles2DNeutral(IdsBaseClass):
    """
    Quantities related to a given neutral species.

    :ivar element: List of elements forming the atom or molecule
    :ivar label: String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)
    :ivar ion_index: Index of the corresponding ion species in the
        ../../ion array
    :ivar temperature: Temperature (average over charge states when
        multiple charge states are considered)
    :ivar density: Density (thermal+non-thermal) (sum over charge states
        when multiple charge states are considered)
    :ivar density_thermal: Density (thermal) (sum over charge states
        when multiple charge states are considered)
    """
    class Meta:
        name = "turbulence_profiles_2d_neutral"

    element: list[PlasmaCompositionNeutralElement] = field(
        default_factory=list
    )
    label: str = field(
        default=""
    )
    ion_index: int = field(
        default=999999999
    )
    temperature: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    density: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    density_thermal: Optional[ndarray[(int,int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class TurbulenceProfiles2D(IdsBaseClass):
    """
    Fluctuating physical quantities for various time slices.

    :ivar electrons: Quantities related to electrons
    :ivar ion: Quantities related to the various ion species
    :ivar neutral: Quantities related to the various neutral species
    :ivar time: Time
    """
    class Meta:
        name = "turbulence_profiles_2d"

    electrons: Optional[TurbulenceProfiles2DElectrons] = field(
        default=None
    )
    ion: list[TurbulenceProfiles2DIons] = field(
        default_factory=list
    )
    neutral: list[TurbulenceProfiles2DNeutral] = field(
        default_factory=list
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class Turbulence(IdsBaseClass):
    """
    Description of plasma turbulence.

    :ivar ids_properties:
    :ivar grid_2d_type: Selection of one of a set of grid types for
        grid_2d
    :ivar grid_2d: Values for the 2D grid, for various time slices. The
        timebase of this array of structure must be a subset of the
        profiles_2d timebase
    :ivar profiles_2d: Fluctuating physical quantities for various time
        slices
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "turbulence"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    grid_2d_type: Optional[Identifier] = field(
        default=None
    )
    grid_2d: list[TurbulenceProfiles2DGrid] = field(
        default_factory=list
    )
    profiles_2d: list[TurbulenceProfiles2D] = field(
        default_factory=list
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
