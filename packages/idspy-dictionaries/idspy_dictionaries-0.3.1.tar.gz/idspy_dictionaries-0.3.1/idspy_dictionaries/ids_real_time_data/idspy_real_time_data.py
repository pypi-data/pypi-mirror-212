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
class RtdAllocatableSignals(IdsBaseClass):
    """
    List of signals which can be allocated to the SDN.

    :ivar name: Signal name
    :ivar definition: Signal definition
    :ivar allocated_position: Allocation of signal to a position in the
        SDN (1..N); this will be implementation specific
    :ivar value: Signal value
    :ivar quality: Indicator of the quality of the signal. Following
        ITER PCS documentation
        (https://user.iter.org/?uid=354SJ3&amp;action=get_document),
        possible values are: 1 - GOOD (the nominal state); 2 - INVALID
        (data no usable); 3 - DATA INTEGRITY ERROR (e.g. out of bounds
        with respect to expectations, calibration error,...)
    """
    class Meta:
        name = "rtd_allocatable_signals"

    name: str = field(
        default=""
    )
    definition: str = field(
        default=""
    )
    allocated_position: int = field(
        default=999999999
    )
    value: Optional[SignalFlt1D] = field(
        default=None
    )
    quality: Optional[SignalInt1D] = field(
        default=None
    )


@dataclass(slots=True)
class RtdTopic(IdsBaseClass):
    """
    List of the topics.

    :ivar name: Topic name
    :ivar signal: List of signals that are allocated to the PCS
        interface
    """
    class Meta:
        name = "rtd_topic"

    name: str = field(
        default=""
    )
    signal: list[RtdAllocatableSignals] = field(
        default_factory=list,
        metadata={
            "max_occurs": 100,
        }
    )


@dataclass(slots=True)
class RealTimeData(IdsBaseClass):
    """Description of the data bus circulating on the real time data network of the
    machine.

    This is typically used (but not only) as an interface to the Plasma
    Control System (PCS)

    :ivar ids_properties:
    :ivar topic: List of topics. Signals are grouped by topic
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "real_time_data"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    topic: list[RtdTopic] = field(
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
