#!/bin/bash
set -euo pipefail

# Path to the AI repository
REPO_DIR="/atn/ai"

# Ensure we are in the repo directory
cd "$REPO_DIR"

log() { echo "[sync-ai] $*" >&2; }
error() {
  echo "[sync-ai] ERROR: $*" >&2
  exit 1
}
warn() { echo "[WARN] $1" >&2; }

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
  log "Uncommitted changes detected. Stashing..."
  git stash push -m "Auto-stash before sync $(date)"
  STASHED=1
else
  STASHED=0
fi

# Fetch and Rebase
log "Fetching updates from origin..."
git fetch origin

log "Rebasing local changes on top of origin/main..."
if ! git rebase origin/main; then
  error "Rebase failed. Please resolve conflicts manually in $REPO_DIR"
fi

# Pop stash if we stashed
if [[ "$STASHED" -eq 1 ]]; then
  log "Restoring local changes..."
  if ! git stash pop; then
    warn "Conflict during stash pop. Please resolve manually."
  fi
fi

# Update symlink if broken (self-healing)
REQUIRED_LINK="/home/alex/.gemini/antigravity/mcp_config.json"
TARGET_CONFIG="$REPO_DIR/config/mcp_config.json"

if [[ ! -L "$REQUIRED_LINK" ]] || [[ "$(readlink "$REQUIRED_LINK")" != "$TARGET_CONFIG" ]]; then
  log "Fixing broken symlink..."
  ln -sf "$TARGET_CONFIG" "$REQUIRED_LINK"
fi

log "Sync complete. Checking if we need to push local changes..."

# Check if we are ahead of origin
if git log origin/main..HEAD --oneline | grep -q .; then
  log "Local changes detected. Pushing to origin..."
  if git push origin main; then
    log "Successfully pushed local changes to GitHub."
  else
    warn "Failed to push to GitHub. You may need to authenticate or resolve issues manually."
  fi
else
  log "Local is up-to-date with origin."
fi

exit 0
