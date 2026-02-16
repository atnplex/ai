---
name: MCP Tools Standards
description: Defines Model Context Protocol server configuration and usage
trigger: always
---

# R93: MCP Tools Standards

> Standardizes MCP (Model Context Protocol) server configuration and usage.

## Configuration Location

**Choose based on your deployment environment:**

| Environment                     | Config Location                                  | Manager Script                     |
| ------------------------------- | ------------------------------------------------ | ---------------------------------- |
| **Local Development (Windows)** | `$WORKSPACE/setup/config/gemini/mcp_config.json` | Manual edit or `easy_mcp_setup.sh` |
| **Linux Baseline (`/atn`)**     | `/atn/ai/config/mcp_registry.json`               | `/atn/ai/scripts/mcp_manager.py`   |
| **Cloud (GCP)**                 | `infrastructure/mcp/registry/servers.yaml`       | `deploy_to_gcp.sh`                 |

> [!NOTE]
> For comprehensive deployment guidance, see [infrastructure/mcp/docs/MCP_INDEX.md](../../../infrastructure/mcp/docs/MCP_INDEX.md).

## Available MCP Servers

| Server                   | Purpose                                  |
| ------------------------ | ---------------------------------------- |
| `mcp-fetch`              | HTTP requests, URL content fetching      |
| `mcp-filesystem`         | File operations beyond workspace         |
| `mcp-git`                | Git operations (add, commit, diff, etc.) |
| `mcp-memory`             | Knowledge graph persistence              |
| `mcp-playwright`         | Browser automation and testing           |
| `mcp-sequentialthinking` | Complex reasoning chains                 |
| `mcp-time`               | Time and timezone operations             |

## Usage Guidelines

### Prefer MCP Tools When Available

> [!IMPORTANT]
> Use MCP tools instead of shell commands when possible for:
>
> - Better error handling
> - Structured output
> - Cross-platform compatibility

| Task       | Prefer                         | Avoid        |
| ---------- | ------------------------------ | ------------ |
| Read file  | `mcp_mcp-filesystem_read_file` | `cat file`   |
| Git status | `mcp_mcp-git_git_status`       | `git status` |
| Fetch URL  | `mcp_mcp-fetch_fetch`          | `curl URL`   |

### Browser Automation

For JavaScript-heavy sites, use `browser_subagent` which leverages `mcp-playwright`:

```
1. Navigate to URL
2. Wait for JS to load
3. Take snapshot
4. Extract content
5. Return structured data
```

### Memory Persistence

Use `mcp-memory` for knowledge that should persist across conversations:

- `create_entities` - Add new knowledge
- `create_relations` - Link entities
- `search_nodes` - Query existing knowledge
- `read_graph` - Full knowledge dump

## Adding New MCP Servers

Edit `$NAMESPACE/.gemini/antigravity/mcp_config.json`:

```json
{
  "servers": {
    "mcp-<name>": {
      "command": "<executable>",
      "args": ["<arg1>", "<arg2>"]
    }
  }
}
```
