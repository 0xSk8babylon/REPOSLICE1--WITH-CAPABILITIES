export const designStatusExplanations = {
  draft: "Draft = early exploration with major planning gaps still expected.",
  exploratory: "Exploratory = concept-level planning with broad assumptions still in play.",
  concept: "Concept = legacy exploratory status retained for older seed data.",
  homeowner_reviewed: "Homeowner Reviewed = priorities and tradeoffs have been reviewed by the homeowner.",
  contractor_reviewed: "Contractor Reviewed = a contractor has reviewed the concept, but field validation may still be needed.",
  estimate_ready: "Estimate Ready = enough information exists for rough estimating, not permit-grade engineering.",
  installation_planning: "Installation Planning = preparing for implementation and site validation.",
  archived: "Archived = retained for comparison, not an active planning path.",
};

const trustStateConfig = {
  demo_seed: { tone: "warning", label: "Demo data" },
  user_created: { tone: "info", label: "User-entered" },
  imported: { tone: "info", label: "Imported" },
  verified: { tone: "success", label: "Verified manufacturer data" },
  derived_estimate: { tone: "warning", label: "Derived estimate" },
  placeholder: { tone: "warning", label: "Placeholder" },
  missing: { tone: "danger", label: "Missing info" },
};

export function getTrustConfig(state) {
  return trustStateConfig[state] || { tone: "default", label: state || "Unknown" };
}

function uniqueStates(states) {
  return Array.from(new Set(states.filter(Boolean)));
}

function containsPlaceholderContent(record) {
  const serialized = JSON.stringify(record || {}).toLowerCase();
  return serialized.includes("placeholder");
}

export function getProductTrustStates(product) {
  return uniqueStates([product?.data_origin, containsPlaceholderContent(product) ? "placeholder" : null]);
}

export function getLoadTrustStates(load) {
  return uniqueStates([load?.data_origin, containsPlaceholderContent(load) ? "placeholder" : null]);
}

export function getPathwayTrustStates(pathway) {
  return uniqueStates([pathway?.data_origin, "placeholder"]);
}

export function getScenarioTrustStates(scenario) {
  return uniqueStates([
    scenario?.data_origin,
    scenario?.upfront_cost_placeholder != null ||
    scenario?.future_expansion_score != null ||
    scenario?.install_complexity_score != null ||
    scenario?.backup_capability_score != null
      ? "placeholder"
      : null,
  ]);
}

export function getTakeoffTrustStates(item) {
  return uniqueStates([
    item?.data_origin,
    item?.unit_cost_placeholder != null || item?.total_cost_placeholder != null ? "placeholder" : null,
    item?.missing_information?.length ? "missing" : null,
  ]);
}

export function getAdvisorTrustStates(issue) {
  return uniqueStates([issue?.data_origin || "derived_estimate"]);
}

export function getDesignStatusExplanation(status) {
  return (
    designStatusExplanations[status] ||
    "Planning lifecycle status exists for collaboration and trust visibility only."
  );
}
