# C1 / Phases 18-19 UI Shell Closeout

## Summary

C1 / Phases 18-19 UI shell is implemented as an additive React route on the existing frontend. It adds local A2 auth headers to the API client and a four-surface Explore/Twin/Plan/Build workspace.

## Runtime Files

- `apps/web/src/lib/api.js`
- `apps/web/src/app/App.jsx`
- `apps/web/src/pages/C1ExperiencePage.jsx`
- `apps/web/src/styles/global.css`

## Completed Scope

- Added local API auth headers from `VITE_API_USER_ID` and `VITE_API_HOME_ACCESS`.
- Added `/experience` route.
- Added Explore/Twin/Plan/Build segmented surface control.
- Added authenticated reads for home, facts, geometry export, and NEC load calculation.
- Added lightweight HomeDiagram-style SVG/CSS visual using geometry/shading metadata where present.
- Added fact confidence, load-calculation, and build-posture summary panels.

## Verification

- `npm run build` passed in `apps/web`.
- `git diff --check` passed.

## Boundary

C1 does not add dependencies, lockfile rewrites, Three.js package, external services, production auth provider, session/cookie login, deploy, push, billing, operational control, final design claims, pricing, proposal generation, permissioned export UI, photo upload, or evidence intake.

## Next Action

Run frontend build verification, commit the completed loop if verification passes, then continue to B3 hardened evidence intake.
