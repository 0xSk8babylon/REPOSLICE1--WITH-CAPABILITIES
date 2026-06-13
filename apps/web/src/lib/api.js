const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
const API_PREFIX = "/api";

async function request(path, options = {}) {
  const { method = "GET", body } = options;
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers: body ? { "Content-Type": "application/json" } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    let detail = response.statusText;

    try {
      const payload = await response.json();
      detail = payload.detail || JSON.stringify(payload);
    } catch (error) {
      detail = response.statusText || "Unknown API error";
    }

    throw new Error(`${response.status} ${detail}`);
  }

  return response.json();
}

function apiPath(path) {
  return `${API_PREFIX}${path}`;
}

export const api = {
  baseUrl: API_BASE_URL,
  getHome: () => request(apiPath("/homes")),
  getAllHomes: () => request(apiPath("/homes/all")),
  createHome: (payload) => request(apiPath("/homes"), { method: "POST", body: payload }),
  updateHome: (homeId, payload) => request(apiPath(`/homes/${homeId}`), { method: "PATCH", body: payload }),

  getBuildings: () => request(apiPath("/buildings")),
  createBuilding: (payload) => request(apiPath("/buildings"), { method: "POST", body: payload }),
  updateBuilding: (buildingId, payload) =>
    request(apiPath(`/buildings/${buildingId}`), { method: "PATCH", body: payload }),

  getPanels: () => request(apiPath("/panels")),
  createPanel: (payload) => request(apiPath("/panels"), { method: "POST", body: payload }),
  updatePanel: (panelId, payload) => request(apiPath(`/panels/${panelId}`), { method: "PATCH", body: payload }),

  getLoads: () => request(apiPath("/loads")),
  getLoadSummary: () => request(apiPath("/loads/summary")),
  createLoad: (payload) => request(apiPath("/loads"), { method: "POST", body: payload }),
  updateLoad: (loadId, payload) => request(apiPath(`/loads/${loadId}`), { method: "PATCH", body: payload }),

  getLoadTemplates: () => request(apiPath("/load-templates")),

  getDesigns: () => request(apiPath("/designs")),
  createDesign: (payload) => request(apiPath("/designs"), { method: "POST", body: payload }),
  updateDesign: (designId, payload) =>
    request(apiPath(`/designs/${designId}`), { method: "PATCH", body: payload }),
  getDesignEquipment: (designId) => request(apiPath(`/designs/${designId}/equipment`)),
  createDesignEquipment: (designId, payload) =>
    request(apiPath(`/designs/${designId}/equipment`), { method: "POST", body: payload }),
  updateDesignEquipment: (designId, equipmentId, payload) =>
    request(apiPath(`/designs/${designId}/equipment/${equipmentId}`), { method: "PATCH", body: payload }),
  deleteDesignEquipment: (designId, equipmentId) =>
    fetch(`${API_BASE_URL}${apiPath(`/designs/${designId}/equipment/${equipmentId}`)}`, {
      method: "DELETE",
    }).then(async (response) => {
      if (!response.ok) {
        let detail = response.statusText;

        try {
          const payload = await response.json();
          detail = payload.detail || JSON.stringify(payload);
        } catch (error) {
          detail = response.statusText || "Unknown API error";
        }

        throw new Error(`${response.status} ${detail}`);
      }

      return null;
    }),

  getProductLibrary: () => request(apiPath("/product-library")),
  getSourceDocuments: () => request(apiPath("/source-documents")),
  getProvenance: (params = "") => request(apiPath(`/provenance${params}`)),
  getRuleProvenance: () => request(apiPath("/rule-provenance")),
  getCompatibilityIssues: () => request(apiPath("/compatibility-rules/issues")),
  evaluateDesign: (designId) => request(apiPath(`/compatibility-rules/evaluate/${designId}`)),

  getScenarios: () => request(apiPath("/scenarios")),
  compareScenarios: () => request(apiPath("/scenarios/compare")),
  createScenario: (payload) => request(apiPath("/scenarios"), { method: "POST", body: payload }),
  updateScenario: (scenarioId, payload) =>
    request(apiPath(`/scenarios/${scenarioId}`), { method: "PATCH", body: payload }),

  getEquipmentLocations: () => request(apiPath("/equipment/locations")),
  createEquipmentLocation: (payload) =>
    request(apiPath("/equipment/locations"), { method: "POST", body: payload }),
  updateEquipmentLocation: (locationId, payload) =>
    request(apiPath(`/equipment/locations/${locationId}`), { method: "PATCH", body: payload }),

  getEstimatedPathways: () => request(apiPath("/estimated-pathways")),
  createEstimatedPathway: (payload) =>
    request(apiPath("/estimated-pathways"), { method: "POST", body: payload }),
  updateEstimatedPathway: (pathwayId, payload) =>
    request(apiPath(`/estimated-pathways/${pathwayId}`), { method: "PATCH", body: payload }),

  getTakeoff: () => request(apiPath("/takeoffs/current")),
  generateTakeoff: (designId) => request(apiPath(`/takeoffs/generate/${designId}`)),
  getDesignAdvisor: (designId) => request(apiPath(`/design-advisor/summary/${designId}`)),
  getAIContext: (designId) => request(apiPath(`/ai-context/design/${designId}`)),
  getEstimatePlaceholder: () => request(apiPath("/estimates/placeholder")),
  getArchitectureVisibility: () => request(apiPath("/system-visibility/architecture")),
};
