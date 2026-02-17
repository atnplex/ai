# System Inventory for Perplexity Collaboration

> **Date**: 2026-02-03T23:10:00Z
> **Prepared by**: Antigravity (Opus 4.5 Thinking)
> **Purpose**: Comprehensive data handoff for AI optimization collaboration

---

## Executive Summary

| Category | Count | Notes |
|----------|-------|-------|
| GitHub Repositories | 26 | 24 atnplex + 2 anguy079 |
| Servers | 4 | VPS1, VPS2, Unraid, WSL |
| Docker Containers | 41 | VPS1: 14, VPS2: 10, Unraid: 17 |
| MCP Servers | 10 | Active in Antigravity |
| Skills | 14 | Context engineering patterns |
| Workflows | 16 | Operational procedures |
| Rules | 70+ | R0-R70 governance rules |

**Key Issues Identified:**
1. VPS1 `/atn` is tmpfs (volatile) - needs SSOT sync strategy
2. Pending secrets management implementation (BWS)
3. Multiple legacy/archived repos need cleanup
4. Cloudflare tunnel routing needs documentation

---

## 1. GitHub Repositories

### 1.1 Primary Organization: atnplex (24 repos)

#### Active/Core Repos

| Repo | Language | Last Commit | Status | Purpose |
|------|----------|-------------|--------|--------|
| atn | Shell | 2026-02-01 | ✅ Active | Core namespace: libs, scripts, docs |
| organizr | PHP | 2026-02-03 | ✅ Active | Dashboard app (forked), security hardening |
| antigravity-pipeline | - | 2026-02-03 | ✅ Active | 6-phase workflow, personas, context engineering |
| actions | - | 2026-01-30 | ✅ Active | Reusable GitHub Actions |
| secrets | - | 2026-01-27 | ✅ Active | Secret templates (private) |
| atn-secrets-manager | PowerShell | 2026-02-01 | ✅ Active | BWS integration pipeline |
| homelab_global | Shell | 2026-02-01 | ✅ Active | Cross-server configs |
| atn-unraid | - | - | ✅ Active | Unraid-specific configs |

#### Legacy/To Evaluate

| Repo | Purpose | Status | Recommendation |
|------|---------|--------|----------------|
| legacy-actions | Old workflows | ⚠️ Superseded | Archive or merge |
| legacy-unraid-cloudflared | Old plugin | ⚠️ Superseded | Archive |
| mcp-auth-smoketest-* | Test repos | 🗑️ Cleanup | Delete |
| homeassistant | HA configs | 🔍 Evaluate | Check if active |

### 1.2 Personal Account: anguy079 (2 repos)

| Repo | Last Update | Status |
|------|-------------|--------|
| public | 2025-07-29 | ⚠️ Old |
| auto-homelab | 2025-09-02 | ⚠️ Old |

---

## 2. Infrastructure

### 2.1 VPS1 (Oracle Cloud - Primary)

| Property | Value |
|----------|-------|
| Hostname | vps |
| OS | Debian 6.1.0-41-cloud-arm64 |
| CPU | 4 ARM cores |
| RAM | 24 GB |
| Disk | 197 GB (73% used) |
| Tailscale IP | 100.67.88.109 |
| Public IP | 159.54.169.21 |
| Docker Network | atn_bridge: 172.18.0.0/16 |

**Containers (14):**

| Container | Status | Ports | Purpose |
|-----------|--------|-------|--------|
| antigravity-manager | Up 24h | 8045 | Agent orchestration |
| ollama | Up 46h | 11434 | Local LLM (llama3.2:3b) |
| suggestarr | Up 5d | 5000 | Media suggestions |
| logarr-* | Up 6d-3w | 3002, 4001 | Log aggregation |
| vector-receiver | Up 6d | 9000 | Log ingestion |
| uptime-kuma | Up 3w | 3010 | Monitoring |
| huntarr | Up 3w | 9705 | Media hunting |
| open-webui | Up 3w | 3000 | Ollama UI |
| caddy | Up 3w | 80, 443 | Reverse proxy |
| watchtower | Up 3w | - | Auto-updates |
| jellyseerr | Up 3w | 5055 | Media requests |

**Special Notes:**
- `/atn` is **tmpfs** (18GB, volatile, lost on reboot)
- `/_atn` is also tmpfs (12GB)
- Ollama installed with llama3.2:3b model
- Caddy handles SSL termination

### 2.2 VPS2 / Condo (Oracle Cloud - Secondary)

| Property | Value |
|----------|-------|
| Hostname | condo |
| OS | Debian 6.1.0-42-cloud-arm64 |
| CPU | 4 ARM cores |
| RAM | 24 GB |
| Disk | 197 GB (20% used) |
| Swap | 4 GB |
| Tailscale IP | 100.102.55.88 |
| Docker Network | atn_bridge: 172.20.0.0/16 |

**Containers (10):**

| Container | Status | Purpose |
|-----------|--------|--------|
| antigravity-manager | Up 17h | Agent orchestration |
| organizr | Up 6d | Dashboard |
| 8x ephemeral | Up 36m | GitHub runner jobs |

**Special Notes:**
- No cloudflared installed
- GitHub Actions runners spawn here
- Less disk usage, good for ephemeral workloads

### 2.3 Unraid (Home Server - Storage)

| Property | Value |
|----------|-------|
| Hostname | unraid |
| OS | Unraid 6.12.54 |
| CPU | Intel i5-10400 @ 2.90GHz |
| RAM | 96 GB |
| Array | 9 disks × 8TB = ~58TB usable |
| Boot Flash | 29 GB |
| Tailscale IP | 100.76.168.116 |
| Home IP | 47.154.0.212 |
| Docker Network | atn_bridge: 172.18.0.0/16 |

**Containers (17):**

| Container | Status | Static IP | Purpose |
|-----------|--------|-----------|--------|
| plex | Up 5d | - | Media streaming |
| sonarr | Up 2w | 172.18.0.89 | TV automation |
| radarr | Up 34h | 172.18.0.78 | Movie automation |
| bazarr | Up 34h | 172.18.0.67 | Subtitles |
| prowlarr | Up 2w | 172.18.0.52 | Indexers |
| sabnzbd | Up 5d | 172.18.0.90 | Downloads |
| flaresolverr | Up 2w | 172.18.0.58 | Cloudflare bypass |
| autoscan | Up 2w | 172.18.0.30 | Plex scanner |
| tautulli | Up 4d | - | Plex stats |
| postgres | Up 2w | - | Database |
| vector | Up 6d | - | Log shipping |
| github-runner | Up 10h | - | CI/CD |

**Filesystem Notes:**
- `/atn` is on array (persistent, btrfs)
- `/boot/atn` is on flash (persistent, survives reboots)
- `/atn_ram_boot` is tmpfs (12GB)

### 2.4 WSL (Windows Desktop)

| Property | Value |
|----------|-------|
| Hostname | antigravity-wsl |
| Parent | amd (Windows desktop) |
| Tailscale IP | 100.114.18.47 |
| Windows Tailscale | 100.118.253.91 |

**Purpose:** Development environment, Antigravity primary interface

### 2.5 Network Summary

| Server | Tailscale IP | Docker CIDR | Notes |
|--------|--------------|-------------|-------|
| VPS1 | 100.67.88.109 | 172.18.0.0/16 | Primary |
| VPS2 | 100.102.55.88 | 172.20.0.0/16 | Secondary |
| Unraid | 100.76.168.116 | 172.18.0.0/16 | Storage |
| WSL | 100.114.18.47 | N/A | Dev |
| Windows | 100.118.253.91 | N/A | Desktop |

---

## 3. AI/Automation Stack

### 3.1 MCP Servers (10 Active)

| Server | Purpose | Usage |
|--------|---------|-------|
| github-mcp-server | GitHub API operations | High |
| mcp-fetch | HTTP requests | Medium |
| mcp-filesystem | File operations | High |
| mcp-git | Git operations | High |
| mcp-memory | Knowledge graph | Low |
| mcp-playwright | Browser automation | Medium |
| mcp-sequentialthinking | Reasoning chains | Low |
| mcp-time | Time operations | Low |
| perplexity-ask | Research queries | Medium |
| bitwarden | Secret fetching | Low (not fully implemented) |

### 3.2 Skills (14 Context Engineering Patterns)

| Skill | Purpose | Status |
|-------|---------|--------|
| ai-reviewer-workflow | Optimize Copilot limits | ✅ |
| brainstorming | Pre-implementation design | ✅ |
| context-compression | Reduce token usage | ✅ |
| context-optimization | Maximize effectiveness | ✅ |
| environment-check | Verify capabilities | ✅ |
| error-recovery | Graceful failure handling | ✅ |
| filesystem-context | Dynamic offloading | ✅ |
| memory-persistence | STM/LTM separation | ✅ |
| parallel-agents | Independent task dispatch | ✅ |
| parallel-research | Flash summarization | ✅ |
| prompt-optimization | Context enhancement | ✅ |
| repomix-optimize | Token-efficient packing | ✅ |
| self-reflection | Reflexion pattern | ✅ |
| verification-before-completion | Evidence before claims | ✅ |

### 3.3 Workflows (16 Operational Procedures)

| Workflow | Purpose |
|----------|--------|
| pipeline-00-triage | Initial request classification |
| pipeline-01-confirm | User confirmation |
| pipeline-02-decompose | Task breakdown |
| pipeline-03-execute | Implementation |
| pipeline-04-pr-lifecycle | PR automation |
| pipeline-05-deliver | Final delivery |
| ops-ssh-remote | SSH shortcuts |
| ops-deploy-service | Docker deployment |
| ops-health-check | Health endpoints |
| jules-pr-automation | Jules.Google integration |
| triage-micro-pipeline | Mini-triage with personas |
| pause/resume | Context preservation |
| disconnection | Error recovery |

### 3.4 Rules (70+ Governance)

**Key Categories:**
- R0-R10: Precedence, mandatory actions
- R15-R35: Formatting (Markdown, JSON, YAML, Shell, Python)
- R40-R49: Security, PR lifecycle
- R50-R70: Operational standards

**Critical Rules:**

| Rule | Purpose |
|------|--------|
| R00 | Mandatory triage for all requests |
| R47 | Never dismiss/bypass reviews |
| R50 | Coding principles (no hardcoding) |
| R61 | Infrastructure standards |
| R66 | Docker networking standards |
| R68 | Unraid-specific standards |
| R69 | Secrets management (BWS) |

---

## 4. User Preferences & Context

### 4.1 Core Philosophy

1. **SSOT (Single Source of Truth)**: GitHub is the source of truth for code
2. **Zero manual input**: Automate everything possible
3. **No hardcoding**: Use variables, configs, environment
4. **Tmpfs for speed**: RAM-based working directories
5. **Quality over cost**: Use best model for critical decisions
6. **Redundancy**: No single points of failure

### 4.2 Model Tiering Strategy

| Phase | Preferred Model | Rationale |
|-------|-----------------|----------|
| Triage | Opus 4.5 Thinking | High-stakes evaluation |
| Simple work | Gemini Flash | Fast, free |
| Standard work | Sonnet 4.5 / Gemini Pro | Balanced |
| Complex work | Opus 4.5 | Architecture |
| Research | Perplexity Sonar | Citations |

### 4.3 Resource Accounts

- **Google Pro**: 15+ accounts (Claude, Gemini, ImageFX)
- **Perplexity Pro**: Multiple accounts ($15/mo budget)
- **GitHub Student**: Copilot, Actions, etc.
- **Microsoft 365**: Family subscription
- **Cloudflare**: Custom domain, Zero Trust

### 4.4 Pending Implementations

| Item | Status | Priority |
|------|--------|----------|
| BWS secrets workflow | Started | P0 |
| VPS1 persistence strategy | Design needed | P0 |
| Multi-model orchestration | Research | P0 |
| Account rotation for quotas | Design needed | P1 |
| Celery + Redis distributed | Not started | P2 |

---

## 5. Identified Issues

### 5.1 Redundancies

| Issue | Details | Impact |
|-------|---------|--------|
| legacy-* repos | Superseded by new repos | Confusion |
| Test repos | mcp-auth-smoketest-* | Clutter |

### 5.2 Legacy/Unused

| Item | Reason | Recommendation |
|------|--------|----------------|
| legacy-actions repo | Replaced by `actions` | Archive |
| legacy-unraid-cloudflared | Plugin replaced | Archive |
| anguy079/auto-homelab | Old, not maintained | Evaluate |
| consolidation branches | Old cleanup work | Delete if merged |

### 5.3 Configuration Drift

| Location | Issue |
|----------|-------|
| VPS1 `/atn` | Tmpfs - not synced to persistent |
| Rules | Some gaps in numbering |

---

*Document generated by Antigravity for Perplexity collaboration.*
