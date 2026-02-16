# Operational Rule: MCP Management

> **ID**: `operational-mcp-management`
> **Version**: 1.2.0
> **Status**: Active

## 0. Synchronization First

At the start of every session (or when instructed), agents MUST run:

```bash
/atn/ai/scripts/sync_ai.sh
```

This ensures the local agent is using the latest configuration from the `ai` repository, and pushes any local improvements back to GitHub.

## 1. Source of Truth

The **`ai` repository** at `/atn/ai` is the **single source of truth** for all MCP configurations, scripts, and rules.

- **Registry (SSOT)**: `/atn/ai/config/mcp_registry.json`
- **Generated Config**: `/atn/ai/config/mcp_config.json` — generated at runtime, NOT in version control
- **Scripts**: `/atn/ai/scripts/`

## 2. No Manual Edits

**NEVER** manually edit `/atn/ai/config/mcp_config.json` or `~/.gemini/antigravity/mcp_config.json`.

- `mcp_config.json` is auto-generated from `mcp_registry.json` at runtime.
- Manual edits will be overwritten.
- The file is excluded from version control via `.gitignore`.

## 3. Use the Manager Script

To enable, disable, generate, or modify MCP servers, you **MUST** use the manager script:

```bash
/atn/ai/scripts/mcp_manager.py [list|generate|enable|disable|reset]
```

### Commands

- `list` — Show all servers and their enabled/disabled status
- `generate` — Generate `mcp_config.json` from registry defaults (use when config doesn't exist)
- `enable <name>` — Enable a specific server
- `disable <name>` — Disable a specific server
- `reset` — Reset config to registry defaults

## 4. Modifying Server Definitions

To add a _new_ server or change an existing definition (e.g., arguments, env vars):

1.  **Edit**: `/atn/ai/config/mcp_registry.json`
2.  **Apply**: Run `/atn/ai/scripts/mcp_manager.py reset` to regenerate the active config.

## 5. Deployment

The active configuration at `~/.gemini/antigravity/mcp_config.json` MUST be a **symlink** to `/atn/ai/config/mcp_config.json`.

If the config doesn't exist, run `mcp_manager.py generate` to create it from the registry.
