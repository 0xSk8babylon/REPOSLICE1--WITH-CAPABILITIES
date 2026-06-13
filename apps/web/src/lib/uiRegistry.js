const SECTION_ORDER = {
  home: 10,
  planner: 20,
  build: 30,
  hidden: 40,
};

function bySectionAndPriority(left, right) {
  return (
    (SECTION_ORDER[left.section] || 999) - (SECTION_ORDER[right.section] || 999) ||
    left.priority - right.priority ||
    left.homeownerLabel.localeCompare(right.homeownerLabel)
  );
}

export const architectureProductCapabilityIds = Object.freeze([
  "capability-energy-twin",
  "capability-energy-passport",
  "capability-readiness",
  "capability-home-facts",
  "capability-compatibility",
  "capability-scenario-builder",
  "capability-product-preferences",
  "capability-planning-intelligence",
  "capability-proposal-options",
  "capability-contractor-context",
  "capability-estimate-readiness",
  "capability-install-path",
  "capability-program-intelligence",
  "capability-architecture-cockpit",
]);

export const allowedFutureSourceCapabilityIds = Object.freeze([
  // Phase 13 exists in backend runtime, but the Architecture/Product cockpit
  // does not yet expose a matching product_capability node.
  "capability-post-install-handoff",
]);

export const uiRegistry = Object.freeze([
  {
    id: "energy-twin-overview",
    productName: "Energy Twin Overview",
    homeownerLabel: "Energy Twin",
    contractorLabel: "Home energy record",
    section: "home",
    cardName: "Energy Twin Overview",
    priority: 10,
    visibleInV1: true,
    dataType: "durable_record",
    sourceCapability: "capability-energy-twin",
    homeownerQuestionAnswered: "What does the system know about my home?",
    emptyStateMessage: "Start the Energy Twin by adding basic home, panel, utility, and load details.",
    trustBoundaryNotes: [
      "Structured home facts are authoritative over generated explanation.",
      "Planning completeness does not mean engineering approval.",
    ],
  },
  {
    id: "single-line-diagram",
    productName: "Single-Line Diagram",
    homeownerLabel: "Home energy outline",
    contractorLabel: "Planning topology outline",
    section: "home",
    cardName: "Home Energy Outline",
    priority: 20,
    visibleInV1: true,
    dataType: "derived_view",
    sourceCapability: "capability-energy-twin",
    homeownerQuestionAnswered: "How do the main home energy parts relate at a planning level?",
    emptyStateMessage: "Add panel, equipment, and pathway context before showing a useful home energy outline.",
    trustBoundaryNotes: [
      "The outline is planning-level topology, not a permit-ready electrical drawing.",
      "Field verification and professional review remain required for final electrical decisions.",
    ],
  },
  {
    id: "known-home-facts",
    productName: "Known Home Facts",
    homeownerLabel: "Known home facts",
    contractorLabel: "Recorded site facts",
    section: "home",
    cardName: "Known Home Facts",
    priority: 30,
    visibleInV1: true,
    dataType: "durable_record",
    sourceCapability: "capability-home-facts",
    homeownerQuestionAnswered: "Which facts are known versus still missing?",
    emptyStateMessage: "Add home, utility, panel, load, and site details to build the fact base.",
    trustBoundaryNotes: [
      "Known facts must stay distinguishable from assumptions and placeholders.",
      "Missing data should be shown plainly instead of inferred.",
    ],
  },
  {
    id: "energy-passport",
    productName: "Energy Passport",
    homeownerLabel: "Energy Passport",
    contractorLabel: "Homeowner-safe system summary",
    section: "home",
    cardName: "Energy Passport",
    priority: 40,
    visibleInV1: false,
    dataType: "derived_view",
    sourceCapability: "capability-energy-passport",
    homeownerQuestionAnswered: "What system summary can I safely review or share later?",
    emptyStateMessage: "Energy Passport becomes useful after system, ownership, and document context are available.",
    trustBoundaryNotes: [
      "Energy Passport is non-authoritative planning summary, not title, legal, warranty, permit, or financial validation.",
      "Future sharing must depend on approved permission and view contracts.",
    ],
  },
  {
    id: "readiness-snapshot",
    productName: "Readiness Snapshot",
    homeownerLabel: "Readiness snapshot",
    contractorLabel: "Planning readiness context",
    section: "home",
    cardName: "Readiness Snapshot",
    priority: 50,
    visibleInV1: true,
    dataType: "derived_view",
    sourceCapability: "capability-readiness",
    homeownerQuestionAnswered: "What is ready to review, and what still needs confirmation?",
    emptyStateMessage: "Readiness improves when service, panel, load, equipment, and goal details are recorded.",
    trustBoundaryNotes: [
      "Readiness is not approval, eligibility, field verification, or engineering review.",
      "Blockers and missing inputs must remain visible.",
    ],
  },
  {
    id: "scenarios",
    productName: "Scenarios",
    homeownerLabel: "Upgrade paths",
    contractorLabel: "Scenario planning",
    section: "planner",
    cardName: "Upgrade Paths",
    priority: 10,
    visibleInV1: true,
    dataType: "workflow",
    sourceCapability: "capability-scenario-builder",
    homeownerQuestionAnswered: "Which upgrade paths should I compare at a planning level?",
    emptyStateMessage: "Create at least one planning path to compare future upgrade options.",
    trustBoundaryNotes: [
      "Scenario comparison is planning context, not final design selection.",
      "Do not rank or choose a best option unless that product behavior is explicitly approved.",
    ],
  },
  {
    id: "compatibility",
    productName: "Compatibility",
    homeownerLabel: "Compatibility",
    contractorLabel: "Compatibility review",
    section: "planner",
    cardName: "Compatibility",
    priority: 20,
    visibleInV1: true,
    dataType: "derived_view",
    sourceCapability: "capability-compatibility",
    homeownerQuestionAnswered: "Which planning paths look compatible or need review?",
    emptyStateMessage: "Compatibility needs a design path, equipment context, and known home constraints.",
    trustBoundaryNotes: [
      "Compatibility is planning guidance, not final equipment approval or code compliance.",
      "Contractor and professional review boundaries must stay visible.",
    ],
  },
  {
    id: "constraints",
    productName: "Constraints",
    homeownerLabel: "Planning constraints",
    contractorLabel: "Constraint and risk context",
    section: "planner",
    cardName: "Planning Constraints",
    priority: 30,
    visibleInV1: false,
    dataType: "derived_view",
    sourceCapability: "capability-planning-intelligence",
    homeownerQuestionAnswered: "What constraints could affect a future plan?",
    emptyStateMessage: "Constraints become clearer after topology, equipment, load, and site context are recorded.",
    trustBoundaryNotes: [
      "Constraints explain planning risk; they do not issue directives or final decisions.",
      "Professional-review needs must remain explicit.",
    ],
  },
  {
    id: "product-preferences",
    productName: "Product Preferences",
    homeownerLabel: "Product preferences",
    contractorLabel: "Product preference and install logic",
    section: "planner",
    cardName: "Product Preferences",
    priority: 40,
    visibleInV1: false,
    dataType: "derived_view",
    sourceCapability: "capability-product-preferences",
    homeownerQuestionAnswered: "What product or install preferences need review before selection?",
    emptyStateMessage: "Product preference mapping needs equipment type, install path, and contractor-review context.",
    trustBoundaryNotes: [
      "Product preferences are not product recommendations, rankings, procurement, pricing, or compatibility guarantees.",
      "Product/spec data must carry provenance before being treated as factual.",
    ],
  },
  {
    id: "planning-intelligence",
    productName: "Planning Intelligence",
    homeownerLabel: "Planning intelligence",
    contractorLabel: "Planning intelligence context",
    section: "planner",
    cardName: "Planning Intelligence",
    priority: 50,
    visibleInV1: false,
    dataType: "derived_view",
    sourceCapability: "capability-planning-intelligence",
    homeownerQuestionAnswered: "What planning context can the system explain without making final recommendations?",
    emptyStateMessage: "Planning intelligence needs structured goals, topology, equipment, and provenance context.",
    trustBoundaryNotes: [
      "AI may explain grounded context but must not invent facts.",
      "Generated explanation must remain subordinate to structured records.",
    ],
  },
  {
    id: "proposal-options",
    productName: "Proposal Options",
    homeownerLabel: "Proposal options",
    contractorLabel: "Proposal option readiness",
    section: "build",
    cardName: "Proposal Options",
    priority: 10,
    visibleInV1: false,
    dataType: "derived_view",
    sourceCapability: "capability-proposal-options",
    homeownerQuestionAnswered: "Which proposal option candidates may be organized later?",
    emptyStateMessage: "Proposal options remain unavailable until estimate readiness and scenario context are sufficient.",
    trustBoundaryNotes: [
      "Proposal options are readiness metadata, not final proposals, prices, quotes, or bids.",
      "Do not imply contractor approval or final design readiness.",
    ],
  },
  {
    id: "contractor-context",
    productName: "Contractor Context",
    homeownerLabel: "Contractor review context",
    contractorLabel: "Contractor context",
    section: "build",
    cardName: "Contractor Context",
    priority: 20,
    visibleInV1: false,
    dataType: "derived_view",
    sourceCapability: "capability-contractor-context",
    homeownerQuestionAnswered: "What should a contractor review before the plan can move forward?",
    emptyStateMessage: "Contractor context needs enough site, equipment, and confirmation-gate information to be useful.",
    trustBoundaryNotes: [
      "Contractor context is not contractor-owned persisted workflow state.",
      "It must not imply authorization, assignment, acceptance, or completion tracking.",
    ],
  },
  {
    id: "estimate-readiness",
    productName: "Estimate Readiness",
    homeownerLabel: "Estimate readiness",
    contractorLabel: "Estimate readiness gates",
    section: "build",
    cardName: "Estimate Readiness",
    priority: 30,
    visibleInV1: false,
    dataType: "derived_view",
    sourceCapability: "capability-estimate-readiness",
    homeownerQuestionAnswered: "What is blocking a planning estimate or proposal prep?",
    emptyStateMessage: "Estimate readiness needs scenarios, topology, confirmation gates, and contractor-review context.",
    trustBoundaryNotes: [
      "Estimate readiness is not an estimate, bid, quote, final bill of materials, or pricing claim.",
      "Readiness gates are metadata and must not imply field confirmation.",
    ],
  },
  {
    id: "install-path",
    productName: "Install Path",
    homeownerLabel: "Install path",
    contractorLabel: "Install path and topology takeoff",
    section: "build",
    cardName: "Install Path",
    priority: 40,
    visibleInV1: false,
    dataType: "derived_view",
    sourceCapability: "capability-install-path",
    homeownerQuestionAnswered: "What install path questions need field review?",
    emptyStateMessage: "Install path mapping needs topology, equipment, and pathway information.",
    trustBoundaryNotes: [
      "Install path is planning-grade and not permit-ready electrical design.",
      "Wire, conduit, breaker, disconnect, AHJ, utility, and field-verification conclusions remain out of scope.",
    ],
  },
  {
    id: "program-intelligence",
    productName: "Program Intelligence",
    homeownerLabel: "Program readiness",
    contractorLabel: "Program and grid-edge readiness",
    section: "build",
    cardName: "Program Intelligence",
    priority: 50,
    visibleInV1: false,
    dataType: "derived_view",
    sourceCapability: "capability-program-intelligence",
    homeownerQuestionAnswered: "What utility or program context still needs confirmation?",
    emptyStateMessage: "Program intelligence needs utility, rate-plan, interconnection, equipment, and jurisdiction context.",
    trustBoundaryNotes: [
      "Program intelligence is not eligibility, enrollment, rebate calculation, tariff optimization, utility approval, or dispatch.",
      "Utility and program context must preserve effective-date and jurisdiction uncertainty.",
    ],
  },
  {
    id: "post-install-handoff",
    productName: "Post-Install Handoff",
    homeownerLabel: "Post-install handoff",
    contractorLabel: "Post-install retention and handoff context",
    section: "build",
    cardName: "Post-Install Handoff",
    priority: 60,
    visibleInV1: false,
    dataType: "derived_view",
    sourceCapability: "capability-post-install-handoff",
    homeownerQuestionAnswered: "What follow-up context may matter after installation?",
    emptyStateMessage: "Post-install handoff needs lifecycle, installation, and follow-up context before it can be useful.",
    trustBoundaryNotes: [
      "Post-install handoff is not CRM integration, CRM write, task creation, email automation, or sales scoring.",
      "Lifecycle detections are request-time metadata unless future persistence is approved.",
    ],
  },
  {
    id: "architecture-cockpit",
    productName: "Product Architecture Cockpit",
    homeownerLabel: "Internal product map",
    contractorLabel: "Internal product map",
    section: "hidden",
    cardName: "Product Architecture Cockpit",
    priority: 10,
    visibleInV1: true,
    dataType: "internal",
    sourceCapability: "capability-architecture-cockpit",
    homeownerQuestionAnswered: "How should internal capabilities be organized into product UI sections?",
    emptyStateMessage: "No product capabilities have been mapped yet.",
    trustBoundaryNotes: [
      "This is an internal planning surface and should not be presented as homeowner product copy.",
      "Mappings are product architecture guidance, not final approval of product direction.",
    ],
  },
  {
    id: "technical-architecture-map",
    productName: "Technical Architecture Map",
    homeownerLabel: "Internal architecture map",
    contractorLabel: "Internal architecture map",
    section: "hidden",
    cardName: "Technical Architecture Map",
    priority: 20,
    visibleInV1: true,
    dataType: "internal",
    sourceCapability: "capability-architecture-cockpit",
    homeownerQuestionAnswered: "Which technical files, tests, and docs support a capability?",
    emptyStateMessage: "No technical architecture nodes are currently mapped.",
    trustBoundaryNotes: [
      "This is for internal planning and testing visibility only.",
      "Do not expose endpoint names, backend enums, or implementation labels as homeowner-facing copy.",
    ],
  },
  {
    id: "test-coverage",
    productName: "Test Coverage",
    homeownerLabel: "Internal verification map",
    contractorLabel: "Internal verification map",
    section: "hidden",
    cardName: "Test Coverage",
    priority: 30,
    visibleInV1: true,
    dataType: "internal",
    sourceCapability: "capability-architecture-cockpit",
    homeownerQuestionAnswered: "Which capabilities have visible test coverage?",
    emptyStateMessage: "No test coverage mapping is currently available.",
    trustBoundaryNotes: [
      "Passing tests are verification evidence, not product or compliance approval.",
      "Test gaps should remain visible in internal planning surfaces.",
    ],
  },
]);

export function getSectionItems(section) {
  return uiRegistry.filter((item) => item.section === section).sort(bySectionAndPriority);
}

export function getVisibleSectionItems(section) {
  return getSectionItems(section).filter((item) => item.visibleInV1);
}

export function getV1Items() {
  return uiRegistry.filter((item) => item.visibleInV1).sort(bySectionAndPriority);
}

export function getItemById(id) {
  return uiRegistry.find((item) => item.id === id) || null;
}

export function validateUiRegistryAlignment({
  registry = uiRegistry,
  architectureCapabilityIds = architectureProductCapabilityIds,
  allowedFutureCapabilityIds = allowedFutureSourceCapabilityIds,
} = {}) {
  const architectureCapabilityIdSet = new Set(architectureCapabilityIds);
  const allowedFutureCapabilityIdSet = new Set(allowedFutureCapabilityIds);
  const registrySourceCapabilityIds = new Set(
    registry.map((item) => item.sourceCapability).filter(Boolean)
  );

  const registryItemsWithoutSourceCapability = registry
    .filter((item) => !item.sourceCapability)
    .map((item) => item.id);
  const missingSourceCapabilityReferences = registry
    .filter(
      (item) =>
        item.sourceCapability &&
        !architectureCapabilityIdSet.has(item.sourceCapability) &&
        !allowedFutureCapabilityIdSet.has(item.sourceCapability)
    )
    .map((item) => ({ id: item.id, sourceCapability: item.sourceCapability }));
  const allowedFutureSourceCapabilityReferences = registry
    .filter((item) => item.sourceCapability && allowedFutureCapabilityIdSet.has(item.sourceCapability))
    .map((item) => ({ id: item.id, sourceCapability: item.sourceCapability }));
  const architectureProductCapabilitiesNotRepresented = architectureCapabilityIds.filter(
    (capabilityId) => !registrySourceCapabilityIds.has(capabilityId)
  );

  return {
    aligned:
      registryItemsWithoutSourceCapability.length === 0 &&
      missingSourceCapabilityReferences.length === 0 &&
      architectureProductCapabilitiesNotRepresented.length === 0,
    registryItemCount: registry.length,
    architectureCapabilityCount: architectureCapabilityIds.length,
    registryItemsWithoutSourceCapability,
    missingSourceCapabilityReferences,
    allowedFutureSourceCapabilityReferences,
    architectureProductCapabilitiesNotRepresented,
  };
}
