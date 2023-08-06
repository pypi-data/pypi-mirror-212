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
class SignalFlt2D(IdsBaseClass):
    """
    Signal (FLT_2D) with its time base.

    :ivar time: Time
    """
    class Meta:
        name = "signal_flt_2d"

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
            default="FLT_2D"
        )


@dataclass(slots=True)
class SignalFlt3D(IdsBaseClass):
    """
    Signal (FLT_3D) with its time base.

    :ivar time: Time
    """
    class Meta:
        name = "signal_flt_3d"

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
            default="FLT_3D"
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
class ControllersNonlinearController(IdsBaseClass):
    """
    Type for a nonlinear controller.

    :ivar name: Name of this controller
    :ivar description: Description of this controller
    :ivar controller_class: One of a known class of controllers
    :ivar input_names: Names of the input signals, following the SDN
        convention
    :ivar output_names: Output signal names following the SDN convention
    :ivar function: Method to be defined
    :ivar inputs: Input signals; the timebase is common  to inputs and
        outputs for any particular controller
    :ivar outputs: Output signals; the timebase is common  to inputs and
        outputs for any particular controller
    """
    class Meta:
        name = "controllers_nonlinear_controller"

    name: str = field(
        default=""
    )
    description: str = field(
        default=""
    )
    controller_class: str = field(
        default=""
    )
    input_names: Optional[list[str]] = field(
        default=None
    )
    output_names: Optional[list[str]] = field(
        default=None
    )
    function: str = field(
        default=""
    )
    inputs: Optional[SignalFlt2D] = field(
        default=None
    )
    outputs: Optional[SignalFlt2D] = field(
        default=None
    )


@dataclass(slots=True)
class ControllersPid(IdsBaseClass):
    """
    Type for a MIMO PID controller.

    :ivar p: Proportional term
    :ivar i: Integral term
    :ivar d: Derivative term
    :ivar tau: Filter time-constant for the D-term
    """
    class Meta:
        name = "controllers_pid"

    p: Optional[SignalFlt3D] = field(
        default=None
    )
    i: Optional[SignalFlt3D] = field(
        default=None
    )
    d: Optional[SignalFlt3D] = field(
        default=None
    )
    tau: Optional[SignalFlt1D] = field(
        default=None
    )


@dataclass(slots=True)
class ControllersStatespace(IdsBaseClass):
    """
    Type for a statespace controller.

    :ivar state_names: Names of the states
    :ivar a: A matrix
    :ivar b: B matrix
    :ivar c: C matrix
    :ivar d: D matrix, normally proper and D=0
    :ivar deltat: Discrete time sampling interval ; if less than 1e-10,
        the controller is considered to be expressed in continuous time
    """
    class Meta:
        name = "controllers_statespace"

    state_names: Optional[list[str]] = field(
        default=None
    )
    a: Optional[SignalFlt3D] = field(
        default=None
    )
    b: Optional[SignalFlt3D] = field(
        default=None
    )
    c: Optional[SignalFlt3D] = field(
        default=None
    )
    d: Optional[SignalFlt3D] = field(
        default=None
    )
    deltat: Optional[SignalFlt1D] = field(
        default=None
    )


@dataclass(slots=True)
class ControllersLinearController(IdsBaseClass):
    """
    Type for a linear controller.

    :ivar name: Name of this controller
    :ivar description: Description of this controller
    :ivar controller_class: One of a known class of controllers
    :ivar input_names: Names of the input signals, following the SDN
        convention
    :ivar output_names: Names of the output signals following the SDN
        convention
    :ivar statespace: Statespace controller in discrete or continuous
        time
    :ivar pid: Filtered PID controller
    :ivar inputs: Input signals; the timebase is common to inputs and
        outputs for any particular controller
    :ivar outputs: Output signals; the timebase is common to inputs and
        outputs for any particular controller
    """
    class Meta:
        name = "controllers_linear_controller"

    name: str = field(
        default=""
    )
    description: str = field(
        default=""
    )
    controller_class: str = field(
        default=""
    )
    input_names: Optional[list[str]] = field(
        default=None
    )
    output_names: Optional[list[str]] = field(
        default=None
    )
    statespace: Optional[ControllersStatespace] = field(
        default=None
    )
    pid: Optional[ControllersPid] = field(
        default=None
    )
    inputs: Optional[SignalFlt2D] = field(
        default=None
    )
    outputs: Optional[SignalFlt2D] = field(
        default=None
    )


@dataclass(slots=True)
class Controllers(IdsBaseClass):
    """
    Feedback and feedforward controllers.

    :ivar ids_properties:
    :ivar linear_controller: A linear controller, this is rather
        conventional
    :ivar nonlinear_controller: A non-linear controller, this is less
        conventional and will have to be developed
    :ivar time:
    :ivar code:
    """
    class Meta:
        name = "controllers"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    linear_controller: list[ControllersLinearController] = field(
        default_factory=list,
        metadata={
            "max_occurs": 20,
        }
    )
    nonlinear_controller: list[ControllersNonlinearController] = field(
        default_factory=list,
        metadata={
            "max_occurs": 20,
        }
    )
    time: Optional[str] = field(
        default=None
    )
    code: Optional[Code] = field(
        default=None
    )
