# Cloudflare Tunnels Inventory

> **Date**: 2026-02-03
> **Source**: cloudflared CLI on VPS1 + manual inspection
> **Purpose**: Document all Cloudflare tunnel configurations

---

## 1. Tunnel Summary

| Tunnel Name | UUID | Created | Status | Connectors |
|-------------|------|---------|--------|------------|
| VPS | 81084d84-3978-42f0-aa37-6fc42d54fad4 | 2025-07-02 | ✅ Active | VPS1 (2 connections) |
| UNRAID | 8a5bea70-dd60-4abd-8f39-486a3f289601 | 2025-08-08 | ✅ Active | Unraid (4 connections) |
| Home Assistant | 7fc3ec62-2adf-4994-b90d-4f583e477575 | 2025-11-11 | ⚠️ Inactive | No connectors |

---

## 2. VPS Tunnel Details

### 2.1 Connector Information

| Property | Value |
|----------|-------|
| Tunnel Name | VPS |
| Tunnel ID | 81084d84-3978-42f0-aa37-6fc42d54fad4 |
| Connector ID | 36d57acd-02e5-4fa0-ae6d-0704374ba231 |
| Architecture | linux_arm64 |
| Version | 2025.9.1 |
| Origin IP | 159.54.169.21 |
| Edge Locations | sjc06, sjc08 (2 connections) |
| Created | 2026-01-07T08:17:56Z |

### 2.2 VPS Tunnel Config

**Location:** `/etc/cloudflared/config.yml` on VPS1

```yaml
tunnel: debian
credentials-file: /home/alex/.cloudflared/81084d84-3978-42f0-aa37-6fc42d54fad4.json

ingress:
  - hostname: pihole-vps.atnplex.com
    service: http://localhost:80
  - hostname: atnplex.com
    service: http://172.19.0.80:80
  - service: http_status:404

edge-ip-version: "4"
```

### 2.3 VPS Public Hostnames

| Hostname | Backend Service | Notes |
|----------|----------------|-------|
| pihole-vps.atnplex.com | http://localhost:80 | Pi-hole DNS admin |
| atnplex.com | http://172.19.0.80:80 | Main site (Docker) |
| (fallback) | http_status:404 | Default catch-all |

---

## 3. UNRAID Tunnel Details

### 3.1 Connector Information

| Property | Value |
|----------|-------|
| Tunnel Name | UNRAID |
| Tunnel ID | 8a5bea70-dd60-4abd-8f39-486a3f289601 |
| Edge Locations | sjc01, sjc06, sjc08, sjc10 (4 connections) |

### 3.2 Unraid Configuration

**Plugin Location:** `/boot/config/plugins/cloudflared/`

**Note:** No `config.yml` found in standard location. The cloudflared plugin on Unraid likely uses the Cloudflare dashboard-managed config (cloudflared service mode) rather than a local config file.

**Plugin Files Present:**
- cloudflared binary (v2025.6.1)
- cloudflared-utils packages
- Log files

**Status:** Tunnel is running (4 edge connections) but config is managed via Cloudflare dashboard, not local file.

### 3.3 Unraid Public Hostnames (Estimated)

Based on previous inventory and Caddyfile references:

| Hostname | Backend Service | Status |
|----------|----------------|--------|
| *.atnplex.com | Various container IPs | Active |
| plex.atnplex.com | Plex Media Server | Active |
| tautulli.atnplex.com | Tautulli | Active |
| sonarr.atnplex.com | 172.18.0.89:8989 | Active |
| radarr.atnplex.com | 172.18.0.78:7878 | Active |
| sabnzbd.atnplex.com | 172.18.0.90:8080 | Active |

> **⚠️ Note:** Full hostname list should be pulled from Cloudflare dashboard or API for accuracy.

---

## 4. Home Assistant Tunnel

| Property | Value |
|----------|-------|
| Tunnel Name | Home Assistant |
| Tunnel ID | 7fc3ec62-2adf-4994-b90d-4f583e477575 |
| Created | 2025-11-11T22:24:23Z |
| Status | ⚠️ Inactive (0 connections) |

**Notes:**
- No active connectors running
- May be legacy or planned but not implemented
- Associated repo: `atnplex/homeassistant`

---

## 5. VPS2/Condo Cloudflare Status

| Property | Value |
|----------|-------|
| cloudflared installed | ❌ NO |
| Tunnel connector | ❌ NO |
| Access method | Tailscale only |

**Notes:**
- VPS2 does not run cloudflared
- Access is via Tailscale (100.102.55.88)
- Could add redundant tunnel connector for HA

---

## 6. Network Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLOUDFLARE EDGE                         │
│                  (anycast, global PoPs)                     │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│   VPS Tunnel  │ │ UNRAID Tunnel │ │   HA Tunnel   │
│ 2 connections │ │ 4 connections │ │   (inactive)  │
└───────┬───────┘ └───────┬───────┘ └───────────────┘
        │                 │
        ▼                 ▼
┌───────────────┐ ┌───────────────┐
│     VPS1      │ │    Unraid     │
│  159.54.169.21│ │ 47.154.0.212  │
│  (OCI ARM)    │ │ (Home Server) │
└───────────────┘ └───────────────┘
        │                 │
        ▼                 ▼
┌───────────────┐ ┌───────────────┐
│  Caddy Proxy  │ │  Caddyfile/   │
│  + Containers │ │   Containers  │
└───────────────┘ └───────────────┘
```

---

## 7. Gotchas & Known Issues

### 7.1 Routing Issues

| Issue | Impact | Mitigation |
|-------|--------|------------|
| VPS tunnel uses `172.19.0.80` for atnplex.com | Different subnet than atn_bridge (172.18.x) | May be intentional separate network |
| UNRAID config managed via dashboard | No local config file to version control | Need to export from Cloudflare API |
| Home Assistant tunnel inactive | Not serving traffic | Evaluate if needed |

### 7.2 High Availability Gaps

| Gap | Current State | Recommendation |
|-----|---------------|----------------|
| VPS tunnel only on VPS1 | Single point of failure | Add connector on VPS2 |
| UNRAID tunnel only on home network | ISP outage = no access | Add cloud replica |
| No tunnel on VPS2 | Only Tailscale access | Consider adding for public services |

### 7.3 Configuration Drift

| Location | Issue |
|----------|-------|
| VPS1 `/etc/cloudflared/config.yml` | Tunnel name "debian" doesn't match tunnel name "VPS" |
| Unraid | No local config - dashboard managed |

---

## 8. Desired HA Pattern

**Proposed Architecture:**

1. **Multi-Connector Tunnels**: Run tunnel connectors on multiple servers
   - VPS tunnel: VPS1 (primary) + VPS2 (backup)
   - UNRAID tunnel: Home (primary) + VPS1 (backup via Tailscale)

2. **Local Config for UNRAID**: Export dashboard config to local file for version control

3. **Monitoring**: Add uptime checks for each public hostname

---

## 9. Data Gaps

| Missing Data | Why | How to Get |
|--------------|-----|------------|
| Full UNRAID hostname list | Dashboard-managed | Cloudflare API or dashboard export |
| Access policies per hostname | Not in local config | Cloudflare Zero Trust dashboard |
| DNS record modes | Not inspected | Cloudflare API |
| TLS settings per hostname | Not inspected | Cloudflare API |

---

*Document created for Perplexity collaboration.*
*Some data pulled from cloudflared CLI, some estimated from prior context.*
