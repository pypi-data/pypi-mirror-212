#__version__='0.3.1'
#__imas_commit__='dd6854b4d07'
#__imas_version__='3.7.1'
from ..dataclasses_idsschema import IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


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
class EmCoupling(IdsBaseClass):
    """
    Description of the axisymmetric mutual electromagnetics; does not include non-
    axisymmetric coil systems; the convention is Quantity_Sensor_Source.

    :ivar ids_properties:
    :ivar mutual_active_active: Mutual inductance coupling from active
        coils to active coils
    :ivar mutual_passive_active: Mutual inductance coupling from active
        coils to passive loops
    :ivar mutual_loops_active: Mutual inductance coupling from active
        coils to poloidal flux loops
    :ivar field_probes_active: Poloidal field coupling from active coils
        to poloidal field probes
    :ivar mutual_passive_passive: Mutual inductance coupling from
        passive loops to passive loops
    :ivar mutual_loops_passive: Mutual  inductance coupling from passive
        loops to poloidal flux loops
    :ivar field_probes_passive: Poloidal field coupling from passive
        loops to poloidal field probes
    :ivar mutual_grid_grid: Mutual inductance from equilibrium grid to
        itself
    :ivar mutual_grid_active: Mutual inductance coupling from active
        coils to equilibrium grid
    :ivar mutual_grid_passive: Mutual inductance coupling from passive
        loops to equilibrium grid
    :ivar field_probes_grid: Poloidal field coupling from equilibrium
        grid to poloidal field probes
    :ivar mutual_loops_grid: Mutual inductance from equilibrium grid to
        poloidal flux loops
    :ivar active_coils: List of the names of the active PF+CS coils
    :ivar passive_loops: List of the names of the passive loops
    :ivar poloidal_probes: List of the names of poloidal field probes
    :ivar flux_loops: List of the names of the axisymmetric flux loops
    :ivar grid_points: List of the names of the plasma region grid
        points
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "em_coupling"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    mutual_active_active: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    mutual_passive_active: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    mutual_loops_active: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    field_probes_active: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    mutual_passive_passive: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    mutual_loops_passive: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    field_probes_passive: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    mutual_grid_grid: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    mutual_grid_active: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    mutual_grid_passive: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    field_probes_grid: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    mutual_loops_grid: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    active_coils: Optional[list[str]] = field(
        default=None
    )
    passive_loops: Optional[list[str]] = field(
        default=None
    )
    poloidal_probes: Optional[list[str]] = field(
        default=None
    )
    flux_loops: Optional[list[str]] = field(
        default=None
    )
    grid_points: Optional[list[str]] = field(
        default=None
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
