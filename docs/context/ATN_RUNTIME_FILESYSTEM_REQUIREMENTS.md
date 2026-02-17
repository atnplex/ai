# ATN Runtime Filesystem Requirements

> **Version**: 1.0.0
> **Date**: 2026-02-03
> **Purpose**: Define /atn tmpfs + persistence strategy across all servers

---

## 1. Design Philosophy

### 1.1 Core Requirements

1. `/atn` is **tmpfs** (RAM-based) for:
   - Fast I/O (no disk latency)
   - Clean state on reboot (no stale locks/state)
   - Avoids physical mount dependencies (critical for Unraid array restart)
   - Available immediately after boot

2. **Some subsets MUST be persistent** for:
   - Offline operation (internet unavailable)
   - Cold boot recovery
   - Recovery from internet outage

3. **GitHub is SSOT** but:
   - Must have local fallback when GitHub is down
   - Bootstrap must work without internet

---

## 2. Current Implementation by Server

### 2.1 VPS1 (Oracle Cloud)

| Mount | Size | Purpose | Persistent |
|-------|------|---------|------------|
| `/atn` | 18 GB tmpfs | Runtime workspace | ❌ NO |
| `/_atn` | 12 GB tmpfs | Secondary workspace | ❌ NO |

**Current Contents of `/atn`:**
```
/atn/
├── bin/           # Scripts
└── github/        # Cloned repos
```

**Issues:**
- **NO persistent storage** - everything lost on reboot
- No local cache of GitHub repos
- No fallback if internet is down at boot

**Persistent Storage Options:**
- Disk at `/` has 52GB free
- Could use `/var/atn` or `/home/alex/atn-persistent`

### 2.2 VPS2 / Condo (Oracle Cloud)

| Mount | Size | Purpose | Persistent |
|-------|------|---------|------------|
| `/atn` | On disk | Full workspace | ✅ YES |

**Current Contents:**
```
/atn/
├── .gemini/       # Rules, configs
├── github/        # Cloned repos
├── baseline/      # Namespace baseline
└── bin/           # Scripts
```

**Status:** ✅ Already persistent (on disk, not tmpfs)

### 2.3 Unraid

| Mount | Size | Purpose | Persistent |
|-------|------|---------|------------|
| `/atn` | On array (btrfs) | Full workspace | ✅ YES |
| `/boot/atn` | On flash | Boot-time configs | ✅ YES |
| `/atn_ram_boot` | 12 GB tmpfs | Hot cache | ❌ NO |

**Current Contents of `/atn`:**
```
/atn/
├── bin/           # Scripts
├── config/        # Service configs
├── git/           # Cloned repos
├── .git/          # Repo metadata
└── vscode-workspaces/
```

**Current Contents of `/boot/atn`:**
```
/boot/atn/
├── appdata/       # App configs
├── bin/           # Boot scripts
├── boot/          # Boot hooks
├── config/        # Service configs
├── lib/           # Libraries
├── lifecycle/     # Startup/shutdown
└── init/          # Init scripts
```

**Status:** ✅ Robust - persistent on array + flash backup

---

## 3. Proposed Persistence Strategy

### 3.1 Path Classification

| Path | Must Persist | Reason |
|------|--------------|--------|
| `/atn/.gemini/rules/` | ✅ YES | Governance rules, critical for operation |
| `/atn/.gemini/scratch/` | 🟡 HYBRID | Backlog yes, transient data no |
| `/atn/bin/` | ✅ YES | Core scripts |
| `/atn/lib/` | ✅ YES | Shared libraries |
| `/atn/github/` | 🟡 HYBRID | Clone from GitHub, cache locally |
| `/atn/config/` | ✅ YES | Service configurations |
| `/atn/baseline/` | ✅ YES | Namespace baseline |
| `/atn/worktrees/` | ❌ NO | Ephemeral, recreatable |
| `/atn/tmp/` | ❌ NO | Truly temporary |

### 3.2 Proposed VPS1 Architecture

```
┌─────────────────────────────────────────┐
│              PERSISTENT                 │
│    /var/atn-persistent/                 │
│    ├── .gemini/rules/                   │
│    ├── .gemini/scratch/backlog.md       │
│    ├── bin/                             │
│    ├── lib/                             │
│    ├── config/                          │
│    ├── baseline/                        │
│    └── github-cache/                    │
└─────────────────────────────────────────┘
              ↓ rsync at boot
┌─────────────────────────────────────────┐
│              TMPFS                      │
│    /atn/                                │
│    ├── .gemini/ → synced from persist  │
│    ├── bin/ → synced from persist      │
│    ├── github/ → git clone or cache    │
│    ├── worktrees/ → created fresh      │
│    └── tmp/                             │
└─────────────────────────────────────────┘
              ↑ rsync on change/shutdown
```

### 3.3 Sync Strategy

**Boot Sequence:**
1. Mount tmpfs at `/atn`
2. Check internet connectivity
3. If internet: `git pull` from GitHub SSOT
4. If no internet: `rsync` from `/var/atn-persistent/`
5. Start services

**Runtime Sync:**
- Critical files synced to persistent on change
- Periodic sync (every 15 min) via cron
- Git push to GitHub when connected

**Shutdown Sequence:**
1. Sync `/atn` → `/var/atn-persistent/`
2. Unmount tmpfs

---

## 4. Implementation Requirements

### 4.1 Systemd Units for VPS1

**atn-tmpfs.mount:**
```ini
[Unit]
Description=ATN tmpfs workspace
Before=docker.service

[Mount]
What=tmpfs
Where=/atn
Type=tmpfs
Options=size=18G,mode=2775,uid=1100,gid=1100

[Install]
WantedBy=multi-user.target
```

**atn-bootstrap.service:**
```ini
[Unit]
Description=ATN Bootstrap from persistent or GitHub
After=atn-tmpfs.mount network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/var/atn-persistent/bin/bootstrap.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

### 4.2 Bootstrap Script

```bash
#!/bin/bash
set -euo pipefail

PERSISTENT="/var/atn-persistent"
TMPFS="/atn"
GITHUB_REPO="https://github.com/atnplex/atn.git"

# Check internet
if ping -c 1 github.com &>/dev/null; then
    echo "Internet available, cloning from GitHub"
    git clone --depth 1 "$GITHUB_REPO" "$TMPFS/github/atn" || \
        rsync -a "$PERSISTENT/" "$TMPFS/"
else
    echo "No internet, using local cache"
    rsync -a "$PERSISTENT/" "$TMPFS/"
fi

chown -R atn:atn "$TMPFS"
```

### 4.3 Shutdown Sync Script

```bash
#!/bin/bash
set -euo pipefail

PERSISTENT="/var/atn-persistent"
TMPFS="/atn"

# Sync critical paths
rsync -a --delete \
    "$TMPFS/.gemini/rules/" \
    "$TMPFS/.gemini/scratch/" \
    "$TMPFS/bin/" \
    "$TMPFS/config/" \
    "$PERSISTENT/"

echo "Synced to persistent at $(date)"
```

---

## 5. Unknowns to Confirm

| Question | Context |
|----------|--------|
| What's the exact list of paths that MUST persist on VPS1? | Need user confirmation |
| Should VPS2 switch to tmpfs + persist pattern? | Currently all on disk |
| Should Unraid `/atn_ram_boot` be synced to `/boot/atn`? | Need to check current sync |
| What's the recovery time target if GitHub is down? | Affects cache strategy |
| Should we use git sparse-checkout for large repos? | Optimize clone time |

---

## 6. Current vs Proposed Summary

| Server | Current | Proposed |
|--------|---------|----------|
| VPS1 | tmpfs only, no persist | Add `/var/atn-persistent` + sync |
| VPS2 | Disk only | Keep as-is (already persistent) |
| Unraid | Array + flash + tmpfs | Keep as-is (robust) |
| WSL | Disk | Keep as-is |

---

*Document created for Perplexity collaboration.*
