# Domain Map

## System Domains

### Accounts

- Purpose: future ownership and subscription scaffolding
- Current state: persisted, no auth or authorization
- Key entities: `Account`
- Boundary: ownership metadata only, not session/auth logic

### Homes

- Purpose: persistent property model
- Current state: persisted and exposed through the main read path
- Key entities: `Home`, `BuildingStructure`, `ElectricalPanel`
- Boundary: property facts only, not engineering conclusions

### Loads

- Purpose: structured consumption and backup-priority modeling
- Current state: persisted
- Key entities: `Load`, `LoadTemplate`
- Boundary: load records and templates, not final backup runtime modeling

### Designs

- Purpose: candidate energy system architectures over time
- Current state: persisted
- Key entities: `EnergySystemDesign`, `DesignEquipment`, `DesignGoalPreset`
- Boundary: design topology and intent, not permitting packages

### Equipment / Product Library

- Purpose: structured product and location records
- Current state: persisted, placeholder-heavy
- Key entities: `EquipmentProduct`, `EquipmentLocation`
- Boundary: factual product data and physical siting placeholders

### Compatibility Rules

- Purpose: structured explanation contracts for fit and planning issues
- Current state: persisted issue records plus placeholder evaluation service
- Key entities: `CompatibilityIssue`
- Boundary: rule outputs, not freeform prose generation

### Scenarios

- Purpose: compare pathway tradeoffs
- Current state: persisted
- Key entities: `Scenario`, `EstimatedPathway`
- Boundary: comparative planning views, not final financial products

### Takeoffs / Estimates

- Purpose: eventual estimating pipeline
- Current state: persisted placeholder takeoff request and line items
- Key entities: `TakeoffRequest`, `TakeoffLineItem`
- Boundary: planning placeholders only, not procurement-grade estimating

### AI Context / Advisor

- Purpose: grounded explanation layer
- Current state: runtime composition on top of persisted data
- Key endpoints: `/design-advisor/summary/{design_id}`, `/ai-context/design/{design_id}`
- Boundary: explain and summarize; never invent authoritative facts

## File-Level Ownership Map

- App bootstrap: `apps/api/app/main.py`
- DB engine/session: `apps/api/app/core/database.py`
- ORM definitions: `apps/api/app/core/models.py`
- Repositories: `apps/api/app/core/repository.py`
- Seed runtime: `apps/api/app/seed/runtime.py`
- API schemas: domain `schemas.py` files
- Frontend API client: `apps/web/src/lib/api.js`
- Frontend live pages: `apps/web/src/pages/*`

## Domain Coupling Warnings

- The current `Home` GET contract is frontend-critical because it includes nested buildings and panels.
- The current design/advisor/context pages depend on stable design IDs and current seed availability.
- Takeoff generation currently assumes seeded/persisted takeoff records rather than deriving line items from live design topology.

