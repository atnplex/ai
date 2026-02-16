#!/bin/bash
# Description: MCP server Docker images
# Dependencies: docker

log "Pulling MCP Docker images..."

docker pull mcp/filesystem
docker pull mcp/git
docker pull mcp/fetch
docker pull mcp/memory
docker pull mcp/playwright
docker pull mcp/sequentialthinking
docker pull mcp/time

# Generate MCP config from SSOT registry
if command -v python3 &>/dev/null && [[ -f "/atn/ai/scripts/mcp_manager.py" ]]; then
	log "Generating MCP config from registry via mcp_manager.py..."
	python3 /atn/ai/scripts/mcp_manager.py generate
elif [[ -f "$REPO_DIR/mcp/mcp_config.json" ]]; then
	log "Fallback: copying static MCP config..."
	mkdir -p /atn/.gemini
	cp "$REPO_DIR/mcp/mcp_config.json" /atn/.gemini/mcp_config.json
fi

log "MCP images pulled"
