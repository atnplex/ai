#!/bin/bash
# MCP Server Launcher with Secrets Resolution
#
# Decrypts the age file and exports secrets as environment variables
# before exec-ing the MCP server process.
#
# Resolution: env → age file (persistent) → BWS (remote, write-back to age)
#
# Usage: mcp_with_secrets.sh <command> [args...]

set -euo pipefail

# ── Paths ────────────────────────────────────────────────────────────────
NAMESPACE="${NAMESPACE:-/atn}"
SECRETS_DIR="${NAMESPACE}/.config/secrets"
AGE_KEY="${SECRETS_DIR}/age.key"
AGE_FILE="${SECRETS_DIR}/secrets.age"

# ── Logging ──────────────────────────────────────────────────────────────
log() { echo "[mcp-secrets] $*" >&2; }
ok() { echo "[mcp-secrets] ✓ $*" >&2; }
warn() { echo "[mcp-secrets] ! $*" >&2; }

# ── MCP Server → Required env vars mapping ───────────────────────────────
declare -A MCP_SECRETS=(
  [github]="GITHUB_PERSONAL_ACCESS_TOKEN"
  [perplexity]="PERPLEXITY_API_KEY"
  [cloudflare]="CLOUDFLARE_ACCOUNT_ID CLOUDFLARE_API_TOKEN"
)

# ── Load all secrets from age file into env ──────────────────────────────
load_age_secrets() {
  if [[ ! -f "$AGE_FILE" ]] || [[ ! -f "$AGE_KEY" ]]; then
    warn "Age file or key not found at $SECRETS_DIR"
    return 1
  fi

  local json
  json=$(timeout 5 age -d -i "$AGE_KEY" "$AGE_FILE" 2>/dev/null) || {
    warn "Could not decrypt age file"
    return 1
  }

  if [[ -z "$json" ]]; then
    warn "Age file decrypted but empty"
    return 1
  fi

  # Parse JSON and export each key
  local keys
  keys=$(echo "$json" | jq -r 'keys[]' 2>/dev/null) || return 1

  while IFS= read -r key; do
    [[ -z "$key" ]] && continue
    # Don't override existing env vars
    if [[ -z "${!key:-}" ]]; then
      local val
      val=$(echo "$json" | jq -r --arg k "$key" '.[$k] // empty' 2>/dev/null)
      if [[ -n "$val" ]]; then
        export "$key=$val"
      fi
    fi
  done <<<"$keys"
}

# ── Export secrets for the matched MCP server ────────────────────────────
export_mcp_secrets() {
  local mcp_cmd="$*"

  for pattern in "${!MCP_SECRETS[@]}"; do
    if [[ "$mcp_cmd" == *"$pattern"* ]]; then
      # shellcheck disable=SC2086
      for env_var in ${MCP_SECRETS[$pattern]}; do
        if [[ -z "${!env_var:-}" ]]; then
          warn "Secret '$env_var' not available for MCP server matching '$pattern'"
        fi
      done
    fi
  done
}

# ── Main ─────────────────────────────────────────────────────────────────
main() {
  if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <mcp-command> [args...]" >&2
    exit 1
  fi

  # Load all secrets from age file into env
  load_age_secrets || true

  # Verify required secrets are present
  export_mcp_secrets "$@"

  # Hardcode Cloudflare paths to ensure consistency
  if [[ "$*" == *"cloudflare"* ]]; then
    export XDG_CONFIG_HOME="/atn/.gemini/antigravity/.config"
    export WRANGLER_CONFIG="/atn/.gemini/antigravity/.config/wrangler"
  fi

  exec "$@"
}

main "$@"
