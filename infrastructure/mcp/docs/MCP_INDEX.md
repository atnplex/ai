# MCP Documentation Index

> Central navigation for all MCP server documentation across deployment environments.

## Choose Your Environment

### 1. Local Development (Windows)

**Use Case**: Running MCP servers on your desktop/laptop for local agent development.

| Component        | Location                                                                                                |
| ---------------- | ------------------------------------------------------------------------------------------------------- |
| **Config File**  | [setup/config/gemini/mcp_config.json](../../setup/config/gemini/mcp_config.json)                        |
| **Setup Script** | [setup/easy_mcp_setup.sh](../../setup/easy_mcp_setup.sh)                                                |
| **Rules**        | [operational-mcp-tools-standards.md](../../setup/config/agent/rules/operational-mcp-tools-standards.md) |
| **Usage Guide**  | [operational-mcp_usage.md](../../setup/config/agent/rules/operational-mcp_usage.md)                     |

**Quick Start**:

```bash
./setup/easy_mcp_setup.sh
```

---

### 2. Linux Servers (`/atn` Namespace)

**Use Case**: VPS1, VPS2, Debian VMs running in the `/atn` baseline infrastructure.

| Component           | Location                                                                               |
| ------------------- | -------------------------------------------------------------------------------------- |
| **Config Registry** | `/atn/ai/config/mcp_registry.json`                                                     |
| **Manager Script**  | `/atn/ai/scripts/mcp_manager.py`                                                       |
| **Rules**           | [ai/rules/operational-mcp-management.md](../../ai/rules/operational-mcp-management.md) |

**Quick Start**:

```bash
/atn/ai/scripts/sync_ai.sh
/atn/ai/scripts/mcp_manager.py generate
```

---

### 3. Cloud Deployment (GCP)

**Use Case**: Deploying stateless, text-only MCP servers to Google Cloud Run.

| Component            | Location                                                             |
| -------------------- | -------------------------------------------------------------------- |
| **Registry**         | [infrastructure/mcp/registry/servers.yaml](../registry/servers.yaml) |
| **Deployment Guide** | [MCP_DEPLOYMENT.md](./MCP_DEPLOYMENT.md)                             |
| **Strategy Guide**   | [infrastructure/mcp/README.md](../README.md)                         |
| **Deploy Script**    | [setup/deploy_to_gcp.sh](../../setup/deploy_to_gcp.sh)               |

**Quick Start**:

```bash
./setup/deploy_to_gcp.sh
```

---

## Deployment Priority

Agents should prefer MCP servers in this order:

1. **Local** (`localhost`, Docker) - Lowest latency, free, full data access
2. **LAN/Tailscale** (VPS, HomeLab) - Low latency, secure, persistent storage
3. **Cloud** (GCP Cloud Run) - Higher latency, cost per request, **text-only**

---

## Common Questions

**Q: Which config file should I edit?**

- **Windows dev**: `setup/config/gemini/mcp_config.json`
- **Linux VPS**: Use `/atn/ai/scripts/mcp_manager.py` (never edit JSON manually)
- **Cloud**: Edit `infrastructure/mcp/registry/servers.yaml`, then deploy

**Q: Can I use the same MCP servers across all environments?**

- Yes, but configurations differ:
  - **Local/Linux**: Can run any server type (including stateful, media-heavy)
  - **Cloud**: Text-only servers with strict resource limits

**Q: How do I add a new MCP server?**

- **Local**: Edit config JSON and restart agent
- **Linux**: `mcp_manager.py` → edit registry → `reset`
- **Cloud**: Add to `servers.yaml` → deploy via script

---

## Related Documentation

- [Tool Manifest](../../setup/config/gemini/tool_manifest.yaml) - Dynamic tool loading keywords
- [Auto-Discovery Rule](../../setup/config/agent/rules/operational-auto-discovery.md) - How agents find MCP tools
- [Secrets Management](../../setup/config/agent/rules/security-secrets.md) - Secure API key handling
