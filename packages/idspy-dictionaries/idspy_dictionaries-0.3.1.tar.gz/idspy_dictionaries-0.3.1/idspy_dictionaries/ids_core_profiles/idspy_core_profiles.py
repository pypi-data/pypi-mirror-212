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
class CoreProfilesGlobalQuantitiesIon(IdsBaseClass):
    """
    Various ion global quantities.

    :ivar t_i_volume_average: Volume averaged temperature of this ion
        species (averaged over the plasma volume up to the LCFS)
    :ivar n_i_volume_average: Volume averaged density of this ion
        species (averaged over the plasma volume up to the LCFS)
    """
    class Meta:
        name = "core_profiles_global_quantities_ion"

    t_i_volume_average: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    n_i_volume_average: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class CoreProfilesVectorComponents1(IdsBaseClass):
    """
    Vector components in predefined directions for 1D profiles, assuming
    core_radial_grid one level above.

    :ivar radial: Radial component
    :ivar diamagnetic: Diamagnetic component
    :ivar parallel: Parallel component
    :ivar poloidal: Poloidal component
    :ivar toroidal: Toroidal component
    """
    class Meta:
        name = "core_profiles_vector_components_1"

    radial: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    diamagnetic: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    poloidal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    toroidal: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class CoreProfilesVectorComponents2(IdsBaseClass):
    """
    Vector components in predefined directions for 1D profiles, assuming
    core_radial_grid two levels above.

    :ivar radial: Radial component
    :ivar diamagnetic: Diamagnetic component
    :ivar parallel: Parallel component
    :ivar poloidal: Poloidal component
    :ivar toroidal: Toroidal component
    """
    class Meta:
        name = "core_profiles_vector_components_2"

    radial: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    diamagnetic: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    poloidal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    toroidal: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class CoreProfilesVectorComponents3(IdsBaseClass):
    """
    Vector components in predefined directions for 1D profiles, assuming
    core_radial_grid 3 levels above.

    :ivar radial: Radial component
    :ivar diamagnetic: Diamagnetic component
    :ivar parallel: Parallel component
    :ivar poloidal: Poloidal component
    :ivar toroidal: Toroidal component
    """
    class Meta:
        name = "core_profiles_vector_components_3"

    radial: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    diamagnetic: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    poloidal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    toroidal: Optional[ndarray[(int,), float]] = field(
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
class PlasmaCompositionNeutralElement(IdsBaseClass):
    """
    Element entering in the composition of the neutral atom or molecule (within a
    type 3 AoS)

    :ivar a: Mass of atom
    :ivar z_n: Nuclear charge
    :ivar atoms_n: Number of atoms of this element in the molecule
    :ivar multiplicity: Multiplicity of the atom
    """
    class Meta:
        name = "plasma_composition_neutral_element"

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
class CoreProfiles1DFit(IdsBaseClass):
    """
    Core profile fit information.

    :ivar measured: Measured values
    :ivar source: Path to the source data for each measurement in the
        IMAS data dictionary, e.g. ece/channel(i)/t_e for the electron
        temperature on the i-th channel in the ECE IDS
    :ivar time_measurement: Exact time slices used from the time array
        of the measurement source data. If the time slice does not exist
        in the time array of the source data, it means linear
        interpolation has been used
    :ivar time_measurement_slice_method: Method used to slice the data :
        index = 0 means using exact time slice of the measurement, 1
        means linear interpolation, ...
    :ivar time_measurement_width: In case the measurements are averaged
        over a time interval, this node is the full width of this time
        interval (empty otherwise). In case the slicing/averaging method
        doesn't use a hard time interval cutoff, this width is the
        characteristic time span of the slicing/averaging method. By
        convention, the time interval starts at time_measurement-
        time_width and ends at time_measurement.
    :ivar local: Integer flag : 1 means local measurement, 0 means line-
        integrated measurement
    :ivar rho_tor_norm: Normalised toroidal flux coordinate of each
        measurement (local value for a local measurement, minimum value
        reached by the line of sight for a line measurement)
    :ivar weight: Weight given to each measured value
    :ivar reconstructed: Value reconstructed from the fit
    :ivar chi_squared: Squared error normalized by the weighted standard
        deviation considered in the minimization process : chi_squared =
        weight^2 *(reconstructed - measured)^2 / sigma^2, where sigma is
        the standard deviation of the measurement error
    :ivar parameters: List of the fit specific parameters in XML format
    """
    class Meta:
        name = "core_profiles_1D_fit"

    measured: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    source: Optional[list[str]] = field(
        default=None
    )
    time_measurement: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    time_measurement_slice_method: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    time_measurement_width: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    local: Optional[ndarray[(int,), int]] = field(
        default=None
    )
    rho_tor_norm: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    weight: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    reconstructed: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    chi_squared: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    parameters: str = field(
        default=""
    )


@dataclass(slots=True)
class CoreProfilesGlobalQuantities(IdsBaseClass):
    """
    Various global quantities calculated from the fields solved in the transport
    equations and from the Derived Profiles.

    :ivar ip: Total plasma current (toroidal component). Positive sign
        means anti-clockwise when viewed from above.
    :ivar current_non_inductive: Total non-inductive current (toroidal
        component). Positive sign means anti-clockwise when viewed from
        above.
    :ivar current_bootstrap: Bootstrap current (toroidal component).
        Positive sign means anti-clockwise when viewed from above.
    :ivar v_loop: LCFS loop voltage (positive value drives positive
        ohmic current that flows anti-clockwise when viewed from above)
    :ivar li: Internal inductance. The li_3 definition is used, i.e.
        li_3 = 2/R0/mu0^2/Ip^2 * int(Bp^2 dV).
    :ivar li_3: Internal inductance. The li_3 definition is used, i.e.
        li_3 = 2/R0/mu0^2/Ip^2 * int(Bp^2 dV).
    :ivar beta_tor: Toroidal beta, defined as the volume-averaged total
        perpendicular pressure divided by (B0^2/(2*mu0)), i.e.
        beta_toroidal = 2 mu0 int(p dV) / V / B0^2
    :ivar beta_tor_norm: Normalised toroidal beta, defined as 100 *
        beta_tor * a[m] * B0 [T] / ip [MA]
    :ivar beta_pol: Poloidal beta. Defined as betap = 4 int(p dV) / [R_0
        * mu_0 * Ip^2]
    :ivar energy_diamagnetic: Plasma energy content = 3/2 * integral
        over the plasma volume of the total perpendicular pressure
    :ivar z_eff_resistive: Volume average plasma effective charge,
        estimated from the flux consumption in the ohmic phase
    :ivar t_e_peaking: Electron temperature peaking factor, defined as
        the Te value at the magnetic axis divided by the volume averaged
        Te (average over the plasma volume up to the LCFS)
    :ivar t_i_average_peaking: Ion temperature (averaged over ion
        species and states) peaking factor, defined as the Ti value at
        the magnetic axis divided by the volume averaged Ti (average
        over the plasma volume up to the LCFS)
    :ivar resistive_psi_losses: Resistive part of the poloidal flux
        losses, defined as the volume-averaged scalar product of the
        electric field and the ohmic current density, normalized by the
        plasma current and integrated in time from the beginning of the
        plasma discharge: int ( (int(E_field_tor.j_ohm_tor) dV) / Ip )
        dt)
    :ivar ejima: Ejima coefficient : resistive psi losses divided by
        (mu0*R*Ip). See S. Ejima et al, Nuclear Fusion, Vol.22, No.10
        (1982), 1313
    :ivar t_e_volume_average: Volume averaged electron temperature
        (average over the plasma volume up to the LCFS)
    :ivar n_e_volume_average: Volume averaged electron density (average
        over the plasma volume up to the LCFS)
    :ivar ion: Quantities related to the different ion species, in the
        sense of isonuclear or isomolecular sequences. The set of ion
        species of this array must be the same as the one defined in
        profiles_1d/ion, at the time slice indicated in ion_time_slice
    :ivar ion_time_slice: Time slice of the profiles_1d array used to
        define the ion composition of the global_quantities/ion array.
    """
    class Meta:
        name = "core_profiles_global_quantities"

    ip: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    current_non_inductive: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    current_bootstrap: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    v_loop: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    li: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    li_3: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    beta_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    beta_tor_norm: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    beta_pol: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    energy_diamagnetic: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    z_eff_resistive: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    t_e_peaking: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    t_i_average_peaking: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    resistive_psi_losses: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    ejima: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    t_e_volume_average: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    n_e_volume_average: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    ion: list[CoreProfilesGlobalQuantitiesIon] = field(
        default_factory=list,
        metadata={
            "max_occurs": 20,
        }
    )
    ion_time_slice: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class CoreProfilesNeutralState(IdsBaseClass):
    """
    Quantities related to the a given state of the neutral species.

    :ivar label: String identifying state
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar neutral_type: Neutral type (if the considered state is a
        neutral), in terms of energy. ID =1: cold; 2: thermal; 3: fast;
        4: NBI
    :ivar velocity: Velocity
    :ivar temperature: Temperature
    :ivar density: Density (thermal+non-thermal)
    :ivar density_thermal: Density of thermal particles
    :ivar density_fast: Density of fast (non-thermal) particles
    :ivar pressure: Pressure (thermal+non-thermal)
    :ivar pressure_thermal: Pressure (thermal) associated with random
        motion ~average((v-average(v))^2)
    :ivar pressure_fast_perpendicular: Fast (non-thermal) perpendicular
        pressure
    :ivar pressure_fast_parallel: Fast (non-thermal) parallel pressure
    """
    class Meta:
        name = "core_profiles_neutral_state"

    label: str = field(
        default=""
    )
    electron_configuration: str = field(
        default=""
    )
    vibrational_level: float = field(
        default=9e+40
    )
    vibrational_mode: str = field(
        default=""
    )
    neutral_type: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    velocity: Optional[CoreProfilesVectorComponents3] = field(
        default=None
    )
    temperature: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast_perpendicular: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class CoreProfileNeutral(IdsBaseClass):
    """
    Quantities related to a given neutral species.

    :ivar element: List of elements forming the atom or molecule
    :ivar label: String identifying the species (e.g. H, D, T, He, C,
        D2, DT, CD4, ...)
    :ivar ion_index: Index of the corresponding ion species in the
        ../../ion array
    :ivar temperature: Temperature (average over charge states when
        multiple charge states are considered)
    :ivar density: Density (thermal+non-thermal) (sum over charge states
        when multiple charge states are considered)
    :ivar density_thermal: Density (thermal) (sum over charge states
        when multiple charge states are considered)
    :ivar density_fast: Density of fast (non-thermal) particles (sum
        over charge states when multiple charge states are considered)
    :ivar pressure: Pressure (thermal+non-thermal) (sum over charge
        states when multiple charge states are considered)
    :ivar pressure_thermal: Pressure (thermal) associated with random
        motion ~average((v-average(v))^2) (sum over charge states when
        multiple charge states are considered)
    :ivar pressure_fast_perpendicular: Fast (non-thermal) perpendicular
        pressure  (sum over charge states when multiple charge states
        are considered)
    :ivar pressure_fast_parallel: Fast (non-thermal) parallel pressure
        (sum over charge states when multiple charge states are
        considered)
    :ivar velocity: Velocity (average over charge states when multiple
        charge states are considered)
    :ivar multiple_states_flag: Multiple states calculation flag :
        0-Only one state is considered; 1-Multiple states are considered
        and are described in the state structure
    :ivar state: Quantities related to the different states of the
        species (energy, excitation, ...)
    """
    class Meta:
        name = "core_profile_neutral"

    element: list[PlasmaCompositionNeutralElement] = field(
        default_factory=list
    )
    label: str = field(
        default=""
    )
    ion_index: int = field(
        default=999999999
    )
    temperature: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast_perpendicular: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    velocity: Optional[CoreProfilesVectorComponents2] = field(
        default=None
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[CoreProfilesNeutralState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class CoreProfilesIonsChargeStates2(IdsBaseClass):
    """
    Quantities related to the a given state of the ion species.

    :ivar z_min: Minimum Z of the charge state bundle
    :ivar z_max: Maximum Z of the charge state bundle (equal to z_min if
        no bundle)
    :ivar z_average: Average Z of the charge state bundle, volume
        averaged over the plasma radius (equal to z_min if no bundle), =
        sum (Z*x_z) where x_z is the relative concentration of a given
        charge state in the bundle, i.e. sum(x_z) = 1 over the bundle.
    :ivar z_square_average: Average Z square of the charge state bundle,
        volume averaged over the plasma radius (equal to z_min squared
        if no bundle), = sum (Z^2*x_z) where x_z is the relative
        concentration of a given charge state in the bundle, i.e.
        sum(x_z) = 1 over the bundle.
    :ivar z_average_1d: Average charge profile of the charge state
        bundle (equal to z_min if no bundle), = sum (Z*x_z) where x_z is
        the relative concentration of a given charge state in the
        bundle, i.e. sum(x_z) = 1 over the bundle.
    :ivar z_average_square_1d: Average square charge profile of the
        charge state bundle (equal to z_min squared if no bundle), = sum
        (Z^2*x_z) where x_z is the relative concentration of a given
        charge state in the bundle, i.e. sum(x_z) = 1 over the bundle.
    :ivar ionisation_potential: Cumulative and average ionisation
        potential to reach a given bundle. Defined as sum (x_z* (sum of
        Epot from z'=0 to z-1)), where Epot is the ionisation potential
        of ion Xz’+, and x_z is the relative concentration of a given
        charge state in the bundle, i.e. sum(x_z) = 1 over the bundle.
    :ivar label: String identifying state (e.g. C+, C+2 , C+3, C+4, C+5,
        C+6, ...)
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar velocity: Velocity
    :ivar rotation_frequency_tor: Toroidal rotation frequency (i.e.
        toroidal velocity divided by the major radius at which the
        toroidal velocity is taken)
    :ivar temperature: Temperature
    :ivar density: Density (thermal+non-thermal)
    :ivar density_fit: Information on the fit used to obtain the density
        profile
    :ivar density_thermal: Density of thermal particles
    :ivar density_fast: Density of fast (non-thermal) particles
    :ivar pressure: Pressure (thermal+non-thermal)
    :ivar pressure_thermal: Pressure (thermal) associated with random
        motion ~average((v-average(v))^2)
    :ivar pressure_fast_perpendicular: Fast (non-thermal) perpendicular
        pressure
    :ivar pressure_fast_parallel: Fast (non-thermal) parallel pressure
    """
    class Meta:
        name = "core_profiles_ions_charge_states2"

    z_min: float = field(
        default=9e+40
    )
    z_max: float = field(
        default=9e+40
    )
    z_average: float = field(
        default=9e+40
    )
    z_square_average: float = field(
        default=9e+40
    )
    z_average_1d: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    z_average_square_1d: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    ionisation_potential: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    electron_configuration: str = field(
        default=""
    )
    vibrational_level: float = field(
        default=9e+40
    )
    vibrational_mode: str = field(
        default=""
    )
    velocity: Optional[CoreProfilesVectorComponents3] = field(
        default=None
    )
    rotation_frequency_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    temperature: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density_fit: Optional[CoreProfiles1DFit] = field(
        default=None
    )
    density_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast_perpendicular: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class CoreProfilesProfiles1DElectrons(IdsBaseClass):
    """
    Quantities related to electrons.

    :ivar temperature: Temperature
    :ivar temperature_validity: Indicator of the validity of the
        temperature profile. 0: valid from automated processing, 1:
        valid and certified by the RO; - 1 means problem identified in
        the data processing (request verification by the RO), -2:
        invalid data, should not be used
    :ivar temperature_fit: Information on the fit used to obtain the
        temperature profile
    :ivar density: Density (thermal+non-thermal)
    :ivar density_validity: Indicator of the validity of the density
        profile. 0: valid from automated processing, 1: valid and
        certified by the RO; - 1 means problem identified in the data
        processing (request verification by the RO), -2: invalid data,
        should not be used
    :ivar density_fit: Information on the fit used to obtain the density
        profile
    :ivar density_thermal: Density of thermal particles
    :ivar density_fast: Density of fast (non-thermal) particles
    :ivar pressure: Pressure (thermal+non-thermal)
    :ivar pressure_thermal: Pressure (thermal) associated with random
        motion ~average((v-average(v))^2)
    :ivar pressure_fast_perpendicular: Fast (non-thermal) perpendicular
        pressure
    :ivar pressure_fast_parallel: Fast (non-thermal) parallel pressure
    :ivar velocity_tor: Toroidal velocity
    :ivar velocity_pol: Poloidal velocity
    :ivar velocity: Velocity
    :ivar collisionality_norm: Collisionality normalised to the bounce
        frequency
    """
    class Meta:
        name = "core_profiles_profiles_1d_electrons"

    temperature: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    temperature_validity: int = field(
        default=999999999
    )
    temperature_fit: Optional[CoreProfiles1DFit] = field(
        default=None
    )
    density: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density_validity: int = field(
        default=999999999
    )
    density_fit: Optional[CoreProfiles1DFit] = field(
        default=None
    )
    density_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast_perpendicular: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    velocity_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    velocity_pol: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    velocity: Optional[CoreProfilesVectorComponents2] = field(
        default=None
    )
    collisionality_norm: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class CoreProfileIons(IdsBaseClass):
    """
    Quantities related to a given ion species.

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed), volume averaged over plasma radius
    :ivar label: String identifying ion (e.g. H, D, T, He, C, D2, ...)
    :ivar neutral_index: Index of the corresponding neutral species in
        the ../../neutral array
    :ivar z_ion_1d: Average charge of the ion species (sum of states
        charge weighted by state density and divided by ion density)
    :ivar z_ion_square_1d: Average square charge of the ion species (sum
        of states square charge weighted by state density and divided by
        ion density)
    :ivar temperature: Temperature (average over charge states when
        multiple charge states are considered)
    :ivar temperature_validity: Indicator of the validity of the
        temperature profile. 0: valid from automated processing, 1:
        valid and certified by the RO; - 1 means problem identified in
        the data processing (request verification by the RO), -2:
        invalid data, should not be used
    :ivar temperature_fit: Information on the fit used to obtain the
        temperature profile
    :ivar density: Density (thermal+non-thermal) (sum over charge states
        when multiple charge states are considered)
    :ivar density_validity: Indicator of the validity of the density
        profile. 0: valid from automated processing, 1: valid and
        certified by the RO; - 1 means problem identified in the data
        processing (request verification by the RO), -2: invalid data,
        should not be used
    :ivar density_fit: Information on the fit used to obtain the density
        profile
    :ivar density_thermal: Density (thermal) (sum over charge states
        when multiple charge states are considered)
    :ivar density_fast: Density of fast (non-thermal) particles (sum
        over charge states when multiple charge states are considered)
    :ivar pressure: Pressure (thermal+non-thermal) (sum over charge
        states when multiple charge states are considered)
    :ivar pressure_thermal: Pressure (thermal) associated with random
        motion ~average((v-average(v))^2) (sum over charge states when
        multiple charge states are considered)
    :ivar pressure_fast_perpendicular: Fast (non-thermal) perpendicular
        pressure  (sum over charge states when multiple charge states
        are considered)
    :ivar pressure_fast_parallel: Fast (non-thermal) parallel pressure
        (sum over charge states when multiple charge states are
        considered)
    :ivar velocity_tor: Toroidal velocity (average over charge states
        when multiple charge states are considered)
    :ivar velocity_pol: Poloidal velocity (average over charge states
        when multiple charge states are considered)
    :ivar rotation_frequency_tor: Toroidal rotation frequency  (i.e.
        toroidal velocity divided by the major radius at which the
        toroidal velocity is taken) (average over charge states when
        multiple charge states are considered)
    :ivar velocity: Velocity (average over charge states when multiple
        charge states are considered) at the position of maximum major
        radius on every flux surface
    :ivar multiple_states_flag: Multiple states calculation flag :
        0-Only the 'ion' level is considered and the 'state' array of
        structure is empty; 1-Ion states are considered and are
        described in the 'state' array of structure
    :ivar state: Quantities related to the different states of the
        species (ionisation, energy, excitation, ...)
    """
    class Meta:
        name = "core_profile_ions"

    element: list[PlasmaCompositionNeutralElement] = field(
        default_factory=list
    )
    z_ion: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    neutral_index: int = field(
        default=999999999
    )
    z_ion_1d: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    z_ion_square_1d: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    temperature: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    temperature_validity: int = field(
        default=999999999
    )
    temperature_fit: Optional[CoreProfiles1DFit] = field(
        default=None
    )
    density: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density_validity: int = field(
        default=999999999
    )
    density_fit: Optional[CoreProfiles1DFit] = field(
        default=None
    )
    density_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    density_fast: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_thermal: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast_perpendicular: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    pressure_fast_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    velocity_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    velocity_pol: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    rotation_frequency_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    velocity: Optional[CoreProfilesVectorComponents2] = field(
        default=None
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[CoreProfilesIonsChargeStates2] = field(
        default_factory=list
    )


@dataclass(slots=True)
class CoreProfilesProfiles1D(IdsBaseClass):
    """
    1D radial profiles for core and edge.

    :ivar grid: Radial grid
    :ivar electrons: Quantities related to the electrons
    :ivar ion: Quantities related to the different ion species, in the
        sense of isonuclear or isomolecular sequences. Ionisation states
        (or other types of states) must be differentiated at the state
        level below
    :ivar neutral: Quantities related to the different neutral species
    :ivar t_i_average: Ion temperature (averaged on charge states and
        ion species)
    :ivar t_i_average_fit: Information on the fit used to obtain the
        t_i_average profile
    :ivar n_i_total_over_n_e: Ratio of total ion density (sum over
        species and charge states) over electron density. (thermal+non-
        thermal)
    :ivar n_i_thermal_total: Total ion thermal density (sum over species
        and charge states)
    :ivar momentum_tor: Total plasma toroidal momentum, summed over ion
        species and electrons weighted by their density and major
        radius, i.e. sum_over_species(n*R*m*Vphi)
    :ivar zeff: Effective charge
    :ivar zeff_fit: Information on the fit used to obtain the zeff
        profile
    :ivar pressure_ion_total: Total (sum over ion species) thermal ion
        pressure
    :ivar pressure_thermal: Thermal pressure (electrons+ions)
    :ivar pressure_perpendicular: Total perpendicular pressure
        (electrons+ions, thermal+non-thermal)
    :ivar pressure_parallel: Total parallel pressure (electrons+ions,
        thermal+non-thermal)
    :ivar j_total: Total parallel current density = average(jtot.B) /
        B0, where B0 = Core_Profiles/Vacuum_Toroidal_Field/ B0
    :ivar current_parallel_inside: Parallel current driven inside the
        flux surface. Cumulative surface integral of j_total
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
    :ivar e_field: Electric field, averaged on the magnetic surface. E.g
        for the parallel component, average(E.B) / B0, using
        core_profiles/vacuum_toroidal_field/b0
    :ivar phi_potential: Electrostatic potential, averaged on the
        magnetic flux surface
    :ivar rotation_frequency_tor_sonic: Derivative of the flux surface
        averaged electrostatic potential with respect to the poloidal
        flux, multiplied by -1. This quantity is the toroidal angular
        rotation frequency due to the ExB drift, introduced in formula
        (43) of Hinton and Wong, Physics of Fluids 3082 (1985), also
        referred to as sonic flow in regimes in which the toroidal
        velocity is dominant over the poloidal velocity
    :ivar q: Safety factor (IMAS uses COCOS=11: only positive when
        toroidal current and magnetic field are in same direction)
    :ivar magnetic_shear: Magnetic shear, defined as rho_tor/q .
        dq/drho_tor
    :ivar time: Time
    """
    class Meta:
        name = "core_profiles_profiles_1d"

    grid: Optional[CoreRadialGrid] = field(
        default=None
    )
    electrons: Optional[CoreProfilesProfiles1DElectrons] = field(
        default=None
    )
    ion: list[CoreProfileIons] = field(
        default_factory=list
    )
    neutral: list[CoreProfileNeutral] = field(
        default_factory=list
    )
    t_i_average: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    t_i_average_fit: Optional[CoreProfiles1DFit] = field(
        default=None
    )
    n_i_total_over_n_e: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    n_i_thermal_total: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    momentum_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    zeff: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    zeff_fit: Optional[CoreProfiles1DFit] = field(
        default=None
    )
    pressure_ion_total: Optional[ndarray[(int,), float]] = field(
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
    current_parallel_inside: Optional[ndarray[(int,), float]] = field(
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
    e_field: Optional[CoreProfilesVectorComponents1] = field(
        default=None
    )
    phi_potential: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    rotation_frequency_tor_sonic: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    q: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    magnetic_shear: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class CoreProfiles(IdsBaseClass):
    """
    Core plasma radial profiles.

    :ivar ids_properties:
    :ivar profiles_1d: Core plasma radial profiles for various time
        slices
    :ivar global_quantities: Various global quantities derived from the
        profiles
    :ivar vacuum_toroidal_field: Characteristics of the vacuum toroidal
        field (used in rho_tor definition and in the normalization of
        current densities)
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "core_profiles"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    profiles_1d: list[CoreProfilesProfiles1D] = field(
        default_factory=list
    )
    global_quantities: Optional[CoreProfilesGlobalQuantities] = field(
        default=None
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
