# 2026-05-25 Deterministic Backup Load Selection

## What Changed

- Added a deterministic backup-load selection layer behind recommendation outputs.
- Recommendation payloads now expose `backup_load_selection` with selected scope label, rule basis, priority band, planning-gap warning, and inspectability metadata.
- Battery, solar, and panel/service guidance now consume the explicit selected scope instead of silently treating all backup-tagged intent as equivalent.
- Panel/service architecture recommendations now stay narrower when broader backup scope is not actually recorded.

## Constraints Preserved

- No migration or persistence change
- No inverter sizing
- No generator sizing
- No smart-panel modifier logic redesign
- No exposed engineering formulas
- Additive API/UI change only

## Verification

- `python3 -m compileall apps/api/app` passed
- `npm run build` passed in `apps/web`

## Exact Next Target

Add the next architecture-fit recommendation slice that explains how current equipment mix and backup-path posture shift profile fit now that selected backup scope is explicit and inspectable.
