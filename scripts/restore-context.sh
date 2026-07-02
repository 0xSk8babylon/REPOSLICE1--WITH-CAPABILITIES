#!/usr/bin/env bash
set -euo pipefail

latest_handoff=""
if ls docs/handoffs/*.md >/dev/null 2>&1; then
  latest_handoff=$(ls -1t docs/handoffs/*.md | head -n 1)
fi

cat <<EOF
Discovery layer:
- AGENTS.md
- PROJECT_STATE.md
- discovery-index.md
- .codex/skills/repo-memory-map/SKILL.md
- .codex/skills/repo-guardrails/SKILL.md

Canonical continuity workflow:
- docs/session-continuity/continuity-workflow.md
EOF

if [[ -n "${latest_handoff}" ]]; then
  printf '\nLatest handoff:\n- %s\n' "${latest_handoff}"
fi
