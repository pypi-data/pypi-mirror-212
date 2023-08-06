#__version__='0.3.1'
#__imas_commit__='dd6854b4d07'
#__imas_version__='3.7.1'
from ..dataclasses_idsschema import IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


@dataclass(slots=True)
class BTorVacuum1(IdsBaseClass):
    """Characteristics of the vacuum toroidal field.

    Time coordinate at the root of the IDS

    :ivar r0: Reference major radius where the vacuum toroidal magnetic
        field is given (usually a fixed position such as the middle of
        the vessel at the equatorial midplane)
    :ivar b0: Vacuum toroidal field at R0 [T]; Positive sign means anti-
        clockwise when viewing from above. The product R0B0 must be
        consistent with the b_tor_vacuum_r field of the tf IDS.
    """
    class Meta:
        name = "b_tor_vacuum_1"

    r0: float = field(
        default=9e+40
    )
    b0: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class Complex1DMhdAlfvenSpectrum(IdsBaseClass):
    """
    Structure for real and imaginary part of the shear Alfven spectrum.

    :ivar real: Real part of the frequency, for a given radial position
        and every root found at this position
    :ivar imaginary: Imaginary part of the frequency, for a given radial
        position and every root found at this position
    """
    class Meta:
        name = "complex_1d_mhd_alfven_spectrum"

    real: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    imaginary: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class Complex2DDynamicAosMhdLinearVector(IdsBaseClass):
    """
    Structure (temporary) for real and imaginary part, while waiting for the
    implementation of complex numbers, dynamic within a type 3 array of structure
    (index on time))

    :ivar real: Real part
    :ivar imaginary: Imaginary part
    :ivar coefficients_real: Interpolation coefficients, to be used for
        a high precision evaluation of the physical quantity (real part)
        with finite elements, provided on the 2D grid
    :ivar coefficients_imaginary: Interpolation coefficients, to be used
        for a high precision evaluation of the physical quantity
        (imaginary part) with finite elements, provided on the 2D grid
    """
    class Meta:
        name = "complex_2d_dynamic_aos_mhd_linear_vector"

    real: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    imaginary: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    coefficients_real: Optional[ndarray[(int,int, int), float]] = field(
        default=None
    )
    coefficients_imaginary: Optional[ndarray[(int,int, int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class Complex2DDynamicAosMhdScalar(IdsBaseClass):
    """
    Structure (temporary) for real and imaginary part, while waiting for the
    implementation of complex numbers, dynamic within a type 3 array of structure
    (index on time))

    :ivar real: Real part
    :ivar imaginary: Imaginary part
    :ivar coefficients_real: Interpolation coefficients, to be used for
        a high precision evaluation of the physical quantity (real part)
        with finite elements, provided on the 2D grid
    :ivar coefficients_imaginary: Interpolation coefficients, to be used
        for a high precision evaluation of the physical quantity
        (imaginary part) with finite elements, provided on the 2D grid
    """
    class Meta:
        name = "complex_2d_dynamic_aos_mhd_scalar"

    real: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    imaginary: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    coefficients_real: Optional[ndarray[(int,int, int), float]] = field(
        default=None
    )
    coefficients_imaginary: Optional[ndarray[(int,int, int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class Complex3DMhdStressTensor(IdsBaseClass):
    """
    Structure for real and imaginary part of MHD stress tensors.

    :ivar real: Real part of the stress tensor, for various radial
        positions
    :ivar imaginary: Imaginary part of the stress tensor, for various
        radial positions
    """
    class Meta:
        name = "complex_3d_mhd_stress_tensor"

    real: Optional[ndarray[(int,int, int), float]] = field(
        default=None
    )
    imaginary: Optional[ndarray[(int,int, int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class EquilibriumProfiles2DGrid(IdsBaseClass):
    """
    Definition of the 2D grid.

    :ivar dim1: First dimension values
    :ivar dim2: Second dimension values
    :ivar volume_element: Elementary plasma volume of plasma enclosed in
        the cell formed by the nodes [dim1(i) dim2(j)], [dim1(i+1)
        dim2(j)], [dim1(i) dim2(j+1)] and [dim1(i+1) dim2(j+1)]
    """
    class Meta:
        name = "equilibrium_profiles_2d_grid"

    dim1: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    dim2: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    volume_element: Optional[ndarray[(int,int), float]] = field(
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
class MhdCoordinateSystem(IdsBaseClass):
    """
    Flux surface coordinate system on a square grid of flux and poloidal angle.

    :ivar grid_type: Selection of one of a set of grid types
    :ivar grid: Definition of the 2D grid
    :ivar r: Values of the major radius on the grid
    :ivar z: Values of the Height on the grid
    :ivar jacobian: Absolute value of the jacobian of the coordinate
        system
    :ivar tensor_covariant: Covariant metric tensor on every point of
        the grid described by grid_type
    :ivar tensor_contravariant: Contravariant metric tensor on every
        point of the grid described by grid_type
    """
    class Meta:
        name = "mhd_coordinate_system"

    grid_type: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    grid: Optional[EquilibriumProfiles2DGrid] = field(
        default=None
    )
    r: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    z: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    jacobian: Optional[ndarray[(int,int), float]] = field(
        default=None
    )
    tensor_covariant: Optional[ndarray[(int,int,int,int), float]] = field(
        default=None
    )
    tensor_contravariant: Optional[ndarray[(int,int,int,int), float]] = field(
        default=None
    )


@dataclass(slots=True)
class MhdLinearVector(IdsBaseClass):
    """
    Vector structure for the MHD IDS.

    :ivar coordinate1: First coordinate (radial)
    :ivar coordinate2: Second coordinate (poloidal)
    :ivar coordinate3: Third coordinate (toroidal)
    """
    class Meta:
        name = "mhd_linear_vector"

    coordinate1: Optional[Complex2DDynamicAosMhdLinearVector] = field(
        default=None
    )
    coordinate2: Optional[Complex2DDynamicAosMhdLinearVector] = field(
        default=None
    )
    coordinate3: Optional[Complex2DDynamicAosMhdLinearVector] = field(
        default=None
    )


@dataclass(slots=True)
class MhdLinearTimeSliceToroidalModePlasma(IdsBaseClass):
    """
    MHD modes in the confined plasma.

    :ivar grid_type: Selection of one of a set of grid types
    :ivar grid: Definition of the 2D grid (the content of dim1 and dim2
        is defined by the selected grid_type)
    :ivar coordinate_system: Flux surface coordinate system of the
        equilibrium used for the MHD calculation on a square grid of
        flux and poloidal angle
    :ivar displacement_perpendicular: Perpendicular displacement of the
        modes
    :ivar displacement_parallel: Parallel displacement of the modes
    :ivar tau_alfven: Alven time=R/vA=R0 sqrt(mi ni(rho))/B0
    :ivar tau_resistive: Resistive time = mu_0 rho*rho/1.22/eta_neo
    :ivar a_field_perturbed: Pertubed vector potential for given
        toroidal mode number
    :ivar b_field_perturbed: Pertubed magnetic field for given toroidal
        mode number
    :ivar velocity_perturbed: Pertubed velocity for given toroidal mode
        number
    :ivar pressure_perturbed: Perturbed pressure for given toroidal mode
        number
    :ivar mass_density_perturbed: Perturbed mass density for given
        toroidal mode number
    :ivar temperature_perturbed: Perturbed temperature for given
        toroidal mode number
    :ivar phi_potential_perturbed: Perturbed electrostatic potential for
        given toroidal mode number
    :ivar psi_potential_perturbed: Perturbed electromagnetic super-
        potential for given toroidal mode number, see ref [Antonsen/Lane
        Phys Fluids 23(6) 1980, formula 34], so that
        A_field_parallel=1/(i*2pi*frequency) (grad
        psi_potential)_parallel
    :ivar alfven_frequency_spectrum: Local shear Alfven spectrum as a
        function of radius (only in case grid/dim1 is a radial
        coordinate)
    :ivar stress_maxwell: Maxwell stress tensor
    :ivar stress_reynolds: Reynolds stress tensor
    :ivar ntv: Neoclassical toroidal viscosity tensor
    """
    class Meta:
        name = "mhd_linear_time_slice_toroidal_mode_plasma"

    grid_type: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    grid: Optional[EquilibriumProfiles2DGrid] = field(
        default=None
    )
    coordinate_system: Optional[MhdCoordinateSystem] = field(
        default=None
    )
    displacement_perpendicular: Optional[Complex2DDynamicAosMhdScalar] = field(
        default=None
    )
    displacement_parallel: Optional[Complex2DDynamicAosMhdScalar] = field(
        default=None
    )
    tau_alfven: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    tau_resistive: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    a_field_perturbed: Optional[MhdLinearVector] = field(
        default=None
    )
    b_field_perturbed: Optional[MhdLinearVector] = field(
        default=None
    )
    velocity_perturbed: Optional[MhdLinearVector] = field(
        default=None
    )
    pressure_perturbed: Optional[Complex2DDynamicAosMhdScalar] = field(
        default=None
    )
    mass_density_perturbed: Optional[Complex2DDynamicAosMhdScalar] = field(
        default=None
    )
    temperature_perturbed: Optional[Complex2DDynamicAosMhdScalar] = field(
        default=None
    )
    phi_potential_perturbed: Optional[Complex2DDynamicAosMhdScalar] = field(
        default=None
    )
    psi_potential_perturbed: Optional[Complex2DDynamicAosMhdScalar] = field(
        default=None
    )
    alfven_frequency_spectrum: list[Complex1DMhdAlfvenSpectrum] = field(
        default_factory=list
    )
    stress_maxwell: Optional[Complex3DMhdStressTensor] = field(
        default=None
    )
    stress_reynolds: Optional[Complex3DMhdStressTensor] = field(
        default=None
    )
    ntv: Optional[Complex3DMhdStressTensor] = field(
        default=None
    )


@dataclass(slots=True)
class MhdLinearTimeSliceToroidalModeVacuum(IdsBaseClass):
    """
    MHD modes in the vacuum.

    :ivar grid_type: Selection of one of a set of grid types
    :ivar grid: Definition of the 2D grid (the content of dim1 and dim2
        is defined by the selected grid_type)
    :ivar coordinate_system: Flux surface coordinate system of the
        equilibrium used for the MHD calculation on a square grid of
        flux and poloidal angle
    :ivar a_field_perturbed: Pertubed vector potential for given
        toroidal mode number
    :ivar b_field_perturbed: Pertubed magnetic field for given toroidal
        mode number
    """
    class Meta:
        name = "mhd_linear_time_slice_toroidal_mode_vacuum"

    grid_type: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    grid: Optional[EquilibriumProfiles2DGrid] = field(
        default=None
    )
    coordinate_system: Optional[MhdCoordinateSystem] = field(
        default=None
    )
    a_field_perturbed: Optional[MhdLinearVector] = field(
        default=None
    )
    b_field_perturbed: Optional[MhdLinearVector] = field(
        default=None
    )


@dataclass(slots=True)
class MhdLinearTimeSliceToroidalModes(IdsBaseClass):
    """
    Vector of toroidal modes.

    :ivar perturbation_type: Type of the perturbation
    :ivar n_tor: Toroidal mode number of the MHD mode
    :ivar m_pol_dominant: Dominant poloidal mode number defining the
        mode rational surface; for TAEs the lower of the two main m's
        has to be specified
    :ivar ballooning_type: Ballooning type of the mode : ballooning 0;
        anti-ballooning:1; flute-like:2
    :ivar radial_mode_number: Radial mode number
    :ivar growthrate: Linear growthrate of the mode
    :ivar frequency: Frequency of the mode
    :ivar phase: Additional phase offset of mode
    :ivar energy_perturbed: Perturbed energy associated to the mode
    :ivar amplitude_multiplier: Multiplier that is needed to convert the
        linear mode structures to the amplitude of a non-linearly
        saturated mode in physical units. If empty, it means that the
        structures contains no information about non-linearly saturated
        mode
    :ivar plasma: MHD modes in the confined plasma
    :ivar vacuum: MHD modes in the vacuum
    """
    class Meta:
        name = "mhd_linear_time_slice_toroidal_modes"

    perturbation_type: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    n_tor: int = field(
        default=999999999
    )
    m_pol_dominant: float = field(
        default=9e+40
    )
    ballooning_type: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    radial_mode_number: float = field(
        default=9e+40
    )
    growthrate: float = field(
        default=9e+40
    )
    frequency: float = field(
        default=9e+40
    )
    phase: float = field(
        default=9e+40
    )
    energy_perturbed: float = field(
        default=9e+40
    )
    amplitude_multiplier: float = field(
        default=9e+40
    )
    plasma: Optional[MhdLinearTimeSliceToroidalModePlasma] = field(
        default=None
    )
    vacuum: Optional[MhdLinearTimeSliceToroidalModeVacuum] = field(
        default=None
    )


@dataclass(slots=True)
class MhdLinearTimeSlice(IdsBaseClass):
    """
    Time slice description of linear MHD stability.

    :ivar toroidal_mode: Vector of toroidal modes. Each mode is
        described as exp(i(n_tor.phi - m_pol.theta - 2.pi.frequency.t -
        phase))
    :ivar time: Time
    """
    class Meta:
        name = "mhd_linear_time_slice"

    toroidal_mode: list[MhdLinearTimeSliceToroidalModes] = field(
        default_factory=list
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class MhdLinear(IdsBaseClass):
    """
    Magnetohydronamic linear stability.

    :ivar ids_properties:
    :ivar model_type: Type of model used to populate this IDS
    :ivar equations: Type of MHD equations used to populate this IDS
    :ivar fluids_n: Number of fluids considered in the model
    :ivar ideal_flag: 1 if ideal MHD is used to populate this IDS, 0 for
        non-ideal MHD
    :ivar vacuum_toroidal_field: Characteristics of the vacuum toroidal
        field (used in rho_tor definition and in the normalization of
        current densities)
    :ivar time_slice: Core plasma radial profiles for various time
        slices
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "mhd_linear"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    model_type: Optional[Identifier] = field(
        default=None
    )
    equations: Optional[Identifier] = field(
        default=None
    )
    fluids_n: int = field(
        default=999999999
    )
    ideal_flag: int = field(
        default=999999999
    )
    vacuum_toroidal_field: Optional[BTorVacuum1] = field(
        default=None
    )
    time_slice: list[MhdLinearTimeSlice] = field(
        default_factory=list
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
