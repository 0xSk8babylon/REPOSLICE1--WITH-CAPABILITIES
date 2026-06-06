# Phase 16 UI / UX Layer Doctrine

## Doctrine Record

- Summary: Phase 16 UI / UX work presents existing backend planning intelligence in clear, homeowner-safe, contractor-useful product views.
- Scope: Frontend presentation doctrine for Phase 16 and later UI work; no runtime implementation approval.
- Assumptions: Backend Phase 1 through Phase 15 planning intelligence remains read-only, request-time, provenance-bearing, and non-authoritative unless Matt approves a later contract change.
- Sources / Provenance: `PROJECT_STATE.md`, `SESSION_HANDOFF.md`, `discovery-index.md`, `docs/API_CONTRACTS.md`, `docs/handoffs/2026-06-05-phase-15-program-intelligence-closeout.md`, `AGENTS.md`.
- Risks / Open Questions: Frontend work can accidentally imply approval, certainty, savings, compliance, or permission authority if labels are weakened.
- Decisions Needed From Matt: Any protected expansion listed in Hard Stops.
- Next Action: Reference this doctrine from scoped Phase 16 UI prompts.

## 1. Purpose

The UI / UX layer exists to present existing backend planning intelligence clearly, safely, and usefully.

The UI may translate backend intelligence into usable product views, support homeowner understanding, support contractor review, preserve uncertainty, provenance, and non-authoritative boundaries, and make existing planning context easier to inspect.

The UI does not create new planning authority. Phase 16 is about making existing intelligence usable, not expanding backend product scope.

## 2. Core Boundary

UI work in Phase 16 is additive and presentation-focused.

Allowed UI work:

- Creating or stabilizing frontend routes, pages, and components.
- Creating an app shell or dashboard shell if missing.
- Displaying existing backend API responses.
- Organizing backend data into cards, panels, tabs, sections, or dashboards.
- Adding readable labels and explanations.
- Adding homeowner-safe summary copy.
- Adding contractor-facing review panels.
- Adding loading states.
- Adding empty states.
- Adding backend-unavailable states.
- Adding partial or degraded-data states.
- Creating a centralized frontend API client/helper layer.
- Improving visual hierarchy and usability.
- Adding lightweight frontend-only type definitions if needed.
- Adding focused frontend tests only if a frontend test framework already exists or can be added without broad tooling expansion.

Prohibited UI work:

- Auth, login, or signup.
- Permission enforcement or security enforcement.
- Database writes, persistence changes, or migrations.
- Deployment infrastructure, hosting configuration, or provider configuration.
- Billing, payment, or commercialization workflows.
- CRM integrations or email automation.
- Product ingestion, distributor portals, or contractor marketplace workflows.
- Final quote, proposal, design, estimate, or bill-of-material generation.
- Permit approval, utility approval, or interconnection approval claims.
- Financial, savings, payback, ROI, or incentive guarantees.
- Broad backend refactors.
- Backend contract changes unless explicitly approved by Matt.
- External services, secrets, or production integrations.
- `git push`.

## 3. Trust-Boundary Language

UI language must preserve backend doctrine. All planning intelligence displayed in the UI must remain clearly labeled as:

- Derived.
- Request-time.
- Non-authoritative.
- Based on available planning context.
- Subject to contractor, customer, utility, program, AHJ, or professional confirmation where applicable.

Preferred language:

- Planning signal.
- Derived view.
- Needs confirmation.
- Missing input.
- Contractor review needed.
- Utility/program verification required.
- Based on available inputs.
- Not a final quote.
- Not a final design.
- Not a final estimate.
- Not utility approval.
- Not permit approval.
- Not interconnection approval.
- Not financial advice.

Avoided language:

- Approved.
- Guaranteed.
- Final estimate.
- Final design.
- Final proposal.
- Best option.
- Utility accepted.
- Permit ready.
- Interconnection approved.
- Guaranteed savings.
- Contractor certified.
- Lowest cost.
- Highest ROI.
- Ready to install.

Stronger language may only be used in a future phase if the system actually gains that authority through Matt-approved backend contracts, source-backed verification, and explicit governance updates.

## 4. Data Handling Rules

The frontend must treat backend API responses as the source of truth.

The UI may:

- Summarize backend data.
- Group backend data.
- Sort or visually organize backend data.
- Explain backend statuses in clearer language.
- Expose provenance and basis information.
- Show confidence or uncertainty indicators when present.

The UI may not:

- Invent missing conclusions.
- Fabricate prices, savings, incentives, eligibility, or payback.
- Override backend readiness status.
- Hide uncertainty.
- Convert a warning into approval.
- Convert partial data into complete data.
- Infer utility, program, permit, interconnection, AHJ, or contractor acceptance.
- Silently suppress blockers.
- Create new authoritative classifications to satisfy UI design.

For degraded responses, prefer language such as:

- "This view is based on available planning inputs."
- "Some planning context is incomplete."
- "Additional contractor or customer confirmation may be needed."
- "Program or utility details require external verification."

## 5. Homeowner vs Contractor Presentation

Homeowner-safe and contractor-facing views may present the same backend intelligence differently, but both remain read-only during Phase 16.

Homeowner UI should:

- Use plain language.
- Avoid overloaded technical detail.
- Highlight next steps.
- Show what is known.
- Show what is missing.
- Show what needs confirmation.
- Clearly explain non-final status.
- Reduce anxiety and confusion.

Contractor UI may:

- Expose more technical context.
- Show install complexity.
- Show confirmation gates.
- Show blockers.
- Show takeoff/material basis.
- Show product preference signals.
- Show proposal option readiness.
- Show energy passport/transfer context.
- Show grid/program intelligence notes.
- Show provenance and basis fields more directly.

## 6. Frontend API Usage

The frontend should:

- Centralize API calls through a small client/helper layer.
- Avoid scattered `fetch` calls throughout components.
- Keep endpoint paths easy to audit.
- Handle errors deterministically.
- Handle missing or partial data gracefully.
- Preserve backend response fields instead of flattening away provenance.
- Avoid creating backend workarounds inside the frontend.

Every consumed endpoint should have clear UI behavior for:

- Loading.
- Success.
- Empty response.
- Backend unavailable.
- `404` or no context.
- Validation or error response.
- Partial or degraded data.

Codex should report which backend endpoints are consumed by any new UI view.

## 7. Suggested UI Information Architecture

These are suggested Phase 16 display sections, not mandatory scope:

- Home Dashboard.
- Energy Twin Summary.
- Planning Readiness.
- Scenario / Option Sets.
- Estimate Readiness.
- Contractor Review.
- Product Preference Signals.
- Post-Install / CRM Handoff Preview.
- Energy Passport.
- Program / Grid Edge Intelligence.

These sections are display layers over existing APIs. They do not create new authority, new backend logic, new permission enforcement, or new product scope.

## 8. Product-Grade UX Direction

Phase 16 should create a credible first product experience, not just a developer dashboard.

The UI should be clear, trustworthy, modern, calm, homeowner-safe, contractor-useful, mobile-aware, and visually consistent. Phase 16 should prioritize clarity and credibility before advanced polish.

Allowed UX work:

- Clean app shell.
- Strong first dashboard impression.
- Readable cards and panels.
- Consistent spacing and typography.
- Simple visual hierarchy.
- Status badges.
- Confidence or confirmation indicators.
- Homeowner-friendly summaries.
- Contractor detail sections.
- Responsive layout basics.
- Light branding direction.
- Simple charts only where backend data supports them.
- Reusable UI components if they stay lightweight.

Avoid overbuilding:

- Full design system.
- Complex animations.
- Custom charting-heavy analytics.
- Mobile app wrapper.
- Role-based portal system.
- Login/signup flow.
- Production-grade onboarding.
- Payment or commercial funnel.
- Unsupported savings/ROI visualizations.
- Visuals that imply finality, authority, or certainty the backend does not provide.

Core principle: Phase 16 should look product-grade enough to demo, but must not expand into deployment, auth, commercial workflows, or unsupported authority.

## 9. Verification Expectations

For later UI implementation work, Codex should report:

- Changed files.
- Routes/pages added.
- Components added.
- Backend endpoints consumed.
- Trust-boundary labels added.
- Homeowner-safe copy added.
- Contractor-facing sections added.
- Loading, error, empty, and degraded states added.
- Tests, lint, or typecheck run.
- Scripts unavailable, if applicable.
- Known gaps.
- Risks or blockers.
- Whether the working tree is clean or dirty.

If frontend scripts do not exist, Codex should say so instead of inventing a large toolchain unnecessarily.

## 10. Hard Stops

Codex must stop and ask Matt before:

- Adding auth.
- Adding login/signup.
- Adding permission enforcement.
- Adding security enforcement.
- Adding writes.
- Adding persistence.
- Adding migrations.
- Adding deployment configuration.
- Adding hosting/provider config.
- Adding external services.
- Adding secrets.
- Adding payments.
- Adding CRM integrations.
- Adding email automation.
- Adding product ingestion.
- Adding distributor portal features.
- Changing backend API contracts.
- Changing backend authority.
- Generating final quote, proposal, design, estimate, or bill-of-material logic.
- Deleting files.
- Broad refactors.
- Running `git push`.

## 11. Relationship To Scoped Prompts

This doctrine is a guardrail, not an execution prompt.

Scoped prompts remain the execution mechanism for Phase 16 UI work. Phase 16 scoped prompts should reference this doctrine and define the exact view, endpoint set, trust labels, verification target, and stop conditions for each session.

Do not create permanent skills for every narrow UI task. Broad reusable rules belong in doctrine. Narrow one-time work belongs in scoped prompts.

## 12. Closeout Output

After any Phase 16 UI doctrine or implementation task, Codex should report:

- File created or changed.
- Whether `docs/doctrine/` had to be created.
- Existing docs reviewed.
- Whether unrelated files changed.
- Final `git status --short`.
- Recommended next scoped Phase 16 prompt.

For implementation tasks, also report routes/pages added, components added, endpoints consumed, trust-boundary labels, homeowner-safe copy, contractor-facing sections, loading/error/empty/degraded states, verification commands, known gaps, and risks/blockers.
