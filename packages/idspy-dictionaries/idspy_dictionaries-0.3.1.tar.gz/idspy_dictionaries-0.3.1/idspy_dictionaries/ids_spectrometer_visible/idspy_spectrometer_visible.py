#__version__='0.3.1'
#__imas_commit__='dd6854b4d07'
#__imas_version__='3.7.1'
from ..dataclasses_idsschema import IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


@dataclass(slots=True)
class DetectorImageCircular(IdsBaseClass):
    """
    Description of circular or elliptic observation cones.

    :ivar radius: Radius of the circle
    :ivar ellipticity: Ellipticity
    """
    class Meta:
        name = "detector_image_circular"

    radius: float = field(
        default=9e+40
    )
    ellipticity: float = field(
        default=9e+40
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
class Rzphi0DDynamicAos3(IdsBaseClass):
    """
    Structure for R, Z, Phi positions (0D, dynamic within a type 3 array of
    structures (index on time))

    :ivar r: Major radius
    :ivar z: Height
    :ivar phi: Toroidal angle (oriented counter-clockwise when viewing
        from above)
    """
    class Meta:
        name = "rzphi0d_dynamic_aos3"

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
class SpectroVisChannelPolarization(IdsBaseClass):
    """
    Physics quantities measured from polarized light spectroscopy.

    :ivar e_field_lh_r: Lower Hybrid electric field component in the
        major radius direction
    :ivar e_field_lh_z: Lower Hybrid electric field component in the
        vertical direction
    :ivar e_field_lh_tor: Lower Hybrid electric field component in the
        toroidal direction
    :ivar b_field_modulus: Modulus of the magnetic field (always
        positive, irrespective of the sign convention for the B-field
        direction), obtained from Zeeman effect fit
    :ivar n_e: Electron density, obtained from Stark broadening fit
    :ivar temperature_cold_neutrals: Fit of cold neutrals temperature
    :ivar temperature_hot_neutrals: Fit of hot neutrals temperature
    :ivar velocity_cold_neutrals: Projection of the cold neutral
        velocity along the line of sight, positive when going from first
        point to second point of the line of sight
    :ivar velocity_hot_neutrals: Projection of the hot neutral velocity
        along the line of sight, positive when going from first point to
        second point of the line of sight
    :ivar time: Timebase for dynamic quantities at this level of the
        data structure
    """
    class Meta:
        name = "spectro_vis_channel_polarization"

    e_field_lh_r: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    e_field_lh_z: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    e_field_lh_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    b_field_modulus: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    n_e: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    temperature_cold_neutrals: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    temperature_hot_neutrals: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    velocity_cold_neutrals: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    velocity_hot_neutrals: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )


@dataclass(slots=True)
class SpectroVisChannelWavelengthCalibration(IdsBaseClass):
    """
    Wavelength calibration.

    :ivar offset: Offset
    :ivar gain: Gain
    """
    class Meta:
        name = "spectro_vis_channel_wavelength_calibration"

    offset: float = field(
        default=9e+40
    )
    gain: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class SpectroVisGeometryMatrixInterpolated(IdsBaseClass):
    """
    Interpolated geometry matrix.

    :ivar r: Major radius of interpolation knots
    :ivar z: Height of interpolation knots
    :ivar phi: Toroidal angle (oriented counter-clockwise when viewing
        from above) of interpolation knots
    """
    class Meta:
        name = "spectro_vis_geometry_matrix_interpolated"

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
    class Data(IdsBaseClass):
        """
        :ivar class_of: Class of Data Item
        """
        class_of: str = field(
            init=False,
            default="FLT_1D"
        )


@dataclass(slots=True)
class SpectroVisGeometryMatrixStep2(IdsBaseClass):
    """
    Geometry matrix of the detector.

    :ivar voxel_indices: List of voxel indices (defined in the voxel
        map) used in the sparse data array
    """
    class Meta:
        name = "spectro_vis_geometry_matrix_step2"

    voxel_indices: Optional[ndarray[(int,), int]] = field(
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
class DetectorImage(IdsBaseClass):
    """Description of the observation volume of the detector or detector pixel at
    the focal plane of the optical system.

    This is basically the image of the detector pixel on the focal plane

    :ivar geometry_type: Type of geometry used to describe the image
        (1:'outline', 2:'circular')
    :ivar outline: Coordinates of the points shaping the polygon of the
        image
    :ivar circular: Description of circular or elliptic image
    """
    class Meta:
        name = "detector_image"

    geometry_type: int = field(
        default=999999999
    )
    outline: Optional[Rzphi1DStatic] = field(
        default=None
    )
    circular: Optional[DetectorImageCircular] = field(
        default=None
    )


@dataclass(slots=True)
class GeometryMatrixEmission(IdsBaseClass):
    """
    Emission grid for the geometry matrix of a detector.

    :ivar grid_type: Grid type
    :ivar dim1: First dimension values
    :ivar dim2: Second dimension values
    :ivar dim3: Third dimension values
    """
    class Meta:
        name = "geometry_matrix_emission"

    grid_type: Optional[IdentifierStatic] = field(
        default=None
    )
    dim1: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    dim2: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    dim3: Optional[ndarray[(int,), float]] = field(
        default=None
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
class SpectroVisChannelFilter(IdsBaseClass):
    """
    Filter spectrometer.

    :ivar processed_lines: Central wavelength of the processed lines
    :ivar line_labels: String identifying the processed line. To avoid
        ambiguities, the following syntax is used : element with
        ionization state_wavelength in Angstrom (e.g. WI_4000)
    :ivar line_radiances: Calibrated, background subtracted line
        integrals
    :ivar line_radiances_adjusted: Calibrated, background subtracted
        line integrals, adjusted as if the line was centred at the peak
        responsivity of the system (for this line)
    :ivar line_power_radiances: Calibrated, background subtracted power
        radiances
    :ivar raw_lines: Central wavelength of the raw lines
    :ivar output_voltage: Raw voltage output of the whole acquisition
        chain for each raw line
    :ivar photoelectric_voltage: Gain corrected and background
        subtracted voltage for each raw line
    :ivar photon_count: Detected photon count for each raw line
    :ivar line_intensities: Line gross integral intensities
    :ivar calibrated_lines: Central wavelength of the calibrated lines
    :ivar calibrated_line_integrals: Calibrated line gross areas
        integrals
    :ivar exposure_time: Exposure time
    :ivar radiance_calibration: Radiance calibration
    :ivar radiance_calibration_date: Date of the radiance calibration
        (yyyy_mm_dd)
    """
    class Meta:
        name = "spectro_vis_channel_filter"

    processed_lines: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    line_labels: Optional[list[str]] = field(
        default=None
    )
    line_radiances: Optional[SignalFlt2D] = field(
        default=None
    )
    line_radiances_adjusted: Optional[SignalFlt2D] = field(
        default=None
    )
    line_power_radiances: Optional[SignalFlt2D] = field(
        default=None
    )
    raw_lines: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    output_voltage: Optional[SignalFlt2D] = field(
        default=None
    )
    photoelectric_voltage: Optional[SignalFlt2D] = field(
        default=None
    )
    photon_count: Optional[SignalFlt2D] = field(
        default=None
    )
    line_intensities: Optional[SignalFlt2D] = field(
        default=None
    )
    calibrated_lines: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    calibrated_line_integrals: Optional[SignalFlt2D] = field(
        default=None
    )
    exposure_time: float = field(
        default=9e+40
    )
    radiance_calibration: float = field(
        default=9e+40
    )
    radiance_calibration_date: str = field(
        default=""
    )


@dataclass(slots=True)
class SpectroVisChannelIsotopesIsotope(IdsBaseClass):
    """
    Isotope ratio.

    :ivar element: List of elements forming the atom or molecule
    :ivar label: String identifying the species (H, D, T, He3, He4)
    :ivar density_ratio: Ratio of the density of neutrals of this
        isotope over the summed neutral densities of all other isotopes
        described in the ../isotope array
    :ivar cold_neutrals_fraction: Fraction of cold neutrals for this
        isotope (n_cold_neutrals/(n_cold_neutrals+n_hot_neutrals))
    :ivar hot_neutrals_fraction: Fraction of hot neutrals for this
        isotope (n_hot_neutrals/(n_cold_neutrals+n_hot_neutrals))
    :ivar cold_neutrals_temperature: Temperature of cold neutrals for
        this isotope
    :ivar hot_neutrals_temperature: Temperature of hot neutrals for this
        isotope
    :ivar time: Timebase for dynamic quantities at this level of the
        data structure
    """
    class Meta:
        name = "spectro_vis_channel_isotopes_isotope"

    element: list[PlasmaCompositionNeutralElementConstant] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    label: str = field(
        default=""
    )
    density_ratio: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    cold_neutrals_fraction: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    hot_neutrals_fraction: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    cold_neutrals_temperature: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    hot_neutrals_temperature: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )


@dataclass(slots=True)
class SpectroVisChannelLightCollection(IdsBaseClass):
    """
    Emission weights for various points.

    :ivar values: Values of the light collection efficiencies
    :ivar positions: List of positions for which the light collection
        efficiencies are provided
    """
    class Meta:
        name = "spectro_vis_channel_light_collection"

    values: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    positions: Optional[Rzphi1DStatic] = field(
        default=None
    )


@dataclass(slots=True)
class SpectroVisChannelProcessedLine(IdsBaseClass):
    """
    Description of a processed line.

    :ivar label: String identifying the processed line. To avoid
        ambiguities, the following syntax is used : element with
        ionization state_wavelength in Angstrom (e.g. WI_4000)
    :ivar wavelength_central: Central wavelength of the processed line
    :ivar radiance: Calibrated, background subtracted radiance
        (integrated over the spectrum for this line)
    :ivar intensity: Non-calibrated intensity (integrated over the
        spectrum for this line)
    """
    class Meta:
        name = "spectro_vis_channel_processed_line"

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


@dataclass(slots=True)
class SpectroVisChannelResolution(IdsBaseClass):
    """
    In case of active spectroscopy, spatial resolution of the measurement.

    :ivar centre: Position of the centre of the spatially resolved zone
    :ivar width: Full width of the spatially resolved zone in the R, Z
        and phi directions
    :ivar time: Time
    """
    class Meta:
        name = "spectro_vis_channel_resolution"

    centre: Optional[Rzphi0DDynamicAos3] = field(
        default=None
    )
    width: Optional[Rzphi0DDynamicAos3] = field(
        default=None
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class SpectroVisChannelGrating(IdsBaseClass):
    """
    Grating spectrometer.

    :ivar grating: Number of grating lines per unit length
    :ivar slit_width: Width of the slit (placed in the object focal
        plane)
    :ivar wavelengths: Measured wavelengths
    :ivar radiance_spectral: Calibrated spectral radiance (radiance per
        unit wavelength)
    :ivar intensity_spectrum: Intensity spectrum (not calibrated), i.e.
        number of photoelectrons detected by unit time by a wavelength
        pixel of the channel, taking into account electronic gain
        compensation and channels relative calibration
    :ivar exposure_time: Exposure time
    :ivar processed_line: Set of processed spectral lines
    :ivar radiance_calibration: Radiance calibration
    :ivar radiance_calibration_date: Date of the radiance calibration
        (yyyy_mm_dd)
    :ivar wavelength_calibration: Wavelength calibration data. The
        wavelength is obtained from the pixel index k by: wavelength =
        k * gain + offset. k is starting from 1.
    :ivar wavelength_calibration_date: Date of the wavelength
        calibration (yyyy_mm_dd)
    :ivar instrument_function: Array of Gaussian widths and amplitudes
        which as a sum make up the instrument function. The instrument
        function is the shape that would be measured by a grating
        spectrometer if perfectly monochromatic line emission would be
        used as input. F(lambda) = 1 / sqrt (2*pi) * sum(
        instrument_function(1,i) / instrument_function(2,i)  ) * exp(
        -lambda^2 / (2 * instrument_function(2,i)^2) )  ), whereby sum(
        instrument_function(1,i) ) = 1
    """
    class Meta:
        name = "spectro_vis_channel_grating"

    grating: float = field(
        default=9e+40
    )
    slit_width: float = field(
        default=9e+40
    )
    wavelengths: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    radiance_spectral: Optional[SignalFlt2D] = field(
        default=None
    )
    intensity_spectrum: Optional[SignalFlt2D] = field(
        default=None
    )
    exposure_time: float = field(
        default=9e+40
    )
    processed_line: list[SpectroVisChannelProcessedLine] = field(
        default_factory=list,
        metadata={
            "max_occurs": 20,
        }
    )
    radiance_calibration: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    radiance_calibration_date: str = field(
        default=""
    )
    wavelength_calibration: Optional[SpectroVisChannelWavelengthCalibration] = field(
        default=None
    )
    wavelength_calibration_date: str = field(
        default=""
    )
    instrument_function: Optional[ndarray[(int,int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class SpectroVisChannelIsotopes(IdsBaseClass):
    """
    Isotope ratios and related information.

    :ivar validity_timed: Indicator of the validity of the isotope
        ratios as a function of time (0 means valid, negative values
        mean non-valid)
    :ivar validity: Indicator of the validity of the isotope ratios for
        the whole acquisition period (0 means valid, negative values
        mean non-valid)
    :ivar signal_to_noise: Log10 of the ratio of the powers in two
        bands, one with the spectral lines of interest (signal) the
        other without spectral lines (noise).
    :ivar method: Fitting method used to calculate isotope ratios
    :ivar isotope: Set of isotopes
    :ivar time: Timebase for dynamic quantities at this level of the
        data structure
    """
    class Meta:
        name = "spectro_vis_channel_isotopes"

    validity_timed: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    validity: int = field(
        default=999999999
    )
    signal_to_noise: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    method: Optional[Identifier] = field(
        default=None
    )
    isotope: list[SpectroVisChannelIsotopesIsotope] = field(
        default_factory=list,
        metadata={
            "max_occurs": 3,
        }
    )
    time: Optional[str] = field(
        default=None
    )


@dataclass(slots=True)
class SpectroVisGeometryMatrix(IdsBaseClass):
    """
    Geometry matrix of the detector.

    :ivar with_reflections: Geometry matrix with reflections
    :ivar without_reflections: Geometry matrix without reflections
    :ivar interpolated: Interpolated geometry matrix for reflected light
    :ivar voxel_map: Voxel map for geometry matrix. The cells with same
        number are merged in the computation into a single emission
        source meta-cell (the voxel). Cells with number -1 are excluded.
        Voxel count starts from 0.
    :ivar voxels_n: Number of voxels defined in the voxel_map.
    :ivar emission_grid: Grid defining the light emission cells
    """
    class Meta:
        name = "spectro_vis_geometry_matrix"

    with_reflections: Optional[SpectroVisGeometryMatrixStep2] = field(
        default=None
    )
    without_reflections: Optional[SpectroVisGeometryMatrixStep2] = field(
        default=None
    )
    interpolated: Optional[SpectroVisGeometryMatrixInterpolated] = field(
        default=None
    )
    voxel_map: Optional[ndarray[(int, int, int), int]] = field(
        default=None
    )
    voxels_n: int = field(
        default=999999999
    )
    emission_grid: Optional[GeometryMatrixEmission] = field(
        default=None
    )


@dataclass(slots=True)
class SpectroVisChannel(IdsBaseClass):
    """
    Visible spectroscopy channel.

    :ivar name: Name of the channel
    :ivar object_observed: Main object observed by the channel
    :ivar type: Type of spectrometer the channel is connected to
        (index=1: grating, 2: filter)
    :ivar detector: Detector description
    :ivar aperture: Description of a set of collimating apertures
    :ivar etendue: Etendue (geometric extent) of the channel's optical
        system
    :ivar etendue_method: Method used to calculate the etendue. Index =
        0 : exact calculation with a 4D integral; 1 : approximation with
        first order formula (detector surface times solid angle
        subtended by the apertures); 2 : other methods
    :ivar line_of_sight: Description of the line of sight of the
        channel, given by 2 points
    :ivar detector_image: Image of the detector or pixel on the focal
        plane of the optical system
    :ivar fibre_image: Image of the optical fibre on the focal plane of
        the optical system
    :ivar light_collection_efficiencies: Light collection efficiencies
        (fraction of the local emission detected by the optical system)
        for a list of points defining regions of interest. To be used
        for non-pinhole optics.
    :ivar active_spatial_resolution: In case of active spectroscopy,
        describes the spatial resolution of the measurement, calculated
        as a convolution of the atomic smearing, magnetic and beam
        geometry smearing and detector projection, for a set of time
        slices
    :ivar polarizer: Polarizer description
    :ivar polarizer_active: Indicator of whether a polarizer is present
        and active in the optical system (set to 1 in this case, set to
        0 or leave empty ottherwise)
    :ivar grating_spectrometer: Quantities measured by the channel if
        connected to a grating spectrometer
    :ivar filter_spectrometer: Quantities measured by the channel if
        connected to a filter spectrometer
    :ivar validity_timed: Indicator of the validity of the channel as a
        function of time (0 means valid, negative values mean non-valid)
    :ivar validity: Indicator of the validity of the channel for the
        whole acquisition period (0 means valid, negative values mean
        non-valid)
    :ivar isotope_ratios: Isotope ratios and related information
    :ivar polarization_spectroscopy: Physics quantities measured from
        polarized light spectroscopy
    :ivar geometry_matrix: Description of geometry matrix (ray transfer
        matrix)
    """
    class Meta:
        name = "spectro_vis_channel"

    name: str = field(
        default=""
    )
    object_observed: str = field(
        default=""
    )
    type: Optional[IdentifierStatic] = field(
        default=None
    )
    detector: Optional[DetectorAperture] = field(
        default=None
    )
    aperture: list[DetectorAperture] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    etendue: float = field(
        default=9e+40
    )
    etendue_method: Optional[IdentifierStatic] = field(
        default=None
    )
    line_of_sight: Optional[LineOfSight2Points] = field(
        default=None
    )
    detector_image: Optional[DetectorImage] = field(
        default=None
    )
    fibre_image: Optional[DetectorImage] = field(
        default=None
    )
    light_collection_efficiencies: Optional[SpectroVisChannelLightCollection] = field(
        default=None
    )
    active_spatial_resolution: list[SpectroVisChannelResolution] = field(
        default_factory=list
    )
    polarizer: Optional[DetectorAperture] = field(
        default=None
    )
    polarizer_active: int = field(
        default=999999999
    )
    grating_spectrometer: Optional[SpectroVisChannelGrating] = field(
        default=None
    )
    filter_spectrometer: Optional[SpectroVisChannelFilter] = field(
        default=None
    )
    validity_timed: Optional[SignalInt1D] = field(
        default=None
    )
    validity: int = field(
        default=999999999
    )
    isotope_ratios: Optional[SpectroVisChannelIsotopes] = field(
        default=None
    )
    polarization_spectroscopy: Optional[SpectroVisChannelPolarization] = field(
        default=None
    )
    geometry_matrix: Optional[SpectroVisGeometryMatrix] = field(
        default=None
    )


@dataclass(slots=True)
class SpectrometerVisible(IdsBaseClass):
    """
    Spectrometer in visible light range diagnostic.

    :ivar ids_properties:
    :ivar detector_layout: Layout of the detector grid employed. Ex:
        '4x16', '4x32', '1x18'
    :ivar channel: Set of channels (detector or pixel of a camera)
    :ivar latency: Upper bound of the delay between physical information
        received by the detector and data available on the real-time
        (RT) network.
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "spectrometer_visible"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    detector_layout: str = field(
        default=""
    )
    channel: list[SpectroVisChannel] = field(
        default_factory=list,
        metadata={
            "max_occurs": 240,
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
