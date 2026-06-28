# UI Registry

## Canonical Role

`uiRegistry.js` is the canonical frontend placement source for the current Home, Explore, Planner, Builder object-view shell plus Internal/Debug and Deferred/Legacy route organization.

It is canonical for frontend section placement, homeowner-safe labels, card names, ordering, V1 visibility, and frontend trust-boundary notes. It is not canonical for backend contracts, product facts, persistence, permissions, or runtime capability existence.

The `/architecture` cockpit remains the canonical internal technical/product architecture visibility surface. The registry must stay aligned with its product capability IDs, but it should not import backend Python code or create runtime coupling.

## What It Is

The UI Registry is a frontend product-architecture map for Home, Explore, Planner, Builder, Internal/Debug, and Deferred/Legacy surfaces.

It lives in `apps/web/src/lib/uiRegistry.js` and lists product capabilities as reusable UI planning items. Each item defines homeowner-safe labels, section placement, card naming, priority, V1 visibility, data type, source capability, empty-state copy, and trust-boundary notes.

The registry is not a backend contract, not persistence, not authorization, and not a page implementation.

## Why It Exists

The Architecture Visibility cockpit maps technical capabilities to product capabilities and UI sections. The UI Registry makes that mapping reusable in frontend code without requiring future pages to scrape the `/architecture` graph, copy endpoint names, or reinterpret backend implementation labels.

Future pages should use the registry to answer:

- Which cards belong in Home, Explore, Planner, Builder, Internal/Debug, or Deferred/Legacy?
- What order should the cards appear in?
- Which cards are visible in V1?
- What homeowner-safe label and empty state should be used?
- What trust boundary must remain visible when the card is rendered?

## How Pages Should Consume It

Home, Explore, Planner, and Builder pages should import the registry helpers when they render registry-driven cards:

```js
import { getVisibleSectionItems } from "../lib/uiRegistry";
```

Recommended use:

- Home page: `getVisibleSectionItems("home")`
- Explore page: `getVisibleSectionItems("explore")`
- Planner page: `getVisibleSectionItems("planner")`
- Builder page: `getVisibleSectionItems("builder")`
- Internal/debug tools: `getSectionItems("internal")` or `getV1Items()`
- Deferred/legacy inventory: `getSectionItems("deferred")`

Compatibility aliases remain supported for older callers:

- `getVisibleSectionItems("build")` resolves to Builder.
- `getSectionItems("hidden")` and `getSectionItems("hidden_internal")` resolve to Internal/Debug.

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

Current allowed future references:

- None. Deferred route and product surfaces should have an explicit Architecture Visibility product capability node, even when the runtime feature is hidden or deferred.

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

1. Change the item's `section` to one of `home`, `explore`, `planner`, `builder`, `internal`, or `deferred`.
2. Adjust `priority` so the item appears in the intended order.
3. Review `homeownerLabel`, `cardName`, `homeownerQuestionAnswered`, and `emptyStateMessage` for the new context.
4. Update `trustBoundaryNotes` if the new placement changes the risk of overclaiming.
5. Confirm `sourceCapability` still points at the Architecture Visibility product capability that owns the card.
6. Run `validateUiRegistryAlignment()`.
7. Keep the Architecture Visibility cockpit aligned in a later pass if the backend graph is still maintaining parallel product metadata.

Moving a capability into a visible homeowner section is product-direction-sensitive. It should be reviewed by Matt before being treated as canonical UI architecture.

Safe section movement rules:

- Home is for the durable Energy Twin record, home outline, known facts, Energy Passport, and readiness snapshot.
- Explore is for homeowner goals and learning context. Goal selection is local UI intent unless a future approved workflow adds persistence.
- Planner is for the current object-view planner surfaces: Guided Templates, Sandbox Drafts, and Comparisons.
- Builder is for project/build-readiness context and selected read-only readiness summaries. It is not contractor workflow, project promotion, proposal generation, or handoff.
- Internal/Debug is for capabilities, architecture cockpit, test coverage, governance, and system visibility items that should not appear in homeowner primary navigation.
- Deferred/Legacy is for hidden routes, legacy/deep routes, future product foundations, and capability surfaces intentionally kept outside primary navigation.

## Hiding Or Deferring A Capability

To hide a capability without removing it:

- Set `visibleInV1: false`.
- Keep the item in its intended future section if the product destination is known.
- Move the item to `section: "internal"` only when it is internal, admin, testing, debug, governance, or system-visibility only.
- Move the item to `section: "deferred"` when it remains reachable for compatibility or future planning but is not part of the current primary shell.
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

Explore:

- Goals
- Learn

Planner:

- Guided templates
- Sandbox drafts
- Comparisons

Builder:

- Estimate readiness
- Program readiness
- Build readiness

Internal/Debug:

- Product Architecture Cockpit
- Technical Architecture Map
- Test Coverage
- Capabilities debug route

Deferred/Legacy:

- Compatibility
- Planning constraints
- Product preferences
- Planning intelligence
- Proposal options
- Contractor review context
- Install path
- Catalog
- Post-install handoff
- Legacy deep routes

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

## Lovable Reference Parity

Lovable screenshots (`~/TwinEnergy/references/lovable-references/`) are visual/card parity evidence only. They rank below this registry and current repo contracts in authority and are not a source of backend truth or section-placement authority. When a parity pass proposes a card, classify it (Home / Explore / Planner / Builder / Internal-Debug / Deferred-Legacy) and place it via this registry — do not let a screenshot promote a card into primary nav.

- `capabilities-*` screenshots are derived-view "Product Objects" references → Internal/Debug visibility only; never auto-promoted to homeowner nav.
- Planner draft templates are render-only mock content (`isDraft`), not backend registry items.
- See `docs/lovable-reference-parity.md` for the full protocol and parity table.
