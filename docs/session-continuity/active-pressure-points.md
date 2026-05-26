# Active Pressure Points

## 1. No Migration Framework Yet

This pressure has been reduced but not eliminated.

- Current pressure: Alembic now exists, but the current setup is still a lightweight baseline rather than a mature ongoing migration practice.
- Risk: future schema work could still drift into direct metadata changes unless revisions become part of the normal workflow.
- Why it matters: editable user workflows should not grow on top of ad hoc schema evolution.

## 2. Provenance Is Broader, But Still Partial

- Current pressure: a provenance foundation now exists, and scenario comparison, products, loads, and pathways now consume lineage summaries, but coverage is still partial and does not yet reach every important field or derived path.
- Risk: future AI layers may overstate confidence unless provenance becomes explicit.

## 12. Recommendation Architecture Exists Before Deep Sizing Math

- Current pressure: the recommendation-profile model now includes first battery and solar sizing layers, better inspectability, explicit backup-scope posture/confidence, a coarse site-aware solar adjustment, a roof-readiness layer, profile-level architecture-fit tradeoffs, a preliminary panel/service architecture layer with consistency checks, a planning-only inverter/system architecture layer, and a structured reasoning graph, but provenance depth and richer site-aware sizing behavior are still incomplete.
- Risk: future sessions may overclaim the current slices as a full sizing engine or bypass the profile architecture with ad hoc recommendation logic.

## 3. Seed Data And Real Data Share The Same Persistence Layer

- Current pressure: record-level separation now exists through `data_origin`, but environment-level and tenancy-level separation still do not.
- Risk: demo assumptions can still leak operationally unless future workflows actively respect origin metadata.

## 4. Editable Workflows Exist, But They Are Still Early-Stage

- Current pressure: the frontend now exercises core POST/PATCH flows, but the editing surface is still partial.
- Risk: sessions may assume the whole product is mature when delete/archive flows and downstream estimating persistence are still absent.

## 5. Takeoff And Estimate Logic Is Still Placeholder

- Current pressure: takeoff generation is now derived from live design composition, but it is still transient and placeholder-priced.
- Risk: users may over-interpret generated line items as procurement-ready or assume placeholder pricing is verified.

## 10. Completeness Can Be Misread As Engineering Readiness

- Current pressure: planning completeness scoring now exists and is useful, but it could be mistaken for code, permitting, or install readiness if messaging drifts.
- Risk: future sessions may overextend the completeness model into false authority.

## 6. No Audit Trail Or Change History

- Current pressure: updates mutate current state directly.
- Risk: future collaborative workflows will need provenance, rollback context, and change diffs.

## 11. Verification Status Can Be Misread As Full Truth

- Current pressure: verification status is now visible through provenance summaries, but it only describes source-document posture, not engineering validity.
- Risk: future sessions may conflate manufacturer references, trust badges, and true engineering certainty.

## 7. Ownership Exists But Enforcement Does Not

- Current pressure: `account_id`, roles, and subscription states are present but inactive.
- Risk: future sessions may mistakenly assume multi-user safety already exists.

## 8. Continuity Risk From Context Resets

- Current pressure: a compact discovery layer now exists, but the detailed continuity and doctrine surface is still large enough that agents can over-load context unless they route carefully.
- Risk: future sessions may either skip needed deep references or reintroduce oversized restore prompts unless they follow the layered restore model.

## 9. Versioning Policy Exists But Is Not Yet Institutionalized

- Current pressure: `/api/*` aliases now exist, but most consumers still use unprefixed routes.
- Risk: future sessions may create inconsistent routing behavior unless one preferred client path is reinforced.

## Recommended Immediate Focus

- Introduce clear UI labeling for persisted placeholders versus verified records.
- Decide whether derived takeoffs should remain transient or be persisted/versioned on design changes.
- Preserve the planning-only boundary around completeness and advisor reasoning.
- Expand provenance coverage without implying that placeholder references are verified.
- Continue extending scenario/pathway/design lineage beyond the current summary layer.
- Convert Alembic from scaffold to normal practice before substantial schema expansion.
- Keep root discovery files, affected continuity docs, and handoffs synchronized with real implementation state.
