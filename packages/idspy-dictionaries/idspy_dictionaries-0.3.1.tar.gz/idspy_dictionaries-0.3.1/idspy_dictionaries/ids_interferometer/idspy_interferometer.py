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
class Rzphi0DStatic(IdsBaseClass):
    """
    Structure for R, Z, Phi positions (0D, static)

    :ivar r: Major radius
    :ivar z: Height
    :ivar phi: Toroidal angle (oriented counter-clockwise when viewing
        from above)
    """
    class Meta:
        name = "rzphi0d_static"

    r: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )
    phi: float = field(
        default=9e+40
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
class SignalFlt1DValidity(IdsBaseClass):
    """
    Signal (FLT_1D) with its time base and validity flags.

    :ivar validity_timed: Indicator of the validity of the data for each
        time slice. 0: valid from automated processing, 1: valid and
        certified by the diagnostic RO; - 1 means problem identified in
        the data processing (request verification by the diagnostic RO),
        -2: invalid data, should not be used (values lower than -2 have
        a code-specific meaning detailing the origin of their
        invalidity)
    :ivar validity: Indicator of the validity of the data for the whole
        acquisition period. 0: valid from automated processing, 1: valid
        and certified by the diagnostic RO; - 1 means problem identified
        in the data processing (request verification by the diagnostic
        RO), -2: invalid data, should not be used (values lower than -2
        have a code-specific meaning detailing the origin of their
        invalidity)
    :ivar time: Time
    """
    class Meta:
        name = "signal_flt_1d_validity"

    validity_timed: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    validity: int = field(
        default=999999999
    )
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
class InterferometerChannelWavelengthInterf(IdsBaseClass):
    """
    Value of the wavelength and density estimators associated to an interferometry
    wavelength.

    :ivar value: Wavelength value
    :ivar phase_corrected: Phase measured for this wavelength, corrected
        from fringe jumps
    :ivar fringe_jump_correction: Signed number of 2pi phase corrections
        applied to remove a fringe jump, for each time slice on which a
        correction has been made
    :ivar fringe_jump_correction_times: List of time slices of the pulse
        on which a fringe jump correction has been made
    :ivar phase_to_n_e_line: Conversion factor to be used to convert
        phase into line density for this wavelength
    """
    class Meta:
        name = "interferometer_channel_wavelength_interf"

    value: float = field(
        default=9e+40
    )
    phase_corrected: Optional[SignalFlt1D] = field(
        default=None
    )
    fringe_jump_correction: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    fringe_jump_correction_times: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    phase_to_n_e_line: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class LineOfSight3Points(IdsBaseClass):
    """
    Generic description of a line of sight, defined by two points (one way) and an
    optional third point to indicate the direction of reflection if the second
    point is e.g. the position of a mirror reflecting the line-of-sight.

    :ivar first_point: Position of the first point
    :ivar second_point: Position of the second point
    :ivar third_point: Position of the third point
    """
    class Meta:
        name = "line_of_sight_3points"

    first_point: Optional[Rzphi0DStatic] = field(
        default=None
    )
    second_point: Optional[Rzphi0DStatic] = field(
        default=None
    )
    third_point: Optional[Rzphi0DStatic] = field(
        default=None
    )


@dataclass(slots=True)
class InterferometerChannel(IdsBaseClass):
    """
    Charge exchange channel.

    :ivar name: Name of the channel
    :ivar identifier: ID of the channel
    :ivar line_of_sight: Description of the line of sight of the
        channel, defined by two points when the beam is not reflected, a
        third point is added to define the reflected beam path
    :ivar wavelength: Set of wavelengths used for interferometry
    :ivar path_length_variation: Optical path length variation due to
        the plasma
    :ivar n_e_line: Line integrated density, possibly obtained by a
        combination of multiple interferometry wavelengths. Corresponds
        to the density integrated along the full line-of-sight (i.e.
        forward AND return for a reflected channel: NO dividing by 2
        correction)
    :ivar n_e_line_average: Line average density, possibly obtained by a
        combination of multiple interferometry wavelengths. Corresponds
        to the density integrated along the full line-of-sight and then
        divided by the length of the line-of-sight
    """
    class Meta:
        name = "interferometer_channel"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    line_of_sight: Optional[LineOfSight3Points] = field(
        default=None
    )
    wavelength: list[InterferometerChannelWavelengthInterf] = field(
        default_factory=list,
        metadata={
            "max_occurs": 2,
        }
    )
    path_length_variation: Optional[SignalFlt1D] = field(
        default=None
    )
    n_e_line: Optional[SignalFlt1DValidity] = field(
        default=None
    )
    n_e_line_average: Optional[SignalFlt1DValidity] = field(
        default=None
    )


@dataclass(slots=True)
class Interferometer(IdsBaseClass):
    """
    Interferometer diagnostic.

    :ivar ids_properties:
    :ivar channel: Set of channels (lines-of-sight)
    :ivar n_e_volume_average: Volume average plasma density estimated
        from the line densities measured by the various channels
    :ivar electrons_n: Total number of electrons in the plasma,
        estimated from the line densities measured by the various
        channels
    :ivar latency: Upper bound of the delay between physical information
        received by the detector and data available on the real-time
        (RT) network.
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "interferometer"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    channel: list[InterferometerChannel] = field(
        default_factory=list,
        metadata={
            "max_occurs": 15,
        }
    )
    n_e_volume_average: Optional[SignalFlt1DValidity] = field(
        default=None
    )
    electrons_n: Optional[SignalFlt1DValidity] = field(
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
