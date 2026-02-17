# Bootstrap and Offline Fallback

> **Date**: 2026-02-03
> **Purpose**: Document cold-start/bootstrap steps and offline fallback behavior
> **Status**: Factual documentation with unknowns marked

---

## 1. VPS1 Bootstrap Sequence

### 1.1 Current Boot Order

```
1. Kernel + systemd init
2. Networking (automatic)
3. Tailscale daemon (auto-start)
4. Docker daemon (auto-start)
5. tmpfs mounts (/atn, /_atn) - via fstab or systemd
6. Docker containers (restart policies)
7. Caddy (reverse proxy)
8. Cloudflared (tunnel connector)
9. Antigravity-manager (agent orchestration)
```

### 1.2 Service Dependencies

| Service | Depends On | Breaks If Missing |
|---------|-----------|-------------------|
| Tailscale | Network | Remote SSH access |
| Docker | Filesystem | All containers |
| Containers | Docker | Application services |
| Caddy | Docker, Network | HTTPS/routing |
| Cloudflared | Network, Caddy | Public access |
| Antigravity | Docker, /atn | Agent operations |

### 1.3 What Breaks Without Internet

| Component | Impact | Mitigation |
|-----------|--------|------------|
| Git clone to /atn | ❌ FAILS - no code | Need local cache |
| Docker image pull | ❌ FAILS if image not cached | Pre-pull images |
| Cloudflared | ❌ FAILS - no tunnel | Expected, use Tailscale |
| Tailscale | ⚠️ Degraded - uses cached peers | Usually works |
| Caddy | ✅ Works with local config | OK |
| Containers | ✅ Work if images cached | OK |

### 1.4 Current Local Cache/Seed

| Path | Exists | Contents |
|------|--------|----------|
| `/var/atn-persistent` | ❌ NO | Not implemented |
| `/home/alex/.cloudflared/` | ✅ YES | Tunnel credentials |
| Docker images | ✅ YES | Cached on disk |
| Git repos | ❌ NO | Only in tmpfs |

**Gap:** No persistent seed for `/atn` contents.

---

## 2. VPS2/Condo Bootstrap Sequence

### 2.1 Current Boot Order

```
1. Kernel + systemd init
2. Networking (automatic)
3. Tailscale daemon (auto-start)
4. Docker daemon (auto-start)
5. /atn (on disk, always available)
6. Docker containers (restart policies)
7. Antigravity-manager
```

### 2.2 What Breaks Without Internet

| Component | Impact | Mitigation |
|-----------|--------|------------|
| Git pull | ⚠️ Uses stale local | Acceptable |
| Docker image pull | ❌ FAILS if not cached | Pre-pull |
| GitHub Actions | ❌ FAILS | Expected |

**Status:** ✅ VPS2 is more resilient because `/atn` is on disk.

---

## 3. Unraid Bootstrap Sequence

### 3.1 Current Boot Order

```
1. BIOS/UEFI
2. Unraid OS loads to RAM from USB flash
3. /boot mounted (flash drive)
4. /boot/config/go script executes
5. Network initialized
6. Tailscale starts
7. Array starts (spins up disks)
8. Docker starts (depends on array)
9. /atn available (on array)
10. Containers start per Docker settings
11. Cloudflared tunnel starts
12. User scripts in /boot/atn/lifecycle/
```

### 3.2 Critical Path: go Script

Location: `/boot/config/go`

**Important:** This script runs BEFORE array is started. Must NOT:
- Reference paths on array (/mnt/user/, /mnt/disk*)
- Exit with code 1 (stops boot)
- Block for long operations

### 3.3 What Breaks Without Internet

| Component | Impact | Mitigation |
|-----------|--------|------------|
| Cloudflared | ❌ FAILS | Use Tailscale |
| Docker pulls | ❌ FAILS if not cached | Images on array |
| Git operations | ❌ FAILS | Local code on array |
| Tailscale | ⚠️ Uses cached config | Usually works |

### 3.4 What Breaks Without Array

| Component | Impact | Timeframe |
|-----------|--------|----------|
| Docker | ❌ Cannot start | Until array up |
| /atn | ❌ Not available | Until array up |
| All containers | ❌ Not running | Until array up |

**Gap:** If array fails to start, no recovery path other than manual intervention.

### 3.5 Current Local Cache/Seed

| Path | Contents | Survives Reboot |
|------|----------|----------------|
| `/boot/atn/` | Scripts, configs, lifecycle | ✅ YES (flash) |
| `/atn/` | Full workspace | ✅ YES (array) |
| `/atn_ram_boot/` | Hot cache | ❌ NO (tmpfs) |

**Status:** ✅ Unraid is most resilient with flash + array redundancy.

---

## 4. WSL Bootstrap Sequence

### 4.1 Current Boot Order

```
1. Windows boots
2. WSL2 starts (manual or auto)
3. Tailscale in WSL starts
4. /atn available (on Windows filesystem via /mnt/c or native)
5. Antigravity ready
```

### 4.2 What Breaks Without Internet

| Component | Impact |
|-----------|--------|
| Git operations | Uses local cache |
| API calls | ❌ FAILS |
| MCP servers | ⚠️ May fail |

---

## 5. Cross-Server Dependencies

### 5.1 Dependency Matrix

| If Down | VPS1 Impact | VPS2 Impact | Unraid Impact | WSL Impact |
|---------|-------------|-------------|---------------|------------|
| GitHub | No code sync | No code sync | Local OK | Local OK |
| Cloudflare | No public access | N/A | No public access | N/A |
| Internet | Tailscale only | Tailscale only | Tailscale only | Tailscale only |
| Tailscale | SSH via public IP | SSH via public IP | Local only | Local only |
| VPS1 | N/A | OK | OK | OK |
| VPS2 | OK | N/A | OK | OK |
| Unraid | OK | OK | N/A | OK |

### 5.2 Single Points of Failure

| SPOF | Impact | Mitigation |
|------|--------|------------|
| GitHub down | No SSOT sync | Local cache |
| Tailscale down | No cross-server SSH | Use public IPs |
| User's internet | No remote access | Tunnels still work |
| Cloudflare down | No public hostnames | Tailscale direct |

---

## 6. Unknowns to Confirm

| Question | Context |
|----------|--------|
| Is there a systemd unit for VPS1 /atn mount? | Need to verify mount mechanism |
| What's the exact go script content on Unraid? | Affects boot behavior |
| How does /atn_ram_boot get populated on Unraid? | Need sync script reference |
| Is there a pre-pull script for Docker images? | Affects offline resilience |
| What's the Tailscale offline grace period? | How long cached peers work |

---

## 7. Desired State

### 7.1 Offline-First Design

1. **Every server can boot and operate without internet**
2. **Local cache is authoritative when offline**
3. **Sync to SSOT when connection restored**
4. **No manual intervention for recovery**

### 7.2 Bootstrap Resilience Targets

| Server | Target Boot Time | Offline Capable |
|--------|-----------------|----------------|
| VPS1 | < 2 min | ❌ Currently NO |
| VPS2 | < 2 min | ✅ YES |
| Unraid | < 5 min (array spin) | ✅ YES |
| WSL | < 30 sec | ✅ YES |

---

*Document created for Perplexity collaboration.*
*Factual where verified, unknowns marked.*
