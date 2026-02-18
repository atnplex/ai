# atnplex/ai

Single Source of Truth (SSOT) for AI agent coordination, protocols, and configuration across the atnplex organization.    


## Repository Structure

| Directory                          | Purpose                                              |
|-----------------------------------|------------------------------------------------------|
| [.comet-browser/](.comet-browser/) | Perplexity Multi-Agent Coordination System           |
| [rules/](rules/)                   | Operational rules (MCP management, state validation) |
| [config/](config/)                 | MCP server registry                                  |
| [scripts/](scripts/)               | Utilities (sync, MCP manager, secrets)               |
| [services/](services/)             | AI Services (Search Gateway, Cloud Run)              |
| [.github/](.github/)               | Issue templates, PR template, CODEOWNERS             |

## 🛠️ MCP Registry (3-Tier Strategy)

Our MCP ecosystem is divided into three tiers for optimal performance, security, and resource management.

### ☁️ Cloud Tier (GCP Cloud Run)
Stateless API wrappers and cloud-native services. High scalability, zero maintenance.
- **search-gateway** [NEW]: Multiplexer for Perplexity Pro keys (rotates 3x keys).
- **jules-api**: Google Labs Jules integration.
- **imagefx**: Gemini-powered image generation.
- **veo-3.1**: Video generation capability.

### 🚀 Performance Tier (OCI VPS)
Stateful services and high-performance workers.
- **playwright**: Headless browser automation.
- **github-mcp**: High-throughput repository interaction.
- **sequential-thinking**: Complex reasoning worker.

### 🏠 Local Tier (homelab/desktop)
Low-latency access to local resources.
- **filesystem**: Direct disk access.
- **git**: Local repository manipulation.
- **memory**: Persistent agentic context.

## Protocol Version

Current version: see [PROTOCOL_VERSION](PROTOCOL_VERSION)
