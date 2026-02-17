# Data Gaps and Missing Information

> **Date**: 2026-02-03
> **Purpose**: Track what data could not be collected and why

---

## 1. Cloudflare Data Gaps

### 1.1 Missing: Full Public Hostname/Route List

| What | Why Missing | How to Get |
|------|-------------|------------|
| Complete public hostname list | Cloudflare MCP not configured | Add Cloudflare MCP server OR use Cloudflare API directly |
| Access policies per hostname | Dashboard-only data | Cloudflare API or dashboard export |
| DNS record modes | Not in local config | Cloudflare API |
| TLS settings per hostname | Not in local config | Cloudflare API |
| UNRAID tunnel ingress rules | Dashboard-managed, no local file | Cloudflare API |

### 1.2 Available MCP Servers

```
bitwarden, github-mcp-server, mcp-fetch, mcp-filesystem, 
mcp-git, mcp-memory, mcp-playwright, mcp-sequentialthinking, 
mcp-time, perplexity-ask
```

**Cloudflare MCP: NOT CONFIGURED**

### 1.3 Recommendation

To get comprehensive Cloudflare data:

**Option A: Add Cloudflare MCP Server**
```json
"cloudflare": {
  "command": "npx",
  "args": ["-y", "@cloudflare/mcp-server-cloudflare"],
  "env": {
    "CLOUDFLARE_API_TOKEN": "<from BWS>"
  }
}
```

**Option B: Direct API Call**
```bash
curl -X GET "https://api.cloudflare.com/client/v4/accounts/<account_id>/cfd_tunnel" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json"
```

---

## 2. Unraid Data Gaps

| What | Why Missing | How to Get |
|------|-------------|------------|
| Unraid cloudflared config.yml | Uses dashboard-managed config | Export from Cloudflare dashboard |
| /boot/config/go script content | Didn't dump full content | `cat /boot/config/go` |
| Docker compose files | Scattered or UI-managed | Check /boot/atn/config/ or Unraid Docker templates |

---

## 3. VPS1 Data Gaps

| What | Why Missing | How to Get |
|------|-------------|------------|
| systemd mount unit for /atn | Not verified | `systemctl cat atn.mount` or check fstab |
| Full container port mappings | Only showed summary | `docker ps --no-trunc` |

---

## 4. Account/Subscription Data Gaps

| What | Why Missing | How to Get |
|------|-------------|------------|
| Google Pro account list | User knowledge required | Manual inventory |
| Perplexity account details | User knowledge required | Manual inventory |
| API token locations | Security - not dumped | Check BWS |

---

## 5. Priority for Filling Gaps

| Gap | Priority | Effort | Impact |
|-----|----------|--------|--------|
| Cloudflare MCP setup | P1 | Medium | High - comprehensive tunnel data |
| UNRAID tunnel config | P1 | Low | Medium - routing visibility |
| VPS1 mount verification | P2 | Low | Low - just confirmation |
| Account inventory | P1 | Medium | High - quota optimization |

---

*Gaps documented for transparency in Perplexity collaboration.*
