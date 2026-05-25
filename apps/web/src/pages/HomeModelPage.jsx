import { useEffect, useMemo, useState } from "react";

import { EmptyState, ErrorState, LoadingState } from "../components/AsyncState";
import { Badge } from "../components/Badge";
import { MetricRow } from "../components/MetricRow";
import { PageSection } from "../components/PageSection";
import { TrustBadge } from "../components/TrustBadge";
import { FormActions } from "../components/form/FormActions";
import { FormStatus } from "../components/form/FormStatus";
import { NumberInput, SelectInput, TextAreaInput, TextInput } from "../components/form/Inputs";
import { api } from "../lib/api";
import { createId } from "../lib/ids";
import { getLoadTrustStates, getPathwayTrustStates } from "../lib/trust";
import { useApiMutation } from "../lib/useApiMutation";
import { useApiQuery } from "../lib/useApiQuery";

const structureOptions = [
  { value: "main_house", label: "Main House" },
  { value: "detached_garage", label: "Detached Garage" },
  { value: "workshop", label: "Workshop" },
  { value: "ADU", label: "ADU" },
  { value: "barn", label: "Barn" },
  { value: "other", label: "Other" },
];

const panelTypeOptions = [
  { value: "main_service_panel", label: "Main Service Panel" },
  { value: "subpanel", label: "Subpanel" },
  { value: "critical_load_panel", label: "Critical Load Panel" },
  { value: "smart_panel", label: "Smart Panel" },
  { value: "solar_ready_panel", label: "Solar-Ready Panel" },
];

const indoorOutdoorOptions = [
  { value: "indoor", label: "Indoor" },
  { value: "outdoor", label: "Outdoor" },
];

const backupPriorityOptions = [
  { value: "essential", label: "Essential" },
  { value: "preferred", label: "Preferred" },
  { value: "optional", label: "Optional" },
  { value: "non_backup", label: "Non-Backup" },
];

const phaseTypeOptions = [
  { value: "single_phase", label: "Single Phase" },
  { value: "split_phase", label: "Split Phase" },
  { value: "three_phase", label: "Three Phase" },
];

const locationTypeOptions = [
  { value: "roof", label: "Roof Array" },
  { value: "garage_wall", label: "Garage Wall" },
  { value: "exterior_wall", label: "Exterior Wall" },
  { value: "utility_area", label: "Utility Area / MSP / Meter" },
  { value: "battery_area", label: "Battery Area" },
  { value: "generator_pad", label: "Generator Pad" },
  { value: "trench_route", label: "Trench Route" },
  { value: "attic", label: "Attic" },
  { value: "crawlspace", label: "Crawlspace" },
  { value: "other", label: "Other" },
];

const priorityTone = {
  essential: "danger",
  preferred: "info",
  optional: "warning",
  non_backup: "default",
};

const pathwayDifficultyOptions = [
  { value: "low", label: "Low" },
  { value: "moderate", label: "Moderate" },
  { value: "high", label: "High" },
];

const pathwayVisibilityOptions = [
  { value: "low", label: "Low visibility" },
  { value: "medium", label: "Potential visible infrastructure" },
  { value: "high", label: "High visibility" },
];

const pathwayConfidenceOptions = [
  { value: "low", label: "Site assessment recommended" },
  { value: "medium", label: "Estimate confidence: medium" },
  { value: "high", label: "Estimate confidence: high" },
];

const pathwayTypeOptions = [
  { value: "attic_drop", label: "Attic Drop" },
  { value: "wall_run", label: "Wall Run" },
  { value: "surface_conduit", label: "Surface Conduit" },
  { value: "trench_route", label: "Trench Route" },
  { value: "mixed", label: "Mixed Route" },
];

function parseOptionalNumber(value) {
  if (value === "" || value == null) {
    return null;
  }

  return Number(value);
}

function renderProvenanceValue(values, emptyLabel = "No structured provenance yet") {
  return values?.length ? values.join(", ") : emptyLabel;
}

function ProvenanceSummaryPanel({ summary, emptyLabel }) {
  const hasSummary =
    summary &&
    (
      summary.source_document_ids?.length ||
      summary.source_types?.length ||
      summary.trust_states?.length ||
      summary.confidence_levels?.length ||
      summary.unverified_fields?.length ||
      summary.notes?.length
    );

  if (!hasSummary) {
    return <p className="callout-copy">{emptyLabel}</p>;
  }

  return (
    <div className="metric-stack">
      <MetricRow label="Source documents" value={summary.source_document_ids?.length ?? 0} />
      <MetricRow label="Source types" value={renderProvenanceValue(summary.source_types)} />
      <MetricRow label="Confidence" value={renderProvenanceValue(summary.confidence_levels)} />
      <MetricRow label="Unverified fields" value={renderProvenanceValue(summary.unverified_fields, "None listed")} />
      <p className="callout-copy">
        {summary.notes?.length ? summary.notes.join(" | ") : "Lineage exists, but no additional notes were recorded."}
      </p>
    </div>
  );
}

function buildHomeState(home) {
  return {
    name: home?.name || "",
    address_line_1: home?.address_line_1 || "",
    address_line_2: home?.address_line_2 || "",
    city: home?.city || "",
    state: home?.state || "",
    postal_code: home?.postal_code || "",
    country: home?.country || "US",
    utility_provider: home?.utility_provider || "",
    service_size: home?.service_size ?? "",
    notes: home?.notes || "",
  };
}

function buildBuildingState(homeId, building) {
  return {
    home_id: homeId,
    name: building?.name || "",
    type: building?.type || "main_house",
    approximate_distance_from_main_service: building?.approximate_distance_from_main_service ?? "",
    notes: building?.notes || "",
  };
}

function buildPanelState(homeId, buildingId, panel) {
  return {
    home_id: homeId,
    building_id: panel?.building_id || buildingId || "",
    panel_type: panel?.panel_type || "main_service_panel",
    amperage: panel?.amperage ?? "",
    busbar_rating: panel?.busbar_rating ?? "",
    breaker_spaces_total: panel?.breaker_spaces_total ?? "",
    breaker_spaces_available: panel?.breaker_spaces_available ?? "",
    indoor_outdoor: panel?.indoor_outdoor || "indoor",
    notes: panel?.notes || "",
  };
}

function buildLoadState(homeId, buildingId, load) {
  return {
    home_id: homeId,
    building_id: load?.building_id || buildingId || "",
    name: load?.name || "",
    category: load?.category || "",
    running_watts: load?.running_watts ?? "",
    surge_watts: load?.surge_watts ?? "",
    estimated_daily_hours: load?.estimated_daily_hours ?? "",
    backup_priority: load?.backup_priority || "essential",
    phase_type: load?.phase_type || "split_phase",
    notes: load?.notes || "",
  };
}

function buildLocationState(homeId, buildingId, location) {
  return {
    home_id: homeId,
    building_id: location?.building_id || buildingId || "",
    name: location?.name || "",
    location_type: location?.location_type || "roof",
    approximate_coordinates: location?.approximate_coordinates || "",
    notes: location?.notes || "",
  };
}

function buildPathwayState(homeId, designId, pathway) {
  return {
    home_id: homeId,
    design_id: pathway?.design_id || designId || "",
    source_location: pathway?.source_location || "",
    destination_location: pathway?.destination_location || "",
    estimated_distance_ft: pathway?.estimated_distance_ft ?? "",
    route_type: pathway?.route_type || "attic_drop",
    route_difficulty: pathway?.route_difficulty || "moderate",
    visibility_level: pathway?.visibility_level || "medium",
    confidence_level: pathway?.confidence_level || "medium",
    notes: pathway?.notes || "",
  };
}

function HomeOverviewEditor({ home, onSaved }) {
  const [formState, setFormState] = useState(buildHomeState(home));
  const mutation = useApiMutation();

  useEffect(() => {
    setFormState(buildHomeState(home));
  }, [home]);

  async function handleSubmit(event) {
    event.preventDefault();
    await mutation.run(() =>
      api.updateHome(home.id, {
        ...formState,
        service_size: parseOptionalNumber(formState.service_size),
      })
    );
    onSaved();
  }

  return (
    <form className="panel form-panel" onSubmit={handleSubmit}>
      <div className="panel-header">
        <h3>Editable Home Overview</h3>
        <Badge tone="info">Living house model</Badge>
      </div>
      <div className="form-grid">
        <TextInput label="Home name" value={formState.name} onChange={(event) => setFormState((current) => ({ ...current, name: event.target.value }))} />
        <TextInput label="Utility provider placeholder" value={formState.utility_provider} onChange={(event) => setFormState((current) => ({ ...current, utility_provider: event.target.value }))} />
        <TextInput label="Address line 1" value={formState.address_line_1} onChange={(event) => setFormState((current) => ({ ...current, address_line_1: event.target.value }))} />
        <TextInput label="Address line 2" value={formState.address_line_2} onChange={(event) => setFormState((current) => ({ ...current, address_line_2: event.target.value }))} />
        <TextInput label="City" value={formState.city} onChange={(event) => setFormState((current) => ({ ...current, city: event.target.value }))} />
        <TextInput label="State" value={formState.state} onChange={(event) => setFormState((current) => ({ ...current, state: event.target.value }))} />
        <TextInput label="Postal code" value={formState.postal_code} onChange={(event) => setFormState((current) => ({ ...current, postal_code: event.target.value }))} />
        <TextInput label="Country" value={formState.country} onChange={(event) => setFormState((current) => ({ ...current, country: event.target.value }))} />
        <NumberInput label="Service size (A)" value={formState.service_size} onChange={(event) => setFormState((current) => ({ ...current, service_size: event.target.value }))} min="0" />
      </div>
      <TextAreaInput label="Notes" value={formState.notes} onChange={(event) => setFormState((current) => ({ ...current, notes: event.target.value }))} />
      <FormStatus saving={mutation.saving} error={mutation.error} />
      <FormActions saving={mutation.saving} onCancel={() => setFormState(buildHomeState(home))} />
    </form>
  );
}

function BuildingEditor({ homeId, building, onSaved, isNew = false }) {
  const [formState, setFormState] = useState(buildBuildingState(homeId, building));
  const mutation = useApiMutation();

  useEffect(() => {
    setFormState(buildBuildingState(homeId, building));
  }, [homeId, building]);

  async function handleSubmit(event) {
    event.preventDefault();
    const payload = {
      ...(isNew ? { id: createId("building") } : {}),
      ...formState,
      approximate_distance_from_main_service: parseOptionalNumber(formState.approximate_distance_from_main_service),
    };

    await mutation.run(() =>
      isNew ? api.createBuilding(payload) : api.updateBuilding(building.id, payload)
    );
    onSaved();
    if (isNew) {
      setFormState(buildBuildingState(homeId, null));
    }
  }

  return (
    <form className="panel form-panel" onSubmit={handleSubmit}>
      <div className="panel-header">
        <h3>{isNew ? "Add Structure" : formState.name || "Edit Structure"}</h3>
        {!isNew && building?.data_origin ? <Badge>{building.data_origin}</Badge> : null}
      </div>
      <div className="form-grid">
        <TextInput label="Structure name" value={formState.name} onChange={(event) => setFormState((current) => ({ ...current, name: event.target.value }))} />
        <SelectInput label="Structure type" value={formState.type} onChange={(event) => setFormState((current) => ({ ...current, type: event.target.value }))} options={structureOptions} />
        <NumberInput
          label="Approximate distance from main service (ft)"
          value={formState.approximate_distance_from_main_service}
          onChange={(event) =>
            setFormState((current) => ({
              ...current,
              approximate_distance_from_main_service: event.target.value,
            }))
          }
          min="0"
        />
      </div>
      <TextAreaInput label="Notes" value={formState.notes} onChange={(event) => setFormState((current) => ({ ...current, notes: event.target.value }))} />
      <FormStatus saving={mutation.saving} error={mutation.error} />
      <FormActions saving={mutation.saving} onCancel={() => setFormState(buildBuildingState(homeId, building))} saveLabel={isNew ? "Add Structure" : "Save Structure"} />
    </form>
  );
}

function PanelEditor({ homeId, buildings, panel, onSaved, isNew = false }) {
  const defaultBuildingId = buildings[0]?.id || "";
  const [formState, setFormState] = useState(buildPanelState(homeId, defaultBuildingId, panel));
  const mutation = useApiMutation();

  useEffect(() => {
    setFormState(buildPanelState(homeId, defaultBuildingId, panel));
  }, [homeId, defaultBuildingId, panel]);

  async function handleSubmit(event) {
    event.preventDefault();
    const payload = {
      ...(isNew ? { id: createId("panel") } : {}),
      ...formState,
      amperage: Number(formState.amperage),
      busbar_rating: parseOptionalNumber(formState.busbar_rating),
      breaker_spaces_total: Number(formState.breaker_spaces_total),
      breaker_spaces_available: Number(formState.breaker_spaces_available),
    };

    await mutation.run(() => (isNew ? api.createPanel(payload) : api.updatePanel(panel.id, payload)));
    onSaved();
    if (isNew) {
      setFormState(buildPanelState(homeId, defaultBuildingId, null));
    }
  }

  return (
    <form className="panel form-panel" onSubmit={handleSubmit}>
      <div className="panel-header">
        <h3>{isNew ? "Add Electrical Panel" : formState.panel_type.replaceAll("_", " ")}</h3>
        {!isNew && panel?.data_origin ? <Badge>{panel.data_origin}</Badge> : null}
      </div>
      <div className="form-grid">
        <SelectInput
          label="Building"
          value={formState.building_id}
          onChange={(event) => setFormState((current) => ({ ...current, building_id: event.target.value }))}
          options={buildings.map((building) => ({ value: building.id, label: building.name }))}
        />
        <SelectInput label="Panel type" value={formState.panel_type} onChange={(event) => setFormState((current) => ({ ...current, panel_type: event.target.value }))} options={panelTypeOptions} />
        <NumberInput label="Amperage" value={formState.amperage} onChange={(event) => setFormState((current) => ({ ...current, amperage: event.target.value }))} min="0" />
        <NumberInput label="Busbar rating" value={formState.busbar_rating} onChange={(event) => setFormState((current) => ({ ...current, busbar_rating: event.target.value }))} min="0" />
        <NumberInput label="Breaker spaces total" value={formState.breaker_spaces_total} onChange={(event) => setFormState((current) => ({ ...current, breaker_spaces_total: event.target.value }))} min="0" />
        <NumberInput label="Breaker spaces available" value={formState.breaker_spaces_available} onChange={(event) => setFormState((current) => ({ ...current, breaker_spaces_available: event.target.value }))} min="0" />
        <SelectInput label="Indoor / Outdoor" value={formState.indoor_outdoor} onChange={(event) => setFormState((current) => ({ ...current, indoor_outdoor: event.target.value }))} options={indoorOutdoorOptions} />
      </div>
      <TextAreaInput label="Notes" value={formState.notes} onChange={(event) => setFormState((current) => ({ ...current, notes: event.target.value }))} />
      <FormStatus saving={mutation.saving} error={mutation.error} />
      <FormActions saving={mutation.saving} onCancel={() => setFormState(buildPanelState(homeId, defaultBuildingId, panel))} saveLabel={isNew ? "Add Panel" : "Save Panel"} />
    </form>
  );
}

function LoadEditor({ homeId, buildings, load, onSaved, isNew = false }) {
  const defaultBuildingId = buildings[0]?.id || "";
  const [formState, setFormState] = useState(buildLoadState(homeId, defaultBuildingId, load));
  const mutation = useApiMutation();

  useEffect(() => {
    setFormState(buildLoadState(homeId, defaultBuildingId, load));
  }, [homeId, defaultBuildingId, load]);

  async function handleSubmit(event) {
    event.preventDefault();
    const payload = {
      ...(isNew ? { id: createId("load") } : {}),
      ...formState,
      running_watts: Number(formState.running_watts),
      surge_watts: parseOptionalNumber(formState.surge_watts),
      estimated_daily_hours: parseOptionalNumber(formState.estimated_daily_hours),
    };

    await mutation.run(() => (isNew ? api.createLoad(payload) : api.updateLoad(load.id, payload)));
    onSaved();
    if (isNew) {
      setFormState(buildLoadState(homeId, defaultBuildingId, null));
    }
  }

  return (
    <form className="panel form-panel" onSubmit={handleSubmit}>
      <div className="panel-header">
        <h3>{isNew ? "Add Manual Load" : formState.name || "Edit Load"}</h3>
        {!isNew ? (
          <div className="badge-row">
            <Badge tone={priorityTone[formState.backup_priority] || "default"}>{formState.backup_priority}</Badge>
            {getLoadTrustStates(load).map((state) => (
              <TrustBadge
                key={`${load.id}-${state}`}
                state={state}
                label={state === "placeholder" ? "Planning load" : undefined}
              />
            ))}
          </div>
        ) : null}
      </div>
      <div className="form-grid">
        <TextInput label="Load name" value={formState.name} onChange={(event) => setFormState((current) => ({ ...current, name: event.target.value }))} />
        <TextInput label="Category" value={formState.category} onChange={(event) => setFormState((current) => ({ ...current, category: event.target.value }))} />
        <SelectInput label="Assigned building" value={formState.building_id} onChange={(event) => setFormState((current) => ({ ...current, building_id: event.target.value }))} options={buildings.map((building) => ({ value: building.id, label: building.name }))} />
        <SelectInput label="Backup priority" value={formState.backup_priority} onChange={(event) => setFormState((current) => ({ ...current, backup_priority: event.target.value }))} options={backupPriorityOptions} />
        <NumberInput label="Running watts" value={formState.running_watts} onChange={(event) => setFormState((current) => ({ ...current, running_watts: event.target.value }))} min="0" />
        <NumberInput label="Surge watts" value={formState.surge_watts} onChange={(event) => setFormState((current) => ({ ...current, surge_watts: event.target.value }))} min="0" />
        <NumberInput label="Estimated daily hours" value={formState.estimated_daily_hours} onChange={(event) => setFormState((current) => ({ ...current, estimated_daily_hours: event.target.value }))} min="0" />
        <SelectInput label="Phase type" value={formState.phase_type} onChange={(event) => setFormState((current) => ({ ...current, phase_type: event.target.value }))} options={phaseTypeOptions} />
      </div>
      <TextAreaInput label="Notes" value={formState.notes} onChange={(event) => setFormState((current) => ({ ...current, notes: event.target.value }))} />
      {!isNew ? (
        <ProvenanceSummaryPanel
          summary={load?.provenance_summary}
          emptyLabel="No structured provenance is linked to this load yet. Treat wattage and runtime assumptions as planning inputs."
        />
      ) : null}
      <FormStatus saving={mutation.saving} error={mutation.error} />
      <FormActions saving={mutation.saving} onCancel={() => setFormState(buildLoadState(homeId, defaultBuildingId, load))} saveLabel={isNew ? "Add Load" : "Save Load"} />
    </form>
  );
}

function EquipmentLocationEditor({ homeId, buildings, location, onSaved, isNew = false }) {
  const defaultBuildingId = buildings[0]?.id || "";
  const [formState, setFormState] = useState(buildLocationState(homeId, defaultBuildingId, location));
  const mutation = useApiMutation();

  useEffect(() => {
    setFormState(buildLocationState(homeId, defaultBuildingId, location));
  }, [homeId, defaultBuildingId, location]);

  async function handleSubmit(event) {
    event.preventDefault();
    const payload = {
      ...(isNew ? { id: createId("location") } : {}),
      ...formState,
    };
    await mutation.run(() =>
      isNew ? api.createEquipmentLocation(payload) : api.updateEquipmentLocation(location.id, payload)
    );
    onSaved();
    if (isNew) {
      setFormState(buildLocationState(homeId, defaultBuildingId, null));
    }
  }

  return (
    <form className="panel form-panel" onSubmit={handleSubmit}>
      <div className="panel-header">
        <h3>{isNew ? "Add Equipment Location" : formState.name || "Edit Location"}</h3>
        {!isNew && location?.data_origin ? <Badge>{location.data_origin}</Badge> : null}
      </div>
      <div className="form-grid">
        <TextInput
          label="Location name"
          hint="Examples: Roof Array, Inverter, Battery, MSP, Backup Panel, Utility Meter, Generator, Workshop Subpanel, Trench Route"
          value={formState.name}
          onChange={(event) => setFormState((current) => ({ ...current, name: event.target.value }))}
        />
        <SelectInput label="General location type" value={formState.location_type} onChange={(event) => setFormState((current) => ({ ...current, location_type: event.target.value }))} options={locationTypeOptions} />
        <SelectInput label="Building" value={formState.building_id} onChange={(event) => setFormState((current) => ({ ...current, building_id: event.target.value }))} options={buildings.map((building) => ({ value: building.id, label: building.name }))} />
        <TextInput label="Approximate coordinates / siting note" value={formState.approximate_coordinates} onChange={(event) => setFormState((current) => ({ ...current, approximate_coordinates: event.target.value }))} />
      </div>
      <TextAreaInput label="Notes" value={formState.notes} onChange={(event) => setFormState((current) => ({ ...current, notes: event.target.value }))} />
      <FormStatus saving={mutation.saving} error={mutation.error} />
      <FormActions saving={mutation.saving} onCancel={() => setFormState(buildLocationState(homeId, defaultBuildingId, location))} saveLabel={isNew ? "Add Location" : "Save Location"} />
    </form>
  );
}

function PathwayEditor({ homeId, designs, pathway, onSaved, isNew = false }) {
  const defaultDesignId = designs[0]?.id || "";
  const [formState, setFormState] = useState(buildPathwayState(homeId, defaultDesignId, pathway));
  const mutation = useApiMutation();

  useEffect(() => {
    setFormState(buildPathwayState(homeId, defaultDesignId, pathway));
  }, [homeId, defaultDesignId, pathway]);

  async function handleSubmit(event) {
    event.preventDefault();
    const derivedName = `${formState.source_location || "Source"} to ${formState.destination_location || "Destination"}`;
    const payload = {
      ...(isNew ? { id: createId("pathway") } : {}),
      ...formState,
      name: derivedName,
      description: formState.notes || "Likely installation pathway estimate.",
      lifecycle_stage: "site_assessment",
      estimated_distance_ft: parseOptionalNumber(formState.estimated_distance_ft),
      design_id: formState.design_id || null,
      upfront_cost_placeholder: pathway?.upfront_cost_placeholder ?? null,
      estimated_monthly_savings_placeholder: pathway?.estimated_monthly_savings_placeholder ?? null,
      resilience_score: pathway?.resilience_score ?? null,
    };

    await mutation.run(() =>
      isNew ? api.createEstimatedPathway(payload) : api.updateEstimatedPathway(pathway.id, payload)
    );
    onSaved();
    if (isNew) {
      setFormState(buildPathwayState(homeId, defaultDesignId, null));
    }
  }

  return (
    <form className="panel form-panel" onSubmit={handleSubmit}>
      <div className="panel-header">
        <div>
          <h3>{isNew ? "Add Estimated Pathway" : "Likely Installation Pathway"}</h3>
          <p className="callout-copy">Site assessment recommended for final routing and visibility assumptions.</p>
        </div>
        {!isNew ? (
          <div className="trust-row">
            {getPathwayTrustStates(pathway).map((state) => (
              <TrustBadge
                key={`${pathway.id}-${state}`}
                state={state}
                label={state === "placeholder" ? "Approximate pathway" : undefined}
              />
            ))}
          </div>
        ) : null}
      </div>
      <div className="form-grid">
        <SelectInput
          label="Linked design"
          hint="Optional"
          value={formState.design_id}
          onChange={(event) => setFormState((current) => ({ ...current, design_id: event.target.value }))}
          options={[{ value: "", label: "No linked design" }, ...designs.map((design) => ({ value: design.id, label: design.name }))]}
        />
        <TextInput label="Source location" hint="Likely installation pathway" value={formState.source_location} onChange={(event) => setFormState((current) => ({ ...current, source_location: event.target.value }))} />
        <TextInput label="Destination location" value={formState.destination_location} onChange={(event) => setFormState((current) => ({ ...current, destination_location: event.target.value }))} />
        <NumberInput label="Estimated distance (ft)" value={formState.estimated_distance_ft} onChange={(event) => setFormState((current) => ({ ...current, estimated_distance_ft: event.target.value }))} min="0" />
        <SelectInput label="Route type" value={formState.route_type} onChange={(event) => setFormState((current) => ({ ...current, route_type: event.target.value }))} options={pathwayTypeOptions} />
        <SelectInput label="Route difficulty" value={formState.route_difficulty} onChange={(event) => setFormState((current) => ({ ...current, route_difficulty: event.target.value }))} options={pathwayDifficultyOptions} />
        <SelectInput label="Visibility level" hint="Potential visible infrastructure" value={formState.visibility_level} onChange={(event) => setFormState((current) => ({ ...current, visibility_level: event.target.value }))} options={pathwayVisibilityOptions} />
        <SelectInput label="Confidence level" hint="Estimate confidence" value={formState.confidence_level} onChange={(event) => setFormState((current) => ({ ...current, confidence_level: event.target.value }))} options={pathwayConfidenceOptions} />
      </div>
      <TextAreaInput label="Notes" hint="Site assessment recommended." value={formState.notes} onChange={(event) => setFormState((current) => ({ ...current, notes: event.target.value }))} />
      {!isNew ? (
        <ProvenanceSummaryPanel
          summary={pathway?.provenance_summary}
          emptyLabel="No structured provenance is linked to this pathway yet. Routing, visibility, and distance should remain approximate until site verification."
        />
      ) : null}
      <FormStatus saving={mutation.saving} error={mutation.error} />
      <FormActions saving={mutation.saving} onCancel={() => setFormState(buildPathwayState(homeId, defaultDesignId, pathway))} saveLabel={isNew ? "Add Pathway" : "Save Pathway"} />
    </form>
  );
}

function LoadTemplateLibrary({ templates, homeId, buildings, onSaved }) {
  const [targetBuildingId, setTargetBuildingId] = useState(buildings[0]?.id || "");
  const mutation = useApiMutation();

  useEffect(() => {
    setTargetBuildingId(buildings[0]?.id || "");
  }, [buildings]);

  const bundleConfigs = [
    {
      key: "essential",
      title: "Essential Backup",
      filter: (template) => template.backup_priority === "essential",
    },
    {
      key: "comfort",
      title: "Comfort Backup",
      filter: (template) => template.backup_priority === "preferred" && template.category !== "hvac",
    },
    {
      key: "whole_home",
      title: "Whole Home Planning",
      filter: (template) => ["essential", "preferred"].includes(template.backup_priority),
    },
    {
      key: "optional",
      title: "Optional add-ons",
      filter: (template) => template.backup_priority === "optional",
    },
  ];

  async function addTemplate(template) {
    if (!targetBuildingId) {
      return;
    }

    await mutation.run(() =>
      api.createLoad({
        id: createId("load"),
        home_id: homeId,
        building_id: targetBuildingId,
        name: template.name,
        category: template.category,
        running_watts: template.running_watts,
        surge_watts: template.surge_watts,
        estimated_daily_hours: template.estimated_daily_hours,
        backup_priority: template.backup_priority,
        phase_type: template.phase_type,
        notes: `Added from starter template. ${template.notes || ""}`.trim(),
      })
    );
    onSaved();
  }

  async function addBundle(bundle) {
    for (const template of bundle) {
      await addTemplate(template);
    }
  }

  return (
    <div className="stack-grid">
      <div className="panel">
        <div className="panel-header">
          <h3>Load Template Workflow</h3>
          <Badge tone="warning">Starter/planning estimates only</Badge>
        </div>
        <p className="callout-copy">
          Starter/planning estimates only. Verify actual appliance ratings before design or installation.
        </p>
        <SelectInput
          label="Add templates into building"
          value={targetBuildingId}
          onChange={(event) => setTargetBuildingId(event.target.value)}
          options={buildings.map((building) => ({ value: building.id, label: building.name }))}
        />
        <FormStatus saving={mutation.saving} error={mutation.error} />
      </div>
      {bundleConfigs.map((bundleConfig) => {
        const bundleTemplates = templates.filter(bundleConfig.filter);
        return (
          <article key={bundleConfig.key} className="panel">
            <div className="panel-header">
              <h3>{bundleConfig.title}</h3>
              <button className="button button-secondary" type="button" disabled={!targetBuildingId || !bundleTemplates.length || mutation.saving} onClick={() => addBundle(bundleTemplates)}>
                Add Bundle To Home
              </button>
            </div>
            {bundleTemplates.length ? (
              <div className="list-panel">
                {bundleTemplates.map((template) => (
                  <div key={template.id} className="list-row list-row-stack">
                    <div>
                      <strong>{template.name}</strong>
                      <p>{template.category}</p>
                    </div>
                    <div className="load-meta">
                      <Badge tone={priorityTone[template.backup_priority] || "default"}>{template.backup_priority}</Badge>
                      <span>{template.running_watts} W run</span>
                      <button className="button button-secondary" type="button" disabled={!targetBuildingId || mutation.saving} onClick={() => addTemplate(template)}>
                        Add Template
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <EmptyState label="No templates in this starter group yet." />
            )}
          </article>
        );
      })}
    </div>
  );
}

export function HomeModelPage() {
  const [refreshKey, setRefreshKey] = useState(0);
  const homeQuery = useApiQuery(`home-${refreshKey}`, api.getHome);
  const loadsQuery = useApiQuery(`loads-${refreshKey}`, api.getLoads);
  const locationsQuery = useApiQuery(`locations-${refreshKey}`, api.getEquipmentLocations);
  const pathwaysQuery = useApiQuery(`pathways-${refreshKey}`, api.getEstimatedPathways);
  const loadTemplatesQuery = useApiQuery(`templates-${refreshKey}`, api.getLoadTemplates);
  const designsQuery = useApiQuery(`designs-home-${refreshKey}`, api.getDesigns);

  const isLoading =
    homeQuery.loading ||
    loadsQuery.loading ||
    locationsQuery.loading ||
    pathwaysQuery.loading ||
    loadTemplatesQuery.loading ||
    designsQuery.loading;
  const error =
    homeQuery.error ||
    loadsQuery.error ||
    locationsQuery.error ||
    pathwaysQuery.error ||
    loadTemplatesQuery.error ||
    designsQuery.error;

  const home = homeQuery.data;
  const buildings = home?.buildings || [];
  const panels = home?.panels || [];
  const loads = loadsQuery.data || [];
  const locations = locationsQuery.data || [];
  const pathways = pathwaysQuery.data || [];
  const loadTemplates = loadTemplatesQuery.data || [];
  const designs = designsQuery.data || [];

  const groupedLoads = useMemo(
    () =>
      ["essential", "preferred", "optional", "non_backup"].map((priority) => ({
        priority,
        loads: loads.filter((load) => load.backup_priority === priority),
      })),
    [loads]
  );

  function refetchAll() {
    setRefreshKey((current) => current + 1);
  }

  return (
    <>
      <PageSection
        title="Property Model"
        description="Persistent house data should outlive any one design iteration."
      >
        {isLoading ? <LoadingState label="Loading property model..." /> : null}
        {error ? <ErrorState error={error} label="Unable to load property model." /> : null}
        {!isLoading && !error && home ? (
          <div className="card-grid">
            <article className="panel">
              <div className="panel-header">
                <h3>{home.name}</h3>
                <div className="trust-row">
                  <TrustBadge state={home.data_origin || "user_created"} />
                  <TrustBadge state="placeholder" label="Planning record" />
                </div>
              </div>
              <MetricRow label="Address" value={`${home.address_line_1}, ${home.city}, ${home.state} ${home.postal_code}`} />
              <MetricRow label="Utility provider" value={home.utility_provider || "Placeholder"} />
              <MetricRow label="Service size" value={home.service_size ? `${home.service_size}A` : "Unknown"} />
              <p>{home.notes || "No notes yet."}</p>
            </article>
            <article className="panel">
              <div className="panel-header">
                <h3>Planning scope</h3>
                <div className="trust-row">
                  <Badge tone="warning">Editable planning prototype</Badge>
                  <TrustBadge state="placeholder" label="Site verification still required" />
                </div>
              </div>
              <MetricRow label="Structures" value={String(buildings.length)} />
              <MetricRow label="Panels" value={String(panels.length)} />
              <MetricRow label="Loads" value={String(loads.length)} />
              <MetricRow label="Equipment locations" value={String(locations.length)} />
            </article>
          </div>
        ) : null}
      </PageSection>

      {!isLoading && !error && home ? (
        <>
          <PageSection
            title="Trust Visibility"
            description="Known facts, user-entered assumptions, and approximate pathway planning remain intentionally distinct in the property model."
          >
            <div className="card-grid">
              <article className="panel">
                <h3>What is known</h3>
                <p>Saved structures, panels, loads, locations, and pathways persist across sessions, but many records still contain planning assumptions.</p>
                <div className="trust-row">
                  <TrustBadge state="user_created" />
                  <TrustBadge state="demo_seed" />
                </div>
              </article>
              <article className="panel">
                <h3>What remains approximate</h3>
                <p>Pathways, some loads, and future routing assumptions are still planning-only and should be validated on site.</p>
                <div className="trust-row">
                  <TrustBadge state="placeholder" label="Approximate planning data" />
                </div>
              </article>
            </div>
          </PageSection>

          <PageSection title="Editable Home Overview" description="Core property fields now save to the persistent home profile.">
            <HomeOverviewEditor home={home} onSaved={refetchAll} />
          </PageSection>

          <PageSection title="Structures" description="Add and update structures that affect service distance, load planning, and future expansion.">
            <div className="stack-grid">
              {buildings.map((building) => (
                <BuildingEditor key={building.id} homeId={home.id} building={building} onSaved={refetchAll} />
              ))}
              <BuildingEditor homeId={home.id} onSaved={refetchAll} isNew />
            </div>
          </PageSection>

          <PageSection title="Electrical Panels" description="Capture service and backup distribution context directly in the persistent home model.">
            <div className="stack-grid">
              {panels.map((panel) => (
                <PanelEditor key={panel.id} homeId={home.id} buildings={buildings} panel={panel} onSaved={refetchAll} />
              ))}
              {buildings.length ? <PanelEditor homeId={home.id} buildings={buildings} onSaved={refetchAll} isNew /> : <EmptyState label="Add at least one structure before adding panels." />}
            </div>
          </PageSection>

          <PageSection title="Load Template Workflow" description="Start from reusable planning templates, then edit the resulting loads against the real property.">
            {buildings.length ? (
              <LoadTemplateLibrary templates={loadTemplates} homeId={home.id} buildings={buildings} onSaved={refetchAll} />
            ) : (
              <EmptyState label="Add a structure first so template loads can be assigned into the home profile." />
            )}
          </PageSection>

          <PageSection title="Loads" description="Starter/planning estimates only. Verify actual appliance ratings before design or installation.">
            <div className="stack-grid">
              {buildings.length ? <LoadEditor homeId={home.id} buildings={buildings} onSaved={refetchAll} isNew /> : null}
              {groupedLoads.map((group) => (
                <div key={group.priority} className="stack-grid">
                  <div className="panel-header">
                    <h3>{group.priority.replace("_", " ")}</h3>
                    <Badge tone={priorityTone[group.priority] || "default"}>{group.loads.length} loads</Badge>
                  </div>
                  {group.loads.length ? (
                    group.loads.map((load) => (
                      <LoadEditor key={load.id} homeId={home.id} buildings={buildings} load={load} onSaved={refetchAll} />
                    ))
                  ) : (
                    <EmptyState label={`No ${group.priority.replace("_", " ")} loads yet.`} />
                  )}
                </div>
              ))}
            </div>
          </PageSection>

          <PageSection title="Equipment Locations" description="Approximate siting records help the house model preserve where major infrastructure may live.">
            <div className="stack-grid">
              {locations.map((location) => (
                <EquipmentLocationEditor key={location.id} homeId={home.id} buildings={buildings} location={location} onSaved={refetchAll} />
              ))}
              {buildings.length ? <EquipmentLocationEditor homeId={home.id} buildings={buildings} onSaved={refetchAll} isNew /> : <EmptyState label="Add a structure before adding equipment locations." />}
            </div>
          </PageSection>

          <PageSection title="Estimated Pathways" description="Capture likely installation pathways and visible infrastructure assumptions as editable planning records.">
            <div className="stack-grid">
              {pathways.map((pathway) => (
                <PathwayEditor key={pathway.id} homeId={home.id} designs={designs} pathway={pathway} onSaved={refetchAll} />
              ))}
              <PathwayEditor homeId={home.id} designs={designs} onSaved={refetchAll} isNew />
            </div>
          </PageSection>
        </>
      ) : null}

      {!isLoading && !error && !home ? <EmptyState label="No home data found." /> : null}
    </>
  );
}
