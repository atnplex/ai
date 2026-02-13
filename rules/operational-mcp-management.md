# Operational Rule: MCP Management

> **ID**: `operational-mcp-management`
> **Version**: 1.1.0
> **Status**: Active

## 0. Synchronization First

At the start of every session (or when instructed), agents MUST run:

```bash
/atn/ai/scripts/sync_ai.sh
```

This ensures the local agent is using the latest configuration from the `ai` repository, and pushes any local improvements back to GitHub.

## 1. Source of Truth

The **`ai` repository** at `/atn/ai` is the **single source of truth** for all MCP configurations, scripts, and rules.

- **Config**: `/atn/ai/config/mcp_config.json`
- **Registry**: `/atn/ai/config/mcp_registry.json`
- **Scripts**: `/atn/ai/scripts/`

## 2. No Manual Edits

**NEVER** manually edit `/atn/ai/config/mcp_config.json` or `~/.gemini/antigravity/mcp_config.json`.

- These files are auto-generated.
- Manual edits will be overwritten.

## 3. Use the Manager Script

To enable, disable, or modify MCP servers, you **MUST** use the manager script:

```bash
/atn/ai/scripts/mcp_manager.py [list|enable|disable|reset]
```

## 4. Modifying Server Definitions

To add a _new_ server or change an existing definition (e.g., arguments, env vars):

1.  **Edit**: `/atn/ai/config/mcp_registry.json`
2.  **Apply**: Run `/atn/ai/scripts/mcp_manager.py reset` to regenerate the active config.

## 5. Deployment

The active configuration at `~/.gemini/antigravity/mcp_config.json` MUST be a **symlink** to `/atn/ai/config/mcp_config.json`.
