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
class DisruptionGlobalQuantities(IdsBaseClass):
    """
    Global quantities related to the disruption.

    :ivar current_halo_pol: Poloidal halo current
    :ivar current_halo_tor: Toroidal halo current
    :ivar power_ohm: Total ohmic power
    :ivar power_ohm_halo: Ohmic power in the halo region
    :ivar power_parallel_halo: Power of the parallel heat flux in the
        halo region
    :ivar power_radiated_electrons_impurities: Total power radiated by
        electrons on impurities
    :ivar power_radiated_electrons_impurities_halo: Power radiated by
        electrons on impurities in the halo region
    :ivar energy_ohm: Total ohmic cumulated energy (integral of the
        power over the disruption duration)
    :ivar energy_ohm_halo: Ohmic cumulated energy (integral of the power
        over the disruption duration) in the halo region
    :ivar energy_parallel_halo: Cumulated parallel energy (integral of
        the heat flux parallel power over the disruption duration) in
        the halo region
    :ivar energy_radiated_electrons_impurities: Total cumulated energy
        (integral of the power over the disruption duration) radiated by
        electrons on impurities
    :ivar energy_radiated_electrons_impurities_halo: Cumulated energy
        (integral of the power over the disruption duration) radiated by
        electrons on impurities in the halo region
    :ivar psi_halo_boundary: Poloidal flux at halo region boundary
    """
    class Meta:
        name = "disruption_global_quantities"

    current_halo_pol: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    current_halo_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_ohm: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_ohm_halo: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_parallel_halo: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_radiated_electrons_impurities: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_radiated_electrons_impurities_halo: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    energy_ohm: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    energy_ohm_halo: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    energy_parallel_halo: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    energy_radiated_electrons_impurities: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    energy_radiated_electrons_impurities_halo: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    psi_halo_boundary: Optional[ndarray[(int,), float]] = field(
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
class Rz0DDynamicAos(IdsBaseClass):
    """
    Structure for scalar R, Z positions, dynamic within a type 3 array of
    structures (index on time)

    :ivar r: Major radius
    :ivar z: Height
    """
    class Meta:
        name = "rz0d_dynamic_aos"

    r: float = field(
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
class DisruptionHaloCurrentsArea(IdsBaseClass):
    """
    Halo currents geometry and values for a given halo area.

    :ivar start_point: Position of the start point of this area
    :ivar end_point: Position of the end point of this area
    :ivar current_halo_pol: Poloidal halo current crossing through this
        area
    """
    class Meta:
        name = "disruption_halo_currents_area"

    start_point: Optional[Rz0DDynamicAos] = field(
        default=None
    )
    end_point: Optional[Rz0DDynamicAos] = field(
        default=None
    )
    current_halo_pol: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class DisruptionProfiles1D(IdsBaseClass):
    """
    1D radial profiles for disruption data.

    :ivar grid: Radial grid
    :ivar j_runaways: Runaways parallel current density = average(j.B) /
        B0, where B0 = Disruption/Vacuum_Toroidal_Field/ B0
    :ivar power_density_conductive_losses: Power density of conductive
        losses to the wall (positive sign for losses)
    :ivar power_density_radiative_losses: Power density of radiative
        losses (positive sign for losses)
    :ivar time: Time
    """
    class Meta:
        name = "disruption_profiles_1d"

    grid: Optional[CoreRadialGrid] = field(
        default=None
    )
    j_runaways: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_density_conductive_losses: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    power_density_radiative_losses: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class DisruptionHaloCurrents(IdsBaseClass):
    """
    Halo currents geometry and values for a given time slice.

    :ivar area: Set of wall areas through which there are halo currents
    :ivar active_wall_point: R,Z position of the point of the plasma
        boundary in contact with the wall
    :ivar time: Time
    """
    class Meta:
        name = "disruption_halo_currents"

    area: list[DisruptionHaloCurrentsArea] = field(
        default_factory=list
    )
    active_wall_point: Optional[Rz0DDynamicAos] = field(
        default=None
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class Disruption(IdsBaseClass):
    """
    Description of physics quantities of specific interest during a disruption, in
    particular halo currents, etc ...

    :ivar ids_properties:
    :ivar global_quantities: Global quantities
    :ivar halo_currents: Halo currents geometry and values for a set of
        time slices
    :ivar profiles_1d: Radial profiles for a set of time slices
    :ivar vacuum_toroidal_field: Characteristics of the vacuum toroidal
        field (used in rho_tor definition and in the normalization of
        current densities)
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "disruption"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    global_quantities: Optional[DisruptionGlobalQuantities] = field(
        default=None
    )
    halo_currents: list[DisruptionHaloCurrents] = field(
        default_factory=list
    )
    profiles_1d: list[DisruptionProfiles1D] = field(
        default_factory=list
    )
    vacuum_toroidal_field: Optional[BTorVacuum1] = field(
        default=None
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
