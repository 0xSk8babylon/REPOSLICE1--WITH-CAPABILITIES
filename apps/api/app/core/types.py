from enum import Enum


class StructureType(str, Enum):
    main_house = "main_house"
    detached_garage = "detached_garage"
    workshop = "workshop"
    adu = "ADU"
    barn = "barn"
    other = "other"


class PanelType(str, Enum):
    main_service_panel = "main_service_panel"
    subpanel = "subpanel"
    critical_load_panel = "critical_load_panel"
    smart_panel = "smart_panel"
    solar_ready_panel = "solar_ready_panel"


class IndoorOutdoor(str, Enum):
    indoor = "indoor"
    outdoor = "outdoor"


class BackupPriority(str, Enum):
    essential = "essential"
    preferred = "preferred"
    optional = "optional"
    non_backup = "non_backup"


class PhaseType(str, Enum):
    single_phase = "single_phase"
    split_phase = "split_phase"
    three_phase = "three_phase"


class DesignGoal(str, Enum):
    lowest_cost = "lowest_cost"
    partial_backup = "partial_backup"
    whole_home_backup = "whole_home_backup"
    expansion_ready = "expansion_ready"
    generator_assisted = "generator_assisted"
    workshop_ready = "workshop_ready"
    off_grid_capable = "off_grid_capable"


class ArchitectureType(str, Enum):
    grid_tied = "grid_tied"
    hybrid = "hybrid"
    off_grid = "off_grid"
    ac_coupled = "ac_coupled"
    dc_coupled = "dc_coupled"
    mixed = "mixed"


class ProductType(str, Enum):
    solar_panel = "solar_panel"
    microinverter = "microinverter"
    string_inverter = "string_inverter"
    hybrid_inverter = "hybrid_inverter"
    battery = "battery"
    generator = "generator"
    gateway = "gateway"
    smart_panel = "smart_panel"
    load_center = "load_center"
    disconnect = "disconnect"
    transfer_switch = "transfer_switch"
    ev_charger = "ev_charger"
    other = "other"


class Ecosystem(str, Enum):
    tesla = "Tesla"
    enphase = "Enphase"
    eg4 = "EG4"
    schneider = "Schneider"
    ecoflow = "EcoFlow"
    span = "SPAN"
    sol_ark = "Sol-Ark"
    generac = "Generac"
    other = "Other"


class LocationType(str, Enum):
    roof = "roof"
    garage_wall = "garage_wall"
    exterior_wall = "exterior_wall"
    utility_area = "utility_area"
    battery_area = "battery_area"
    generator_pad = "generator_pad"
    trench_route = "trench_route"
    attic = "attic"
    crawlspace = "crawlspace"
    other = "other"


class Severity(str, Enum):
    info = "info"
    warning = "warning"
    blocker = "blocker"


class IssueCategory(str, Enum):
    product_fit = "product_fit"
    capacity = "capacity"
    backup = "backup"
    expansion = "expansion"
    code_guidance = "code_guidance"
    install_complexity = "install_complexity"
    cost_driver = "cost_driver"


class AccountRole(str, Enum):
    homeowner = "homeowner"
    contractor = "contractor"
    admin = "admin"


class SubscriptionStatus(str, Enum):
    trialing = "trialing"
    active = "active"
    paused = "paused"
    canceled = "canceled"


class PlanType(str, Enum):
    demo = "demo"
    homeowner = "homeowner"
    contractor = "contractor"
    contractor_team = "contractor_team"


class FactLifecycleState(str, Enum):
    """Canonical lifecycle/trust vocabulary for planning facts.

    This is the single vocabulary for both ``data_origin`` (how a record
    entered the system / how it should be badged) and provenance
    ``trust_state`` (how much a recorded fact can be trusted). States are
    ordered roughly from least to most trustworthy, with ``expired`` as the
    explicit end-of-life state.

    ``SourceDocument.verification_status`` remains a separate document-level
    axis (see ``VerificationStatus`` and ``VERIFICATION_STATUS_TO_LIFECYCLE``).
    """

    demo_seed = "demo_seed"
    placeholder = "placeholder"
    claimed = "claimed"
    user_created = "user_created"
    derived_estimate = "derived_estimate"
    imported = "imported"
    photo_verified = "photo_verified"
    contractor_verified = "contractor_verified"
    verified = "verified"
    expired = "expired"


class FactSource(str, Enum):
    utility_bill = "utility_bill"
    homeowner_stated = "homeowner_stated"
    photo_verified = "photo_verified"
    contractor_measured = "contractor_measured"
    derived = "derived"
    manufacturer_spec = "manufacturer_spec"


class FactConfidenceTier(str, Enum):
    known = "known"
    derived = "derived"
    assumed = "assumed"
    missing = "missing"


class FactDecayPolicy(str, Enum):
    no_decay = "no_decay"
    slow_decay = "slow_decay"
    standard_decay = "standard_decay"
    fast_decay = "fast_decay"


# Backward-compatible alias: every existing ``data_origin: DataOrigin`` and
# ``trust_state: DataOrigin`` annotation now resolves to the canonical fact
# lifecycle vocabulary (stored string values are unchanged).
DataOrigin = FactLifecycleState


class SourceDocumentType(str, Enum):
    manufacturer_datasheet = "manufacturer_datasheet"
    installation_manual = "installation_manual"
    user_entry = "user_entry"
    demo_seed = "demo_seed"
    imported_file = "imported_file"
    internal_rule = "internal_rule"
    calculation = "calculation"
    other = "other"


class VerificationStatus(str, Enum):
    """Verification state of a source document (document axis).

    Distinct from ``FactLifecycleState``: a document's verification describes
    the document itself, while the lifecycle state describes a recorded fact.
    Stored values are preserved as-is; use the crosswalk below when an engine
    needs to fold document verification into the fact lifecycle vocabulary.
    """

    unverified = "unverified"
    user_entered = "user_entered"
    imported = "imported"
    manufacturer_verified = "manufacturer_verified"
    deprecated = "deprecated"


# Crosswalk from document verification status to the canonical fact
# lifecycle vocabulary, for engines that reason over a single axis.
VERIFICATION_STATUS_TO_LIFECYCLE = {
    VerificationStatus.unverified: FactLifecycleState.claimed,
    VerificationStatus.user_entered: FactLifecycleState.user_created,
    VerificationStatus.imported: FactLifecycleState.imported,
    VerificationStatus.manufacturer_verified: FactLifecycleState.verified,
    VerificationStatus.deprecated: FactLifecycleState.expired,
}


class ConfidenceLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class AuthorityLayer(str, Enum):
    canonical = "canonical"
    derived = "derived"
    advisory = "advisory"
    operational = "operational"
    historical = "historical"


class DataClassification(str, Enum):
    public_reference = "public_reference"
    planning_private = "planning_private"
    contractor_scoped = "contractor_scoped"
    utility_scoped = "utility_scoped"
    operational_control = "operational_control"
    internal_governance = "internal_governance"


class ApiViewAudience(str, Enum):
    consumer = "consumer"
    ai = "ai"
    contractor = "contractor"
    utility = "utility"
    operator = "operator"
    internal = "internal"


class RecommendationProfile(str, Enum):
    critical_efficient = "critical_efficient"
    balanced = "balanced"
    conservative = "conservative"
    premium_future_ready = "premium_future_ready"


class BatterySizingPosture(str, Enum):
    lean = "lean"
    balanced = "balanced"
    elevated = "elevated"
    robust = "robust"


class SolarSizingPosture(str, Enum):
    load_matched = "load_matched"
    resilience_balanced = "resilience_balanced"
    recovery_weighted = "recovery_weighted"
    future_weighted = "future_weighted"


class AutonomyReservePosture(str, Enum):
    minimal = "minimal"
    standard = "standard"
    elevated = "elevated"
    extended = "extended"


class FutureGrowthMarginPosture(str, Enum):
    tight = "tight"
    planned = "planned"
    expansion_oriented = "expansion_oriented"
    future_ready = "future_ready"


class LowSolarAssumptionPosture(str, Enum):
    favorable = "favorable"
    typical = "typical"
    protective = "protective"
    defensive = "defensive"


class ReserveMarginPosture(str, Enum):
    lean = "lean"
    standard = "standard"
    elevated = "elevated"
    robust = "robust"


class RecoveryStrengthPosture(str, Enum):
    modest = "modest"
    balanced = "balanced"
    strong = "strong"
    aggressive = "aggressive"


class SeasonalConservatismPosture(str, Enum):
    mild = "mild"
    standard = "standard"
    protective = "protective"
    defensive = "defensive"
