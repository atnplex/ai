#!/bin/bash
set -e

# Easy MCP Setup Script
# Configures MCP servers based on Priority: Local > Tailscale > Cloud

echo "=== MCP Server Setup ==="

# 1. Detect Environment
if [ -f "/etc/wsl.conf" ] || [ -n "$WSL_DISTRO_NAME" ]; then
    ENV_TYPE="wsl"
    echo "Detected: Windows Subsystem for Linux (WSL)"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    ENV_TYPE="windows"
    echo "Detected: Windows (Git Bash/MinGW)"
else
    ENV_TYPE="linux"
    echo "Detected: Linux (VPS/Server)"
fi

# 2. Check Dependencies
echo "Checking dependencies..."
command -v docker >/dev/null 2>&1 || { echo >&2 "Docker is required but not installed. Aborting."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo >&2 "Python3 is required but not installed. Aborting."; exit 1; }

# 3. Load/Prompt Secrets
SECRETS_FILE=".agent/secrets.env"
if [ ! -f "$SECRETS_FILE" ]; then
    echo "Creating secrets file at $SECRETS_FILE..."
    mkdir -p .agent
    touch "$SECRETS_FILE"
fi

# Function to prompt for secret if missing
ensure_secret() {
    local key=$1
    local desc=$2
    if ! grep -q "^$key=" "$SECRETS_FILE"; then
        read -sp "Enter $desc ($key): " value
        echo
        echo "$key=$value" >> "$SECRETS_FILE"
    fi
}

echo "Ensuring required secrets..."
ensure_secret "GITHUB_PERSONAL_ACCESS_TOKEN" "GitHub PAT (repo, read:user)"
ensure_secret "PERPLEXITY_API_KEY" "Perplexity API Key"

# 4. Generate Configuration
echo "Generating MCP Configuration..."
# export ENV_TYPE for mcp_manager.py to read if needed
export DETECTED_ENV="$ENV_TYPE"
python3 ai/scripts/mcp_manager.py generate --auto

echo "=== Setup Complete ==="
echo "Restart your agent or reload the window to apply changes."
