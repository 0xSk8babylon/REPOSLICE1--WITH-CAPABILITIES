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


class DataOrigin(str, Enum):
    demo_seed = "demo_seed"
    user_created = "user_created"
    imported = "imported"
    verified = "verified"
    derived_estimate = "derived_estimate"
    placeholder = "placeholder"


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
    unverified = "unverified"
    user_entered = "user_entered"
    imported = "imported"
    manufacturer_verified = "manufacturer_verified"
    deprecated = "deprecated"


class ConfidenceLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
