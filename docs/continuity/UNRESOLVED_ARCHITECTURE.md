# Unresolved Architecture

## Current Open Areas

- field-level provenance coverage
- versioned takeoff snapshot semantics
- full advisor payload revision storage
- deployment lineage manifest
- topology lifecycle graph
- contractor-safe output package
- utility-safe abstraction model
- role-aware API view implementation and permission binding
- field-level data classification policy
- audit trail and change history
- delete/archive behavior
- production auth and billing enforcement

## Migration Risks

- schema changes may outrun Alembic practice
- local SQLite databases may need reseeding after provenance or revision changes
- frontend GET contracts remain compatibility-sensitive
- seed demo records may be mistaken for verified facts
- existing APIs may be mistaken for RBAC-filtered or contractor/utility-ready views

## Trust And Provenance Gaps

- verification status does not equal engineering validity
- recommendation profiles remain planning-only
- roof-readiness is not measured roof capacity
- scenario revisions are compact lineage records, not full replayable design histories
- data classification is a design boundary, not current runtime enforcement

## Deferred Decisions

- when to persist takeoff snapshots
- when to create a general revision graph
- how to model field verification
- how to represent operational topology
- how to expose scoped contractor and utility views
- how to bind future RBAC roles to scoped API views without breaking existing contracts
