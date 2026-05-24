import { useEffect, useState } from "react";

import { EmptyState, ErrorState, LoadingState } from "../components/AsyncState";
import { Badge } from "../components/Badge";
import { PageSection } from "../components/PageSection";
import { TrustBadge } from "../components/TrustBadge";
import { FormActions } from "../components/form/FormActions";
import { FormStatus } from "../components/form/FormStatus";
import { NumberInput, SelectInput, TextAreaInput, TextInput } from "../components/form/Inputs";
import { api } from "../lib/api";
import { createId } from "../lib/ids";
import { getDesignStatusExplanation, getProductTrustStates } from "../lib/trust";
import { useApiMutation } from "../lib/useApiMutation";
import { useApiQuery } from "../lib/useApiQuery";

const designGoalOptions = [
  { value: "lowest_cost", label: "Lowest Cost" },
  { value: "partial_backup", label: "Partial Backup" },
  { value: "whole_home_backup", label: "Whole Home Backup" },
  { value: "expansion_ready", label: "Expansion Ready" },
  { value: "generator_assisted", label: "Generator Assisted" },
  { value: "workshop_ready", label: "Workshop Ready" },
  { value: "off_grid_capable", label: "Off Grid Capable" },
];

const architectureTypeOptions = [
  { value: "grid_tied", label: "Grid Tied" },
  { value: "hybrid", label: "Hybrid" },
  { value: "off_grid", label: "Off Grid" },
  { value: "ac_coupled", label: "AC Coupled" },
  { value: "dc_coupled", label: "DC Coupled" },
  { value: "mixed", label: "Mixed" },
];

const designStatusOptions = [
  { value: "draft", label: "Draft" },
  { value: "exploratory", label: "Exploratory" },
  { value: "homeowner_reviewed", label: "Homeowner Reviewed" },
  { value: "contractor_reviewed", label: "Contractor Reviewed" },
  { value: "estimate_ready", label: "Estimate Ready" },
  { value: "installation_planning", label: "Installation Planning" },
  { value: "archived", label: "Archived" },
  { value: "concept", label: "Concept (Legacy)" },
];

const equipmentRoleSuggestions = [
  { value: "primary_generation", label: "Primary Generation" },
  { value: "backup_storage", label: "Backup Storage" },
  { value: "system_control", label: "System Control" },
  { value: "generator_assist", label: "Generator Assist" },
  { value: "load_management", label: "Load Management" },
  { value: "transfer_control", label: "Transfer Control" },
  { value: "distribution", label: "Distribution" },
  { value: "other", label: "Other" },
];

function buildDesignState(homeId, design) {
  return {
    home_id: design?.home_id || homeId || "",
    name: design?.name || "",
    design_goal: design?.design_goal || "partial_backup",
    architecture_type: design?.architecture_type || "ac_coupled",
    status: design?.status || "draft",
    notes: design?.notes || "",
  };
}

function buildEquipmentState(designId, item) {
  return {
    id: item?.id || "",
    design_id: item?.design_id || designId,
    product_id: item?.product_id || "",
    quantity: item?.quantity || 1,
    location_id: item?.location_id || "",
    role_in_system: item?.role_in_system || "primary_generation",
    notes: item?.notes || "",
  };
}

function buildProductOptions(products) {
  return [{ value: "", label: "Select product" }].concat(
    products.map((product) => ({
      value: product.id,
      label: `${product.manufacturer} ${product.model}`,
    }))
  );
}

function buildLocationOptions(locations) {
  return [{ value: "", label: "Unassigned location" }].concat(
    locations.map((location) => ({
      value: location.id,
      label: location.name,
    }))
  );
}

function EquipmentAssignmentEditor({ design, item, products, locations, onSaved, isNew = false }) {
  const [formState, setFormState] = useState(buildEquipmentState(design.id, item));
  const mutation = useApiMutation();
  const productOptions = buildProductOptions(products);
  const locationOptions = buildLocationOptions(locations);

  useEffect(() => {
    setFormState(buildEquipmentState(design.id, item));
  }, [design.id, item]);

  async function handleSubmit(event) {
    event.preventDefault();
    const payload = {
      ...formState,
      quantity: Number(formState.quantity) || 0,
      location_id: formState.location_id || null,
    };

    await mutation.run(() =>
      isNew
        ? api.createDesignEquipment(design.id, {
            ...payload,
            id: createId("design_equipment"),
            design_id: design.id,
          })
        : api.updateDesignEquipment(design.id, item.id, payload)
    );
    onSaved();
    if (isNew) {
      setFormState(buildEquipmentState(design.id, null));
    }
  }

  async function handleDelete() {
    if (!item) {
      return;
    }
    await mutation.run(() => api.deleteDesignEquipment(design.id, item.id));
    onSaved();
  }

  return (
    <form className="panel form-panel equipment-assignment-panel" onSubmit={handleSubmit}>
      <div className="panel-header">
        <h4>{isNew ? "Add Product Assignment" : "Assigned Product"}</h4>
        {!isNew && item?.data_origin ? <Badge>{item.data_origin}</Badge> : null}
      </div>
      <div className="form-grid">
        <SelectInput
          label="Product"
          value={formState.product_id}
          onChange={(event) => setFormState((current) => ({ ...current, product_id: event.target.value }))}
          options={productOptions}
        />
        <NumberInput
          label="Quantity"
          min="0"
          value={formState.quantity}
          onChange={(event) => setFormState((current) => ({ ...current, quantity: event.target.value }))}
        />
        <SelectInput
          label="System role"
          value={formState.role_in_system}
          onChange={(event) => setFormState((current) => ({ ...current, role_in_system: event.target.value }))}
          options={equipmentRoleSuggestions}
        />
        <SelectInput
          label="Location"
          value={formState.location_id}
          onChange={(event) => setFormState((current) => ({ ...current, location_id: event.target.value }))}
          options={locationOptions}
        />
      </div>
      <TextAreaInput
        label="Assignment notes"
        value={formState.notes}
        onChange={(event) => setFormState((current) => ({ ...current, notes: event.target.value }))}
      />
      <FormStatus saving={mutation.saving} error={mutation.error} />
      <div className="form-actions">
        <button
          className="button button-primary"
          type="submit"
          disabled={mutation.saving || !formState.product_id || Number(formState.quantity) <= 0}
        >
          {mutation.saving ? "Saving..." : isNew ? "Add Product" : "Save Assignment"}
        </button>
        {!isNew ? (
          <button className="button button-danger" type="button" onClick={handleDelete} disabled={mutation.saving}>
            Remove
          </button>
        ) : null}
        <button
          className="button button-secondary"
          type="button"
          onClick={() => setFormState(buildEquipmentState(design.id, item))}
          disabled={mutation.saving}
        >
          Reset
        </button>
      </div>
    </form>
  );
}

function DesignEditor({ homeId, design, products, locations, onSaved, isNew = false }) {
  const [formState, setFormState] = useState(buildDesignState(homeId, design));
  const mutation = useApiMutation();

  useEffect(() => {
    setFormState(buildDesignState(homeId, design));
  }, [homeId, design]);

  async function handleSubmit(event) {
    event.preventDefault();
    const payload = {
      ...(isNew ? { id: createId("design"), equipment: [] } : {}),
      ...formState,
    };

    await mutation.run(() => (isNew ? api.createDesign(payload) : api.updateDesign(design.id, payload)));
    onSaved();
    if (isNew) {
      setFormState(buildDesignState(homeId, null));
    }
  }

  return (
    <form className="panel form-panel" onSubmit={handleSubmit}>
      <div className="panel-header">
        <div>
          <h3>{isNew ? "Create Design" : formState.name || "Edit Design"}</h3>
          {!isNew ? <p className="callout-copy">{getDesignStatusExplanation(formState.status)}</p> : null}
        </div>
        {!isNew ? (
          <div className="trust-row">
            <Badge tone="info">{formState.status.replaceAll("_", " ")}</Badge>
            {design?.data_origin ? <TrustBadge state={design.data_origin} /> : null}
          </div>
        ) : null}
      </div>
      <div className="form-grid">
        <TextInput label="Design name" value={formState.name} onChange={(event) => setFormState((current) => ({ ...current, name: event.target.value }))} />
        <SelectInput label="Design goal" value={formState.design_goal} onChange={(event) => setFormState((current) => ({ ...current, design_goal: event.target.value }))} options={designGoalOptions} />
        <SelectInput label="Architecture type" value={formState.architecture_type} onChange={(event) => setFormState((current) => ({ ...current, architecture_type: event.target.value }))} options={architectureTypeOptions} />
        <SelectInput label="Status" value={formState.status} onChange={(event) => setFormState((current) => ({ ...current, status: event.target.value }))} options={designStatusOptions} />
      </div>
      <TextAreaInput label="Notes" value={formState.notes} onChange={(event) => setFormState((current) => ({ ...current, notes: event.target.value }))} />
      {!isNew ? (
        <div className="equipment-composition">
          <div className="panel panel-subsection">
            <div className="panel-header">
              <h4>Composition Summary</h4>
              <Badge tone={design?.equipment?.length ? "info" : "warning"}>
                {design?.equipment?.length || 0} assignment{design?.equipment?.length === 1 ? "" : "s"}
              </Badge>
            </div>
            {design?.equipment?.length ? (
              <div className="list-panel">
                {design.equipment.map((item) => {
                  const product = products.find((candidate) => candidate.id === item.product_id);
                  const location = locations.find((candidate) => candidate.id === item.location_id);
                  return (
                    <div key={item.id} className="list-row list-row-stack">
                      <div>
                        <strong>{product ? `${product.manufacturer} ${product.model}` : item.product_id}</strong>
                        <p>{item.role_in_system}</p>
                        <div className="trust-row">
                          <TrustBadge state={item.data_origin} />
                          {product
                            ? getProductTrustStates(product).map((state) => (
                                <TrustBadge
                                  key={`${item.id}-${state}`}
                                  state={state}
                                  label={state === "placeholder" ? "Placeholder specs" : undefined}
                                />
                              ))
                            : <TrustBadge state="missing" label="Missing product" />}
                        </div>
                      </div>
                      <div className="takeoff-meta">
                        <span>{item.quantity} each</span>
                        <span>{location?.name || "Unassigned location"}</span>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <EmptyState label="No products are assigned to this design yet." />
            )}
          </div>

          <EquipmentAssignmentEditor design={design} products={products} locations={locations} onSaved={onSaved} isNew />

          {design?.equipment?.map((item) => (
            <EquipmentAssignmentEditor
              key={item.id}
              design={design}
              item={item}
              products={products}
              locations={locations}
              onSaved={onSaved}
            />
          ))}
        </div>
      ) : null}
      <FormStatus saving={mutation.saving} error={mutation.error} />
      <FormActions saving={mutation.saving} onCancel={() => setFormState(buildDesignState(homeId, design))} saveLabel={isNew ? "Create Design" : "Save Design"} />
    </form>
  );
}

export function SystemDesignBuilderPage() {
  const [refreshKey, setRefreshKey] = useState(0);
  const homeQuery = useApiQuery(`design-home-${refreshKey}`, api.getHome);
  const designsQuery = useApiQuery(`designs-${refreshKey}`, api.getDesigns);
  const productsQuery = useApiQuery(`products-${refreshKey}`, api.getProductLibrary);
  const locationsQuery = useApiQuery(`equipment-locations-${refreshKey}`, api.getEquipmentLocations);

  const home = homeQuery.data;
  const designs = designsQuery.data || [];
  const products = productsQuery.data || [];
  const locations = locationsQuery.data || [];
  const loading = homeQuery.loading || designsQuery.loading || productsQuery.loading || locationsQuery.loading;
  const error = homeQuery.error || designsQuery.error || productsQuery.error || locationsQuery.error;

  return (
    <>
      <PageSection
        title="System Design Builder"
        description="Designs should be composable, comparable, and traceable back to structured house facts and product records."
      >
        {loading ? <LoadingState label="Loading designs..." /> : null}
        {error ? <ErrorState error={error} label="Unable to load design composition data." /> : null}
        {!loading && !error ? (
          <div className="panel warning-panel">
            <div className="panel-header">
              <h3>Planning maturity and trust</h3>
              <div className="trust-row">
                <TrustBadge state="placeholder" label="Not engineering approval" />
                <TrustBadge state="derived_estimate" label="Derived takeoffs stay transient" />
              </div>
            </div>
            <p>
              Design status communicates planning maturity only. `Estimate Ready` means the design has enough context for rough estimating, while `Installation Planning` means the design is preparing for site validation and implementation review.
            </p>
          </div>
        ) : null}
        {!loading && home ? (
          <div className="stack-grid">
            <DesignEditor
              homeId={home.id}
              products={products}
              locations={locations}
              onSaved={() => setRefreshKey((current) => current + 1)}
              isNew
            />
            {designs.map((design) => (
              <DesignEditor
                key={design.id}
                homeId={home.id}
                design={design}
                products={products}
                locations={locations}
                onSaved={() => setRefreshKey((current) => current + 1)}
              />
            ))}
          </div>
        ) : null}
        {!loading && !home ? (
          <EmptyState label="No home profile is available for design creation yet." />
        ) : null}
      </PageSection>
    </>
  );
}
