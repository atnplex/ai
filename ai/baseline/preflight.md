# Preflight Check - Mandatory Before Repo Processing

## Purpose

The preflight check is a **mandatory gate** that must pass before processing any repository. It validates the execution environment, workspace configuration, and tool availability to prevent known failure modes.

**Enforces:** See [`RULES.md`](RULES.md) for complete rule definitions

- **R1**: Environment-First Execution
- **R3**: Canonical Paths by Execution Target
- **R5**: Workspace Watcher Reliability (UNC detection)
- **R6**: Universal Time (UTC timestamps)
- **R7**: Determinism (sorted JSON)
- **R8**: Stop-the-Run Policy

## How to Run Preflight

### From WSL/Linux

```bash
cd /atn/x/repo-integrations
bash tools/preflight.sh ./preflight.json
```

### Output

- **JSON to stdout** - For inline consumption
- **JSON to file** - For auditability (default: `./preflight.json`)
- **Exit code** - 0 (pass) or 1 (fail)

## What PASS/FAIL Means (R8)

### PASS (status: "pass")

- Execution environment supported (WSL, remote Linux, or Windows)
- Workspace mode valid (NOT windows_unc - R5)
- Required tools available (git, python3 for Linux)
- Critical paths exist (`/atn` for Linux, `C:\atn` for Windows)
- **Action:** Proceed with repo processing

### FAIL (status: "fail")

- One or more critical failures detected
- **Action:** STOP IMMEDIATELY - Do NOT proceed

## Mandatory Rule (R8)

**⛔ IF PREFLIGHT FAILS → STOP**

Do not continue to repo analysis, cloning, or any processing steps until preflight passes.
