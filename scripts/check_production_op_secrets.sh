#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"

op_vault="${OP_VAULT:-TwinEnergy}"
op_item_id="${OP_ITEM_ID:-j3qbtqgq3ywnrem3hxxcx2ngle}"
template_path="${repo_root}/scripts/templates/production-op.env.tpl"

required_fields=(
  DATABASE_URL
  DATABASE_PUBLIC_URL
  PGHOST
  PGPORT
  PGUSER
  PGPASSWORD
  PGDATABASE
)

secret_ref() {
  local field="$1"
  printf 'op://%s/%s/%s' "${op_vault}" "${op_item_id}" "${field}"
}

echo "1Password production secret preflight"
echo "op auth working: pending"

if [ ! -f "${template_path}" ]; then
  echo "template exists: no"
  exit 1
fi

echo "template exists: yes"

if ! command -v op >/dev/null 2>&1; then
  echo "op installed: no"
  echo "op auth working: no"
  exit 1
fi

echo "op installed: yes"

if op whoami >/dev/null 2>&1; then
  echo "op auth working: yes"
else
  echo "op auth working: no"
  exit 1
fi

if op item get "${op_item_id}" --vault "${op_vault}" >/dev/null 2>&1; then
  echo "production item exists: yes"
else
  echo "production item exists: no"
  exit 1
fi

missing_fields=()
for field in "${required_fields[@]}"; do
  if ! op read "$(secret_ref "${field}")?attribute=title" >/dev/null 2>&1; then
    missing_fields+=("${field}")
  fi
done

if [ "${#missing_fields[@]}" -eq 0 ]; then
  echo "required fields present: yes"
else
  echo "required fields present: no"
  printf 'missing field: %s\n' "${missing_fields[@]}"
  exit 1
fi

echo "template: scripts/templates/production-op.env.tpl"
echo "proposed Gate 2 command, do not run until explicitly approved:"
printf "%s\n" "op run --env-file scripts/templates/production-op.env.tpl -- bash -lc 'cd apps/api && python3 -m alembic upgrade head'"
