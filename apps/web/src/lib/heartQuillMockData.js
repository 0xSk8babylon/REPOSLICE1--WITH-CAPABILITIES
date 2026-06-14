export const homeRecord = {
  name: "Demo Energy Twin",
  address: "Placeholder residence",
  service: "200A service",
  utility: "Utility context not connected",
  status: "Planning record",
  provenance: "Static shell data",
};

export const twinNodes = [
  {
    id: "solar",
    label: "Solar",
    x: 24,
    y: 18,
    status: "known",
    title: "Rooftop solar",
    detail: "Existing PV context is represented as a known planning object.",
    basis: "Mock shell data",
  },
  {
    id: "utility",
    label: "Utility",
    x: 76,
    y: 18,
    status: "needs",
    title: "Utility context",
    detail: "Rate, tariff, and program details remain deferred until source-backed wiring.",
    basis: "Placeholder",
  },
  {
    id: "battery",
    label: "Battery",
    x: 15,
    y: 48,
    status: "needs",
    title: "Battery storage",
    detail: "Storage size and backup behavior are draft assumptions only.",
    basis: "Mock shell data",
  },
  {
    id: "panel",
    label: "Main panel",
    x: 50,
    y: 47,
    status: "known",
    title: "Main service panel",
    detail: "Panel is the planning hub for load, backup, and upgrade readiness.",
    basis: "Mock shell data",
    hub: true,
  },
  {
    id: "meter",
    label: "Meter",
    x: 88,
    y: 49,
    status: "known",
    title: "Service meter",
    detail: "Meter context is visible, but interval data is not imported in this shell.",
    basis: "Static placeholder",
  },
  {
    id: "ev",
    label: "EV",
    x: 19,
    y: 78,
    status: "known",
    title: "EV charger",
    detail: "EV readiness is shown as a homeowner goal and load-planning object.",
    basis: "Mock shell data",
  },
  {
    id: "backup",
    label: "Backup loads",
    x: 50,
    y: 80,
    status: "needs",
    title: "Backup loads",
    detail: "Critical circuits must be confirmed before backup planning can harden.",
    basis: "Derived placeholder",
  },
  {
    id: "generator",
    label: "Generator",
    x: 82,
    y: 78,
    status: "missing",
    title: "Generator",
    detail: "Generator presence, fuel, and transfer equipment are unknown.",
    basis: "Missing data",
  },
];

export const twinEdges = [
  ["solar", "panel"],
  ["utility", "meter"],
  ["meter", "panel"],
  ["battery", "panel"],
  ["ev", "panel"],
  ["backup", "panel"],
  ["generator", "panel"],
];

export const homeFacts = [
  ["Energy Twin status", "Created from static shell data"],
  ["Known facts", "Solar, service panel, meter, EV planning object"],
  ["Needs confirmation", "Utility program context, battery assumptions, backup loads"],
  ["Missing data", "Generator details, interval usage, field verification"],
];

export const goals = [
  {
    id: "lower-bill",
    title: "Lower my bill",
    blurb: "Explore load shifting and self-consumption without claiming savings.",
    seeds: ["Template"],
  },
  {
    id: "add-solar",
    title: "Add solar",
    blurb: "Start from a PV pattern and check what facts are missing.",
    seeds: ["Template", "Sandbox"],
  },
  {
    id: "battery-backup",
    title: "Add battery backup",
    blurb: "Sketch critical-load coverage before any design is committed.",
    seeds: ["Template", "Sandbox"],
  },
  {
    id: "ev-charging",
    title: "Add EV charging",
    blurb: "Plan around panel/service capacity and future load growth.",
    seeds: ["Template"],
  },
  {
    id: "outages",
    title: "Prepare for outages",
    blurb: "Frame resilience needs and missing backup-load inputs.",
    seeds: ["Template"],
  },
  {
    id: "future-proof",
    title: "Future-proof the home",
    blurb: "Preserve headroom for later heat pump, EV, and storage upgrades.",
    seeds: ["Template"],
  },
];

export const learnTopics = [
  {
    title: "Energy Twin",
    summary: "A durable record of known home energy facts, gaps, and planning context.",
    ties: "The Home view shows which facts are known, assumed, or missing.",
  },
  {
    title: "Critical Loads",
    summary: "The circuits a homeowner wants powered during an outage.",
    ties: "Backup drafts stay provisional until these loads are confirmed.",
  },
  {
    title: "AC vs. DC Coupling",
    summary: "Different ways solar, storage, and inverters connect.",
    ties: "Guided templates use this as an architecture starting point, not a final design.",
  },
  {
    title: "Readiness Gates",
    summary: "Checks that keep a sketch from becoming overconfident.",
    ties: "Builder shows confirmation gates before project/build readiness.",
  },
];

export const templates = [
  {
    id: "ac-solar",
    architecture: "AC-Coupled",
    intent: "Solar only",
    backup: "None",
    cost: 1,
    complexity: 1,
    blurb: "A simple PV starting pattern for bill-offset exploration.",
  },
  {
    id: "ac-partial",
    architecture: "AC-Coupled",
    intent: "Partial backup",
    backup: "Critical loads",
    cost: 2,
    complexity: 2,
    blurb: "PV plus storage aimed at critical circuits during outages.",
  },
  {
    id: "dc-tou",
    architecture: "DC-Coupled",
    intent: "TOU self-consumption",
    backup: "None",
    cost: 2,
    complexity: 2,
    blurb: "Hybrid inverter pattern for daily cycling and future storage planning.",
  },
  {
    id: "hy-whole",
    architecture: "Hybrid",
    intent: "Whole-home backup",
    backup: "Whole home",
    cost: 3,
    complexity: 4,
    blurb: "Mixed architecture pattern that requires substantial confirmation.",
  },
  {
    id: "off-gen",
    architecture: "Off-Grid",
    intent: "Generator-assisted",
    backup: "Long duration",
    cost: 3,
    complexity: 4,
    blurb: "Long-duration resilience sketch with fuel and transfer assumptions.",
  },
];

export const templateOverlays = {
  "ac-solar": {
    color: "#f2b84b",
    nodes: ["solar", "panel", "meter"],
    caption: "Highlights PV, meter, and panel touchpoints.",
  },
  "ac-partial": {
    color: "#8fb8d8",
    nodes: ["solar", "battery", "panel", "backup"],
    caption: "Highlights storage and critical-load backup touchpoints.",
  },
  "dc-tou": {
    color: "#8ecf9b",
    nodes: ["solar", "battery", "panel"],
    caption: "Highlights hybrid inverter and self-consumption touchpoints.",
  },
  "hy-whole": {
    color: "#c7a4ff",
    nodes: ["solar", "battery", "panel", "backup", "generator"],
    caption: "Highlights whole-home backup dependencies and unknowns.",
  },
  "off-gen": {
    color: "#e0913f",
    nodes: ["solar", "battery", "generator", "panel", "backup"],
    caption: "Highlights long-duration resilience dependencies.",
  },
};

export const sandboxDrafts = [
  {
    name: "Summer resilience sketch",
    templateId: "ac-partial",
    goal: "Prepare for outages",
    maturity: "draft",
    fields: ["AC-coupled", "Battery", "Smart panel", "Critical-load backup"],
    assumptions: ["Critical loads estimated", "Battery sized to essentials only"],
    missing: ["Panel make/model", "Confirmed backup circuits"],
  },
  {
    name: "EV plus future heat pump",
    templateId: "dc-tou",
    goal: "Future-proof the home",
    maturity: "draft",
    fields: ["DC-coupled", "Hybrid inverter", "L2 charger"],
    assumptions: ["200A service", "Single EV charger"],
    missing: ["Heat-pump load estimate", "Service capacity confirmation"],
  },
];

export const comparisonRows = [
  ["Goal match", "Outage resilience", "Future load growth", "Daily self-consumption"],
  ["Cost tier", "2 of 4", "3 of 4", "2 of 4"],
  ["Complexity", "2 of 4", "3 of 4", "2 of 4"],
  ["Readiness", "55% mock", "40% mock", "60% mock"],
  ["Missing facts", "2 items", "2 items", "1 item"],
  ["Boundary", "Draft only", "Draft only", "Template only"],
];

export const upgradePath = [
  ["Current", "Keep known panel and service facts visible.", "known"],
  ["Template", "Pick an architecture pattern in Planner.", "ready"],
  ["Sandbox", "Customize goals and assumptions without persistence.", "draft"],
  ["Validated scenario", "Deferred until readiness checks and facts mature.", "blocked"],
  ["Project", "Builder is build-readiness context, not contractor handoff.", "future"],
];

export const builderReadiness = [
  ["Selected plan", "Summer resilience sketch", "draft"],
  ["Build readiness", "Not ready for contractor handoff", "blocked"],
  ["Confirmation gates", "Backup loads and panel details pending", "needs"],
  ["Estimate posture", "No pricing or proposal generated", "blocked"],
  ["Project promotion", "Deferred", "blocked"],
  ["Contractor handoff", "Deferred", "blocked"],
];

export const capabilities = [
  ["Energy Twin", "Home facts, provenance, missing data, status"],
  ["Explore Goals", "Homeowner intent that can seed future templates"],
  ["Planner Sandbox", "Guided templates, draft shapes, validation vocabulary"],
  ["Builder Readiness", "Confirmation gates and project-readiness framing"],
  ["Catalog", "Static route preserved outside primary navigation"],
];

export const catalogItems = [
  ["Solar PV", "Planning category only"],
  ["Battery storage", "Planning category only"],
  ["Smart panel", "Planning category only"],
  ["EV charger", "Planning category only"],
  ["Generator", "Planning category only"],
];
