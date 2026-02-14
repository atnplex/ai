# Workspace Incident & Resolution Log

This document tracks system-level issues, environment fixes, and stabilization efforts for the Antigravity/ATN ecosystem.

---

## 📋 Logging Guidelines (For Agents & Humans)

When adding a new entry, please follow this structure to ensure AI readability and quick triage:

1.  **Date & Env**: `[YYYY-MM-DD]` | **Context**: `[Windows Desktop | Debian VM | WSL]`
2.  **Symptom**: Clear description of the error or "hanging" behavior.
3.  **Root Cause**: Why did it happen? (e.g., path mismatch, missing env var).
4.  **🚨 RESOLUTION**: The exact steps/commands to fix it. Mark as "Validated" if confirmed working.
5.  **Persistence**: Notes on whether the fix survives reboots or extension updates.

---

## ⚡ Quick-Fix Index (Active Issues)

| Date | Issue | Env | Status |
| :--- | :--- | :--- | :--- |
| 2026-02-14 | Playwright browser fails ($HOME) | Windows | ✅ Resolved/Persistent |
| 2026-02-14 | Terminal hanging (stdout pipes) | Windows | ✅ Stabilized |

---

## 📝 Recent Incidents

### [2026-02-14] | Context: Windows 11 Desktop (Physical)

**Symptom**: 
- `browser_subagent` (background browser) failed with: `failed to create browser context: failed to install playwright: $HOME environment variable is not set`.
- `run_command` calls were hanging indefinitely without returning output.

**Root Cause**: 
- Playwright requires a Unix-style `$HOME` variable even on Windows to locate the browser binary cache.
- VS Code Shell Integration was interfering with the redirection of stdout in headless sessions.

**🚨 RESOLUTION (Validated)**:
1.  **Browser Cache Path**: Set permanent User environment variable `HOME`.
    - `[Environment]::SetEnvironmentVariable('HOME', 'C:\Users\Alex', 'User')`
2.  **Shell Stability**: Updated `settings.json` to disable shell integration.
    - Set `"terminal.integrated.shellIntegration.enabled": false`.

**Persistence**:
- **HOME**: Persistent (User Registry).
- **Settings**: Persistent (`%APPDATA%`).
- **Antigravity**: Requires restart to pick up the new `HOME` value.

---
