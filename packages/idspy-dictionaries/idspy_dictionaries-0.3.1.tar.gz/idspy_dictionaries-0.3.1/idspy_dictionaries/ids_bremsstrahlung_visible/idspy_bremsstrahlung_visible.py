#__version__='0.3.1'
#__imas_commit__='dd6854b4d07'
#__imas_version__='3.7.1'
from ..dataclasses_idsschema import IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


@dataclass(slots=True)
class FilterWavelength(IdsBaseClass):
    """
    Spectrocscopy filter wavelength range and detection efficiency.

    :ivar wavelength_lower: Lower bound of the filter wavelength range
    :ivar wavelength_upper: Upper bound of the filter wavelength range
    :ivar wavelengths: Array of wavelength values
    :ivar detection_efficiency: Probability of detection of a photon
        impacting the detector as a function of its wavelength
    """
    class Meta:
        name = "filter_wavelength"

    wavelength_lower: float = field(
        default=9e+40
    )
    wavelength_upper: float = field(
        default=9e+40
    )
    wavelengths: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    detection_efficiency: Optional[ndarray[(int,), float]] = field(
        default=None
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
class LineOfSight2Points(IdsBaseClass):
    """
    Generic description of a line of sight, defined by two points.

    :ivar first_point: Position of the first point
    :ivar second_point: Position of the second point
    """
    class Meta:
        name = "line_of_sight_2points"

    first_point: Optional[Rzphi0DStatic] = field(
        default=None
    )
    second_point: Optional[Rzphi0DStatic] = field(
        default=None
    )


@dataclass(slots=True)
class BremsstrahlungChannel(IdsBaseClass):
    """
    Bremsstrahlung channel.

    :ivar name: Name of the channel
    :ivar line_of_sight: Description of the line of sight of the
        channel, given by 2 points
    :ivar filter: Filter wavelength range and detection efficiency
    :ivar intensity: Intensity, i.e. number of photoelectrons detected
        by unit time, taking into account electronic gain compensation
        and channels relative calibration
    :ivar radiance_spectral: Calibrated spectral radiance (radiance per
        unit wavelength)
    :ivar zeff_line_average: Average effective charge along the line of
        sight
    """
    class Meta:
        name = "bremsstrahlung_channel"

    name: str = field(
        default=""
    )
    line_of_sight: Optional[LineOfSight2Points] = field(
        default=None
    )
    filter: Optional[FilterWavelength] = field(
        default=None
    )
    intensity: Optional[SignalFlt1D] = field(
        default=None
    )
    radiance_spectral: Optional[SignalFlt1D] = field(
        default=None
    )
    zeff_line_average: Optional[SignalFlt1DValidity] = field(
        default=None
    )


@dataclass(slots=True)
class BremsstrahlungVisible(IdsBaseClass):
    """
    Diagnostic for measuring the bremsstrahlung from thermal particules in the
    visible light range, in view of determining the effective charge of the plasma.

    :ivar ids_properties:
    :ivar channel: Set of channels (detector or pixel of a camera)
    :ivar latency: Upper bound of the delay between physical information
        received by the detector and data available on the real-time
        (RT) network.
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "bremsstrahlung_visible"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    channel: list[BremsstrahlungChannel] = field(
        default_factory=list,
        metadata={
            "max_occurs": 10,
        }
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
