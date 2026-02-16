# State Validation Rules

## Purpose
Enforce state transition validation to prevent invalid operations and maintain system integrity.

## Critical Validations

> Canonical state transitions: see [AGENT_PROTOCOL.md § Task Lifecycle State Machine](../.comet-browser/AGENT_PROTOCOL.md#task-lifecycle-state-machine)
### Invalid Transitions
- Cannot claim completed/failed issues
- Cannot mark as completed without being in-progress
- Cannot transition from failed to in-progress (must re-claim)
- Cannot remove agent-task label once assigned

## Pre-Action Checks

Before claiming:
1. Verify issue has `agent-task` label
2. Check issue is OPEN with no assignee
3. Validate no conflicting `claimed`/`in-progress` labels
4. Confirm agent identity is available

Before marking in-progress:
1. Verify issue has `claimed` label
2. Confirm current agent is assignee
3. Check issue not marked as `blocked`

Before completing:
1. Verify issue has `in-progress` label
2. Confirm current agent is assignee
3. Validate deliverables are documented
4. Check all sub-tasks are resolved

## Conflict Prevention

### Race Condition Protection
- Always refresh issue state before state changes
- Use GitHub's conditional updates when available
- Document timestamp in comments for audit trail

### Label Conflicts
- Only one of: `claimed`, `in-progress`, `completed`, `failed` at a time
- Remove previous state label when applying new one
- `blocked` can coexist with `claimed`/`in-progress`

## Error Recovery

> Timeouts: see [AGENT_PROTOCOL.md § Timeouts](../.comet-browser/AGENT_PROTOCOL.md#timeouts)

### Orphaned Claims
If issue is `claimed` > 30 minutes with no progress:
1. Add comment: "@{assignee} claim timeout approaching"
2. Wait 15 minutes
3. Remove `claimed` label and assignee
4. Add `stale` label

### Stuck In-Progress
If issue is `in-progress` > 4 hours:
1. Add `blocked` label
2. Comment requesting status update
3. Do not auto-fail (requires manual intervention)

## Validation Checklist

Agents MUST verify before ANY action:
- [ ] Issue state is compatible with intended action
- [ ] No conflicting labels present
- [ ] Current agent has permission for action
- [ ] All prerequisites are met
- [ ] Change will be documented in comment

## Implementation

These rules are MANDATORY. Agents must:
1. Read and understand all transition rules
2. Execute validation checks programmatically
3. Log all validation failures
4. Never override validations for convenience
