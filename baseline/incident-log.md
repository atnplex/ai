# Workspace Incident & Resolution Log

This document tracks system-level issues, environment fixes, and stabilization efforts for the Antigravity/ATN ecosystem.

## [2026-02-14] - Browser Engine & Terminal Stabilization

**Issue**: 
1. `browser_subagent` failed with: `failed to create browser context: failed to install playwright: $HOME environment variable is not set`.
2. `run_command` calls were hanging (stdout capture failure) despite YOLO/Auto-Approve being enabled.

**Fixes Applied**:
1. **Environment Persistence**: Set a permanent User environment variable `HOME` to `C:\Users\Alex`. This is required by Playwright (cross-platform mismatch) to locate the browser cache on Windows.
   - *Command used*: `[Environment]::SetEnvironmentVariable('HOME', 'C:\Users\Alex', 'User')`
2. **Terminal Stabilization**: Updated `settings.json` to disable `terminal.integrated.shellIntegration.enabled`. Shell integration can interfere with headless terminal pipes in some versions of VS Code/Antigravity.
   - *File*: `C:\Users\Alex\AppData\Roaming\Code\User\settings.json`
3. **Verification**: Successfully tested network-level browsing using `read_url_content` and verified command execution via file redirection.

**Recommended Recovery**:
- If browser tools fail again, verify `$env:HOME` in a fresh terminal.
- Ensure Antigravity is restarted after environment variable changes.
