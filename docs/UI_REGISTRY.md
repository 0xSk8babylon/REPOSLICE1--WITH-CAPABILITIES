# UI Registry

## Canonical Role

`uiRegistry.js` is the canonical frontend placement source for future Home, Planner, Build, and Hidden/Internal card organization.

It is canonical for frontend section placement, homeowner-safe labels, card names, ordering, V1 visibility, and frontend trust-boundary notes. It is not canonical for backend contracts, product facts, persistence, permissions, or runtime capability existence.

The `/architecture` cockpit remains the canonical internal technical/product architecture visibility surface. The registry must stay aligned with its product capability IDs, but it should not import backend Python code or create runtime coupling.

## What It Is

The UI Registry is a frontend product-architecture map for future Home, Planner, and Build pages.

It lives in `apps/web/src/lib/uiRegistry.js` and lists product capabilities as reusable UI planning items. Each item defines homeowner-safe labels, section placement, card naming, priority, V1 visibility, data type, source capability, empty-state copy, and trust-boundary notes.

The registry is not a backend contract, not persistence, not authorization, and not a page implementation.

## Why It Exists

The Architecture Visibility cockpit maps technical capabilities to product capabilities and UI sections. The UI Registry makes that mapping reusable in frontend code without requiring future pages to scrape the `/architecture` graph, copy endpoint names, or reinterpret backend implementation labels.

Future pages should use the registry to answer:

- Which cards belong in Home, Planner, Build, or Hidden/Internal?
- What order should the cards appear in?
- Which cards are visible in V1?
- What homeowner-safe label and empty state should be used?
- What trust boundary must remain visible when the card is rendered?

## How Pages Should Consume It

Future Home, Planner, and Build pages should import the registry helpers:

```js
import { getVisibleSectionItems } from "../lib/uiRegistry";
```

Recommended use:

- Home page: `getVisibleSectionItems("home")`
- Planner page: `getVisibleSectionItems("planner")`
- Build page: `getVisibleSectionItems("build")`
- Internal planning tools: `getSectionItems("hidden")` or `getV1Items()`

Pages should render cards from registry metadata first, then attach data-specific content through explicit page logic. The registry should decide placement and labels; it should not fetch API data or calculate planning results.

## Alignment Check

`uiRegistry.js` exports `validateUiRegistryAlignment()`.

The helper compares every `uiRegistry.sourceCapability` value against known Architecture Visibility product capability IDs from `/api/system-visibility/architecture`.

It reports:

- `registryItemsWithoutSourceCapability`
- `missingSourceCapabilityReferences`
- `allowedFutureSourceCapabilityReferences`
- `architectureProductCapabilitiesNotRepresented`

Run it with:

```bash
cd apps/web
node --input-type=module -e "import('./src/lib/uiRegistry.js').then(({validateUiRegistryAlignment}) => { console.log(JSON.stringify(validateUiRegistryAlignment(), null, 2)); })"
```

Expected steady state:

- `aligned` is `true`
- `registryItemsWithoutSourceCapability` is empty
- `missingSourceCapabilityReferences` is empty
- `architectureProductCapabilitiesNotRepresented` is empty
- `allowedFutureSourceCapabilityReferences` contains only explicitly documented deferred items

Current allowed future reference:

- `post-install-handoff` may reference `capability-post-install-handoff` until the Architecture Visibility cockpit adds a matching product capability node or Matt decides to remove/defer that Build card.

## What Should Not Go In It

Do not put these in the UI Registry:

- API endpoint names as homeowner-facing labels
- backend enum names as UI copy
- pricing, savings, payback, rebate, or tariff conclusions
- NEC, code-compliance, permit, AHJ, utility-approval, or engineering approval claims
- auth, permission enforcement, RBAC, ABAC, or tenant-isolation behavior
- persistence rules, migrations, database schema decisions, or source-of-truth ownership
- final product recommendations, rankings, procurement logic, bids, quotes, or proposals
- generated AI explanation text as a source of fact

The registry may reference a `sourceCapability` string so internal tools can trace the card back to the Architecture/Product Mapping cockpit.

## Moving A Capability Between Sections

To move a capability:

1. Change the item's `section` to one of `home`, `planner`, `build`, or `hidden`.
2. Adjust `priority` so the item appears in the intended order.
3. Review `homeownerLabel`, `cardName`, `homeownerQuestionAnswered`, and `emptyStateMessage` for the new context.
4. Update `trustBoundaryNotes` if the new placement changes the risk of overclaiming.
5. Confirm `sourceCapability` still points at the Architecture Visibility product capability that owns the card.
6. Run `validateUiRegistryAlignment()`.
7. Keep the Architecture Visibility cockpit aligned in a later pass if the backend graph is still maintaining parallel product metadata.

Moving a capability into a visible homeowner section is product-direction-sensitive. It should be reviewed by Matt before being treated as canonical UI architecture.

Safe section movement rules:

- Home is for Energy Twin overview, home outline, known facts, Energy Passport, and readiness snapshot.
- Planner is for scenarios, compatibility, constraints, product preferences, and planning intelligence.
- Build is for proposal options, contractor context, estimate readiness, install path, program intelligence, and post-install handoff.
- Hidden/Internal is for technical, admin, testing, governance, or system visibility items.

## Hiding Or Deferring A Capability

To hide a capability without removing it:

- Set `visibleInV1: false`.
- Keep the item in its intended future section if the product destination is known.
- Move the item to `section: "hidden"` only when it is internal, admin, testing, or system-visibility only.
- Use the empty state to explain missing prerequisites without implying the feature exists in runtime.

Deferred items should remain traceable. Do not delete a future capability solely because it is not visible in V1.

## Homeowner-Safe Label Rules

Homeowner labels must:

- use plain product language, not endpoint names
- avoid backend enum names, file names, route names, and implementation jargon
- avoid certainty words such as approved, verified, compliant, eligible, guaranteed, optimized, or final unless the system has explicit authority
- distinguish known facts from assumptions, placeholders, and derived views
- preserve professional-review, contractor-review, AHJ, utility, and field-verification boundaries where relevant
- describe what question the card helps answer rather than what backend service powers it

Examples:

- Use `Readiness snapshot`, not `recommendation_eligibility_readiness`.
- Use `Program readiness`, not `GET /api/program-intelligence`.
- Use `Known home facts`, not `TwinPlanningContext sections`.

## Current Sections

Home:

- Energy Twin overview
- Home energy outline
- Known home facts
- Energy Passport
- Readiness snapshot

Planner:

- Upgrade paths
- Compatibility
- Planning constraints
- Product preferences
- Planning intelligence

Build:

- Proposal options
- Contractor review context
- Estimate readiness
- Install path
- Program readiness
- Post-install handoff

Hidden/Internal:

- Product Architecture Cockpit
- Technical Architecture Map
- Test Coverage

## Relationship To `/architecture`

`/architecture` currently consumes `/api/system-visibility/architecture`, which includes parallel product/UI metadata for graph nodes and exports.

The registry intentionally does not replace that endpoint yet. Keeping both surfaces separate avoids silently changing backend contracts or making the frontend registry authoritative before Matt approves that direction.

Drift prevention:

- Keep `architectureProductCapabilityIds` in `uiRegistry.js` synchronized with backend `product_capability` node IDs.
- Keep intentionally deferred references in `allowedFutureSourceCapabilityIds` with comments.
- Run `validateUiRegistryAlignment()` after adding, moving, hiding, or deleting registry items.
- If validation reports `architectureProductCapabilitiesNotRepresented`, either add a registry item or document why the backend capability is intentionally internal.
- If validation reports `missingSourceCapabilityReferences`, fix the typo, add the backend product capability, or move the item to the explicit future allowance list with a comment.

Future connection options:

- Use `uiRegistry.js` as the frontend source of UI section ordering and labels while `/architecture` continues using backend graph relationships.
- Promote the validation helper into a formal test once frontend/backend source-of-truth ownership is approved.
- Move product mapping authority to one source only after Matt approves whether the canonical source is frontend registry metadata, backend visibility metadata, or a generated shared artifact.
