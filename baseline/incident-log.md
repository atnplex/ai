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
| 2026-02-14 | Persistent Auto-Approval prompts | Windows | 🔄 In Progress |
| 2026-02-14 | Antigravity Launcher / WSL Clutter | Windows | ✅ Resolved/Self-Healing |
| 2026-02-14 | Playwright browser fails ($HOME) | Windows | ✅ Resolved/Persistent |
| 2026-02-14 | Terminal hanging (stdout pipes) | Windows | ✅ Stabilized |

---

## 📝 Recent Incidents

### [2026-02-14] | Context: Windows 11 Desktop - Persistent Auto-Approval Blocking

**Symptom**: 
- Agent continues to be interrupted by "Run command?", "Allow JavaScript execution?", and "Confirm MCP arguments?" prompts despite `yoloMode` and `alwaysProceed` policies.
- Efficiency is heavily degraded by constant manual approval requirements.

**Root Cause**: 
- Top-level YOLO settings were missing specific granular sub-settings for Tool Calls, JavaScript execution in browser sub-agents, and wildcard tool eligibility in the chat interface.

**🚨 RESOLUTION (In Progress)**:
1.  **Hardened Auto-Approval**: 
    - Added `"*": true` to `chat.tools.eligibleForAutoApproval` for full wildcard tool autonomy.
    - Set `"antigravity.security.autoApproveToolCalls": true` and `"antigravity.agent.autoApproveToolCalls": true`.
    - Set `"antigravity.browser.allowJavaScriptExecution": true` to avoid JS execution prompts.
2.  **Profile Synchronization**: Verified all settings are synced to dynamic profiles like "NewProfile" via `workbench.settings.applyToAllProfiles`.

**Persistence**:
- Settings updated in Roaming APPDATA. 
- Rule R15 enforced to track future interruptions.

---

### [2026-02-14] | Context: Windows 11 Desktop (Physical) - Environment Hardening

**Symptom**: 
- `ag` launcher failing with "bws.exe not recognized".
- WSL profiles cluttering the terminal area despite being unused.
- Multiple terminal instances and relaunch warnings on startup.
- Warnings about unknown CLI flags `--yolo` and `--disable-agent-review`.
- Browser subagent visibility (Chrome opening for background tasks).

**Root Cause**: 
- Bitwarden Secrets Manager CLI (`bws.exe`) was missing from the hardcoded path in the launcher.
- Antigravity's discovery of WSL profiles defaults to "on", and VS Code shell integration in `Microsoft.PowerShell_profile.ps1` caused redundant terminal environments.
- Legacy launch parameters passed to the executable caused Electron warnings.

**🚨 RESOLUTION (Validated)**:
1.  **Self-Healing Launcher**: Re-engineered `launch-antigravity.ps1` to:
    - Automatically search common paths and the User's PATH for `bws.exe`.
    - Auto-install `bws.exe` to `$HOME\.antigravity_tools\bin` if missing (via GitHub download).
    - Map Bitwarden secret names (e.g., `github` -> `GITHUB_PERSONAL_ACCESS_TOKEN`).
2.  **CLI Sanitization**: Removed unsupported flags from the launch command.
3.  **Terminal Declutter**:
    - Set `"terminal.integrated.useWslProfiles": false` in `settings.json`.
    - Commented out shell integration in the PowerShell profile (handled automatically by Antigravity).
4.  **Autonomy & Security**: 
    - Added `vibe.atnplex.dev` and `*.atnplex.dev` to `workbench.trustedDomains` to reduce "Allow?" prompts.
    - Added **R15: INCIDENT_LOGGING** to `baseline/rules/governance.md`.

**Persistence**:
- **Launcher**: Persistent.
- **Settings**: Persistent in APPDATA.
- **Rules**: Enforced for all agents.

---
