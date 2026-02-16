---
description: Import Antigravity configuration (rules, workflows, skills) from a Debian machine to Windows.
---

# Antigravity Migration: Debian to Windows

Follow these steps to migrate your AG configuration from a Debian machine to this Windows environment.

## 1. Prepare Debian Export

On your **Debian machine**, run the following commands to bundle your configuration:

```bash
# Navigate to your AG config directory (usually ~/.atn or similar)
cd ~/.atn

# Create a tarball of your baseline rules and workflows
tar -czf ag_config_export.tar.gz baseline/rules baseline/workflows skills/
```

## 2. Transfer to Windows

Transfer `ag_config_export.tar.gz` to your Windows machine (e.g., via SCP, SFTP, or a shared drive). Place it in `C:\atn\`.

## 3. Initialize Windows Environment

Ensure your `C:\atn` directory is ready:

```powershell
# Create directories if they don't exist
New-Item -ItemType Directory -Force -Path "C:\atn\baseline\rules", "C:\atn\baseline\workflows", "C:\atn\skills"
```

## 4. Extract and Merge

Extract the tarball in WSL (if installed) or manually:

```bash
# In WSL
cd /mnt/c/atn
tar -xzf ag_config_export.tar.gz --strip-components=1
```

## 5. Sync and Verify

Run the enhanced sync script to register the new configurations:

```powershell
# Run the sync script to restore settings and link workflows
C:\atn\homelab-env\scripts\sync.ps1 -Restore
```

## 6. Restart Antigravity

Reload the Antigravity window to apply the new rules and workflows.

---
// turbo-all
// Status: Ready for migration
