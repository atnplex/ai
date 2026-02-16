# MCP Configuration

This directory contains the configuration and definitions for Model Context Protocol (MCP) servers in the `galactic-galileo` ecosystem.

## 1. Strategy

### Hybrid Deployment Tiers

To optimize for cost, latency, and centralization, agents follow this tier system:

| Tier                   | Transport | Location                           | Purpose                                                                                         |
| ---------------------- | --------- | ---------------------------------- | ----------------------------------------------------------------------------------------------- |
| **Tier 1: Local**      | stdio     | Same machine (`localhost`, Docker) | Lowest latency, file/system access (git, filesystem, docker)                                    |
| **Tier 2: Remote VPS** | SSE/HTTP  | Tailscale VPS (VPS1/VPS2)          | Shared APIs, persistent state, centralized credentials (github, perplexity, cloudflare, memory) |
| **Tier 3: Cloud GCP**  | SSE/HTTP  | Cloud Run                          | Stateless, text-only, cost-optimized (brave-search, context7, mcp-time)                         |

**See Also**: [Remote MCP Hub Documentation](docs/MCP_INDEX.md#4-remote-mcp-hub-docker-on-vps)

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

## 3. Quick Start (One-Liner)

**Setup:**

```bash
./setup/easy_mcp_setup.sh
```

**Deploy to GCP:**

```bash
./setup/deploy_to_gcp.sh
```

## 4. Concepts

### What is a VPC (Virtual Private Cloud)?

Think of a **VPC** as your **private "Gated Community"** in the cloud.

- **Public Internet**: Anyone can knock on your door. You need strong locks (Passwords/Auth).
- **VPC (Private)**: Only people inside the gates (your servers, or you via VPN/Tailscale) can see you.
- **MCP Strategy**: We prefer deploying to the VPC (`--ingress=internal`). This means your agent is safe from public scanners without needing complex public authentication, as long as you connect via Tailscale.

## 5. Account Management & Costs

### Multi-Account Strategy

To manage costs and separate environments (e.g., Free Tier vs Credits):

1.  Run `./setup/deploy_to_gcp.sh`.
2.  Choose **Option 3: Create New Configuration** to add a second account.
3.  Switch between them easily using **Option 2** in the future.

### Cost Control

- **Budgets**: Set up a Budget Alert at [GCP Billing Budgets](https://console.cloud.google.com/billing/budgets).
- **Alerts**: Configure an alert at **$1.00** (or your limit) to get notified immediately of unexpected usage.
- **Note**: GCP does not auto-stop spending by default. Alerts are crucial for monitoring.
