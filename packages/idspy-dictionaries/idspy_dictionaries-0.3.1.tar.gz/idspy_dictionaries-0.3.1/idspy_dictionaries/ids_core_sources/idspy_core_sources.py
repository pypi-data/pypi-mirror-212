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
class CoreSourcesSourceGlobalElectrons(IdsBaseClass):
    """
    Source terms related to electrons.

    :ivar particles: Electron particle source
    :ivar power: Power coupled to electrons
    """
    class Meta:
        name = "core_sources_source_global_electrons"

    particles: float = field(
        default=9e+40
    )
    power: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class CoreSourcesSourceProfiles1DEnergyDecomposed2(IdsBaseClass):
    """
    Source terms decomposed for the energy transport equation, assuming
    core_radial_grid 2 levels above.

    :ivar implicit_part: Implicit part of the source term, i.e. to be
        multiplied by the equation's primary quantity
    :ivar explicit_part: Explicit part of the source term
    """
    class Meta:
        name = "core_sources_source_profiles_1d_energy_decomposed_2"

    implicit_part: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    explicit_part: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class CoreSourcesSourceProfiles1DEnergyDecomposed3(IdsBaseClass):
    """
    Source terms decomposed for the energy transport equation, assuming
    core_radial_grid 3 levels above.

    :ivar implicit_part: Implicit part of the source term, i.e. to be
        multiplied by the equation's primary quantity
    :ivar explicit_part: Explicit part of the source term
    """
    class Meta:
        name = "core_sources_source_profiles_1d_energy_decomposed_3"

    implicit_part: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    explicit_part: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class CoreSourcesSourceProfiles1DEnergyDecomposed4(IdsBaseClass):
    """
    Source terms decomposed for the energy transport equation, assuming
    core_radial_grid 4 levels above.

    :ivar implicit_part: Implicit part of the source term, i.e. to be
        multiplied by the equation's primary quantity
    :ivar explicit_part: Explicit part of the source term
    """
    class Meta:
        name = "core_sources_source_profiles_1d_energy_decomposed_4"

    implicit_part: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    explicit_part: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class CoreSourcesSourceProfiles1DMomentumDecomposed4(IdsBaseClass):
    """
    Source terms decomposed for the momentum transport equation, assuming
    core_radial_grid 4 levels above.

    :ivar implicit_part: Implicit part of the source term, i.e. to be
        multiplied by the equation's primary quantity
    :ivar explicit_part: Explicit part of the source term
    """
    class Meta:
        name = "core_sources_source_profiles_1d_momentum_decomposed_4"

    implicit_part: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    explicit_part: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class CoreSourcesSourceProfiles1DParticlesDecomposed3(IdsBaseClass):
    """
    Source terms decomposed for the particle transport equation, assuming
    core_radial_grid 3 levels above.

    :ivar implicit_part: Implicit part of the source term, i.e. to be
        multiplied by the equation's primary quantity
    :ivar explicit_part: Explicit part of the source term
    """
    class Meta:
        name = "core_sources_source_profiles_1d_particles_decomposed_3"

    implicit_part: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    explicit_part: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class CoreSourcesSourceProfiles1DParticlesDecomposed4(IdsBaseClass):
    """
    Source terms decomposed for the particle transport equation, assuming
    core_radial_grid 4 levels above.

    :ivar implicit_part: Implicit part of the source term, i.e. to be
        multiplied by the equation's primary quantity
    :ivar explicit_part: Explicit part of the source term
    """
    class Meta:
        name = "core_sources_source_profiles_1d_particles_decomposed_4"

    implicit_part: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    explicit_part: Optional[ndarray[(int,), float]] = field(
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
class PlasmaCompositionIonStateConstant(IdsBaseClass):
    """
    Definition of an ion state (when describing the plasma composition) (constant)

    :ivar z_min: Minimum Z of the charge state bundle (z_min = z_max = 0
        for a neutral)
    :ivar z_max: Maximum Z of the charge state bundle (equal to z_min if
        no bundle)
    :ivar label: String identifying ion state (e.g. C+, C+2 , C+3, C+4,
        C+5, C+6, ...)
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    """
    class Meta:
        name = "plasma_composition_ion_state_constant"

    z_min: float = field(
        default=9e+40
    )
    z_max: float = field(
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
class CoreSourcesSourceGlobal(IdsBaseClass):
    """
    Source global quantities for a given time slice.

    :ivar power: Total power coupled to the plasma
    :ivar total_ion_particles: Total ion particle source (summed over
        ion  species)
    :ivar total_ion_power: Total power coupled to ion species (summed
        over ion  species)
    :ivar electrons: Sources for electrons
    :ivar torque_tor: Toroidal torque
    :ivar current_parallel: Parallel current driven
    :ivar time: Time
    """
    class Meta:
        name = "core_sources_source_global"

    power: float = field(
        default=9e+40
    )
    total_ion_particles: float = field(
        default=9e+40
    )
    total_ion_power: float = field(
        default=9e+40
    )
    electrons: Optional[CoreSourcesSourceGlobalElectrons] = field(
        default=None
    )
    torque_tor: float = field(
        default=9e+40
    )
    current_parallel: float = field(
        default=9e+40
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class CoreSourcesSourceProfiles1DComponents2(IdsBaseClass):
    """
    Source terms for vector components in predefined directions, assuming
    core_radial_grid 2 levels above.

    :ivar radial: Radial component
    :ivar diamagnetic: Diamagnetic component
    :ivar parallel: Parallel component
    :ivar poloidal: Poloidal component
    :ivar toroidal: Toroidal component
    :ivar toroidal_decomposed: Decomposition of the source term for ion
        toroidal momentum equation into implicit and explicit parts
    """
    class Meta:
        name = "core_sources_source_profiles_1d_components_2"

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
    toroidal_decomposed: Optional[CoreSourcesSourceProfiles1DMomentumDecomposed4] = field(
        default=None
    )


@dataclass(slots=True)
class CoreSourcesSourceProfiles1DElectrons(IdsBaseClass):
    """
    Source terms related to electrons.

    :ivar particles: Source term for electron density equation
    :ivar particles_decomposed: Decomposition of the source term for
        electron density equation into implicit and explicit parts
    :ivar particles_inside: Electron source inside the flux surface.
        Cumulative volume integral of the source term for the electron
        density equation.
    :ivar energy: Source term for the electron energy equation
    :ivar energy_decomposed: Decomposition of the source term for
        electron energy equation into implicit and explicit parts
    :ivar power_inside: Power coupled to electrons inside the flux
        surface. Cumulative volume integral of the source term for the
        electron energy equation
    """
    class Meta:
        name = "core_sources_source_profiles_1d_electrons"

    particles: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    particles_decomposed: Optional[CoreSourcesSourceProfiles1DParticlesDecomposed3] = field(
        default=None
    )
    particles_inside: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    energy: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    energy_decomposed: Optional[CoreSourcesSourceProfiles1DEnergyDecomposed3] = field(
        default=None
    )
    power_inside: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class CoreSourcesSourceProfiles1DIonsChargeStates(IdsBaseClass):
    """
    Source terms related to the a given state of the ion species.

    :ivar z_min: Minimum Z of the charge state bundle
    :ivar z_max: Maximum Z of the charge state bundle
    :ivar label: String identifying charge state (e.g. C+, C+2 , C+3,
        C+4, C+5, C+6, ...)
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar is_neutral: Flag specifying if this state corresponds to a
        neutral (1) or not (0)
    :ivar neutral_type: Neutral type (if the considered state is a
        neutral), in terms of energy. ID =1: cold; 2: thermal; 3: fast;
        4: NBI
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar particles: Source term for the charge state density transport
        equation
    :ivar particles_decomposed: Decomposition of the source term for
        state density equation into implicit and explicit parts
    :ivar energy: Source terms for the charge state energy transport
        equation
    :ivar energy_decomposed: Decomposition of the source term for state
        energy equation into implicit and explicit parts
    """
    class Meta:
        name = "core_sources_source_profiles_1d_ions_charge_states"

    z_min: float = field(
        default=9e+40
    )
    z_max: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    vibrational_level: float = field(
        default=9e+40
    )
    vibrational_mode: str = field(
        default=""
    )
    is_neutral: int = field(
        default=999999999
    )
    neutral_type: Optional[IdentifierDynamicAos3] = field(
        default=None
    )
    electron_configuration: str = field(
        default=""
    )
    particles: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    particles_decomposed: Optional[CoreSourcesSourceProfiles1DParticlesDecomposed4] = field(
        default=None
    )
    energy: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    energy_decomposed: Optional[CoreSourcesSourceProfiles1DEnergyDecomposed4] = field(
        default=None
    )


@dataclass(slots=True)
class CoreSourcesSourceProfiles1DNeutralState(IdsBaseClass):
    """
    Source terms related to the a given state of the neutral species.

    :ivar label: String identifying state
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar neutral_type: Neutral type (if the considered state is a
        neutral), in terms of energy. ID =1: cold; 2: thermal; 3: fast;
        4: NBI
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar particles: Source term for the state density transport
        equation
    :ivar energy: Source terms for the state energy transport equation
    """
    class Meta:
        name = "core_sources_source_profiles_1d_neutral_state"

    label: str = field(
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
    electron_configuration: str = field(
        default=""
    )
    particles: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    energy: Optional[ndarray[(int,), float]] = field(
        default=None
    )


@dataclass(slots=True)
class PlasmaCompositionIonsConstant(IdsBaseClass):
    """
    Description of plasma ions (constant)

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed)
    :ivar label: String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)
    :ivar state: Quantities related to the different states of the
        species (ionisation, energy, excitation, ...)
    """
    class Meta:
        name = "plasma_composition_ions_constant"

    element: list[PlasmaCompositionNeutralElementConstant] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    z_ion: float = field(
        default=9e+40
    )
    label: str = field(
        default=""
    )
    state: Optional[PlasmaCompositionIonStateConstant] = field(
        default=None
    )


@dataclass(slots=True)
class PlasmaCompositionNeutralStateConstant(IdsBaseClass):
    """
    Definition of a neutral state (when describing the plasma composition)
    (constant)

    :ivar label: String identifying neutral state
    :ivar electron_configuration: Configuration of atomic orbitals of
        this state, e.g. 1s2-2s1
    :ivar vibrational_level: Vibrational level (can be bundled)
    :ivar vibrational_mode: Vibrational mode of this state, e.g. "A_g".
        Need to define, or adopt a standard nomenclature.
    :ivar neutral_type: Neutral type, in terms of energy. ID =1: cold;
        2: thermal; 3: fast; 4: NBI
    """
    class Meta:
        name = "plasma_composition_neutral_state_constant"

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
    neutral_type: Optional[Identifier] = field(
        default=None
    )


@dataclass(slots=True)
class CoreSourcesSourceProfiles1DIons(IdsBaseClass):
    """
    Source terms related to a given ion species.

    :ivar element: List of elements forming the atom or molecule
    :ivar z_ion: Ion charge (of the dominant ionisation state; lumped
        ions are allowed)
    :ivar label: String identifying ion (e.g. H, D, T, He, C, D2, ...)
    :ivar neutral_index: Index of the corresponding neutral species in
        the ../../neutral array
    :ivar particles: Source term for ion density equation
    :ivar particles_decomposed: Decomposition of the source term for ion
        density equation into implicit and explicit parts
    :ivar energy: Source term for the ion energy transport equation.
    :ivar energy_decomposed: Decomposition of the source term for ion
        energy equation into implicit and explicit parts
    :ivar momentum: Source term for the ion momentum transport equations
        along various components (directions)
    :ivar multiple_states_flag: Multiple states calculation flag :
        0-Only the 'ion' level is considered and the 'state' array of
        structure is empty; 1-Ion states are considered and are
        described in the 'state' array of structure
    :ivar state: Source terms related to the different charge states of
        the species (ionisation, energy, excitation, ...)
    """
    class Meta:
        name = "core_sources_source_profiles_1d_ions"

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
    particles: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    particles_decomposed: Optional[CoreSourcesSourceProfiles1DParticlesDecomposed3] = field(
        default=None
    )
    energy: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    energy_decomposed: Optional[CoreSourcesSourceProfiles1DEnergyDecomposed3] = field(
        default=None
    )
    momentum: Optional[CoreSourcesSourceProfiles1DComponents2] = field(
        default=None
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[CoreSourcesSourceProfiles1DIonsChargeStates] = field(
        default_factory=list
    )


@dataclass(slots=True)
class CoreSourcesSourceProfiles1DNeutral(IdsBaseClass):
    """
    Source terms related to a given neutral species.

    :ivar element: List of elements forming the atom or molecule
    :ivar label: String identifying the neutral species (e.g. H, D, T,
        He, C, ...)
    :ivar ion_index: Index of the corresponding ion species in the
        ../../ion array
    :ivar particles: Source term for neutral density equation
    :ivar energy: Source term for the neutral energy transport equation.
    :ivar multiple_states_flag: Multiple states calculation flag :
        0-Only one state is considered; 1-Multiple states are considered
        and are described in the state structure
    :ivar state: Source terms related to the different charge states of
        the species (energy, excitation, ...)
    """
    class Meta:
        name = "core_sources_source_profiles_1d_neutral"

    element: list[PlasmaCompositionNeutralElement] = field(
        default_factory=list
    )
    label: str = field(
        default=""
    )
    ion_index: int = field(
        default=999999999
    )
    particles: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    energy: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    multiple_states_flag: int = field(
        default=999999999
    )
    state: list[CoreSourcesSourceProfiles1DNeutralState] = field(
        default_factory=list
    )


@dataclass(slots=True)
class PlasmaCompositionNeutralConstant(IdsBaseClass):
    """
    Definition of plasma neutral (constant)

    :ivar element: List of elements forming the atom or molecule
    :ivar label: String identifying neutral (e.g. H, D, T, He, C, ...)
    :ivar state: State of the species (energy, excitation, ...)
    """
    class Meta:
        name = "plasma_composition_neutral_constant"

    element: list[PlasmaCompositionNeutralElementConstant] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    label: str = field(
        default=""
    )
    state: Optional[PlasmaCompositionNeutralStateConstant] = field(
        default=None
    )


@dataclass(slots=True)
class CoreSourcesSourceProfiles1D(IdsBaseClass):
    """
    Source terms for a given time slice.

    :ivar grid: Radial grid
    :ivar electrons: Sources for electrons
    :ivar total_ion_energy: Source term for the total (summed over ion
        species) energy equation
    :ivar total_ion_energy_decomposed: Decomposition of the source term
        for total ion energy equation into implicit and explicit parts
    :ivar total_ion_power_inside: Total power coupled to ion species
        (summed over ion  species) inside the flux surface. Cumulative
        volume integral of the source term for the total ion energy
        equation
    :ivar momentum_tor: Source term for total toroidal momentum equation
    :ivar torque_tor_inside: Toroidal torque inside the flux surface.
        Cumulative volume integral of the source term for the total
        toroidal momentum equation
    :ivar momentum_tor_j_cross_b_field: Contribution to the toroidal
        momentum source term (already included in the momentum_tor node)
        corresponding to the toroidal torques onto the thermal plasma
        due to Lorentz force associated with radial currents. These
        currents appear as return-currents (enforcing quasi-neutrality,
        div(J)=0) balancing radial currents of non-thermal particles,
        e.g. radial currents of fast and trapped neutral-beam-ions.
    :ivar j_parallel: Parallel current density source, average(J.B) /
        B0, where B0 = core_sources/vacuum_toroidal_field/b0
    :ivar current_parallel_inside: Parallel current driven inside the
        flux surface. Cumulative surface integral of j_parallel
    :ivar conductivity_parallel: Parallel conductivity due to this
        source
    :ivar ion: Source terms related to the different ions species, in
        the sense of isonuclear or isomolecular sequences. Ionisation
        states (and other types of states) must be differentiated at the
        state level below
    :ivar neutral: Source terms related to the different neutral species
    :ivar time: Time
    """
    class Meta:
        name = "core_sources_source_profiles_1d"

    grid: Optional[CoreRadialGrid] = field(
        default=None
    )
    electrons: Optional[CoreSourcesSourceProfiles1DElectrons] = field(
        default=None
    )
    total_ion_energy: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    total_ion_energy_decomposed: Optional[CoreSourcesSourceProfiles1DEnergyDecomposed2] = field(
        default=None
    )
    total_ion_power_inside: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    momentum_tor: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    torque_tor_inside: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    momentum_tor_j_cross_b_field: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    j_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    current_parallel_inside: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    conductivity_parallel: Optional[ndarray[(int,), float]] = field(
        default=None
    )
    ion: list[CoreSourcesSourceProfiles1DIons] = field(
        default_factory=list
    )
    neutral: list[CoreSourcesSourceProfiles1DNeutral] = field(
        default_factory=list
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class DistributionSpecies(IdsBaseClass):
    """
    Description of a species in a distribution function related IDS.

    :ivar type: Species type. index=1 for electron; index=2 for ion
        species in a single/average state (refer to ion structure);
        index=3 for ion species in a particular state (refer to
        ion/state structure);  index=4 for neutral species in a
        single/average state (refer to neutral structure); index=5 for
        neutral species in a particular state (refer to neutral/state
        structure);  index=6 for neutron; index=7 for photon
    :ivar ion: Description of the ion or neutral species, used if
        type/index = 2 or 3
    :ivar neutral: Description of the neutral species, used if
        type/index = 4 or 5
    """
    class Meta:
        name = "distribution_species"

    type: Optional[Identifier] = field(
        default=None
    )
    ion: Optional[PlasmaCompositionIonsConstant] = field(
        default=None
    )
    neutral: Optional[PlasmaCompositionNeutralConstant] = field(
        default=None
    )


@dataclass(slots=True)
class CoreSourcesSource(IdsBaseClass):
    """
    Source terms for a given actuator.

    :ivar identifier: Source term identifier (process causing this
        source term)
    :ivar species: Species causing this source term (if relevant, e.g. a
        particular ion or neutral state in case of line radiation)
    :ivar global_quantities: Total source quantities integrated over the
        plasma volume or surface
    :ivar profiles_1d: Source profiles for various time slices. Source
        terms are positive (resp. negative) when there is a gain (resp.
        a loss) to the considered channel.
    """
    class Meta:
        name = "core_sources_source"

    identifier: Optional[Identifier] = field(
        default=None
    )
    species: Optional[DistributionSpecies] = field(
        default=None
    )
    global_quantities: list[CoreSourcesSourceGlobal] = field(
        default_factory=list
    )
    profiles_1d: list[CoreSourcesSourceProfiles1D] = field(
        default_factory=list
    )


@dataclass(slots=True)
class CoreSources(IdsBaseClass):
    """Core plasma thermal source terms (for the transport equations of the thermal
    species).

    Energy terms correspond to the full kinetic energy equation (i.e.
    the energy flux takes into account the energy transported by the
    particle flux)

    :ivar ids_properties:
    :ivar vacuum_toroidal_field: Characteristics of the vacuum toroidal
        field (used in Rho_Tor definition and in the normalization of
        current densities)
    :ivar source: Set of source terms
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "core_sources"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    vacuum_toroidal_field: Optional[BTorVacuum1] = field(
        default=None
    )
    source: list[CoreSourcesSource] = field(
        default_factory=list,
        metadata={
            "max_occurs": 80,
        }
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
