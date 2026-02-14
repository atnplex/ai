# Changelog

## [1.0.0] - 2026-02-14

### Added
- Unified timeout values (SSOT in AGENT_PROTOCOL.md): claimed=5min, in-progress=2hrs, review=24hrs
- Canonical state machine with transition table (backlog→claimed→in-progress→review→completed)
- Protocol versioning system (PROTOCOL_VERSION file, manifest.json)
- Dynamic agent identity system: `{platform}-{profile}` formula
- Root README.md as repository index
- manifest.json agent registry with profiles, labels, and timeout config
- GitHub labels: `failed`, `completed`, agent-scoped labels
- Issue templates: bug-report, feature-request, agent-task
- PR template and CODEOWNERS

### Fixed
- Removed all dead `TASK_LIFECYCLE.md` references across documentation
- Fixed timeout contradictions between `.comet-browser/README.md` and `AGENT_PROTOCOL.md`
- Fixed `sync_ai.sh`: added missing `warn()` function, corrected `origin/master` → `origin/main`
- Deduplicated `.comet-browser/README.md` (407 → 31 lines, now a concise index)

### Changed
- `state-validation.md` now references AGENT_PROTOCOL.md SSOT instead of redefining transitions
- `SPACE_SETUP.md` updated: removed hardcoded timeouts, replaced static Agent-1/2/3 with derived IDs
- MCP config consolidated: `mcp_config.json` generated at runtime from `mcp_registry.json`
- `COMET_BOOTSTRAP.md` adds protocol version check and agent ID derivation as first steps
- `VERIFICATION_CHECKLIST.md` adds 5 identity/protocol verification questions
