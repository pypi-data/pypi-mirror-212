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
class CoreRadialGrid(IdsBaseClass):
    """
    1D radial grid for core* IDSs.

    :ivar rho_tor_norm: Normalised toroidal flux coordinate. The
        normalizing value for rho_tor_norm, is the toroidal flux
        coordinate at the equilibrium boundary (LCFS or 99.x % of the
        LCFS in case of a fixed boundary equilibium calculation, see
        time_slice/boundary/b_flux_pol_norm in the equilibrium IDS)
    :ivar rho_tor: Toroidal flux coordinate. rho_tor =
        sqrt(b_flux_tor/(pi*b0)) ~ sqrt(pi*r^2*b0/(pi*b0)) ~ r [m]. The
        toroidal field used in its definition is indicated under
        vacuum_toroidal_field/b0
    :ivar rho_pol_norm: Normalised poloidal flux coordinate =
        sqrt((psi(rho)-psi(magnetic_axis)) /
        (psi(LCFS)-psi(magnetic_axis)))
    :ivar psi: Poloidal magnetic flux
    :ivar volume: Volume enclosed inside the magnetic surface
    :ivar area: Cross-sectional area of the flux surface
    :ivar surface: Surface area of the toroidal flux surface
    :ivar psi_magnetic_axis: Value of the poloidal magnetic flux at the
        magnetic axis (useful to normalize the psi array values when the
        radial grid doesn't go from the magnetic axis to the plasma
        boundary)
    :ivar psi_boundary: Value of the poloidal magnetic flux at the
        plasma boundary (useful to normalize the psi array values when
        the radial grid doesn't go from the magnetic axis to the plasma
        boundary)
    """
    class Meta:
        name = "core_radial_grid"

    rho_tor_norm: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    rho_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    rho_pol_norm: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    psi: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    volume: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    area: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    surface: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    psi_magnetic_axis: float = field(
        default=9e+40
    )
    psi_boundary: float = field(
        default=9e+40
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
class SawteethDiagnostics(IdsBaseClass):
    """
    Detailed information about the sawtooth characteristics.

    :ivar magnetic_shear_q1: Magnetic shear at surface q = 1, defined as
        rho_tor/q . dq/drho_tor
    :ivar rho_tor_norm_q1: Normalised toroidal flux coordinate at
        surface q = 1
    :ivar rho_tor_norm_inversion: Normalised toroidal flux coordinate at
        inversion radius
    :ivar rho_tor_norm_mixing: Normalised toroidal flux coordinate at
        mixing radius
    :ivar previous_crash_trigger: Previous crash trigger. Flag
        indicating whether a crash condition has been satisfied : 0 = no
        crash. N(&gt;0) = crash triggered due to condition N
    :ivar previous_crash_time: Time at which the previous sawtooth crash
        occured
    :ivar previous_period: Previous sawtooth period
    """
    class Meta:
        name = "sawteeth_diagnostics"

    magnetic_shear_q1: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    rho_tor_norm_q1: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    rho_tor_norm_inversion: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    rho_tor_norm_mixing: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    previous_crash_trigger: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    previous_crash_time: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    previous_period: Optional[ndarray[(int,), float]] = field(
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
class SawteethProfiles1D(IdsBaseClass):
    """
    Core profiles after sawtooth crash.

    :ivar grid: Radial grid
    :ivar t_e: Electron temperature
    :ivar t_i_average: Ion temperature (averaged on charge states and
        ion species)
    :ivar n_e: Electron density (thermal+non-thermal)
    :ivar n_e_fast: Density of fast (non-thermal) electrons
    :ivar n_i_total_over_n_e: Ratio of total ion density (sum over
        species and charge states) over electron density. (thermal+non-
        thermal)
    :ivar momentum_tor: Total plasma toroidal momentum, summed over ion
        species and electrons
    :ivar zeff: Effective charge
    :ivar p_e: Electron pressure
    :ivar p_e_fast_perpendicular: Fast (non-thermal) electron
        perpendicular pressure
    :ivar p_e_fast_parallel: Fast (non-thermal) electron parallel
        pressure
    :ivar p_i_total: Total ion pressure (sum over the ion species)
    :ivar p_i_total_fast_perpendicular: Fast (non-thermal) total ion
        (sum over the ion species) perpendicular pressure
    :ivar p_i_total_fast_parallel: Fast (non-thermal) total ion (sum
        over the ion species) parallel pressure
    :ivar pressure_thermal: Thermal pressure (electrons+ions)
    :ivar pressure_perpendicular: Total perpendicular pressure
        (electrons+ions, thermal+non-thermal)
    :ivar pressure_parallel: Total parallel pressure (electrons+ions,
        thermal+non-thermal)
    :ivar j_total: Total parallel current density = average(jtot.B) /
        B0, where B0 = Core_Profiles/Vacuum_Toroidal_Field/ B0
    :ivar j_tor: Total toroidal current density = average(J_Tor/R) /
        average(1/R)
    :ivar j_ohmic: Ohmic parallel current density = average(J_Ohmic.B) /
        B0, where B0 = Core_Profiles/Vacuum_Toroidal_Field/ B0
    :ivar j_non_inductive: Non-inductive (includes bootstrap) parallel
        current density = average(jni.B) / B0, where B0 =
        Core_Profiles/Vacuum_Toroidal_Field/ B0
    :ivar j_bootstrap: Bootstrap current density =
        average(J_Bootstrap.B) / B0, where B0 =
        Core_Profiles/Vacuum_Toroidal_Field/ B0
    :ivar conductivity_parallel: Parallel conductivity
    :ivar e_field_parallel: Parallel electric field = average(E.B) / B0,
        where Core_Profiles/Vacuum_Toroidal_Field/ B0
    :ivar q: Safety factor
    :ivar magnetic_shear: Magnetic shear, defined as rho_tor/q .
        dq/drho_tor
    :ivar phi: Toroidal flux
    :ivar psi_star_pre_crash: Psi* = psi - phi, just before the sawtooth
        crash
    :ivar psi_star_post_crash: Psi* = psi - phi, after the sawtooth
        crash
    :ivar time: Time
    """
    class Meta:
        name = "sawteeth_profiles_1d"

    grid: Optional[CoreRadialGrid] = field(
        default=None
    )
    t_e: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    t_i_average: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    n_e: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    n_e_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    n_i_total_over_n_e: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    momentum_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    zeff: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    p_e: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    p_e_fast_perpendicular: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    p_e_fast_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    p_i_total: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    p_i_total_fast_perpendicular: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    p_i_total_fast_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_perpendicular: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    j_total: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    j_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    j_ohmic: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    j_non_inductive: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    j_bootstrap: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    conductivity_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    e_field_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    q: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    magnetic_shear: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    phi: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    psi_star_pre_crash: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    psi_star_post_crash: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class Sawteeth(IdsBaseClass):
    """Description of sawtooth events.

    This IDS must be used in homogeneous_time = 1 mode

    :ivar ids_properties:
    :ivar vacuum_toroidal_field: Characteristics of the vacuum toroidal
        field (used in rho_tor definition)
    :ivar crash_trigger: Flag indicating whether a crash condition has
        been satisfied : 0 = no crash. N(&gt;0) = crash triggered due to
        condition N as follows. 1: crash triggered by the ideal kink
        criterion; 2: crash triggered by the ideal kink criterion
        including kinetic effects from fast particles; 31: crash
        triggered by the resistive kink criterion (meeting necessary
        conditions for reconnection); 32: crash triggered by the
        resistive kink criterion (resistive kink mode is unstable). The
        distinction between 31 and 32 only indicates whether (31) or
        (32) was the last criterion to be satisfied
    :ivar profiles_1d: Core profiles after sawtooth crash for various
        time slices
    :ivar diagnostics: Detailed information about the sawtooth
        characteristics
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "sawteeth"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    vacuum_toroidal_field: Optional[BTorVacuum1] = field(
        default=None
    )
    crash_trigger: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    profiles_1d: list[SawteethProfiles1D] = field(
        default_factory=list
    )
    diagnostics: Optional[SawteethDiagnostics] = field(
        default=None
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
