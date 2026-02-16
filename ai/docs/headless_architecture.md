# Headless Architecture Vision

> **Goal**: Run Antigravity entirely on remote servers, accessible from any device (phone, tablet, laptop) via a browser, with zero local dependencies.

---

## 🏗️ Target Architecture

```mermaid
graph TD
    User[📱 You (Phone/Browser)] -->|Tailscale VPN| VPS[☁️ OCI VPS Instance]

    subgraph "VPS Infrastructure (Docker)"
        WebUI[🌐 Open WebUI / Chat Interface]
        AG_Mgr[🧠 Antigravity Manager]
        MCP_Hub[🔌 Remote MCP Hub]
    end

    subgraph "Agent Execution Plane"
        Agent1[🤖 Agent: Coding]
        Agent2[🕵️ Agent: Research]
        Agent3[🛠️ Agent: Infra]
    end

    WebUI --> AG_Mgr
    AG_Mgr --> MCP_Hub
    AG_Mgr --> Agent1 & Agent2 & Agent3

    MCP_Hub --> GitHub[GitHub API]
    MCP_Hub --> OCI[Oracle Cloud API]
    MCP_Hub --> Cloudflare[Cloudflare API]

    Agent1 -->|Git Ops| GitHub
```

---

## 🔑 Key Components

### 1. The Frontend: Open WebUI

- **Role**: Your interface to the system.
- **Hosted**: Docker container on VPS.
- **Access**: `http://100.x.y.z:3000` (Tailscale IP).
- **Features**: Chat history, model toggling (Sonnet/Opus), file uploads.

### 2. The Brain: Antigravity Manager (Headless)

- **Role**: Orchestrates agents and routed LLM calls.
- **Hosted**: Docker container / Systemd service.
- **Config**: `tool_manifest.yaml` rules everything.
- **No GUI**: Does not run VS Code or a local window. It exposes an API.

### 3. The Hands: Remote MCP Hub

- **Role**: The _only_ way agents interact with the world.
- **Hosted**: Docker containers (`mcp/fetch`, `mcp/git`, etc.).
- **Crucial Change**:
  - **Current**: VS Code extensions (GitLens, etc.) do the work.
  - **Target**: MCP servers do the work.
  - _Result_: You don't need VS Code installed to manage git, view files, or deploy.

### 4. The Trigger: GitHub Issues

- **Role**: Asynchronous task dispatch.
- **Workflow**:
  1. Phone → GitHub App → Create Issue "Fix bug in auth".
  2. GitHub Action → Webhook → Antigravity Manager.
  3. Agent wakes up → Clones repo → Fixes bug → Pushes PR.
  4. Phone → Notification "PR Created".

---

## 🚀 Migration Path

1. **Consolidate Tools**: Move all local VS Code extension functionality to MCP servers (Git, Filesystem, Search).
   - _Status_: ✅ `tool_manifest.yaml` created with 12 servers.
2. **Deploy Control Plane**: Run Open WebUI + Antigravity Manager on VPS.
   - _Status_: 📝 Issue created to deploy Open WebUI.

3. **Connect the Pipes**: Set up GitHub Action for issue-to-agent dispatch.
   - _Status_: 📝 Issue created to build this pipeline.

4. **Go Headless**: Uninstall local extensions. Use only the browser.
   - _Status_: ⏳ Future phase.
