# Frontend Diagnosis: HeartQuill vs Legacy

Date: 2026-07-01
Scope: `apps/web/src` (frontend), `apps/api/app` (backend route verification)
Method: read-only static audit of every route, component, api.js export, and backend router. No source files were modified.

## Executive verdict

**Both prior assessments were partially right; neither was fully right.**

- The Codex claim ("HeartQuill wires real API calls") is TRUE for the Home, Planner (templates), and Builder screens: 9 distinct endpoints are called through real `fetch` and their responses are rendered.
- The code-review claim ("HeartQuill runs on static mock data") is TRUE only for Explore, Catalog, Capabilities, the Energy Twin diagram, sandbox drafts, comparisons, and the upgrade path — and for **every** screen's fallback state: each live panel silently falls back to labeled static data from `heartQuillMockData.js` when the backend errors or the database is empty. Observing the app against an empty backend shows `provenance: "Static shell data"` everywhere, which is almost certainly how that assessment arose. As a blanket statement it is FALSE.
- The legacy pages are fully API-backed — 9 of 10 are entirely LIVE, with all of the app's mutation capability (CRUD) — but they are **orphaned**: no rendered navigation links to any of them. They are reachable only by typing URLs.

HeartQuill is the intended production surface (owns `/`, owns the nav) but is a read-mostly shell. The legacy pages are the app's only editing workbench. They currently serve different purposes and neither can replace the other yet.

---

## Part 1: Route map

Routing lives entirely in `apps/web/src/app/App.jsx:23-57`. All routes render inside `<HeartQuillAppShell>` (App.jsx:25). The header nav renders exactly 4 items: Home, Explore, Planner, Builder (`HeartQuillShellPage.jsx:25-30`, rendered 263-275).

### Bucket A — HeartQuill shell routes

| Route | Component | File | Reachable? |
|---|---|---|---|
| `/` (App.jsx:27) | `HomeShellPage` | `pages/HeartQuillShellPage.jsx:319` | Yes — nav "Home" |
| `/home` (App.jsx:28) | `HomeShellPage` | same | Duplicate of `/`; URL-only (nav uses `/`) |
| `/onboarding/address` (App.jsx:29) | `AddressOnboardingPage` | `pages/AddressOnboardingPage.jsx:58` | Conditional — only via the notice shown when `getHome` 404s (shell:311, 338) |
| `/explore` (App.jsx:30) | `ExploreShellPage` | shell:488 | Yes — nav + Home hero button (shell:352) |
| `/planner` (App.jsx:31) | `PlannerShellPage` | shell:573 | Yes — nav + shell:355, 545 |
| `/builder` (App.jsx:32) | `BuilderShellPage` | shell:837 | Yes — nav |
| `/capabilities` (App.jsx:34) | `CapabilitiesShellPage` | shell:942 | **Orphaned** — zero links; page self-describes as "preserved off primary navigation" (shell:947-951) |
| `/internal/capabilities` (App.jsx:35) | `CapabilitiesShellPage` (internal) | shell:942 | **Orphaned** — URL-only |
| `/catalog` (App.jsx:36) | `CatalogShellPage` | shell:966 | **Orphaned** — URL-only |

### Bucket B — legacy routes (all API-backed, ALL orphaned from rendered navigation)

The only inter-legacy links found: `DashboardPage.jsx:177,309` → `/home-model` — but DashboardPage itself is unreachable except by URL.

| Route | Component | File |
|---|---|---|
| `/dashboard-legacy` (App.jsx:43) | `DashboardPage` | `pages/DashboardPage.jsx` |
| `/home-model` (App.jsx:44) | `HomeModelPage` | `pages/HomeModelPage.jsx` |
| `/design-builder` (App.jsx:45) | `SystemDesignBuilderPage` | `pages/SystemDesignBuilderPage.jsx` |
| `/product-library` (App.jsx:46) | `ProductLibraryPage` | `pages/ProductLibraryPage.jsx` |
| `/scenario-comparison` (App.jsx:47) | `ScenarioComparisonPage` | `pages/ScenarioComparisonPage.jsx` |
| `/design-advisor` (App.jsx:48) | `DesignAdvisorPage` | `pages/DesignAdvisorPage.jsx` |
| `/ai-context` (App.jsx:49) | `AIContextPage` | `pages/AIContextPage.jsx` |
| `/architecture` (App.jsx:50) | `ArchitecturePage` | `pages/ArchitecturePage.jsx` |
| `/takeoff-estimate` (App.jsx:51) | `TakeoffEstimatePage` | `pages/TakeoffEstimatePage.jsx` |

### Bucket C — redirects and dead routes

| Route | Redirect target | Line |
|---|---|---|
| `/experience` | → `/explore` (replace) | App.jsx:38 |
| `/twin` | → `/` | App.jsx:39 |
| `/scenario` | → `/planner` | App.jsx:40 |
| `/progress` | → `/builder` | App.jsx:41 |
| `*` | → `/` (catch-all) | App.jsx:53 |

No route points to a nonexistent component. `pages/C1ExperiencePage.jsx` has no route at all (dead code — see Part 8).

---

## Part 2: HeartQuill component-by-component data audit

All shell components live in `pages/HeartQuillShellPage.jsx`. Imports: `api` (line 4), ~17 mock exports from `lib/heartQuillMockData.js` (lines 5-22), `useApiQuery` (line 23). `useApiQuery` (`lib/useApiQuery.js:9-42`) performs a real `fetch` in a mount effect; `lib/api.js:13-38` fetches against `VITE_API_BASE_URL || http://localhost:8000` with demo auth headers.

| Component (lines) | Classification | Evidence |
|---|---|---|
| `HeartQuillAppShell` + `ShellHeader` (251-290) | FULLY-MOCK (static chrome) | Hardcoded `navItems` (25-30); hardcoded "Read-only shell" badge (277) |
| `HomeShellPage` (319-486) | **HYBRID** | LIVE: `getHome` (321), `getFacts` (324-326), `getNec220LoadCalculation` (327-329); home record rendered 364-385, facts table 475-481, NEC panel 446-462, KPI counts prefer backend (334-336). MOCK always: Energy Twin diagram (410) and "Selected object" panel (419-424). MOCK on failure: `staticHomeRecord` / `staticHomeFacts` fallbacks (56, 86-91), labeled via `ApiStatus` badges (389-393) |
| `HomeDiagram` (188-249) | **FULLY-MOCK** | Built exclusively from mock `twinNodes`/`twinEdges` (189-190); `aria-label="Mock Energy Twin diagram"` (193). Never populated from API |
| `HomeOnboardingNotice` (292-317) | Static copy, API-gated display | Renders only when `getHome` 404s (338, 342); links to `/onboarding/address` (311) |
| `ExploreShellPage` (488-571) | **FULLY-MOCK** | Mock `goals` (517; mockData:111-172), `learnTopics` (560; mockData:174-195); selection is local state only; UI says "Selections are local UI only" (514) |
| `PlannerShellPage` (573-677) | **HYBRID** | LIVE: `getPlannerSandboxTemplates` (576) → backend template cards via `toTemplateCard` (579-581, mapper 122-138), rendered 622-645, 672. MOCK: `liveTemplateFallback` on failure (581), 3 always-appended `draftTemplates` (582), hardcoded overlays (589, 640), mock diagram (620), mock upgrade path (651) |
| `TemplatesView` (679-726) | HYBRID | Renders whatever the templates prop holds (backend + mock drafts); shows real `registry.read_only` (686-688) |
| `SandboxView` (728-751) | **FULLY-MOCK** | `sandboxDrafts` (731; mockData:307-326) |
| `ComparisonsView` (766-800) | **FULLY-MOCK** | `comparisonRows` (787; mockData:328-335 — values literally say "55% mock") |
| `BuilderShellPage` (837-940) | **HYBRID (API-first)** | LIVE: `getHome` (838), `getEstimateReadiness` (840-842), `getProductPreferences` (843-845), `getProgramIntelligence` (846-848), `getEnergyPassport` (849-851); rows built from real readiness fields (802-835, rendered 880-885); backend summary grid rendered directly (904-921). MOCK: fallback rows only if all four reads absent (803-805); static "Readiness lane" checklist (932-936) |
| `CapabilitiesShellPage` (942-964) | **FULLY-MOCK** | `capabilities` (954; mockData:354-360) |
| `CatalogShellPage` (966-985) | **FULLY-MOCK** | `catalogItems` (975; mockData:362-368) |

No shell component is IMPORTED-NOT-CALLED or CALLED-NOT-RENDERED. Every `api.*` reference is invoked, and every successful response is rendered. The uniform pattern: real read → render; failed/absent read → labeled static placeholder.

---

## Part 3: Legacy pages data audit

| Page | Classification | api.js calls (evidence) |
|---|---|---|
| `DashboardPage` | **HYBRID** | `getHome`/`getLoadSummary`/`getDesigns`/`getScenarios` (152-155). LIVE: known-facts section interpolates real fields (7-66, rendered 233-238). HYBRID: "Opportunity paths" (68-99) and "Complete the Twin" (101-149) — API data only selects which hardcoded string shows. Static: hero SVG, grounding, CTA |
| `AddressOnboardingPage` | **LIVE** | `getMe` (63) drives account options (125-133); `submitAddressOnboarding` (81-83) drives navigation (84-91) |
| `AIContextPage` | **LIVE** | `getDesigns` (12), `getAIContext` (18-22); all panels render response (73-186) |
| `ArchitecturePage` | **LIVE** | `getArchitectureVisibility` (192); entire page renders from the graph response (256-518) |
| `DesignAdvisorPage` | **LIVE** | `getDesigns` (1390), `getDesignAdvisor` (1396-1400), `getAIContext` (1402-1406), `getPlannerIntelligence` (1408-1412); ~30 presentational subcomponents render only props derived from responses; zero mock constants in the file |
| `HomeModelPage` | **LIVE (full CRUD)** | Queries: `getHome`/`getLoads`/`getEquipmentLocations`/`getEstimatedPathways`/`getLoadTemplates`/`getDesigns` (683-688). Mutations: `updateHome` (230), `createBuilding`/`updateBuilding` (279), `createPanel`/`updatePanel` (335), `createLoad`/`updateLoad` (388, 602), equipment locations (451), pathways (509) |
| `ProductLibraryPage` | **LIVE** | `getProductLibrary` (18); rendered per ecosystem/type (57-133) |
| `ScenarioComparisonPage` | **LIVE (CRUD)** | `getHome`/`getScenarios`/`getDesigns`/`compareScenarios` (303-306); `createScenario`/`updateScenario` (232-233) |
| `SystemDesignBuilderPage` | **LIVE (CRUD)** | Queries 313-316; `createDesignEquipment`/`updateDesignEquipment` (118-123), `deleteDesignEquipment` (135 — **broken, see Part 4**), `createDesign`/`updateDesign` (218) |
| `TakeoffEstimatePage` | **LIVE** | `getDesigns` (13), `generateTakeoff`/`getTakeoff` (18-22), `getEstimatePlaceholder` (23) |

No legacy page is FULLY-MOCK. All `heartQuillMockData.js` usage is confined to `HeartQuillShellPage.jsx`.

---

## Part 4: api.js coverage

`api` is exported as a single object (`api.js:44`); all 12 importing files invoke at least one method, so there are no import-only files. Backend registration: routers in the `main.py:88-111` loop are mounted at both bare path and `/api`; routers added via `api_router.include_router` (main.py:113-133) are `/api`-only. api.js always prefixes `/api` (api.js:40-42), so both resolve. All route decorators were verified to exist in the router modules.

| # | Function (api.js line) | Endpoint | Invoked by | Backend route | Status |
|---|---|---|---|---|---|
| 1 | `baseUrl` (45) | — | none | — | UNUSED export |
| 2 | `getMe` (46) | GET /api/auth/me | AddressOnboardingPage:63 | auth/router.py:35 | OK |
| 3 | `getHome` (47) | GET /api/homes | 6 live pages + dead C1 | homes/router.py:15 | OK |
| 4 | `getAllHomes` (48) | GET /api/homes/all | none | homes/router.py:27 | UNUSED |
| 5 | `createHome` (49) | POST /api/homes | none | homes/router.py:34 | UNUSED |
| 6 | `updateHome` (50) | PATCH /api/homes/{id} | HomeModelPage:230 | homes/router.py:40 | OK |
| 7 | `submitAddressOnboarding` (51) | POST /api/onboarding/address | AddressOnboardingPage:82 | onboarding/router.py:41 | OK |
| 8 | `getBuildings` (54) | GET /api/buildings | none | buildings/router.py:15 | UNUSED |
| 9 | `createBuilding` (55) | POST /api/buildings | HomeModelPage:279 | buildings/router.py:27 | OK |
| 10 | `updateBuilding` (56) | PATCH /api/buildings/{id} | HomeModelPage:279 | buildings/router.py:33 | OK |
| 11 | `getPanels` (59) | GET /api/panels | none | panels/router.py:15 | UNUSED |
| 12 | `createPanel` (60) | POST /api/panels | HomeModelPage:335 | panels/router.py:27 | OK |
| 13 | `updatePanel` (61) | PATCH /api/panels/{id} | HomeModelPage:335 | panels/router.py:34 | OK |
| 14 | `getLoads` (63) | GET /api/loads | HomeModelPage:684 | loads/router.py:22 | OK |
| 15 | `getLoadSummary` (64) | GET /api/loads/summary | DashboardPage:153 | loads/router.py:29 | OK |
| 16 | `createLoad` (65) | POST /api/loads | HomeModelPage:388,602 | loads/router.py:36 | OK |
| 17 | `updateLoad` (66) | PATCH /api/loads/{id} | HomeModelPage:388 | loads/router.py:45 | OK |
| 18 | `getLoadTemplates` (68) | GET /api/load-templates | HomeModelPage:687 | planning/router.py:96 | OK |
| 19 | `getDesigns` (70) | GET /api/designs | 7 pages | designs/router.py:22 | OK |
| 20 | `createDesign` (71) | POST /api/designs | SystemDesignBuilderPage:218 | designs/router.py:27 | OK |
| 21 | `updateDesign` (72) | PATCH /api/designs/{id} | SystemDesignBuilderPage:218 | designs/router.py:33 | OK |
| 22 | `getDesignEquipment` (74) | GET /api/designs/{id}/equipment | none | designs/router.py:49 | UNUSED |
| 23 | `createDesignEquipment` (75) | POST /api/designs/{id}/equipment | SystemDesignBuilderPage:118 | designs/router.py:60 | OK |
| 24 | `updateDesignEquipment` (77) | PATCH .../equipment/{eid} | SystemDesignBuilderPage:123 | designs/router.py:86 | OK |
| 25 | `deleteDesignEquipment` (79-97) | DELETE .../equipment/{eid} | SystemDesignBuilderPage:135 | designs/router.py:114 (204) | **BUG — see below** |
| 26 | `getProductLibrary` (99) | GET /api/product-library | SDB:315, ProductLibraryPage:18 | product_library/router.py:15 | OK |
| 27 | `getSourceDocuments` (100) | GET /api/source-documents | none | source_documents/router.py:13 | UNUSED |
| 28 | `getProvenance` (101) | GET /api/provenance | none | provenance/router.py:15 | UNUSED |
| 29 | `getRuleProvenance` (102) | GET /api/rule-provenance | none | rule_provenance/router.py:13 | UNUSED |
| 30 | `getCompatibilityIssues` (103) | GET /api/compatibility-rules/issues | none | compatibility_rules/router.py:16 | UNUSED |
| 31 | `evaluateDesign` (104) | GET /api/compatibility-rules/evaluate/{id} | none | compatibility_rules/router.py:21 | UNUSED |
| 32 | `getScenarios` (106) | GET /api/scenarios | Dashboard:155, ScenarioComparison:304 | scenarios/router.py:31 | OK |
| 33 | `compareScenarios` (107) | GET /api/scenarios/compare | ScenarioComparisonPage:306 | scenarios/router.py:37 | OK |
| 34 | `createScenario` (108) | POST /api/scenarios | ScenarioComparisonPage:233 | scenarios/router.py:54 | OK |
| 35 | `updateScenario` (109) | PATCH /api/scenarios/{id} | ScenarioComparisonPage:233 | scenarios/router.py:67 | OK |
| 36 | `getEquipmentLocations` (112) | GET /api/equipment/locations | SDB:316, HomeModel:685 | equipment/router.py:15 | OK |
| 37 | `createEquipmentLocation` (113) | POST /api/equipment/locations | HomeModelPage:451 | equipment/router.py:20 | OK |
| 38 | `updateEquipmentLocation` (115) | PATCH .../locations/{id} | HomeModelPage:451 | equipment/router.py:31 | OK |
| 39 | `getEstimatedPathways` (118) | GET /api/estimated-pathways | HomeModelPage:686 | planning/router.py:33 | OK |
| 40 | `createEstimatedPathway` (119) | POST /api/estimated-pathways | HomeModelPage:509 | planning/router.py:48 | OK |
| 41 | `updateEstimatedPathway` (121) | PATCH .../{id} | HomeModelPage:509 | planning/router.py:61 | OK |
| 42 | `getTakeoff` (124) | GET /api/takeoffs/current | TakeoffEstimatePage:20 | takeoffs/router.py:14 | OK |
| 43 | `generateTakeoff` (125) | GET /api/takeoffs/generate/{id} | TakeoffEstimatePage:20 | takeoffs/router.py:22 | OK |
| 44 | `getDesignAdvisor` (126) | GET /api/design-advisor/summary/{id} | DesignAdvisorPage:1398 | design_advisor/router.py:13 | OK |
| 45 | `getPlannerIntelligence` (127) | GET /api/planner-intelligence/designs/{id}/summary | DesignAdvisorPage:1410 | planner_intelligence/router.py:65 | OK |
| 46 | `getAIContext` (128) | GET /api/ai-context/design/{id} | AIContext:20, DesignAdvisor:1404 | ai_context/router.py:13 | OK |
| 47 | `getEstimatePlaceholder` (129) | GET /api/estimates/placeholder | TakeoffEstimatePage:23 | estimates/router.py:6 | OK |
| 48 | `getArchitectureVisibility` (130) | GET /api/system-visibility/architecture | ArchitecturePage:192 | system_visibility/router.py:9 | OK |
| 49 | `getFacts` (131) | GET /api/homes/{id}/facts | HeartQuillShellPage:324 (+dead C1) | facts/router.py:14 | OK |
| 50 | `getGeometryExport` (132) | GET /api/homes/{id}/geometry/export | only dead C1ExperiencePage:43 | geometry/router.py:52 | DEAD IN PRACTICE |
| 51 | `getNec220LoadCalculation` (133) | GET /api/homes/{id}/load-calculations/nec-220 | HeartQuillShellPage:327 (+dead C1) | nec_load_calculation/router.py:12 | OK |
| 52 | `getPrivacyExport` (134) | GET /api/privacy/homes/{id}/export | none | privacy/router.py:15 | UNUSED |
| 53 | `getPlannerSandboxTemplates` (135) | GET /api/planner-sandbox/templates | HeartQuillShellPage:576 | planner_sandbox/router.py:9 | OK |
| 54 | `getEstimateReadiness` (136) | GET /api/estimate-readiness/homes/{id} | HeartQuillShellPage:840 | estimate_readiness/router.py:11 | OK |
| 55 | `getProductPreferences` (137) | GET /api/product-preferences/homes/{id} | HeartQuillShellPage:843 | product_preferences/router.py:11 | OK |
| 56 | `getEnergyPassport` (138) | GET /api/energy-passport/homes/{id} | HeartQuillShellPage:849 | energy_passport/router.py:11 | OK |
| 57 | `getProgramIntelligence` (139) | GET /api/program-intelligence/homes/{id} | HeartQuillShellPage:846 | program_intelligence/router.py:11 | OK |

### Flag summary

- **Imported but never called:** none (single-object export pattern).
- **Exported but never invoked (12):** `baseUrl`, `getAllHomes`, `createHome`, `getBuildings`, `getPanels`, `getDesignEquipment`, `getSourceDocuments`, `getProvenance`, `getRuleProvenance`, `getCompatibilityIssues`, `evaluateDesign`, `getPrivacyExport`. Plus `getGeometryExport`, whose only caller is the dead C1ExperiencePage.
- **Called but backend missing:** none. Every called endpoint has a verified route decorator and registration.
- **request() bypass (1 confirmed, the only one):** `deleteDesignEquipment` (api.js:79-97) hand-rolls `fetch` without `authHeaders()`. Concrete impact: `/api/designs` is in `HOME_DATA_PREFIXES` (`apps/api/app/security/auth.py:30`), so `HomeAccessMiddleware` runs; a missing `x-user-id` makes `scaffold_principal_from_headers` return `None` (`security/principal.py:113-115`) → **401 "Authentication required"** (auth.py:61-73). Equipment deletion from SystemDesignBuilderPage:135 fails whenever scaffold header auth is active. Likely reason for the bypass: the DELETE returns 204 and the shared `request()` unconditionally calls `response.json()` (api.js:37), which throws on an empty body. A proper fix needs both `authHeaders()` and 204 handling in `request()`.

---

## Part 5: Design advisor / planner intelligence placement

- `getPlannerIntelligence(designId)` exists at api.js:127, calls exactly `GET /api/planner-intelligence/designs/{design_id}/summary` through the shared `request()` helper (auth headers included).
- **Its only caller is a legacy page**: `DesignAdvisorPage.jsx:1408-1412`, routed at `/design-advisor` (App.jsx:48). No HeartQuill shell component calls it.
- **It renders real data, not mock**: `plannerIntelligenceQuery.data` feeds `PlannerIntelligencePanel` (DesignAdvisorPage.jsx:1513-1514; panel at line 188), which reads `summary.blocks.*` and `summary.limitations` directly. Zero mock constants in the file. Loading/error/empty states handled (1508-1518).
- **`getDesignAdvisor` is still called — by the same component** (DesignAdvisorPage.jsx:1396-1400), rendered in the Advisor Summary and Compatibility sections (1446-1501, 1525-1570). The page consumes the old advisor endpoint, the new planner-intelligence facade, and `getAIContext` side by side.
- Backend verified: `planner_intelligence/router.py:17` (prefix), decorator at line 65 with a real handler doing design-scoped authz and 404/403 auditing; registered via `api_router` (main.py:131) mounted with `/api` prefix (main.py:134).

**Net effect: the newest backend capability (planner-intelligence slice 1) is only surfaced on an orphaned legacy page that no navigation reaches.**

---

## Part 6: Address onboarding flow

- File/route: `pages/AddressOnboardingPage.jsx:58`, served at `/onboarding/address` (App.jsx:29).
- **Reachability**: not in the primary nav. The only link is `HeartQuillShellPage.jsx:311` inside `HomeOnboardingNotice`, which renders **only** when `api.getHome` returns 404 (`isNoHomeError` shell:67-69; gate shell:338, 342). Non-404 errors deliberately do not show it (shell:394-399). So the flow is reachable exactly in the "empty database / no home record" state.
- **The flow is real end-to-end**: `api.getMe` populates account options (page:63); submit runs `api.submitAddressOnboarding` → real `POST /api/onboarding/address` (page:81-83; api.js:51) via `useApiMutation` (real await, no mocking).
- **Post-success navigation**: `navigate(response.next_route || "/", { replace: true, state: {...} })` (page:84-91). The backend hardcodes `next_route="/"` (`apps/api/app/onboarding/router.py:270`; confirmed by `apps/api/tests/test_address_onboarding.py:47`).
- **Where the user lands**: `/` → `HomeShellPage` remounts, `getHome` now succeeds, the onboarding notice disappears, and the home record panel renders **real created data** (name/address/service/utility, provenance "Backend user_entered"). The gated `getFacts`/`getNec220LoadCalculation` queries fire with the new homeId.
- **Caveats on landing**: a brand-new home has no facts, so the facts table shows placeholders labeled "Static shell placeholder" (shell:85-91); the Energy Twin diagram remains mock regardless (shell:410). The router `state` payload passed on navigate is never read (`HomeShellPage` has no `useLocation`) — dead-ended.

---

## Part 7: Gap matrix (user-flow order)

| Screen/Section | Route | Component file | Data source | api.js function(s) | Backend endpoint(s) | Backend exists? |
|---|---|---|---|---|---|---|
| Address onboarding | `/onboarding/address` | AddressOnboardingPage.jsx | LIVE | getMe, submitAddressOnboarding | /api/auth/me, POST /api/onboarding/address | Yes |
| Home — record panel | `/` | HeartQuillShellPage.jsx (HomeShellPage) | LIVE (mock fallback) | getHome | GET /api/homes | Yes |
| Home — known facts | `/` | same | LIVE (mock fallback) | getFacts | GET /api/homes/{id}/facts | Yes |
| Home — NEC panel | `/` | same | LIVE (mock fallback) | getNec220LoadCalculation | GET /api/homes/{id}/load-calculations/nec-220 | Yes |
| Home — Energy Twin diagram | `/` | same (HomeDiagram) | **MOCK always** | none | — (getBuildings/getPanels/getLoads exist unused) | Yes (unwired) |
| Home — selected-object panel | `/` | same | **MOCK always** | none | — | — |
| Explore — goals + learn | `/explore` | same (ExploreShellPage) | **FULLY-MOCK** | none | — | — |
| Planner — template cards | `/planner` | same (PlannerShellPage) | LIVE (mock fallback + 3 mock drafts) | getPlannerSandboxTemplates | GET /api/planner-sandbox/templates | Yes |
| Planner — canvas/overlays/upgrade path | `/planner` | same | **MOCK always** | none | — | — |
| Planner — sandbox view | `/planner` | same (SandboxView) | **FULLY-MOCK** | none | — | — |
| Planner — comparisons view | `/planner` | same (ComparisonsView) | **FULLY-MOCK** | none | — (compareScenarios exists, used only by legacy) | Yes (unwired) |
| Builder — readiness rows + summary | `/builder` | same (BuilderShellPage) | LIVE (mock fallback) | getEstimateReadiness, getProductPreferences, getProgramIntelligence, getEnergyPassport | 4 × GET /api/*/homes/{id} | Yes |
| Capabilities | `/capabilities` | same (CapabilitiesShellPage) | **FULLY-MOCK** (orphaned route) | none | — | — |
| Catalog | `/catalog` | same (CatalogShellPage) | **FULLY-MOCK** (orphaned route) | none | — | — |
| Dashboard (legacy) | `/dashboard-legacy` | DashboardPage.jsx | HYBRID | getHome, getLoadSummary, getDesigns, getScenarios | 4 endpoints | Yes |
| Home model editor (legacy) | `/home-model` | HomeModelPage.jsx | LIVE (full CRUD) | 13 functions | homes/buildings/panels/loads/equipment/pathways/load-templates | Yes |
| Design builder (legacy) | `/design-builder` | SystemDesignBuilderPage.jsx | LIVE (CRUD; delete broken) | 8 functions | designs + equipment | Yes (DELETE 401s from UI) |
| Product library (legacy) | `/product-library` | ProductLibraryPage.jsx | LIVE | getProductLibrary | GET /api/product-library | Yes |
| Scenario comparison (legacy) | `/scenario-comparison` | ScenarioComparisonPage.jsx | LIVE (CRUD) | 6 functions | scenarios + compare | Yes |
| Design advisor (legacy) | `/design-advisor` | DesignAdvisorPage.jsx | LIVE | getDesigns, getDesignAdvisor, getAIContext, getPlannerIntelligence | 4 endpoints | Yes |
| AI context (legacy) | `/ai-context` | AIContextPage.jsx | LIVE | getDesigns, getAIContext | 2 endpoints | Yes |
| Architecture map (legacy) | `/architecture` | ArchitecturePage.jsx | LIVE | getArchitectureVisibility | GET /api/system-visibility/architecture | Yes |
| Takeoff/estimate (legacy) | `/takeoff-estimate` | TakeoffEstimatePage.jsx | LIVE | getDesigns, getTakeoff, generateTakeoff, getEstimatePlaceholder | 4 endpoints | Yes |

---

## Part 8: Dead code

**Orphaned component files (imported nowhere):**
1. `apps/web/src/pages/C1ExperiencePage.jsx` (105 lines) — LIVE-shaped code (getHome/getFacts/getGeometryExport/getNec220LoadCalculation) that never executes; its old `/experience` path now redirects to `/explore`.
2. `apps/web/src/components/Shell.jsx` (22 lines) — superseded by `HeartQuillAppShell`.
3. `apps/web/src/components/StatCard.jsx` (10 lines) — ArchitecturePage uses raw markup instead.

**Orphaned lib modules:**
4. `apps/web/src/lib/uiRegistry.js` (603 lines) — no JS/JSX file imports it. Only referenced as a path *string* in `apps/api/app/services/system_visibility.py:1567` and in `architecture-map.html` (which defines its own independent inline copy).

**api.js members invoked by no live component (13):** `baseUrl`, `getAllHomes`, `createHome`, `getBuildings`, `getPanels`, `getDesignEquipment`, `getSourceDocuments`, `getProvenance`, `getRuleProvenance`, `getCompatibilityIssues`, `evaluateDesign`, `getPrivacyExport`, `getGeometryExport` (dead-page-only).

**Dead exports inside live modules:** `lib/trust.js` `designStatusExplanations` (line 1, only used internally); `lib/heartQuillMockData.js` `templates` (line 197, only used internally).

**Routes to nonexistent components:** none. **CSS imported by no component:** none (both stylesheets loaded in `main.jsx:6-7`).

---

## Part 9: Verdict

**1. Is HeartQuill the intended production frontend, with legacy kept only for reference?**
HeartQuill is the intended production *surface* — it owns `/`, the navigation, and the visual system, and it self-describes as a "Read-only shell." But the legacy pages are not mere reference: they are the **only place any data can be created or edited** (all CRUD lives in HomeModelPage, SystemDesignBuilderPage, ScenarioComparisonPage), and the only place the newest backend work (planner-intelligence, design advisor, AI context, architecture visibility, takeoffs) is surfaced. Today the app is a read-mostly showroom (HeartQuill) sitting in front of an unlinked workshop (legacy). They serve different purposes, and neither is complete without the other.

**2. If a user hit the app today, which routes show real backend data and which show mock/nothing?**
With a seeded backend: `/` shows real home record, facts, and NEC data (but a mock diagram); `/planner` shows real template cards (on a mock canvas); `/builder` shows real readiness from four endpoints; `/onboarding/address` works end-to-end. `/explore`, `/catalog`, `/capabilities` are 100% mock. All nine legacy routes show real data — but only if the user types the URL, because nothing links to them. With an **empty** backend, every HeartQuill panel falls back to labeled static data, and the app looks fully mock — which is exactly how the two conflicting assessments arose.

**3. Minimum work for one complete live flow (onboarding → home view → one meaningful screen)?**
The flow onboarding → home record/facts/NEC → builder readiness is **already live end-to-end**. The minimum work to make it feel real rather than half-mocked:
- Wire `HomeDiagram` to real data (`HeartQuillShellPage.jsx:188-249`): replace `twinNodes`/`twinEdges` with entities from `getBuildings`, `getPanels`, `getLoads` — all three api.js functions and backend endpoints already exist and are currently unused. This is the single largest mock surface on the landing page.
- Make onboarding reachable deliberately (a nav or hero entry point), not only via the 404-gated notice.
- Optional polish: suppress the "Static shell placeholder" facts rows for a brand-new home in favor of an honest empty state.
No new backend work is required for this flow.

**4. Should legacy pages be deleted, kept as fallback, or absorbed first?**
**Absorb first — do not delete.** HeartQuill has zero mutation capability; deleting legacy removes the only way to edit the home model, build designs, or manage scenarios. It would also orphan the only consumers of `getPlannerIntelligence`, `getDesignAdvisor`, `getAIContext`, `getArchitectureVisibility`, and the takeoff flow. The rational sequence: (a) absorb HomeModelPage's CRUD into a HeartQuill editing surface, (b) surface planner-intelligence inside the shell (its natural home is the Planner or a design view), (c) then retire legacy pages one at a time as each capability lands. `DashboardPage` (hybrid, superseded by `HomeShellPage`) and dead files (C1ExperiencePage, Shell.jsx, StatCard.jsx, uiRegistry.js) can go now without loss.

**5. Single most important frontend file to fix/wire first?**
`apps/web/src/lib/api.js` — for two reasons. First, the confirmed `deleteDesignEquipment` bug (missing auth headers → 401) breaks the only delete mutation in the app; fixing `request()` to handle 204 responses removes the reason the bypass exists and hardens every future mutation. Second, api.js is the seam every screen shares: its 13 unused functions (`getBuildings`, `getPanels`, `getLoads` for the diagram; `compareScenarios` for ComparisonsView; `getCompatibilityIssues`/`evaluateDesign` for planner overlays) are exactly the wiring the HeartQuill mock sections need. After api.js, the highest-leverage file is `HeartQuillShellPage.jsx` (985 lines, all shell pages in one file) — splitting it per-page is the precondition for wiring Explore/Planner/Builder without merge chaos.
