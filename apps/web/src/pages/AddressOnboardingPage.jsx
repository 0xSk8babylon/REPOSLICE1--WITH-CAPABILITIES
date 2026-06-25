import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { FormActions } from "../components/form/FormActions";
import { FormStatus } from "../components/form/FormStatus";
import { SelectInput, TextInput } from "../components/form/Inputs";
import { api } from "../lib/api";
import { useApiMutation } from "../lib/useApiMutation";
import { useApiQuery } from "../lib/useApiQuery";

const initialFormState = {
  account_id: "",
  name: "",
  address_line_1: "",
  address_line_2: "",
  city: "",
  state: "",
  postal_code: "",
  country: "US",
};

function cleanPayload(formState, includeAccountId) {
  const payload = {
    name: formState.name.trim(),
    address_line_1: formState.address_line_1.trim(),
    city: formState.city.trim(),
    state: formState.state.trim(),
    postal_code: formState.postal_code.trim(),
    country: (formState.country || "US").trim(),
  };

  const addressLine2 = formState.address_line_2.trim();
  if (addressLine2) {
    payload.address_line_2 = addressLine2;
  }
  if (includeAccountId && formState.account_id) {
    payload.account_id = formState.account_id;
  }

  return payload;
}

function isAccountRequiredError(error) {
  return error?.message?.toLowerCase().includes("account_id is required");
}

function friendlyOnboardingError(error) {
  if (!error) return null;
  if (isAccountRequiredError(error)) {
    return new Error("Choose which account should own this home, then submit again.");
  }
  if (error.message?.startsWith("403")) {
    return new Error("Your current account role cannot create a home record.");
  }
  return error;
}

export function AddressOnboardingPage() {
  const navigate = useNavigate();
  const [formState, setFormState] = useState(initialFormState);
  const [requiresAccountSelection, setRequiresAccountSelection] = useState(false);
  const mutation = useApiMutation();
  const meQuery = useApiQuery("address-onboarding-me", api.getMe, { initialData: null });
  const accountIds = meQuery.data?.account_ids || [];
  const shouldShowAccountSelector = requiresAccountSelection || accountIds.length > 1;
  const accountOptions = [
    { value: "", label: "Select account" },
    ...accountIds.map((accountId) => ({ value: accountId, label: accountId })),
  ];

  function updateField(fieldName) {
    return (event) => {
      setFormState((current) => ({ ...current, [fieldName]: event.target.value }));
    };
  }

  async function handleSubmit(event) {
    event.preventDefault();

    try {
      const response = await mutation.run(() =>
        api.submitAddressOnboarding(cleanPayload(formState, shouldShowAccountSelector))
      );
      navigate(response.next_route || "/", {
        replace: true,
        state: {
          addressOnboardingStatus: response.status,
          homeId: response.home_id,
          accountId: response.account_id,
        },
      });
    } catch (error) {
      if (isAccountRequiredError(error)) {
        setRequiresAccountSelection(true);
      }
    }
  }

  return (
    <div className="hq-page hq-onboarding-page">
      <section className="hq-page-head hq-onboarding-head">
        <div>
          <p className="hq-eyebrow">Address onboarding</p>
          <h1>Start the Energy Twin with an address.</h1>
          <p>
            This records a user-entered address for planning. It does not geocode, validate property ownership,
            infer utility service, or determine climate, AHJ, or program eligibility.
          </p>
        </div>
        <Link className="hq-btn hq-btn-secondary" to="/">
          Back to Home
        </Link>
      </section>

      <section className="hq-onboarding-grid">
        <form className="hq-panel hq-onboarding-form form-panel" onSubmit={handleSubmit}>
          <div className="hq-panel-head">
            <div>
              <p className="hq-eyebrow">Home record</p>
              <h2>Address details</h2>
            </div>
            <span className="hq-badge hq-badge-info">User-entered</span>
          </div>

          {shouldShowAccountSelector ? (
            <SelectInput
              label="Account"
              hint="Backend membership rules still decide whether this account can create a home."
              value={formState.account_id}
              onChange={updateField("account_id")}
              options={accountOptions}
            />
          ) : null}

          <div className="form-grid">
            <TextInput
              label="Home name"
              value={formState.name}
              onChange={updateField("name")}
              required
              autoComplete="organization"
            />
            <TextInput
              label="Address line 1"
              value={formState.address_line_1}
              onChange={updateField("address_line_1")}
              required
              autoComplete="address-line1"
            />
            <TextInput
              label="Address line 2"
              value={formState.address_line_2}
              onChange={updateField("address_line_2")}
              autoComplete="address-line2"
            />
            <TextInput
              label="City"
              value={formState.city}
              onChange={updateField("city")}
              required
              autoComplete="address-level2"
            />
            <TextInput
              label="State"
              value={formState.state}
              onChange={updateField("state")}
              required
              autoComplete="address-level1"
            />
            <TextInput
              label="Postal code"
              value={formState.postal_code}
              onChange={updateField("postal_code")}
              required
              autoComplete="postal-code"
            />
            <TextInput
              label="Country"
              value={formState.country}
              onChange={updateField("country")}
              required
              autoComplete="country"
            />
          </div>

          <FormStatus saving={mutation.saving} error={friendlyOnboardingError(mutation.error)} />
          <FormActions saving={mutation.saving} saveLabel="Record address" />
        </form>

        <aside className="hq-panel hq-onboarding-side">
          <p className="hq-eyebrow">Trust boundary</p>
          <h2>What this step does</h2>
          <ul className="hq-checklist">
            <li>Creates or resolves an account-scoped home record.</li>
            <li>Records address fields as user-entered planning data.</li>
            <li>Keeps ownership checks in app-owned account memberships.</li>
            <li>Leaves geocoding, validation, utility, climate, AHJ, and program inference deferred.</li>
          </ul>
          {meQuery.error ? (
            <p className="hq-muted">Account details could not be read. The backend will still verify account access.</p>
          ) : null}
        </aside>
      </section>
    </div>
  );
}
