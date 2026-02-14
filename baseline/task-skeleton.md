# Task Skeleton - Modular Execution Framework

## Purpose

ALL repository processing tasks MUST follow this modular skeleton to ensure reproducibility and drift resistance across runs and AI agents.

## Skeleton Structure

Every task follows **6 phases** (A → B → C → D → E → F):

### A) Obtain Information (Parallelizable)

- Run preflight check
- Detect environment
- Check tool availability
- Query repo metadata

### B) Plan Execution

- List viable execution targets
- Select best path
- Record decision + rationale

### C) Ensure Dependencies

- Check for missing required tools
- Attempt installation (if allowed)
- Validate installations

### D) Implement Changes

- Make file edits
- Run scripts
- Generate outputs
- Minimal, deterministic, reversible

### E) Verify Results

- Re-run checks/tests
- Validate file integrity
- Compare before/after

### F) Record Artifacts

- Update metadata.json
- Write processing logs
- Create summary documents
- Capture metrics

## Template Checklist

```markdown
## A) Obtain Information ⏳

- [ ] Run preflight (see preflight.md)
- [ ] Check preflight.json status
- [ ] Validate environment
- [ ] Gather repo facts

## B) Plan Execution ⏳

- [ ] List execution options
- [ ] Select execution_target
- [ ] Document decision rationale

## C) Ensure Dependencies ⏳

- [ ] Check tool availability
- [ ] Attempt installations
- [ ] Record missing deps

## D) Implement ⏳

- [ ] [Task-specific actions]

## E) Verify ⏳

- [ ] Run verification checks
- [ ] Validate results

## F) Record ⏳

- [ ] Update metadata.json
- [ ] Write summary
- [ ] Commit artifacts
```
