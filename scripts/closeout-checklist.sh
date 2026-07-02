#!/usr/bin/env bash
set -euo pipefail

cat <<'EOF'
Closeout checklist:
- update PROJECT_STATE.md
- update discovery-index.md if routing or canonical references changed
- update docs/CURRENT_STATE.md
- update docs/NEXT_STEPS.md
- update docs/ACTIVE_TASKS.md if status changed
- append docs/SESSION_LOG.md
- update only the affected docs/session-continuity/* files
- create a dated docs/handoffs/*.md entry for real milestones or useful continuity records
EOF
