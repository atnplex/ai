# MCP Configuration

This directory contains the configuration and definitions for Model Context Protocol (MCP) servers in the `galactic-galileo` ecosystem.

## 1. Strategy

### Priority Order

To optimize for cost, latency, and data privacy, agents must prefer servers in this order:

1.  **Local** (`localhost`, Docker): Lowest latency, free, full data access.
2.  **LAN / Tailscale** (VPS, HomeLab): Low latency, secure, persistent storage.
3.  **Cloud** (GCP Cloud Run): Higher latency, cost per request, strictly **stateless** and **text-only**.

### Resource Constraints

- **Cloud (GCP)**: strictly for **text-based tasks** (search, reasoning, API transformations).
  - **FORBIDDEN**: Image processing, video transcoding, large file uploads.
  - **Authorized Only**: All public endpoints must require authentication.
- **Local/VPS**: Use for heavy lifting (media processing, large datasets).

### Tool Loading

To minimize overhead and token usage, we do NOT load all tools for every agent.

- **Manifest**: `setup/config/gemini/tool_manifest.yaml` defines all available tools.
- **Dynamic Loading**: Agents scan user requests for `keywords` defined in the manifest.
- **Activation**: Only relevant tools (e.g., "cloudflared" for tunnel tasks) are loaded into the context.

## 2. Directory Structure

- `registry/`: YAML definitions of available MCP servers (the "Menu").
- `profiles/`: Agent-specific server sets (e.g., `infra.yaml`, `review.yaml`).
- `servers/`: Placeholder for custom server implementations.
- `docs/`: Deployment guides (see `MCP_DEPLOYMENT.md`).

## 3. Quick Start

Run the automated setup to configure your environment:

```bash
./setup/easy_mcp_setup.sh
```
