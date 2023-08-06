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
class X1X21DStatic(IdsBaseClass):
    """
    Structure for list of X1, X2 positions (1D, static)

    :ivar x1: Positions along x1 axis
    :ivar x2: Positions along x2 axis
    """
    class Meta:
        name = "x1x21d_static"

    x1: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    x2: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class Xyz0DStatic(IdsBaseClass):
    """
    Structure for list of X, Y, Z components (0D, static)

    :ivar x: Component along X axis
    :ivar y: Component along Y axis
    :ivar z: Component along Z axis
    """
    class Meta:
        name = "xyz0d_static"

    x: float = field(
        default=9e+40
    )
    y: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class ChargeExchangeChannelBes(IdsBaseClass):
    """Charge exchange channel - BES parameters

    :ivar a: Mass of atom of the diagnostic neutral beam particle
    :ivar z_ion: Ion charge of the diagnostic neutral beam particle
    :ivar z_n: Nuclear charge of the diagnostic neutral beam particle
    :ivar label: String identifying the diagnostic neutral beam particle
    :ivar transition_wavelength: Unshifted wavelength of the BES
        transition
    :ivar doppler_shift: Doppler shift due to the diagnostic neutral
        beam particle velocity
    :ivar lorentz_shift: Lorentz shift due to the Lorentz electric field
        (vxB) in the frame of the diagnostic neutral beam particles
        moving with a velocity v across the magnetic field B
    :ivar radiances: Calibrated intensities of the 9 splitted lines
        (Stark effect due to Lorentz electric field). Note: radiances
        are integrated over the sightline crossing the neutral beam
    """
    class Meta:
        name = "charge_exchange_channel_bes"

    a: float = field(
        default=9e+40
    )
    z_ion: float = field(
        default=9e+40
    )
    z_n: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    transition_wavelength: float = field(
        default=9e+40
    )
    doppler_shift: Optional[SignalFlt1D] = field(
        default=None
    )
    lorentz_shift: Optional[SignalFlt1D] = field(
        default=None
    )
    radiances: Optional[SignalFlt2D] = field(
        default=None
    )


@dataclass(slots=True)
class ChargeExchangeChannelIon(IdsBaseClass):
    """
    Charge exchange channel for a given ion species.

    :ivar a: Mass of atom of the ion
    :ivar z_ion: Ion charge
    :ivar z_n: Nuclear charge
    :ivar label: String identifying the ion (e.g. H+, D+, T+, He+2, C+6,
        ...)
    :ivar t_i: Ion temperature at the channel measurement point
    :ivar t_i_method: Description of the method used to derive the ion
        temperature
    :ivar velocity_tor: Toroidal velocity of the ion (oriented counter-
        clockwise when seen from above) at the channel measurement point
    :ivar velocity_tor_method: Description of the method used to
        reconstruct the ion toroidal velocity
    :ivar velocity_pol: Poloidal velocity of the ion (oriented clockwise
        when seen from front on the right side of the tokamak axi-
        symmetry axis) at the channel measurement point
    :ivar velocity_pol_method: Description of the method used to
        reconstruct the ion poloidal velocity
    :ivar n_i_over_n_e: Ion concentration (ratio of the ion density over
        the electron density) at the channel measurement point
    :ivar n_i_over_n_e_method: Description of the method used to derive
        the ion concentration
    """
    class Meta:
        name = "charge_exchange_channel_ion"

    a: float = field(
        default=9e+40
    )
    z_ion: float = field(
        default=9e+40
    )
    z_n: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    t_i: Optional[SignalFlt1D] = field(
        default=None
    )
    t_i_method: Optional[Identifier] = field(
        default=None
    )
    velocity_tor: Optional[SignalFlt1D] = field(
        default=None
    )
    velocity_tor_method: Optional[Identifier] = field(
        default=None
    )
    velocity_pol: Optional[SignalFlt1D] = field(
        default=None
    )
    velocity_pol_method: Optional[Identifier] = field(
        default=None
    )
    n_i_over_n_e: Optional[SignalFlt1D] = field(
        default=None
    )
    n_i_over_n_e_method: Optional[Identifier] = field(
        default=None
    )


@dataclass(slots=True)
class ChargeExchangeChannelIonFast(IdsBaseClass):
    """
    Charge exchange channel: fast ion CX quantities.

    :ivar a: Mass of atom of the fast ion
    :ivar z_ion: Fast ion charge
    :ivar z_n: Nuclear charge of the fast ion
    :ivar label: String identifying the fast ion (e.g. H+, D+, T+, He+2,
        C+6, ...)
    :ivar transition_wavelength: Unshifted wavelength of the fast ion
        charge exchange transition
    :ivar radiance: Calibrated radiance of the fast ion charge exchange
        spectrum assuming the shape is pre-defined (e.g. by the Fokker-
        Planck slowing-down function). Note: radiance is integrated over
        the sightline crossing the neutral beam
    :ivar radiance_spectral_method: Description of the method used to
        reconstruct the fast ion charge exchange spectrum (e.g. what
        pre-defined slowing-down and source functions used)
    """
    class Meta:
        name = "charge_exchange_channel_ion_fast"

    a: float = field(
        default=9e+40
    )
    z_ion: float = field(
        default=9e+40
    )
    z_n: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    transition_wavelength: float = field(
        default=9e+40
    )
    radiance: Optional[SignalFlt1D] = field(
        default=None
    )
    radiance_spectral_method: Optional[Identifier] = field(
        default=None
    )


@dataclass(slots=True)
class ChargeExchangeChannelProcessedLine(IdsBaseClass):
    """
    Description of a processed spectral line.

    :ivar label: String identifying the processed spectral line:
        Spectroscopy notation emitting element (e.g. D I, Be IV,  W I, C
        VI), transition - if known - between round brackets (e.g. (3-2)
        ) and indication type of charge exchange - if applicable -
        between square brackets (e.g. [ACX] or [PCX]). Example for
        beryllium active charge exchange line at 468.5 nm: 'Be IV (8-6)
        [ACX]'. Example for impact excitation tungsten line coming from
        the plasma edge: 'W I'
    :ivar wavelength_central: Unshifted central wavelength of the
        processed spectral line
    :ivar radiance: Calibrated, background subtracted radiance
        (integrated over the spectrum for this line)
    :ivar intensity: Non-calibrated intensity (integrated over the
        spectrum for this line), i.e. number of photoelectrons detected
        by unit time, taking into account electronic gain compensation
        and channels relative calibration
    :ivar width: Full width at Half Maximum (FWHM) of the emission line
    :ivar shift: Shift of the emission line wavelength with respected to
        the unshifted cental wavelength (e.g. Doppler shift)
    """
    class Meta:
        name = "charge_exchange_channel_processed_line"

    label: str = field(
        default=""
    )
    wavelength_central: float = field(
        default=9e+40
    )
    radiance: Optional[SignalFlt1D] = field(
        default=None
    )
    intensity: Optional[SignalFlt1D] = field(
        default=None
    )
    width: Optional[SignalFlt1D] = field(
        default=None
    )
    shift: Optional[SignalFlt1D] = field(
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
class DetectorAperture(IdsBaseClass):
    """
    Generic description of a plane detector or collimating aperture.

    :ivar geometry_type: Type of geometry used to describe the surface
        of the detector or aperture (1:'outline', 2:'circular',
        3:'rectangle'). In case of 'outline', the surface is described
        by an outline of point in a local coordinate system defined by a
        centre and three unit vectors X1, X2, X3. Note that there is
        some flexibility here and the data provider should choose the
        most convenient coordinate system for the object, respecting the
        definitions of (X1,X2,X3) indicated below. In case of
        'circular', the surface is a circle defined by its centre,
        radius, and normal vector oriented towards the plasma X3.  In
        case of 'rectangle', the surface is a rectangle defined by its
        centre, widths in the X1 and X2 directions, and normal vector
        oriented towards the plasma X3.
    :ivar centre: If geometry_type=2, coordinates of the centre of the
        circle. If geometry_type=1 or 3, coordinates of the origin of
        the local coordinate system (X1,X2,X3) describing the plane
        detector/aperture. This origin is located within the
        detector/aperture area.
    :ivar radius: Radius of the circle, used only if geometry_type = 2
    :ivar x1_unit_vector: Components of the X1 direction unit vector in
        the (X,Y,Z) coordinate system, where X is the major radius axis
        for phi = 0, Y is the major radius axis for phi = pi/2, and Z is
        the height axis. The X1 vector is more horizontal than X2 (has a
        smaller abs(Z) component) and oriented in the positive phi
        direction (counter-clockwise when viewing from above).
    :ivar x2_unit_vector: Components of the X2 direction unit vector in
        the (X,Y,Z) coordinate system, where X is the major radius axis
        for phi = 0, Y is the major radius axis for phi = pi/2, and Z is
        the height axis. The X2 axis is orthonormal so that uX2 = uX3 x
        uX1.
    :ivar x3_unit_vector: Components of the X3 direction unit vector in
        the (X,Y,Z) coordinate system, where X is the major radius axis
        for phi = 0, Y is the major radius axis for phi = pi/2, and Z is
        the height axis. The X3 axis is normal to the detector/aperture
        plane and oriented towards the plasma.
    :ivar x1_width: Full width of the aperture in the X1 direction, used
        only if geometry_type = 3
    :ivar x2_width: Full width of the aperture in the X2 direction, used
        only if geometry_type = 3
    :ivar outline: Irregular outline of the detector/aperture in the
        (X1, X2) coordinate system. Do NOT repeat the first point.
    :ivar surface: Surface of the detector/aperture, derived from the
        above geometric data
    """
    class Meta:
        name = "detector_aperture"

    geometry_type: int = field(
        default=999999999
    )
    centre: Optional[Rzphi0DStatic] = field(
        default=None
    )
    radius: float = field(
        default=9e+40
    )
    x1_unit_vector: Optional[Xyz0DStatic] = field(
        default=None
    )
    x2_unit_vector: Optional[Xyz0DStatic] = field(
        default=None
    )
    x3_unit_vector: Optional[Xyz0DStatic] = field(
        default=None
    )
    x1_width: float = field(
        default=9e+40
    )
    x2_width: float = field(
        default=9e+40
    )
    outline: Optional[X1X21DStatic] = field(
        default=None
    )
    surface: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class Rzphi1DDynamicAos1(IdsBaseClass):
    """
    Structure for list of R, Z, Phi positions (1D, dynamic within a type 1 array of
    structures (indexed on objects, data/time structure)

    :ivar r: Major radius
    :ivar z: Height
    :ivar phi: Toroidal angle (oriented counter-clockwise when viewing
        from above)
    """
    class Meta:
        name = "rzphi1d_dynamic_aos1"

    r: Optional[SignalFlt1D] = field(
        default=None
    )
    z: Optional[SignalFlt1D] = field(
        default=None
    )
    phi: Optional[SignalFlt1D] = field(
        default=None
    )


@dataclass(slots=True)
class ChargeExchangeChannelSpectrum(IdsBaseClass):
    """
    CX spectrum observed via a grating.

    :ivar grating: Number of grating lines per unit length
    :ivar slit_width: Width of the slit (placed in the object focal
        plane)
    :ivar instrument_function: Array of Gaussian widths and amplitudes
        which as a sum make up the instrument fuction. IF(lambda) = sum(
        instrument_function(1,i)/sqrt(2 * pi *
        instrument_function(2,i)^2  ) * exp( -lambda^2/(2 *
        instrument_function(2,i)^2) )  ),whereby sum(
        instrument_function(1,i) ) = 1
    :ivar exposure_time: Exposure time
    :ivar wavelengths: Measured wavelengths
    :ivar intensity_spectrum: Intensity spectrum (not calibrated), i.e.
        number of photoelectrons detected by unit time by a wavelength
        pixel of the channel, taking into account electronic gain
        compensation and channels relative calibration
    :ivar radiance_spectral: Calibrated spectral radiance (radiance per
        unit wavelength)
    :ivar processed_line: Set of processed spectral lines
    :ivar radiance_calibration: Radiance calibration
    :ivar radiance_calibration_date: Date of the radiance calibration
        (yyyy_mm_dd)
    :ivar wavelength_calibration_date: Date of the wavelength
        calibration (yyyy_mm_dd)
    :ivar radiance_continuum: Calibrated continuum intensity  in the
        middle of the spectrum per unit wavelength
    """
    class Meta:
        name = "charge_exchange_channel_spectrum"

    grating: float = field(
        default=9e+40
    )
    slit_width: float = field(
        default=9e+40
    )
    instrument_function: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    exposure_time: float = field(
        default=9e+40
    )
    wavelengths: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    intensity_spectrum: Optional[SignalFlt2D] = field(
        default=None
    )
    radiance_spectral: Optional[SignalFlt2D] = field(
        default=None
    )
    processed_line: list[ChargeExchangeChannelProcessedLine] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    radiance_calibration: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    radiance_calibration_date: str = field(
        default=""
    )
    wavelength_calibration_date: str = field(
        default=""
    )
    radiance_continuum: Optional[SignalFlt2D] = field(
        default=None
    )


@dataclass(slots=True)
class ChargeExchangeChannel(IdsBaseClass):
    """
    Charge exchange channel.

    :ivar name: Name of the channel
    :ivar identifier: ID of the channel
    :ivar position: Position of the measurements
    :ivar t_i_average: Ion temperature (averaged on charge states and
        ion species) at the channel measurement point
    :ivar t_i_average_method: Description of the method used to
        reconstruct the average ion temperature
    :ivar zeff: Local ionic effective charge at the channel measurement
        point
    :ivar zeff_method: Description of the method used to reconstruct the
        local effective charge
    :ivar zeff_line_average: Ionic effective charge, line average along
        the channel line-of-sight
    :ivar zeff_line_average_method: Description of the method used to
        reconstruct the line average effective charge
    :ivar momentum_tor: Total plasma toroidal momentum, summed over ion
        species and electrons weighted by their density and major
        radius, i.e. sum_over_species(n*R*m*Vphi), at the channel
        measurement point
    :ivar momentum_tor_method: Description of the method used to
        reconstruct the total plasma toroidal momentum
    :ivar ion: Physical quantities related to ion species and charge
        stage (H+, D+, T+, He+2, Li+3, Be+4, C+6, N+7, O+8, Ne+10,
        Si+14, Ar+16 or Ar+18) derived from the measured charge exchange
        emission of each species, at the position of the measurement
    :ivar bes: Derived Beam Emission Spectroscopy (BES) parameters
    :ivar ion_fast: Derived Fast Ion Charge eXchange (FICX) parameters
    :ivar spectrum: Set of spectra obtained by various gratings
    """
    class Meta:
        name = "charge_exchange_channel"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    position: Optional[Rzphi1DDynamicAos1] = field(
        default=None
    )
    t_i_average: Optional[SignalFlt1D] = field(
        default=None
    )
    t_i_average_method: Optional[Identifier] = field(
        default=None
    )
    zeff: Optional[SignalFlt1D] = field(
        default=None
    )
    zeff_method: Optional[Identifier] = field(
        default=None
    )
    zeff_line_average: Optional[SignalFlt1D] = field(
        default=None
    )
    zeff_line_average_method: Optional[Identifier] = field(
        default=None
    )
    momentum_tor: Optional[SignalFlt1D] = field(
        default=None
    )
    momentum_tor_method: Optional[Identifier] = field(
        default=None
    )
    ion: list[ChargeExchangeChannelIon] = field(
        default_factory=list,
        metadata={
            "max_occurs": 13,
        }
    )
    bes: Optional[ChargeExchangeChannelBes] = field(
        default=None
    )
    ion_fast: list[ChargeExchangeChannelIonFast] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    spectrum: list[ChargeExchangeChannelSpectrum] = field(
        default_factory=list,
        metadata={
            "max_occurs": 3,
        }
    )


@dataclass(slots=True)
class ChargeExchange(IdsBaseClass):
    """
    Charge exchange spectroscopy diagnostic.

    :ivar ids_properties:
    :ivar aperture: Description of the collimating aperture of the
        diagnostic, relevant to all lines-of-sight (channels)
    :ivar etendue: Etendue (geometric extent) of the optical system
    :ivar etendue_method: Method used to calculate the etendue. Index =
        0 : exact calculation with a 4D integral; 1 : approximation with
        first order formula (detector surface times solid angle
        subtended by the apertures); 2 : other methods
    :ivar channel: Set of channels (lines-of-sight). The line-of-sight
        is defined by the centre of the collimating aperture and the
        position of the measurements.
    :ivar latency: Upper bound of the delay between physical information
        received by the detector and data available on the real-time
        (RT) network.
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "charge_exchange"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    aperture: Optional[DetectorAperture] = field(
        default=None
    )
    etendue: float = field(
        default=9e+40
    )
    etendue_method: Optional[IdentifierStatic] = field(
        default=None
    )
    channel: list[ChargeExchangeChannel] = field(
        default_factory=list,
        metadata={
            "max_occurs": 100,
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
